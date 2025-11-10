from lambdas.utils.response import build_response
from decimal import Decimal

def createTownhouseTypeCheck(body):
    required_fields = ['type', 'title', 'isForSale', 'location', 'coordinate', 'price', 'area', 'discription']
    for field in required_fields:
        if field not in body or body[field] is None:
            return build_response(400, {'error': f'Missing required field: {field}'})
    coordinate = body.get('coordinate', {})

    return {
        'type': body['type'],
        'title': body['title'],
        'isForSale': body['isForSale'],
        'location': body['location'],
        'coordinate': {
            'latitude': Decimal(str(coordinate['latitude'])),
            'longitude': Decimal(str(coordinate['longitude']))
        },
        'detail_location': body.get('detail_location'),
        'price': Decimal(str(body['price'])),
        'area': Decimal(str(body['area'])),
        'bedroom': body.get('bedroom'),
        'bathroom': body.get('bathroom'),
        'discription': body['discription'],
        'policy': body.get('policy'),
        'numberOfFloors': body.get('numberOfFloors'),
        'interior': body.get('interior'),
        'entranceWay': body.get('entranceWay'),
    }