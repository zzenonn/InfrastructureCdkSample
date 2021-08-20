from ecs_stack import EcsStack
from network_stack import NetworkStack

from aws_cdk import core
import os


class ContainerAppStage(core.Stage):
  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    NETWORK       = NetworkStack(
                    self, "NetworkStack", 
                    )
    ECS_STACK    = EcsStack(self, 
                    "EcsStack",
                    vpc=NETWORK.vpc)


                                                                               