from wsgiref.simple_server import make_server


def application(environ, start_response):
    """
    :param environ: словарь данных от сервера
    :param start_response: функция для ответа серверу
    """
    # сначала в функцию start_response передаем код ответа и заголовки
    start_response('200 OK', [('Content-Type', 'text/html')])
    # возвращаем тело ответа в виде списка из bite
    return [b'Hello world from a simple WSGI application!']


with make_server('', 8000, application) as httpd:
    print('Serving on port 8000...', 'http://localhost:8000')
    httpd.serve_forever()