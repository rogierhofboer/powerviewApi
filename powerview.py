"""
Powerview api
"""

import base64
import json
import pprint
import requests
import time

from decode import decode_base64
from powerviewbase import PowerViewBase, BaseShadeType1
from shades import ShadeType1, ShadeType3, ShadeType2

__author__ = 'sander'


class PowerView(PowerViewBase):
    """
    The power view class representing one powerview hub with a
    unique ip address
    """

    def __init__(self, ip_address):
        PowerViewBase.__init__(self, ip_address)
        # self.pvb = PowerViewBase(ip_address)

    def get_user_data(self):
        """gets user data"""
        response = requests.get(self._user_path).json()
        self.sanitize_user_data(response)
        return response

    def get_rooms(self):
        """
        gets room data

        returns a dict:
        {
          "roomIds":[64902],
          "roomData":[
            {
              "id":64902,
              "name":"<roomname>",
              "order":0,
              "colorId":6,
              "iconId":0,
              "order":0
            }
          ]
        }
        """
        _room_data = requests.get(self.pvb.rooms_path).json()
        for room in _room_data["roomData"]:
            room["name"] = decode_base64(room["name"])
        return _room_data

    def get_scenes(self):
        """get scenes

        returns a dict:
        {
          "sceneIds":[7214,64073,15890,42747],
          "sceneData":[
            {
              "id":7214,
              "name":"QWxsIGRvd24=",
              "roomId":64902,
              "order":0,
              "colorId":2,
              "iconId":0
            }
          ]
        }
        """
        response = requests.get(self._scenes_path).json()
        self.sanitize_scenes(response)
        return response

    def activate_scene(self, scene_id):
        """

        :param scene_id:
         The id of the scene
        :return:
        """
        _scene_path = self._get_activate_scene_data(scene_id)
        requests.get(_scene_path)

    # def jog_shade(self, shade_id):
    #     url, body = self._get_jog_data(shade_id)
    #     r = requests.put(url, body)
    #     return r.status_code

    def get_shades(self):
        r = requests.get(self._shades_path).json()
        self.sanitize_shades(r)
        return r

    # def get_shade_data(self, shade_id, update_battery_level=None, force_refresh=None):
    #     url = self._get_shade_data(shade_id)
    #     r = requests.get(url, params={"refresh": force_refresh}).json()
    #     return r

    # def move_blind(self, blind_id, position, positionkind):
    #     """
    #
    #     :param blind_id:
    #     :param position: value between 0 and 65535
    #     :return:
    #     """
    #     url, dta = self._get_activate_blind_data(blind_id, position, positionkind)
    #     r = requests.put(url, data=dta)
    #     return r.json()

    def shade_factory(self, shadedata):
        _name = shadedata["name"]
        _id = shadedata["id"]
        _type = shadedata["type"]
        if _type in self.type1_shades:
            return ShadeType1(_name, _id, self._shades_path)
        elif _type in self.type2_shades:
            return ShadeType2(_name,_id,self._shades_path)
        elif _type in self.type3_shades:
            return ShadeType3(_name, _id, self._shades_path)
        else:
            return ShadeType1(_name, _id, self._shades_path)

if __name__ == "__main__":
    import pprint

    pv = PowerView("192.168.0.106")
    # pv = PowerView("192.168.2.4")
    shades = pv.get_shades()
    pprint.pprint(shades)
    _shade = next((shade for shade in shades["shadeData"] if shade["id"] == 32653))
    shade = pv.shade_factory(_shade)
    #shade.close()
    shade.move(None,shade.tiltcloseposition)

    # shade = pv.shade_factory(shades["shadeData"][0])
    # shade.jog()
    # shade.move(shade.pos1openposition,shade.pos2openposition)
    # shade.open()
    # shade.move2(1000)
    # shade.move(1000,10000)
    # pv.set_blind('7271',0,3)
    # pprint.pprint(pv.get_shade_data('11155', force_refresh=True)['shade'])
