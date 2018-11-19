from functools import wraps
from flask import request, make_response, jsonify
from app.models.user_model import User
from app import conn

# app.config['SECRET_KEY'] = "thisissecret"

cur = conn.cursor()
def token_required(f):
    """
    Decorator function to ensure that a resource is access by only authenticated users`
    provided their auth tokens are valid
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response(jsonify({
                'status': 'failed',
                'message': 'Token is missing'
            })), 401

        try:
            decode_response = User.decode_auth_token(token)
            
            sql1 = """
                SELECT email FROM Users WHERE user_id=%s
            """
            cur.execute(sql1,(decode_response,))
            user = cur.fetchone()
            current_user = user[0]
            
        except:
            message = "Invalid token"
            decode_response = User.decode_auth_token(token)
            if isinstance(decode_response, str):
                message = decode_response
            return make_response(jsonify({
                'status': 'failed',
                'message': message
            })), 401

        return f(current_user,*args, **kwargs)

    return decorated_function


def response(status, message, status_code):
    """
    Helper method to make an Http response
    :param status: Status
    :param message: Message
    :param status_code: Http status code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code


def response_auth(status, message, token, status_code):
    """
    Make a Http response to send the auth token
    :param status: Status
    :param message: Message
    :param token: Authorization Token
    :param status_code: Http status code
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': status,
        'message': message,
        'auth_token': token.decode("utf-8")
    })), status_code

def response_for_user_order(status, item, status_code):
    """
    Http response for response with a order item.
    :param status: Status Message
    :param item: OrderId
    :param status_code: Http Status Code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'item': item
    })), status_code

def response_for_user_orders(status, orders, status_code):
    """
    Http response for response with users orders.
    :param status: Status Message
    :param status_code: Http Status Code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'orders': orders
    })), status_code

