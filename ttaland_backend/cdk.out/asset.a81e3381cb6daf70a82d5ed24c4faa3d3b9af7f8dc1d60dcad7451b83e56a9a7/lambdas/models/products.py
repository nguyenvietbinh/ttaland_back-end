from lambdas.utils.response import build_response

def createProductTypeCheck(body, product_id, bucket_name):
    required_fields = ['type', 'title', 'isForSale', 'location', 'coordinate', 'price', 'area', 'discription', 'images']
    for field in required_fields:
        if field not in body or body[field] is None:
            return build_response(400, {'error': f'Missing required field: {field}'})
    coordinate = body.get('coordinate', {})

    productData = {
        'type': body['type'],
        'title': body['title'],
        'isForSale': body['isForSale'],
        'location': body['location'],
        'coordinate': {
            'latitude': coordinate['latitude'],
            'longitude': coordinate['longitude']
        },
        'detail_location': body.get('detail_location'),
        'price': body['price'],
        'area': body['area'],
        'bedroom': body.get('bedroom'),
        'bathroom': body.get('bathroom'),
        'discription': body['discription'],
        'policy': body.get('policy'),
        'numberOfFloors': body.get('numberOfFloors'),
        'interior': body.get('interior'),
        'entranceWay': body.get('entranceWay'),
        'images': [f'https://{bucket_name}.s3.amazonaws.com/products/{product_id}/{item['name']}.jpg' for item in body.get('images')]
    }

    productData = {k: v for k, v in productData.items() if v is not None}

    return productData