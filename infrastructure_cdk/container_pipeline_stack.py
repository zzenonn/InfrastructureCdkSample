from constructs import Construct
import aws_cdk as cdk

from container_app_stage import ContainerAppStage


class ContainerPipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        codestar_arn = cdk.CfnParameter(self, "CodeStarArn", type="String",
            description="The ARN of the codestar connection to be used in the source action.")

        source_artifact = cdk.aws_codepipeline.Artifact()
        cloud_assembly_artifact = cdk.aws_codepipeline.Artifact()
        
        pipeline = cdk.pipelines.CodePipeline(self, 'ContainerPipeline',
            self_mutation=True,
            pipeline_name="ContainerPipeline",
            synth=cdk.pipelines.ShellStep("Synth",
                input=cdk.pipelines.CodePipelineSource.connection("zzenonn/InfrastructureCdkSample", 
                    "v2.0.0",
                    connection_arn=codestar_arn.value_as_string
                ),
            install_commands=["npm install -g aws-cdk"],
            commands=["pip install -r requirements.txt", "cdk synth"]
            )
        )     
        
        pipeline.add_stage(ContainerAppStage(self, "Dev",
                                env=cdk.Environment(account  = cdk.Aws.ACCOUNT_ID, 
                                                     region   = cdk.Aws.REGION)))
                                                                               