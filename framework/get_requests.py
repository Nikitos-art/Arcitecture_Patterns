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


# get requests
class GetRequests:
    def get_request_params(self, environ):
        # Getting request parameters
        query_string = environ['QUERY_STRING']
        # Turning parameters into a dictionary
        request_params = parse_input_data(query_string)
        return request_params
