from datetime import datetime
from functools import update_wrapper
from time import time

# routes_dict = {}

# # route decorator
# def routes(route):
#     def wrap(cls):
#         if not route in routes_dict:
#             routes_dict[route] = cls()
#         return cls
#     return wrap

class AppRoutes:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()
#
# def debug(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         datetime_now = datetime.now()
#         print(datetime_now, ': ', func.__name__)
#         return func(*args, **kwargs)
#     return wrapper

class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            '''Оборачивает каждый метод декорируемого класса'''
            def timed(*args, **kwargs):
                t_start = time()
                result = method(*args, **kwargs)
                t_end = time()
                delta = t_end - t_start
                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result
            return timed
        return timeit(cls)