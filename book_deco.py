#decorators for logging the requests
from functools import wraps
from flask import request

def print_query(func):
	def deco_Books_query_string(*arg, **kwargs):
		q = func(*arg, **kwargs)
		print(q)
		return q
	return deco_Books_query_string

def print_body_books(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if request.method == 'POST' or request.method == 'PUT':
            data = request.json
            print(data)
        return func(*args, **kwargs)
    return wrapper_func
