from quopri import decodestring


class ParseSaveInputData:

    @staticmethod
    def parsing(str_data):
        result = {}
        if str_data:
            params = str_data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

    @staticmethod
    def write_contact_msg_file(data):
        with open('messages.txt', 'a', encoding='utf-8') as f:
            for k, v in data.items():
                f.write(f'{k}: {v}\n')
            f.write(('-' * 20) + '\n')


class GetRequests:
    def __init__(self, environ):
        self.environ = environ

    def __call__(self):
        query_string = self.environ['QUERY_STRING']
        if query_string:
            # print('query_string', query_string)
            params = ParseSaveInputData().parsing(query_string)
            # print('get params', params)
            checked_params = ParseSaveInputData().decode_value(params)
            return checked_params


class PostRequests:
    def __init__(self, environ):
        self.environ = environ

    def __call__(self):
        data_length = self.environ['CONTENT_LENGTH']
        # print('data_length:', data_length)
        if data_length:
            raw_data = self.environ['wsgi.input'].read(int(data_length))
            # print('raw POST data:', raw_data)
            data = raw_data.decode(encoding='utf-8')
            # print('str data:', data)
            params = ParseSaveInputData.parsing(data)
            # print('post params', params)
            checked_params = ParseSaveInputData().decode_value(params)
            ParseSaveInputData().write_contact_msg_file(checked_params)
            return  checked_params
        return b''


