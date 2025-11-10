from lambdas.utils.response import build_response

def createProductTypeCheck(body, product_id, bucket_name):
    required_fields = ['type', 'title', 'isForSale', 'location', 'coordinate', 'price', 'area', 'discription', 'images']
    for field in required_fields:
        if field not in body or body[field] is None:
            return build_response(400, {'error': f'Missing required field: {field}'})
    coordinate = body.get('coordinate', {})
    images = body.get('images', [])
    imagesUrls = []
    for i in images:
        name = i['name'] | 'Bla'
        imagesUrls.append(f'https://{bucket_name}.s3.amazonaws.com/products/{product_id}/{name}')
    print(imagesUrls)
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
        'images': imagesUrls
    }

    productData = {k: v for k, v in productData.items() if v is not None}

    return productData