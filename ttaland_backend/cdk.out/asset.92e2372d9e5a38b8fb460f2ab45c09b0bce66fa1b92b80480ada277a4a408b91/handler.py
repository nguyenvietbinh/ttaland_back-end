import json
import routes_handler.users_routes_handler
import routes_handler.products_routes_handler

def handler(event, context):
    
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
            return routes_handler.users_routes_handler.routes_handler(http_method, path, body, cors_headers)
        elif '/products' in path:
            return routes_handler.products_routes_handler.routes_handler(http_method, path, body, cors_headers)
        else:
            return build_response(404, {"error": "Route not found"}, cors_headers)
    except Exception as e:
        return build_response(500, {'error': str(e)}, cors_headers)
    

def build_response(status_code, body, headers):
    """Hàm helper để build response"""
    return {
        'statusCode': status_code,
        'headers': {**headers, 'Content-Type': 'application/json'},
        'body': json.dumps(body, ensure_ascii=False)
    }