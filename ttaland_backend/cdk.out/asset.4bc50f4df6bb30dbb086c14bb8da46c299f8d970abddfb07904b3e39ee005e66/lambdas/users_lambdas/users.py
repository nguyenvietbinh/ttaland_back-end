import json
import boto3
import os
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])


def get_all_users(headers):
    try:
        response = users_table.scan()
        users = response.get('Items', [])
        return build_response(200, users, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def get_user(user_id, headers):
    try:
        response = users_table.get_item(Key={'id': user_id})
        user = response.get('Item')
        
        if not user:
            return build_response(404, {'error': 'User not found'}, headers)
        
        return build_response(200, user, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def create_user(body, headers):
    try:
        # Validate required fields
        if not body.get('id') or not body.get('name') or not body.get('email'):
            return build_response(400, {'error': 'Missing required fields: id, name, email'}, headers)
        
        users_table.put_item(Item=body)
        return build_response(201, {'message': 'User created successfully', 'user': body}, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def update_user(user_id, body, headers):
    try:
        # Check if user exists
        response = users_table.get_item(Key={'id': user_id})
        if 'Item' not in response:
            return build_response(404, {'error': 'User not found'}, headers)
        
        # Update user
        update_expression = "SET "
        expression_attribute_names = {}
        expression_attribute_values = {}
        
        for key, value in body.items():
            if key != 'id':  # Don't update the id
                update_expression += f"#{key} = :{key}, "
                expression_attribute_names[f"#{key}"] = key
                expression_attribute_values[f":{key}"] = value
        
        update_expression = update_expression.rstrip(', ')
        
        users_table.update_item(
            Key={'id': user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )
        
        return build_response(200, {'message': 'User updated successfully'}, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def delete_user(user_id, headers):
    try:
        users_table.delete_item(Key={'id': user_id})
        return build_response(200, {'message': 'User deleted successfully'}, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)



def build_response(status_code, body, headers):
    """Hàm helper để build response"""
    return {
        'statusCode': status_code,
        'headers': {**headers, 'Content-Type': 'application/json'},
        'body': json.dumps(body, ensure_ascii=False)
    }