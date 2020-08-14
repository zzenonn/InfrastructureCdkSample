#!/usr/bin/env python3

import os

from aws_cdk import core

from infrastructure_cdk.network_stack import NetworkStack
from infrastructure_cdk.instance_stack import InstanceStack
from infrastructure_cdk.database_stack import DatabaseStack
from infrastructure_cdk.ecs_stack import EcsStack
from infrastructure_cdk.lambda_stack import LambdaStack
import jsii

# As part of AWS CDK v2.0, the add_warning function will be deprecated
# in favor of the Annotations.of(construct) API.
# See https://github.com/aws/aws-cdk-rfcs/blob/master/text/0192-remove-constructs-compat.md#09-logging
@jsii.implements(core.IAspect)
class CheckTerminationProtection:
    
  def visit(self, stack):
    # See that we're dealing with a stack object
    if isinstance(stack, core.Stack):
      # Check if termination protection is enabled on the stack
      if (not stack.termination_protection):
        stack.node.add_warning('This stack does not have termination protection enabled.')

with open("./user_data/user_data.sh") as f:
    user_data = f.read()

app = core.App()
NETWORK       = NetworkStack(app, 
                             "NetworkStack", 
                             env=core.Environment(account = os.environ["CDK_DEFAULT_ACCOUNT"], 
                                                  region  = os.environ["CDK_DEFAULT_REGION"]))
                                                     
EC2_INSTANCES = InstanceStack(app, 
                              "InstanceStack", 
                              vpc=NETWORK.vpc, 
                              user_data=user_data,
                              env=core.Environment(account  = os.environ["CDK_DEFAULT_ACCOUNT"],
                                                   region   = os.environ["CDK_DEFAULT_REGION"]))

ECS_STACK    = EcsStack(app, 
                        "EcsStack",
                        vpc=NETWORK.vpc,
                        env=core.Environment(account  = os.environ["CDK_DEFAULT_ACCOUNT"],
                                             region   = os.environ["CDK_DEFAULT_REGION"]))
                                                           
LAMBDA_STACK = LambdaStack(app, 
                           "LambdaStack", 
                           env=core.Environment(account = os.environ["CDK_DEFAULT_ACCOUNT"], 
                                                region  = os.environ["CDK_DEFAULT_REGION"]))                                                           
            
DB_INSTANCES = DatabaseStack(app, 
                             "DatabaseStack", 
                             vpc=NETWORK.vpc, 
                             backend_security_groups=EC2_INSTANCES.asg.connections.security_groups, 
                             env=core.Environment(account  = os.environ["CDK_DEFAULT_ACCOUNT"], 
                                                  region   = os.environ["CDK_DEFAULT_REGION"]))

app.node.apply_aspect(CheckTerminationProtection())
app.synth()
