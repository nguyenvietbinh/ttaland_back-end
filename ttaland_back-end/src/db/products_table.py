import os
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["PRODUCTS_TABLE"])



def post_product(product_id, title, discription):
  table.put_item(Item={
    "product_id": product_id,
    "title": title,
    "discription": discription
  })
  return {"message": "Product created"}

def get_products():
  response = table.scan()
  return response.get('Items', [])

