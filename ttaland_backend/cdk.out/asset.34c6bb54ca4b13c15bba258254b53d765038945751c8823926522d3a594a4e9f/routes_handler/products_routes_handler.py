from lambdas.products_lambdas.products import get_product, get_all_products, create_product, update_product, delete_product
from lambdas.utils.response import build_response


def routes_handler(http_method, path, body, cors_headers):
    if http_method == 'GET' and path == '/products':
      return get_all_products(cors_headers)
    elif http_method == 'POST' and path == '/products':
        return create_product(body, cors_headers)
    elif http_method == 'GET' and '/products/' in path:
        product_id = path.split('/')[-1]
        return get_product(product_id, cors_headers)
    elif http_method == 'PUT' and '/products/' in path:
        product_id = path.split('/')[-1]
        return update_product(product_id, body, cors_headers)
    elif http_method == 'DELETE' and '/products/' in path:
        product_id = path.split('/')[-1]
        return delete_product(product_id, cors_headers)
    else:
        return build_response(405, {'error': 'Method not allowed'}, cors_headers)