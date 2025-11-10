import uuid
from datetime import datetime
import boto3
import os
from botocore.exceptions import ClientError
from lambdas.utils.response import build_response
from lambdas.models.products import createProductTypeCheck

dynamodb = boto3.resource('dynamodb')
products_table = dynamodb.Table(os.environ['VILLAS_TABLE'])


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
        body = createProductTypeCheck(body)
        product_data = {
            'id': str(uuid.uuid4()),
            'created_at': datetime.now().isoformat(),
            **body
        }
        products_table.put_item(Item=product_data)
        return build_response(201, {'message': 'Product created successfully', 'product': product_data['id']}, headers)
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