from aws_cdk import (
    core,
    aws_ecs as ecs,
    aws_ecr_assets as ecs_assets,
    aws_ecs_patterns as ecs_patterns
)

import boto3

class EcsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc=None, **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)
        
        cluster = ecs.Cluster(self, "Globomantics-Cluser", vpc=vpc)
        
        image_asset = ecs_assets.DockerImageAsset(self, "Globomantics-Landing-Page",
                                                         directory="./globomantics-container-app/"
        )
        
        image = ecs.ContainerImage.from_docker_image_asset(image_asset)
        
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "Globomantics-Fargate",
            cluster             = cluster,            
            cpu                 = 256,                  
            desired_count       = 3,      
            listener_port       = 80,
            task_image_options  = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                    image          = image,
                                    container_name = "Globomantics-Landing-Page",
                                    container_port = 80
                                    ),
            memory_limit_mib=512,      
            public_load_balancer=True)  
        
