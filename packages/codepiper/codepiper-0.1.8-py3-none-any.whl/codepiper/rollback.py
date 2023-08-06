""" Rollback pipeline """

import json
from datetime import datetime, timezone
from boto3.session import Session
from codepiper.context import LogContextManager
from codepiper.build import BuildMonitor


def sort_last_update_time(action):
    """used to sort by last update time"""
    return action["lastUpdateTime"]


def get_latest_execution_id(
    session: Session,
    pipeline: str,
    stage: str,
    commit: str = None,
):
    """Get the latest execution id for a pipeline"""
    codepipeline = session.client("codepipeline")
    paginator = codepipeline.get_paginator("list_action_executions")
    response_iterator = paginator.paginate(
        pipelineName=pipeline,
        filter={},
    )
    executions = {}
    for response in response_iterator:
        for action in response["actionExecutionDetails"]:
            execution_id = action["pipelineExecutionId"]
            if execution_id not in executions:
                executions[execution_id] = {
                    "last_update_time": datetime.fromtimestamp(0, timezone.utc),
                    "failed_count": 0,
                    "in_progress_count": 0,
                    "succeeded_count": 0,
                }

            if action["input"]["actionTypeId"]["category"] == "Source":
                executions[execution_id]["commit_id"] = action["output"][
                    "outputVariables"
                ].get("CommitId", "")

            if action["stageName"] != stage:
                continue

            if action["status"] == "Failed":
                executions[execution_id]["failed_count"] += 1
            if action["status"] == "InProgress":
                executions[execution_id]["in_progress_count"] += 1
            if action["status"] == "Succeeded":
                executions[execution_id]["succeeded_count"] += 1

            executions[execution_id]["last_update_time"] = max(
                executions[execution_id]["last_update_time"], action["lastUpdateTime"]
            )

    executions = [
        {
            "id": e_id,
            "lastUpdateTime": e["last_update_time"],
        }
        for e_id, e in executions.items()
        if (commit is not None and commit in e["commit_id"])
        or (
            commit is None
            and e["failed_count"] == 0
            and e["in_progress_count"] == 0
            and e["succeeded_count"] > 0
        )
    ]
    executions.sort(key=sort_last_update_time)
    if not executions:
        raise ValueError("Unable to find latest execution id")
    return executions[-1]["id"]


def rerun_build(
    session: Session,
    build_id: str,
    input_artifact,
    output_artifact,
    dryrun,
):
    """Rerun a prior build from a pipeline"""
    codebuild = session.client("codebuild")
    build = codebuild.batch_get_builds(ids=[build_id])["builds"][0]
    build_kwargs = {}

    def set_build_arg(dst_path, *src_path):
        val = build
        for path_part in src_path:
            if val is not None:
                val = val.get(path_part)
        if val is not None:
            build_kwargs[dst_path] = val

    set_build_arg("projectName", "projectName")
    set_build_arg("secondaryArtifactsOverride", "secondaryArtifacts")
    set_build_arg("environmentVariablesOverride", "environment", "environmentVariables")
    set_build_arg("sourceVersion", "sourceVersion")
    set_build_arg("sourceAuthOverride", "source", "auth")
    set_build_arg("secondarySourcesOverride", "secondarySources")
    set_build_arg("secondarySourcesVersionOverride", "secondarySourceVersions")
    set_build_arg("gitCloneDepthOverride", "source", "gitCloneDepth")
    set_build_arg("gitSubmodulesConfigOverride", "source", "gitSubmodulesConfig")
    set_build_arg("buildspecOverride", "source", "buildspec")
    set_build_arg("insecureSslOverride", "source", "insecureSsl")
    set_build_arg("buildStatusConfigOverride", "source", "buildStatusConfig")
    set_build_arg("environmentTypeOverride", "environment", "type")
    set_build_arg("imageOverride", "environment", "image")
    set_build_arg("computeTypeOverride", "environment", "computeType")
    set_build_arg("certificateOverride", "environment", "certificate")
    set_build_arg("cacheOverride", "cache")
    set_build_arg("serviceRoleOverride", "serviceRole")
    set_build_arg("privilegedModeOverride", "environment", "priviledgedMode")
    set_build_arg("timeoutInMinutesOverride", "timeoutInMinutes")
    set_build_arg("queuedTimeoutInMinutesOverride", "queuedTimeoutInMinutes")
    set_build_arg("encryptionKeyOverride", "encryptionKey")
    set_build_arg("registryCredentialOverride", "environment", "registryCredential")
    set_build_arg(
        "imagePullCredentialsTypeOverride", "environment", "imagePullCredentialsType"
    )
    set_build_arg("debugSessionEnabled", "debugSession", "sessionEnabled")
    build_kwargs["logsConfigOverride"] = {
        k: v for k, v in build["logs"].items() if k in ("cloudWatchLogs", "s3Logs")
    }
    if len(build_kwargs["logsConfigOverride"]) == 0:
        del build_kwargs["logsConfigOverride"]

    if output_artifact is None:
        build_kwargs["artifactsOverride"] = {"type": "NO_ARTIFACTS"}
    elif "s3location" in output_artifact:
        build_kwargs["artifactsOverride"] = {
            "type": "S3",
            "location": output_artifact["s3location"]["bucket"],
            "path": output_artifact["s3location"]["key"],
        }

    if dryrun:
        print(
            f"[DRYRUN] Would start build with args: {json.dumps(build_kwargs, indent=1)}"
        )
        return {"id": "0"}

    res = codebuild.start_build(**build_kwargs)
    return res["build"]


def rollback_pipeline(
    session: Session,
    pipeline: str,
    stage: str,
    commit: str = None,
    dryrun: bool = False,
    no_wait: bool = False,
    follow_logs: bool = False,
    **kwargs,
):
    """Rollback a pipeline to a prior execution"""
    execution_id = get_latest_execution_id(
        session=session,
        pipeline=pipeline,
        stage=stage,
        commit=commit,
    )

    print(f"Rollback to {execution_id}")

    codepipeline = session.client("codepipeline")

    # find source info
    commit_id = "???"
    commit_message = ""
    artifacts = codepipeline.get_pipeline_execution(
        pipelineName=pipeline,
        pipelineExecutionId=execution_id,
    )["pipelineExecution"]["artifactRevisions"]
    for artifact in artifacts:
        if "revisionSummary" in artifact:
            try:
                revision_summary = json.loads(artifact["revisionSummary"])
                if revision_summary["ProviderType"] == "GitHub":
                    commit_id = artifact["revisionId"]
                    commit_message = revision_summary["CommitMessage"]
            except:
                commit_id = artifact["revisionId"]
                commit_message = artifact["revisionSummary"]

    actions = codepipeline.list_action_executions(
        pipelineName=pipeline, filter={"pipelineExecutionId": execution_id}
    )

    ctx_mgr = LogContextManager()
    builds = BuildMonitor(session=session)

    details = actions["actionExecutionDetails"]
    details.sort(key=sort_last_update_time)

    for action in details:
        if action["stageName"] != stage:
            continue

        if action["input"]["actionTypeId"]["provider"] == "CodeBuild":
            primary_source_name = action["input"]["resolvedConfiguration"].get(
                "PrimarySource", None
            )
            primary_source = None
            for artifact in action["input"]["inputArtifacts"]:
                if artifact["name"] == primary_source_name:
                    primary_source = artifact
            if len(action["output"]["outputArtifacts"]) > 0:
                primary_artifact = action["output"]["outputArtifacts"][0]
            else:
                primary_artifact = None

            if "executionResult" in action["output"]:
                build = rerun_build(
                    session=session,
                    build_id=action["output"]["executionResult"]["externalExecutionId"],
                    input_artifact=primary_source,
                    output_artifact=primary_artifact,
                    dryrun=dryrun,
                )

            if not dryrun and not no_wait:
                logger = ctx_mgr.set_context(
                    build["id"],
                    commit_id=commit_id,
                    commit_message=commit_message,
                    status="Rollback ▶",
                )

                build_future = builds.monitor(
                    build["id"],
                    follow_logs=follow_logs,
                    logger=logger,
                )
                build_future.result()
                ctx_mgr.clear_context(build["id"])
