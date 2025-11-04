from lambdas.products_lambdas.apartment_lambda import get_product, get_all_products, create_product, update_product, delete_product
from lambdas.utils.response import build_response


def apartments_routes_handler(http_method, path, body, cors_headers):
    if http_method == 'GET':
      if path == '/products/apartments':
        return get_all_products(cors_headers)
      else:
        return get_product(path.split('/')[-1], cors_headers) 
    elif http_method == 'POST':
        return create_product(body, cors_headers)
    elif http_method == 'PUT':
        return update_product(path.split('/')[-1], body, cors_headers)
    elif http_method == 'DELETE':
        return delete_product(path.split('/')[-1], cors_headers)
    else:
        return build_response(405, {'error': 'Method not allowed'}, cors_headers)