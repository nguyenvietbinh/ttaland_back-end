import json
import boto3
import os
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
products_table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    
    # CORS headers
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
    }
    
    try:
        # Handle OPTIONS request
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        if http_method == 'GET' and path == '/products':
            return get_all_products(cors_headers)
        elif http_method == 'POST' and path == '/products':
            body = json.loads(event['body'])
            return create_product(body, cors_headers)
        elif http_method == 'GET' and '/products/' in path:
            product_id = path.split('/')[-1]
            return get_product(product_id, cors_headers)
        elif http_method == 'PUT' and '/products/' in path:
            product_id = path.split('/')[-1]
            body = json.loads(event['body'])
            return update_product(product_id, body, cors_headers)
        elif http_method == 'DELETE' and '/products/' in path:
            product_id = path.split('/')[-1]
            return delete_product(product_id, cors_headers)
        else:
            return build_response(405, {'error': 'Method not allowed'}, cors_headers)
    except Exception as e:
        return build_response(500, {'error': str(e)}, cors_headers)

def get_all_products(headers):
    try:
        response = products_table.scan()
        products = response.get('Items', [])
        return build_response(200, products, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def get_product(product_id, headers):
    try:
        response = products_table.get_item(Key={'id': product_id})
        product = response.get('Item')
        
        if not product:
            return build_response(404, {'error': 'Product not found'}, headers)
        
        return build_response(200, product, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def create_product(body, headers):
    try:
        if not body.get('id') or not body.get('name') or not body.get('price'):
            return build_response(400, {'error': 'Missing required fields: id, name, price'}, headers)
        
        products_table.put_item(Item=body)
        return build_response(201, {'message': 'Product created successfully', 'product': body}, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def update_product(product_id, body, headers):
    try:
        response = products_table.get_item(Key={'id': product_id})
        if 'Item' not in response:
            return build_response(404, {'error': 'Product not found'}, headers)
        
        update_expression = "SET "
        expression_attribute_names = {}
        expression_attribute_values = {}
        
        for key, value in body.items():
            if key != 'id':
                update_expression += f"#{key} = :{key}, "
                expression_attribute_names[f"#{key}"] = key
                expression_attribute_values[f":{key}"] = value
        
        update_expression = update_expression.rstrip(', ')
        
        products_table.update_item(
            Key={'id': product_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )
        
        return build_response(200, {'message': 'Product updated successfully'}, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def delete_product(product_id, headers):
    try:
        products_table.delete_item(Key={'id': product_id})
        return build_response(200, {'message': 'Product deleted successfully'}, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def build_response(status_code, body, headers):
    """Hàm helper để build response"""
    return {
        'statusCode': status_code,
        'headers': {**headers, 'Content-Type': 'application/json'},
        'body': json.dumps(body, ensure_ascii=False)
    }