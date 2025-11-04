from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_s3 as s3,
    Duration,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct
import os

class BackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)




        # ----- create tables -----

        # Users table
        users_table = dynamodb.Table(
            self, "UsersTable",
            table_name="Users_table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN
        )
        # Townhouses table
        townhouses_table = dynamodb.Table(
            self, "TownhousesTable",
            table_name="Townhouses_table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN
        )
        # Villas table
        villas_table = dynamodb.Table(
            self, "VillasTable",
            table_name="Villas_table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN
        )
        # Land table
        land_table = dynamodb.Table(
            self, "LandTable",
            table_name="Land_table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN
        )
        # Apartments table
        apartments_table = dynamodb.Table(
            self, "ApartmentsTable",
            table_name="Apartments_table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN
        )


        # ----- create S3 bucket -----
        
        bucket = s3.Bucket(
            self, "BackendImagesBucket",
            bucket_name="ttaland-backend-images",
            versioned=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.RETAIN,
            auto_delete_objects=False
        )
        


        # ----- add lambda role -----

        lambda_role = iam.Role(
            self, "LambdaDynamoDBRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )
        users_table.grant_read_write_data(lambda_role)
        townhouses_table.grant_read_write_data(lambda_role)
        villas_table.grant_read_write_data(lambda_role)
        land_table.grant_read_write_data(lambda_role)
        apartments_table.grant_read_write_data(lambda_role)
        bucket.grant_read_write(lambda_role)




        # ----- add lambda function -----
        
        backend_lambda = _lambda.Function(
            self, "BackendLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="handler.handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), "src")),
            role=lambda_role,
            timeout=Duration.seconds(30),
            environment={
                "USERS_TABLE": users_table.table_name,
                "TOWNHOUSES_TABLE": townhouses_table.table_name,
                "VILLAS_TABLE": villas_table.table_name,
                "LAND_TABLE": land_table.table_name,
                "APARTMENT_TABLE": apartments_table.table_name,
                "IMAGES_BUCKET": bucket.bucket_name
            }
        ) 


        # ----- add api gateway -----

        api = apigw.RestApi(
            self, "BackendAPI",
            rest_api_name="Backend API",
            description="API for TTALand",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=apigw.Cors.DEFAULT_HEADERS,
                max_age=Duration.days(1)
            )
        )


        
        # ----- add endpoint -----


        api.root.add_proxy(
            default_integration=apigw.LambdaIntegration(backend_lambda),
            any_method=True 
        )





        # Output: API Endpoint
        CfnOutput(
            self, "ApiEndpoint",
            value=api.url,
            description="URL of the API Gateway"
        )