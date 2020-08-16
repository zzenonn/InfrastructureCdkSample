from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    core
)


class LambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        hello_function = _lambda.Function(
            self, 'WelcomeHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda-api'),
            handler='welcome.handler',
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_function,
        )