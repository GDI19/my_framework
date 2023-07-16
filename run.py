from wsgiref.simple_server import make_server
from framework.main import Framework
from urls import routes, fronts


application = Framework(routes, fronts)


with make_server('', 8000, application) as httpd:
    print('Serving on port 8000...', 'http://localhost:8000')
    httpd.serve_forever()