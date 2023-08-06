""" Verify pipeline clear """

import sys
from boto3.session import Session


def verify_clear(
    session: Session,
    pipeline: str,
    **kwargs,
):
    """Verifying pipeline is currently clear"""
    state = session.client("codepipeline").get_pipeline_state(name=pipeline)
    first_stage_state = state['stageStates'][0]
    execution_id = first_stage_state['latestExecution']['pipelineExecutionId']
    is_clear = True
    error_message = None
    for stage_state in state['stageStates']:
        if('latestExecution' not in stage_state
                or 'Succeeded' != stage_state['latestExecution']['status']
                or execution_id != stage_state['latestExecution']['pipelineExecutionId']):
            if is_clear:
                is_clear = False
                error_message = f"    Stage: {stage_state['stageName']}\n    Status: {stage_state['latestExecution']['status']}\n    Execution ID: {stage_state['latestExecution']['pipelineExecutionId']}"
    if is_clear :
        print(f"✅  The \'{pipeline}\' pipeline is clear.")
        sys.exit(0)
    else:
        print(f"❌  The \'{pipeline}\' pipeline is NOT clear!")
        print(f"{error_message}")
        sys.exit(1)
