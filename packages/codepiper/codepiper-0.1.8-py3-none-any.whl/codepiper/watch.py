""" Watch pipeline """

from typing import List
import json
import time
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from boto3.session import Session
from codepiper.context import LogContextManager
from codepiper.build import BuildMonitor


@dataclass
class PipelineExecution:
    """Represents a current pipeline execution"""

    execution_id: str
    commit_id: str = None
    commit_message: str = None

    def __eq__(self, other):
        return self.execution_id == other.execution_id

    def __hash__(self):
        return hash(self.execution_id)

    def __repr__(self):
        commit_message_summary = self.commit_message.split("\n")[0][:70]
        return f"[{self.commit_id[:8]}] {commit_message_summary}"


@dataclass
class PipelineActivity:
    """Represents current activity on a pipeline"""

    execution: PipelineExecution
    stage: str
    action: str
    status: str
    last_status_change: datetime = None
    error_message: str = None
    summary: str = None
    percent_complete: float = 0
    codebuild_id: str = None

    def __eq__(self, other):
        return self.execution == other.execution

    def __hash__(self):
        return hash(self.execution)

    def __lt__(self, other):
        return self.last_status_change < other.last_status_change

    def status_message(self) -> str:
        if self.status == "Succeeded":
            status = "✅"
        elif self.status == "InProgress":
            status = "🔄"
        elif self.status == "Failed":
            status = "❌"

        return f"{status} stage={self.stage} ▶ action={self.action}"

    def __repr__(self):
        return f"{self.status_message()} - {self.error_message or ''}"


class PipelineState:
    """Represents the current state of a pipeline"""

    def __init__(self, session: Session, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.all_executions = set()
        self.active_executions = set()
        self.codepipeline = session.client("codepipeline")

    def process_execution_id(self, execution_id: str) -> PipelineExecution:
        execution = PipelineExecution(
            execution_id=execution_id,
        )
        if execution in self.all_executions:
            for prior_execution in self.all_executions:
                if prior_execution == execution:
                    execution = prior_execution
        else:
            artifacts = self.codepipeline.get_pipeline_execution(
                pipelineName=self.pipeline_name,
                pipelineExecutionId=execution.execution_id,
            )["pipelineExecution"]["artifactRevisions"]
            for artifact in artifacts:
                if "revisionSummary" in artifact:
                    try:
                        revision_summary = json.loads(artifact["revisionSummary"])
                        if revision_summary["ProviderType"] == "GitHub":
                            execution.commit_id = artifact["revisionId"]
                            execution.commit_message = revision_summary["CommitMessage"]
                    except:
                        execution.commit_id = artifact["revisionId"]
                        execution.commit_message = artifact["revisionSummary"]

            self.all_executions.add(execution)

        return execution

    def get_activity(self, execution_id: str = None) -> List[PipelineActivity]:
        """get current activities"""
        activities = []
        state = self.codepipeline.get_pipeline_state(name=self.pipeline_name)

        # If this is first load, don't restrict to just active stages
        active_only = len(self.all_executions) > 0

        # Update list of executions
        prior_active_executions = self.active_executions.copy()
        self.active_executions.clear()
        for stage in state["stageStates"]:
            if "latestExecution" not in stage:
                continue

            if (
                execution_id
                and execution_id not in stage["latestExecution"]["pipelineExecutionId"]
            ):
                continue

            execution = self.process_execution_id(
                stage["latestExecution"]["pipelineExecutionId"]
            )

            if "inboundExecution" in stage:
                if (
                    not execution_id
                    or execution_id in stage["inboundExecution"]["pipelineExecutionId"]
                ):
                    inbound_execution = self.process_execution_id(
                        stage["inboundExecution"]["pipelineExecutionId"]
                    )
                    self.active_executions.add(inbound_execution)

            if stage["latestExecution"]["status"] == "InProgress":
                # This stage is active - keep track of it
                self.active_executions.add(execution)
            elif active_only and execution not in prior_active_executions:
                # Bail - this is an inactive stage and it wasn't a prior active
                continue

            for i, action in enumerate(stage["actionStates"]):
                if (
                    i > 0
                    and "latestExecution" in stage["actionStates"][i - 1]
                    and "lastStatusChange"
                    in stage["actionStates"][i - 1]["latestExecution"]
                ):
                    default_date = stage["actionStates"][i - 1]["latestExecution"][
                        "lastStatusChange"
                    ] + timedelta(seconds=1)
                else:
                    default_date = datetime.now(tz=timezone.utc)

                if "latestExecution" not in action:
                    continue

                activity = PipelineActivity(
                    execution=execution,
                    stage=stage["stageName"],
                    status=action["latestExecution"]["status"],
                    action=action["actionName"],
                    last_status_change=action["latestExecution"].get(
                        "lastStatusChange", default_date
                    ),
                    summary=action["latestExecution"].get("summary", None),
                    percent_complete=action["latestExecution"].get(
                        "percentComplete", None
                    ),
                    error_message=action["latestExecution"]
                    .get("errorDetails", {})
                    .get("message", None),
                )

                # determine if this action is for CodeBuild
                if (
                    "externalExecutionUrl" in action["latestExecution"]
                    and "https://console.aws.amazon.com/codebuild/home"
                    in action["latestExecution"]["externalExecutionUrl"]
                ):
                    activity.codebuild_id = action["latestExecution"][
                        "externalExecutionId"
                    ]

                add_new_activity = True
                for existing_activity in activities.copy():
                    if existing_activity.execution == activity.execution:
                        if (
                            activity.status == "InProgress"
                            and existing_activity.status != "InProgress"
                        ):
                            activities.remove(existing_activity)
                        elif (
                            activity.status != "InProgress"
                            and existing_activity.status == "InProgress"
                        ):
                            add_new_activity = False
                        elif existing_activity < activity:
                            activities.remove(existing_activity)
                        else:
                            add_new_activity = False

                if add_new_activity:
                    activities.append(activity)

        activities.sort()

        has_more = True
        for activity in activities:
            if (
                execution_id is None
                or execution_id not in activity.execution.execution_id
            ):
                continue
            if activity.status in ("Cancelled", "Failed", "Stopped"):
                has_more = False
            if (
                activity.stage == state["stageStates"][-1]["stageName"]
                and activity.status == "Succeeded"
            ):
                has_more = False

        return activities, has_more


def watch_pipeline(
    session: Session,
    pipeline: str,
    execution_id: str = None,
    follow_logs: bool = False,
    **kwargs,
):
    """Monitor pipeline for new executions and codebuild logs"""
    ctx_mgr = LogContextManager()
    builds = BuildMonitor(session=session)
    pipeline_state = PipelineState(session=session, pipeline_name=pipeline)

    last_check_time = datetime.fromtimestamp(0, tz=timezone.utc)
    keep_watching = True
    prior_execution_ids = set()
    while keep_watching:
        new_execution_ids = set()
        activities, keep_watching = pipeline_state.get_activity(execution_id)
        for activity in activities:
            new_execution_ids.add(activity.execution.execution_id)
            logger = ctx_mgr.set_context(
                activity.execution.execution_id,
                commit_id=activity.execution.commit_id,
                commit_message=activity.execution.commit_message,
                status=activity.status_message(),
            )
            if last_check_time < activity.last_status_change:
                logger.header(activity.status_message())
                if activity.error_message:
                    logger.write(activity.error_message)
                if activity.codebuild_id:
                    builds.monitor(
                        codebuild_id=activity.codebuild_id,
                        follow_logs=follow_logs,
                        logger=logger,
                    )

        for old_execution_id in prior_execution_ids - new_execution_ids:
            ctx_mgr.clear_context(old_execution_id)
        prior_execution_ids = new_execution_ids

        last_check_time = datetime.now(tz=timezone.utc)
        try:
            if keep_watching:
                time.sleep(5)
        except KeyboardInterrupt:
            keep_watching = False

    builds.stop()
