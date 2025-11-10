from lambdas.utils.response import build_response
from routes_handler.products.apartments_routes_handler import apartments_routes_handler
from routes_handler.products.land_routes_handler import land_routes_handler
from routes_handler.products.townhouses_routes_handler import townhouses_routes_handler
from routes_handler.products.villas_routes_handler import villas_routes_handler

def routes_handler(http_method, path, body, cors_headers):
    if '/products/townhouses' in path:
        return townhouses_routes_handler(http_method, path, body, cors_headers)
    elif '/products/villas' in path:
        return villas_routes_handler(http_method, path, body, cors_headers)
    elif '/products/land' in path:
        return land_routes_handler(http_method, path, body, cors_headers)
    elif '/products/apartments' in path:
        return apartments_routes_handler(http_method, path, body, cors_headers)
    else:
        return build_response(404, {'error': 'Page not found'}, cors_headers)