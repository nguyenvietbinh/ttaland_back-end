from lambdas.utils.response import build_response

def createNewsTypeCheck(body, id, bucket_name):
    required_fields = ['title', 'thumb', 'discription', 'contents']
    for field in required_fields:
        if field not in body or body[field] is None:
            return build_response(400, {'error': f'Missing required field: {field}'})
    images = [body['thumb']]
    for i in body['contents']:
        if i['type'] == 'image':
            images.append({
                'name': i['content'],
                'type': i['imageType']
            })
            i['content'] = f"https://{bucket_name}.s3.amazonaws.com/products/{id}/{i['content']}"


    newsData = {
        'title': body['title'],
        'thumb': f"https://{bucket_name}.s3.amazonaws.com/products/{id}/{body['thumb']}",
        'discription': body['discription'],
        'contents': body['contents']
    }

    return newsData