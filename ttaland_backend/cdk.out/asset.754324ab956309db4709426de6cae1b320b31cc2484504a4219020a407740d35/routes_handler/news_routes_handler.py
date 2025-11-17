from lambdas.utils.response import build_response
from lambdas.news_lambdas.news import create_news, get_all_news, get_news


def routes_handler(http_method, path, body, cors_headers):
  if http_method == 'POST' and path == '/news':
    return create_news(body, cors_headers)
  elif http_method == 'GET' and path == '/news':
    return get_all_news(cors_headers)
  elif http_method == 'GET' and '/news/' in path:
    id = path.split('/')[-1]
    return get_news(id, cors_headers)
  else:
    return build_response(405, {'error': 'Method not allowed'}, cors_headers)