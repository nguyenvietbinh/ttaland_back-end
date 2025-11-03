from lambdas.users_lambdas.users import get_all_users, get_user, create_user, update_user, delete_user
from lambdas.utils.response import build_response



def routes_handler(http_method, path, body, cors_headers):
    if http_method == 'GET' and path == '/users':
        return get_all_users(cors_headers)
    elif http_method == 'POST' and path == '/users':
        return create_user(body, cors_headers)
    elif http_method == 'GET' and '/users/' in path:
        user_id = path.split('/')[-1]
        return get_user(user_id, cors_headers)
    elif http_method == 'PUT' and '/users/' in path:
        user_id = path.split('/')[-1]
        return update_user(user_id, body, cors_headers)
    elif http_method == 'DELETE' and '/users/' in path:
        user_id = path.split('/')[-1]
        return delete_user(user_id, cors_headers)
    else:
        return build_response(405, {'error': 'Method not allowed'}, cors_headers)