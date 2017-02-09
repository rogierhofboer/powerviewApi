import json
import requests


def sync_api(cls):
    """Class wrapper which adds the request methods to the
    PowerView API calls."""

    def put_wrapper(func):
        # @functools.wraps(func)
        def wrapped1(self, *args, **kwargs):
            url, params = func(self, *args, **kwargs)
            body = json.dumps(params)
            response = requests.put(url, data=body)
            _json = response.json()
            # args[0].process_response(response.json())
            return self.process_response(_json)

        return wrapped1

    def get_wrapper(func):
        def wrapped(self, *args, **kwargs):
            url, params = func(self, *args, **kwargs)
            response = requests.get(url, params)
            _json = response.json()
            return self.process_response(_json)

        return wrapped

    for name in dir(cls):
        func = getattr(cls, name)
        try:
            if getattr(func, 'get_method', False):
                setattr(cls, name, get_wrapper(func))

            elif getattr(func, 'put_method', False):
                setattr(cls, name, put_wrapper(func))
        except AttributeError:
            pass

    return cls