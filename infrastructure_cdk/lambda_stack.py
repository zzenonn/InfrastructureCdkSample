from constructs import Construct
import aws_cdk as cdk


class LambdaStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        hello_function = cdk.aws_lambda.Function(
            self, 'WelcomeHandler',
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
            code=cdk.aws_lambda.Code.from_asset('lambda-api'),
            handler='welcome.handler',
        )

        cdk.aws_apigateway.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_function,
        )