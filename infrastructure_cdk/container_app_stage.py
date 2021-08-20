from ecs_stack import EcsStack

from aws_cdk import core
import os


class ContainerAppStage(core.Stage):
  def __init__(self, scope: core.Construct, id: str, vpc, **kwargs):
    super().__init__(scope, id, **kwargs)

    ECS_STACK    = EcsStack(self, 
                    "EcsStack",
                    vpc=vpc)


                                                                               