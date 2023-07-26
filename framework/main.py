from framework.frame_requests import GetRequests, PostRequests


class PageNotFound404:
    def __call__(self, request):
        return '404 Upps', '404 Not Found!'


class Framework:
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
        возвращаем тело ответа в виде списка из bytes
        """
        path = environ['PATH_INFO']
        request = {}

        if not path.endswith('/'):
            path = f'{path}/'

        method = environ['REQUEST_METHOD']
        request['method'] = method
        print('method:', method)

        if method == 'GET':
            get_data = GetRequests(environ).__call__()
            request['data'] = get_data
            if get_data:
                print(f'пришёл GET-запрос: {get_data}')
        elif method == 'POST':
            post_data = PostRequests(environ).__call__()
            request['data'] = post_data
            print(f'пришёл POST-запрос: {post_data}')


        # page controller
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        # Front controller
        for item in self.fronts:
            item(request)
        # print('Application request:', request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

