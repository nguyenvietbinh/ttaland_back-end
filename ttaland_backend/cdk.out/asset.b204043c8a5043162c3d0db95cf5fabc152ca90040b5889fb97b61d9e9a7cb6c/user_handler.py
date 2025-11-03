import json
import boto3
import os
from botocore.exceptions import ClientError
from lambdas.users_lambdas.users import get_all_users, get_user, create_user, update_user, delete_user

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    cors_headers = {
        'Access-Control-Allow-Origin': '*',  # Hoặc 'http://localhost:3000' cho cụ thể
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
    }
    
    try:
        # Xử lý OPTIONS request cho CORS preflight
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        if http_method == 'GET' and path == '/users':
            return get_all_users(cors_headers)
        elif http_method == 'POST' and path == '/users':
            body = json.loads(event['body'])
            return create_user(body, cors_headers)
        elif http_method == 'GET' and '/users/' in path:
            user_id = path.split('/')[-1]
            return get_user(user_id, cors_headers)
        elif http_method == 'PUT' and '/users/' in path:
            user_id = path.split('/')[-1]
            body = json.loads(event['body'])
            return update_user(user_id, body, cors_headers)
        elif http_method == 'DELETE' and '/users/' in path:
            user_id = path.split('/')[-1]
            return delete_user(user_id, cors_headers)
        else:
            return build_response(405, {'error': 'Method not allowed'}, cors_headers)
    except Exception as e:
        return build_response(500, {'error': str(e)}, cors_headers)

def build_response(status_code, body, headers):
    """Hàm helper để build response"""
    return {
        'statusCode': status_code,
        'headers': {**headers, 'Content-Type': 'application/json'},
        'body': json.dumps(body, ensure_ascii=False)
    }