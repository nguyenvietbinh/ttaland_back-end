import uuid
from datetime import datetime
import boto3
import os
from botocore.exceptions import ClientError
from lambdas.utils.response import build_response
from lambdas.models.news import createNewsTypeCheck

dynamodb = boto3.resource('dynamodb')
news_table = dynamodb.Table(os.environ['NEWS_TABLE'])
s3 = boto3.client("s3")
bucket_name = os.environ["IMAGES_BUCKET"]


def get_all_news(headers):
    try:
        response = news_table.scan()
        news = response.get('Items', [])
        return build_response(200, news, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def get_news(id, headers):
    try:
        response = news_table.get_item(Key={'id': id})
        news = response.get('Item')
        
        if not news:
            return build_response(404, {'error': 'news not found'}, headers)
        
        return build_response(200, news, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def create_news(body, headers):
    try:
        id = str(uuid.uuid4())
        uploadUrls = genPresignUrl(body.get('images'), id)
        body = createNewsTypeCheck(body, id, bucket_name)
        news_data = {
            'id': id,
            'created_at': datetime.now().isoformat(),
            **body
        }
        news_table.put_item(Item=news_data)
        return build_response(201, {'message': 'News created successfully', 'News_id': id, 'uploadUrls': uploadUrls}, headers)
    except ClientError as e:
        return build_response(500, {'error': e.response['Error']['Message']}, headers)

def genPresignUrl(images, id):
    uploadUrls = []
    for file in images:
        key = f"news/{id}/{file['name']}"

        presigned_url = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": bucket_name,
                "Key": key,
                "ContentType": file['type'] or "application/octet-stream",
            },
            ExpiresIn=900
        )
        uploadUrls.append(presigned_url)
    return uploadUrls
