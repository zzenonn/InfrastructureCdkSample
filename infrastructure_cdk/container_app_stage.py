from ecs_stack import EcsStack
from network_stack import NetworkStack

from constructs import Construct
import aws_cdk as cdk

import os


class ContainerAppStage(cdk.Stage):
  def __init__(self, scope: Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    NETWORK       = NetworkStack(
                    self, "NetworkStack", 
                    )
    ECS_STACK    = EcsStack(self, 
                    "EcsStack",
                    vpc=NETWORK.vpc)


                                                                               