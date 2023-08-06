# codepiper 
[![PyPI version shields.io](https://img.shields.io/pypi/v/codepiper)](https://pypi.python.org/pypi/codepiper/)

This tool provides some utilities for working with AWS CodePipeline:

* `watch` - Monitor a pipeline for executions and also follow CodeBuild logs.
* `rollback`- Rollback a stage of a pipeline to a prior execution.
* `verify_clear`- Verify that a pipeline is clear, or the details if not.

![](codepiper.gif)

# Watch

To monitor all active executions for a pipeline:

`codepiper --profile toolchain --region us-west-2 watch -p my-pipeline-name` 

To monitor a pipeline along with logs from CodeBuild:

`codepiper --profile toolchain --region us-west-2 watch -p my-pipeline-name -f` 

To monitor one specific execution for a pipeline:

`codepiper --profile toolchain --region us-west-2 watch -p my-pipeline-name -e 20b20f00-f63d-4b05-8921-20a4fc16090e`

`codepiper --profile toolchain --region us-west-2 verify_clear -p my-pipeline-name` 

# Rollback

To rollback a pipeline stage to last successful execution:

`codepiper --profile toolchain --region us-west-2 rollback -p my-pipeline-name -s Production` 

To rollback a pipeline stage to a specific commit id:

`codepiper --profile toolchain --region us-west-2 rollback -p my-pipeline-name -s Production -c af32c18` 

To rollback a pipeline stage and watch logs

`codepiper --profile toolchain --region us-west-2 rollback -p my-pipeline-name -s Production -f`

# Verify Pipeline Clear

To verify that a pipeline is currently clear:
`codepiper --profile toolchain --region us-west-2 verify_clear --pipeline my-pipeline-name`

# Installation

`pip install codepiper`

# Limitations

* `$CODEBUILD_RESOLVED_SOURCE_VERSION` is unavailable since the CodeBuild execution is not initiated via CodePipeline. The workaround for this is to use [CodePipeline Variables](https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-variables.html) to pass the `CommitId` from source stage as a user defined environment variable to your CodeBuild project.
