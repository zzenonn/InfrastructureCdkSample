#!/usr/bin/env python3

from aws_cdk import core

from infrastructure_cdk.infrastructure_cdk_stack import InfrastructureCdkStack


app = core.App()
InfrastructureCdkStack(app, "infrastructure-cdk", env={'region': 'us-west-2'})

app.synth()
