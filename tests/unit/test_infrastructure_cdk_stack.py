import json
import pytest

from aws_cdk import core
from infrastructure_cdk.infrastructure_cdk_stack import InfrastructureCdkStack


def get_template():
    app = core.App()
    InfrastructureCdkStack(app, "infrastructure-cdk")
    return json.dumps(app.synth().get_stack("infrastructure-cdk").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
