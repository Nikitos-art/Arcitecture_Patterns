def parse_input_data(data: str):
    """Helper function for parsing both GET and POST input data"""
    result = {}
    if data:
        # separating parameters using &
        params = data.split('&')
        for item in params:
            # separating key and value using =
            k, v = item.split('=')
            result[k] = v
    return result


def get_wsgi_input_data(env) -> bytes:
    # Getting body length
    content_length_data = env.get('CONTENT_LENGTH')
    # Turning into integer
    content_length = int(content_length_data) if content_length_data else 0
    print(content_length)
    # Reading data, if it's there
    # env['wsgi.input'] -> <class '_io.BufferedReader'>
    # Launching read mode

    data = env['wsgi.input'].read(content_length) \
        if content_length > 0 else b''
    return data


def parse_wsgi_input_data(data: bytes) -> dict:
    result = {}
    if data:
        # Decoding data
        data_str = data.decode(encoding='utf-8')
        print(f'строка после декод - {data_str}')
        # Putting it into dictionary
        result = parse_input_data(data_str)
    return result


# post requests
class PostRequests:

    def get_request_params(self, environ):
        # получаем данные
        data = get_wsgi_input_data(environ)
        # превращаем данные в словарь
        data = parse_wsgi_input_data(data)
        return data
