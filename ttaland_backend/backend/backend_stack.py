from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    Duration,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct
import os

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Bảng Users
        users_table = dynamodb.Table(
            self, "UsersTable",
            table_name="Users_table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY  # Xóa khi destroy stack (dev only)
        )

        # Bảng Products
        products_table = dynamodb.Table(
            self, "ProductsTable",
            table_name="Products_table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # IAM Role cho Lambda: Quyền DynamoDB
        lambda_role = iam.Role(
            self, "LambdaDynamoDBRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )
        users_table.grant_read_write_data(lambda_role)
        products_table.grant_read_write_data(lambda_role)

        # Lambda cho Users
        user_lambda = _lambda.Function(
            self, "UserLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="user_handler.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), "handlers")),
            role=lambda_role,
            timeout=Duration.seconds(30)
        )

        # Lambda cho Products
        product_lambda = _lambda.Function(
            self, "ProductLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="product_handler.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), "handlers")),
            role=lambda_role,
            timeout=Duration.seconds(30)
        )

        # API Gateway
        api = apigw.RestApi(
            self, "BackendAPI",
            rest_api_name="Backend API",
            description="API for Users and Products"
        )

        # Resources và Methods cho Users
        users_resource = api.root.add_resource("users")
        users_resource.add_method("GET", apigw.LambdaIntegration(user_lambda))
        users_resource.add_method("POST", apigw.LambdaIntegration(user_lambda))

        user_id_resource = users_resource.add_resource("{id}")
        user_id_resource.add_method("GET", apigw.LambdaIntegration(user_lambda))
        user_id_resource.add_method("PUT", apigw.LambdaIntegration(user_lambda))
        user_id_resource.add_method("DELETE", apigw.LambdaIntegration(user_lambda))

        # Resources và Methods cho Products (tương tự)
        products_resource = api.root.add_resource("products")
        products_resource.add_method("GET", apigw.LambdaIntegration(product_lambda))
        products_resource.add_method("POST", apigw.LambdaIntegration(product_lambda))

        product_id_resource = products_resource.add_resource("{id}")
        product_id_resource.add_method("GET", apigw.LambdaIntegration(product_lambda))
        product_id_resource.add_method("PUT", apigw.LambdaIntegration(product_lambda))
        product_id_resource.add_method("DELETE", apigw.LambdaIntegration(product_lambda))

        # Output: API Endpoint
        CfnOutput(
            self, "ApiEndpoint",
            value=api.url,
            description="URL of the API Gateway"
        )





