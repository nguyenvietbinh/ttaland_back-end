import json
try:
    from routes_handler.users_routes_handler import routes_handler as users_routes
    from routes_handler.products_routes_handler import routes_handler as products_routes
except ImportError:
    # Xử lý lỗi import
    pass
from lambdas.utils.response import build_response
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f"Processing {event['httpMethod']} {event['path']}")
    http_method = event['httpMethod']
    path = event['path']
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
    }
    body = {}
    if event.get('body'):
        try:
            body = json.loads(event['body'])
        except:
            body = {}
    try:
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        if '/users' in path:
            return users_routes(http_method, path, body, cors_headers)
        elif '/products' in path:
            return products_routes.products_routes_handler.routes_handler(http_method, path, body, cors_headers)
        else:
            return build_response(404, {"error": "Route not found"}, cors_headers)
    except Exception as e:
        return build_response(500, {'error': str(e)}, cors_headers)
    