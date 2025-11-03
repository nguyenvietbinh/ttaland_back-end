import json
import boto3
import os
import logging
from botocore.exceptions import ClientError

# Setup logging với format chi tiết
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Custom formatter để dễ đọc logs
class CustomFormatter(logging.Formatter):
    def format(self, record):
        return f"[{record.levelname}] {record.asctime} - {record.getMessage()}"

# Áp dụng formatter
for handler in logger.handlers:
    handler.setFormatter(CustomFormatter())

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])

def lambda_handler(event, context):
    # Print cơ bản - sẽ xuất hiện trong CloudWatch
    print("=== LAMBDA EXECUTION STARTED ===")
    print(f"Event: {json.dumps(event, indent=2)}")
    print(f"Context: {context}")
    
    # Sử dụng logger
    logger.info("Lambda function invoked")
    logger.info(f"HTTP Method: {event.get('httpMethod')}")
    logger.info(f"Path: {event.get('path')}")
    
    # Debug environment variables (không log sensitive data)
    logger.info(f"Users Table: {os.environ.get('USERS_TABLE')}")
    
    try:
        # CORS headers
        cors_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        }
        
        http_method = event['httpMethod']
        path = event['path']
        
        logger.info(f"Processing: {http_method} {path}")
        
        if http_method == 'OPTIONS':
            print("Handling OPTIONS request")
            return build_response(200, {'message': 'CORS preflight'}, cors_headers)
        
        if http_method == 'GET' and path == '/users':
            print("Getting all users")
            return get_all_users(cors_headers)
        elif http_method == 'POST' and path == '/users':
            print("Creating new user")
            body = json.loads(event['body'])
            logger.info(f"User data: {body}")
            return create_user(body, cors_headers)
        elif http_method == 'GET' and '/users/' in path:
            user_id = path.split('/')[-1]
            print(f"Getting user: {user_id}")
            return get_user(user_id, cors_headers)
        else:
            print(f"Method not allowed: {http_method} {path}")
            return build_response(405, {'error': 'Method not allowed'}, cors_headers)
            
    except Exception as e:
        # Log lỗi chi tiết
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        print(f"ERROR: {str(e)}")
        return build_response(500, {'error': str(e)}, cors_headers)

def get_all_users(headers):
    try:
        print("Scanning users table...")
        response = users_table.scan()
        users = response.get('Items', [])
        print(f"Found {len(users)} users")
        
        for user in users:
            print(f"User: {user.get('id')} - {user.get('name')}")
        
        return build_response(200, users, headers)
    except ClientError as e:
        error_msg = f"DynamoDB error: {e.response['Error']['Message']}"
        print(f"ERROR: {error_msg}")
        logger.error(error_msg)
        return build_response(500, {'error': error_msg}, headers)

def get_user(user_id, headers):
    try:
        print(f"Getting user with ID: {user_id}")
        response = users_table.get_item(Key={'id': user_id})
        user = response.get('Item')
        
        if not user:
            print(f"User {user_id} not found")
            return build_response(404, {'error': 'User not found'}, headers)
        
        print(f"User found: {user}")
        return build_response(200, user, headers)
    except ClientError as e:
        error_msg = f"DynamoDB error: {e.response['Error']['Message']}"
        print(f"ERROR: {error_msg}")
        return build_response(500, {'error': error_msg}, headers)

def create_user(body, headers):
    try:
        print(f"Creating user with data: {body}")
        
        # Validate required fields
        if not body.get('id') or not body.get('name') or not body.get('email'):
            error_msg = "Missing required fields: id, name, email"
            print(f"VALIDATION ERROR: {error_msg}")
            return build_response(400, {'error': error_msg}, headers)
        
        users_table.put_item(Item=body)
        print("User created successfully")
        
        return build_response(201, {
            'message': 'User created successfully', 
            'user': body
        }, headers)
    except ClientError as e:
        error_msg = f"DynamoDB error: {e.response['Error']['Message']}"
        print(f"ERROR: {error_msg}")
        return build_response(500, {'error': error_msg}, headers)

def build_response(status_code, body, headers):
    """Hàm helper để build response"""
    print(f"Building response with status: {status_code}")
    response = {
        'statusCode': status_code,
        'headers': {**headers, 'Content-Type': 'application/json'},
        'body': json.dumps(body, ensure_ascii=False)
    }
    print(f"Response: {response}")
    return response

