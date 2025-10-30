import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    
    if http_method == 'GET' and path == '/users':
        # List all users
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    elif http_method == 'GET' and path.startswith('/users/'):
        # Get user by id
        user_id = path.split('/')[-1]
        response = table.get_item(Key={'id': user_id})
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Item', {}))
        }
    elif http_method == 'POST' and path == '/users':
        # Create user
        body = json.loads(event['body'])
        table.put_item(Item=body)
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'User created'})
        }
    elif http_method == 'PUT' and path.startswith('/users/'):
        # Update user
        user_id = path.split('/')[-1]
        body = json.loads(event['body'])
        table.update_item(
            Key={'id': user_id},
            UpdateExpression='SET name=:n, email=:e',
            ExpressionAttributeValues={':n': body['name'], ':e': body['email']}
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User updated'})
        }
    elif http_method == 'DELETE' and path.startswith('/users/'):
        # Delete user
        user_id = path.split('/')[-1]
        table.delete_item(Key={'id': user_id})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User deleted'})
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Not found'})
        }