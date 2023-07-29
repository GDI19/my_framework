from wsgiref.simple_server import make_server
from framework.main import Framework
from urls import fronts
from views import routes_dict

application = Framework(routes_dict, fronts)


with make_server('', 8000, application) as httpd:
    print('Serving on port 8000...', 'http://localhost:8000')
    httpd.serve_forever()