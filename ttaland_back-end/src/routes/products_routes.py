from src.db import products_table
from src.utils.response import success_response, error_response



def handle_request(method, body):
    if method == "POST":
        product = products_table.post_product(body["product_id"], body["title"], body["discription"])
        return success_response(product)
    elif method == "GET":
        product = products_table.get_products()
        return success_response(product)
    elif method == "DELETE":
        product = products_table.delete_product(body["porduct_id"])
        return success_response(product)
    else:
        return error_response(405, "Method not allowed")