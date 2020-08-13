#!/usr/bin/env python3

import os

from aws_cdk import core

from infrastructure_cdk.network_stack import NetworkStack
from infrastructure_cdk.instance_stack import InstanceStack
from infrastructure_cdk.database_stack import DatabaseStack


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

app.synth()
