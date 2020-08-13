#!/usr/bin/env python3

import os

from aws_cdk import core

from infrastructure_cdk.network_stack import NetworkStack
from infrastructure_cdk.instance_stack import InstanceStack
from infrastructure_cdk.database_stack import DatabaseStack
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

app = core.App()
network = NetworkStack(app, 
                       "NetworkStack", 
                        env=core.Environment(account = os.environ["CDK_DEFAULT_ACCOUNT"], 
                                             region  = os.environ["CDK_DEFAULT_REGION"]))
                                             
ec2_instances = InstanceStack(app, 
                              "InstanceStack", 
                              network.vpc, 
                              env=core.Environment(account  = os.environ["CDK_DEFAULT_ACCOUNT"],
                                                   region   = os.environ["CDK_DEFAULT_REGION"]))
                                                   
db_instances = DatabaseStack(app, 
                             "DatabaseStack", 
                             network.vpc, 
                             ec2_instances.asg.connections.security_groups, 
                             env= core.Environment(account  = os.environ["CDK_DEFAULT_ACCOUNT"], 
                                                              region   = os.environ["CDK_DEFAULT_REGION"]))


app.node.apply_aspect(CheckTerminationProtection())
app.synth()
