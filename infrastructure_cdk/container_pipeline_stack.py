from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    pipelines,
    core
)


class ContainerPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        codestar_arn = core.CfnParameter(self, "CodeStarArn", type="String",
            description="The ARN of the codestar connection to be used in the source action.")

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()
        
        pipelines.CdkPipeline(self, 'ContainerPipeline',
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name="ContainerPipeline",
            source_action=codepipeline_actions.CodeStarConnectionsSourceAction(
                connection_arn=codestar_arn.value_as_string,
                owner="zzenonn",
                repo="InfrastructureCdkSample",
                branch="master",
                action_name="GitHubSource",
                run_order=1,
                output=source_artifact
            ),
            # Install CDK dependencies.
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command="npm install -g aws-cdk && pip install -r requirements.txt",
                synth_command="cdk synth"
            )
                                                                               
        )                                                                       
                                                                               