from constructs import Construct
import aws_cdk as cdk

import boto3

class EcsStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, vpc=None, **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)
        
        cluster = cdk.aws_ecs.Cluster(self, "Globomantics-Cluser", vpc=vpc)
        
        image_asset = cdk.aws_ecr_assets.DockerImageAsset(self, "Globomantics-Landing-Page",
                                                         directory="./globomantics-container-app/"
        )
        
        image = cdk.aws_ecs.ContainerImage.from_docker_image_asset(image_asset)
        
        cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateService(self, "Globomantics-Fargate",
            cluster             = cluster,            
            cpu                 = 256,                  
            desired_count       = 3,      
            listener_port       = 80,
            task_image_options  = cdk.aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                    image          = image,
                                    container_name = "Globomantics-Landing-Page",
                                    container_port = 80
                                    ),
            memory_limit_mib    = 512,
            task_subnets        = cdk.aws_ec2.SubnetSelection(subnet_type=cdk.aws_ec2.SubnetType.PRIVATE_WITH_NAT), # Released in v1.77.0
            public_load_balancer=True)  
        
