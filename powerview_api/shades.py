import json

import requests

from powerview_api.powerviewbase import BaseShadeType1, BaseShadeType3, JOG_DATA, BaseShadeType2


def jog(shade_api_path):
    body = JOG_DATA
    requests.put(shade_api_path, data=JOG_DATA)


def putt(function):
    def wrapper(*args,**kwargs):
        shade_api_path = args[0].shade_api_path
        body = json.dumps(function(*args,**kwargs))
        response = requests.put(shade_api_path, data=body)
        args[0].process_response(response.json())

    return wrapper


def gett(function):
    def wrapper(*args):
        shade_api_path = args[0].shade_api_path
        params = function(*args)
        response = requests.get(shade_api_path, params=params)
        args[0].process_response(response.json())

    return wrapper


class ShadeType1(BaseShadeType1):
    def __init__(self, name, shade_id, shades_api_path):
        BaseShadeType1.__init__(self, name, shade_id, shades_api_path)

    def jog(self):
        jog(self.shade_api_path)

    @putt
    def move(self, position, percentage=False):
        return self._get_move_data(position)

    @gett
    def update(self):
        return self.get_update_data()


class ShadeType2(BaseShadeType2):
    def __init__(self, name, shade_id, shades_api_path):
        BaseShadeType2.__init__(self, name, shade_id, shades_api_path)

    @gett
    def update(self):
        return self.get_update_data()

    @putt
    def move(self, position, tilt, percentage=False):
        return self._get_move_data(position, tilt, percentage)


class ShadeType3(BaseShadeType3):
    def __init__(self, name, shade_id, shades_api_path):
        BaseShadeType3.__init__(self, name, shade_id, shades_api_path)

    @gett
    def update(self):
        return self.get_update_data()

    @putt
    def move(self, position1, position2,percentage=False):
        return self._get_move_data(position1, position2,percentage=percentage)
