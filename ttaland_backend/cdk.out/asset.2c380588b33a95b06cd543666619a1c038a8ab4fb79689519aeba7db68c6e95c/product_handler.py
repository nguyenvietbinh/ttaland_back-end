import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Products_table')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    
    if http_method == 'GET' and path == '/products':
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    elif http_method == 'GET' and path.startswith('/products/'):
        product_id = path.split('/')[-1]
        response = table.get_item(Key={'id': product_id})
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Item', {}))
        }
    elif http_method == 'POST' and path == '/products':
        body = json.loads(event['body'])
        table.put_item(Item=body)
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Product created'})
        }
    elif http_method == 'PUT' and path.startswith('/products/'):
        product_id = path.split('/')[-1]
        body = json.loads(event['body'])
        table.update_item(
            Key={'id': product_id},
            UpdateExpression='SET name=:n, price=:p',
            ExpressionAttributeValues={':n': body['name'], ':p': body['price']}
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Product updated'})
        }
    elif http_method == 'DELETE' and path.startswith('/products/'):
        product_id = path.split('/')[-1]
        table.delete_item(Key={'id': product_id})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Product deleted'})
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Not found'})
        }