import json

import asyncio
import requests
import time


def putt(function):
    def wrapper(*args,**kwargs):
        time.sleep(1)
        function(args)
    return wrapper

def async_putt(function):
    def wrapper(*args, **kwargs):
        asyncio.sleep(1)
        function(args)
    wrapper = asyncio.coroutine(wrapper)

    return wrapper
