# import json
# import boto3
# from datetime import datetime
# import os

# dynamodb = boto3.resource('dynamodb')
# table_name = os.environ.get('TABLE_NAME', 'Users')
# table = dynamodb.Table(table_name)

# def lambda_handler(event, context):
#     http_method = event['httpMethod']
#     path = event['path']
    
#     # Handle CORS preflight
#     if http_method == 'OPTIONS':
#         return {
#             'statusCode': 200,
#             'headers': {
#                 'Access-Control-Allow-Origin': '*',
#                 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
#                 'Access-Control-Allow-Headers': 'Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token'
#             },
#             'body': json.dumps({'message': 'CORS preflight'})
#         }
    
#     # Route handling
#     if http_method == 'GET' and path == '/users':
#         return get_users()
#     elif http_method == 'POST' and path == '/users':
#         return create_user(event)
#     elif http_method == 'GET' and path.startswith('/users/'):
#         user_id = path.split('/')[-1]
#         return get_user(user_id)
#     else:
#         return {
#             'statusCode': 404,
#             'headers': {
#                 'Access-Control-Allow-Origin': '*',
#                 'Content-Type': 'application/json'
#             },
#             'body': json.dumps({'message': 'Route not found'})
#         }

# def get_users():
#     try:
#         response = table.scan()
#         users = response.get('Items', [])
#         return {
#             'statusCode': 200,
#             'headers': {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*'
#             },
#             'body': json.dumps(users)
#         }
#     except Exception as e:
#         return error_response(str(e))

# def get_user(user_id):
#     try:
#         response = table.get_item(Key={'user_id': user_id})
#         if 'Item' in response:
#             return {
#                 'statusCode': 200,
#                 'headers': {
#                     'Content-Type': 'application/json',
#                     'Access-Control-Allow-Origin': '*'
#                 },
#                 'body': json.dumps(response['Item'])
#             }
#         else:
#             return {
#                 'statusCode': 404,
#                 'headers': {
#                     'Content-Type': 'application/json',
#                     'Access-Control-Allow-Origin': '*'
#                 },
#                 'body': json.dumps({'message': 'User not found'})
#             }
#     except Exception as e:
#         return error_response(str(e))

# def create_user(event):
#     try:
#         body = json.loads(event['body'])
#         user_id = body.get('user_id')
#         name = body.get('name')
#         email = body.get('email')
        
#         if not all([user_id, name, email]):
#             return {
#                 'statusCode': 400,
#                 'headers': {
#                     'Content-Type': 'application/json',
#                     'Access-Control-Allow-Origin': '*'
#                 },
#                 'body': json.dumps({'message': 'Missing required fields: user_id, name, email'})
#             }
        
#         item = {
#             'user_id': user_id,
#             'name': name,
#             'email': email,
#             'created_at': datetime.now().isoformat()
#         }
        
#         table.put_item(Item=item)
        
#         return {
#             'statusCode': 201,
#             'headers': {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*'
#             },
#             'body': json.dumps({'message': 'User created successfully', 'user': item})
#         }
#     except Exception as e:
#         return error_response(str(e))

# def error_response(error_message):
#     return {
#         'statusCode': 500,
#         'headers': {
#             'Content-Type': 'application/json',
#             'Access-Control-Allow-Origin': '*'
#         },
#         'body': json.dumps({'error': error_message})
#     }
















import json
from src.routes import products_routes
from src.utils.response import success_response, error_response

def lambda_handler(event, context):
    path = event.get("path", "")
    method = event.get("httpMethod", "")
    body = json.loads(event.get("body") or "{}")

    try:
        if path == "/products":
            return products_routes.handle_request(method, body)
        elif path.startswith("/users"):
            return {"statusCode": 200, "body": "List of users"}
        else:
            return error_response(404, "Route not found")
    except Exception as e:
        print("Error:", e)
        return error_response(500, str(e))
