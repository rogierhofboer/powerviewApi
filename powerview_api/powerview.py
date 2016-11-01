"""
Powerview api
"""
import json

import requests

from powerview_api.powerviewbase import PowerViewBase
from powerview_api.shades import ShadeType1, ShadeType3, ShadeType2

__author__ = 'sander'


def putt(function):
    def wrapper(*args, **kwargs):
        shade_api_path = args[0].shade_api_path
        body = json.dumps(function(*args, **kwargs))
        response = requests.put(shade_api_path, data=body)
        args[0].process_response(response.json())

    return wrapper


def gett(function):
    def wrapper(*args, **kwargs):
        # shade_api_path = args[0].shade_api_path
        url, params = function(*args)
        response = requests.get(url, params)
        _json = response.json()
        return function.__self__.process_response(_json)
        # slr.process_response(_json)

    return wrapper


class PowerView(PowerViewBase):
    """
    The power view class representing one powerview hub with a
    unique ip address
    """

    def __init__(self, ip_address, get_wrapper, put_wrapper):
        PowerViewBase.__init__(self, ip_address, get_wrapper, put_wrapper)

    # def jog_shade(self, shade_id):
    #     url, body = self._get_jog_data(shade_id)
    #     r = requests.put(url, body)
    #     return r.status_code

    def define_all_shades(self):
        shades = self.get_shades()
        self.all_shades = []
        for shade in shades["shadeData"]:
            self.all_shades.append(self.shade_factory(shade))

    def shade_factory(self, shadedata):
        _type = shadedata["type"]
        if _type in self.type1_shades:
            return ShadeType1(self._shades_path, shadedata)
        elif _type in self.type2_shades:
            return ShadeType2(self._shades_path, shadedata)
        elif _type in self.type3_shades:
            return ShadeType3(self._shades_path, shadedata)
        else:
            return ShadeType1(self._shades_path, shadedata)


if __name__ == "__main__":
    import pprint

    # pv = PowerView("192.168.0.106")
    pv = PowerView("192.168.2.4", gett, putt)
    userdata = pv.get_scenes()
    pv.activate_scene(7247)
    pprint.pprint(userdata)
    # _shade = next((shade for shade in shades["shadeData"] if shade["id"] == 32653))
    # shade = pv.shade_factory(_shade)
    # #shade.close()
    # shade.move(None,shade.tiltcloseposition)

    # shade = pv.shade_factory(shades["shadeData"][0])
    # shade.jog()
    # shade.move(shade.pos1openposition,shade.pos2openposition)
    # shade.open()
    # shade.move2(1000)
    # shade.move(1000,10000)
    # pv.set_blind('7271',0,3)
    # pprint.pprint(pv.get_shade_data('11155', force_refresh=True)['shade'])
