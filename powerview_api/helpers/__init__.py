import requests
import json


def add_api_path(func):
    def wrapper(self, *args, **kwargs):
        return self.shade_api_path, func(self, *args, **kwargs)

    return wrapper





def get_method(func):
    func.get_method = True
    return func


def put_method(func):
    func.put_method = True
    return func