from lambdas.utils.response import build_response

def createNewsTypeCheck(body, id, bucket_name):
    required_fields = ['title', 'thumb', 'discription', 'contents', 'src']
    for field in required_fields:
        if field not in body or body[field] is None:
            return build_response(400, {'error': f'Missing required field: {field}'})
    for i in body['contents']:
        if i['type'] == 'image':
            i['content'] = f"https://{bucket_name}.s3.amazonaws.com/products/{id}/{i['content']}"


    newsData = {
        'title': body['title'],
        'src': body['src'],
        'thumb': f"https://{bucket_name}.s3.amazonaws.com/products/{id}/{body['thumb']['name']}",
        'discription': body['discription'],
        'contents': body['contents']
    }

    return newsData