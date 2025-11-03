import json
import routes_handler.users_routes_handler
import routes_handler.products_routes_handler
from lambdas.utils.response import build_response
import os
import boto3

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])


def handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    print(path)
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
    }
    body = json.loads(event['body'])
    try:
        # Handle OPTIONS request
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        if '/users' in path:
            response = users_table.scan()
            users = response.get('Items', [])
            return build_response(200, users, cors_headers)
        elif '/products' in path:
            routes_handler.products_routes_handler.routes_handler(http_method, path, body, cors_headers)
    except Exception as e:
        return build_response(500, {'error': str(e)}, cors_headers)