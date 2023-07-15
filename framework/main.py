from wsgiref.simple_server import make_server

# page controller
def index(request):
    print('index request', request)
    return '200 OK', [b'Hello world from Index!']

def about(request):
    print('about request', request)
    return '200 OK', [b'About page!']

def not_found_404_view(request):
    print('404 request', request)
    return '404 Upps', [b'404 Not Found!']

class Other:
    def __call__(self, request):
        print('Other request:', request)
        return '200 ok', [b'<h1>Other page!</h1>']

routes = {
    '/': index,
    '/about/': about,
    '/other/': Other()
}

# Front controller
def secret_req(request):
    request['secret'] = 'some secret'

def key_req(request):
    request['key'] = 'key'

fronts = [secret_req, key_req]


class Application:
    """Bypass our routes. Get html body in bytes with
    start_response to server"""
    def __init__(self, routes, fronts):
        """receive our routes"""
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        сначала в функцию start_response передаем код ответа и заголовки
        возвращаем тело ответа в виде списка из bite
        """
        path = environ['PATH_INFO']
        request = {}
        # page controller
        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404_view

        # Front controller
        for item in fronts:
            item(request)
        print('Application request:', request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return body


application = Application(routes, fronts)


with make_server('', 8000, application) as httpd:
    print('Serving on port 8000...', 'http://localhost:8000')
    httpd.serve_forever()