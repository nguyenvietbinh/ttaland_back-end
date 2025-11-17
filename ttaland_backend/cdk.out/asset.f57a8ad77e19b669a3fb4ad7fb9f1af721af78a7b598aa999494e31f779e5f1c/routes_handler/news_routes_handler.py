
from lambdas.utils.response import build_response


def routes_handler(http_method, path, body, cors_headers):
  if http_method == 'POST' and path == '/news':
    return
  elif http_method == 'GET' and path == '/news':
    return
  elif http_method == 'GET' and '/news/' in path:
    return
  else:
    return build_response(405, {'error': 'Method not allowed'}, cors_headers)