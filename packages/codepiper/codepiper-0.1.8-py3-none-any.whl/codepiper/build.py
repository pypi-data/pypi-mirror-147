import traceback
from datetime import datetime, timezone
import time
from concurrent.futures import ThreadPoolExecutor, Future
from boto3.session import Session
from codepiper.context import LogContext


class BuildMonitor:
    def __init__(self, session: Session):
        self.builds = []
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.active = True
        self.codebuild = session.client("codebuild")
        self.cloudwatchlogs = session.client("logs")

    def monitor(
        self, codebuild_id: str, follow_logs: bool, logger: LogContext
    ) -> Future:
        if codebuild_id in self.builds:
            return

        self.builds.append(codebuild_id)

        def build_watcher():
            self.watch_build_events(codebuild_id, follow_logs, logger)

        return self.executor.submit(build_watcher)

    def get_build(self, codebuild_id: str):
        builds = self.codebuild.batch_get_builds(ids=[codebuild_id])["builds"]
        if len(builds) != 1:
            return None
        return builds[0]

    def log_events(self, events, logger: LogContext):
        last_log_time = datetime.fromtimestamp(0, tz=timezone.utc)
        for event in events:
            log_time = datetime.fromtimestamp(
                event["timestamp"] / 1000, tz=timezone.utc
            )
            for line in event["message"].splitlines():
                try:
                    logger.write(line)
                except:
                    pass
            last_log_time = max(log_time, last_log_time)
        # logger.write("len:{} last:{}", len(events), last_log_time)
        return last_log_time

    def watch_build_events(
        self, codebuild_id: str, follow_logs: bool, logger: LogContext
    ):
        last_log_time = datetime.fromtimestamp(0, tz=timezone.utc)
        prior_phase = None
        prior_status = None
        while self.active:
            try:
                build = self.get_build(codebuild_id)
                if build is None:
                    logger.write("Unable to find build for id {}", codebuild_id)
                    return

                if (
                    prior_phase != build["currentPhase"]
                    or prior_status != build["buildStatus"]
                ):
                    logger.header(
                        "🛠️  CodeBuild[{}] phase={} status={}",
                        build["buildNumber"],
                        build["currentPhase"],
                        build["buildStatus"],
                    )
                    prior_phase = build["currentPhase"]
                    prior_status = build["buildStatus"]

                if follow_logs and "groupName" in build["logs"]:
                    if last_log_time.timestamp() == 0:
                        ## Just grab recent log events
                        events = self.cloudwatchlogs.get_log_events(
                            logGroupName=build["logs"]["groupName"],
                            logStreamName=build["logs"]["streamName"],
                            limit=25,
                            startFromHead=False,
                        )["events"]
                        last_log_time = max(
                            last_log_time, self.log_events(events, logger)
                        )
                    else:
                        paginator = self.cloudwatchlogs.get_paginator(
                            "filter_log_events"
                        )
                        response_iterator = paginator.paginate(
                            logGroupName=build["logs"]["groupName"],
                            logStreamNames=[build["logs"]["streamName"]],
                            startTime=int(last_log_time.timestamp() * 1000 + 999),
                        )
                        for response in response_iterator:
                            last_log_time = max(
                                last_log_time,
                                self.log_events(response["events"], logger),
                            )

                if build["currentPhase"] == "COMPLETED":
                    break

            except Exception as ex:
                print(f"EXCEPTION - {ex}")
                traceback.print_exc()

            time.sleep(1)

    def stop(self):
        self.executor.shutdown(wait=False)
        self.active = False
