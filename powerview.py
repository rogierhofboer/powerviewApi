"""
Powerview api
"""

import base64
import json
import pprint
import requests
import time

from decode import decode_base64
from powerviewbase import PowerViewBase

__author__ = 'sander'


class PowerView:
    """
    The power view class representing one powerview hub with a
    unique ip address
    """

    def __init__(self, ip_address):
        self.pvb = PowerViewBase(ip_address)

    def get_user_data(self):
        """gets user data"""
        _str = self.pvb.get_user_data()
        _user = requests.get(_str)
        dta = _user.json()
        dta["userData"]["hubName"] = decode_base64(dta["userData"]["hubName"])
        return dta

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
            },
            {
              "id":64073,
              "name":"UGxpc3NlIDE=",
              "roomId":64902,
              "order":1,
              "colorId":5,
              "iconId":0
            },
            {
              "id":15890,
              "name":"QWxsIHVw",
              "roomId":64902,
              "order":2,
              "colorId":0,
              "iconId":0
            },
            {
              "id":42747,
              "name":"UGxpc3NlIDI=",
              "roomId":64902,
              "order":3,
              "colorId":7,
              "iconId":0
            }
          ]
        }
        """
        dta = requests.get(self.pvb.scenes_path).json()
        for scene in dta['sceneData']:
            scene['name'] = decode_base64(scene['name'])
        return dta

    def activate_scene(self, scene_id):
        """

        :param scene_id:
         The id of the scene
        :return:
        """
        _scene_path = self.pvb.get_activate_scene_path(scene_id)
        requests.get(_scene_path)

    def jog_shade(self, blind_id):
        url = self.pvb.get_blind_path_url(blind_id)
        r = requests.put(url, self.pvb.get_jog_body())
        return r.status_code

    def get_shades(self):
        url = self.pvb.get_shades()
        r = requests.get(url).json()
        self.pvb.sanitize_shades(r)
        return r

    def get_shade_data(self,shade_id,update_battery_level=False):
        url = self.pvb.get_shade_data(shade_id,update_battery_level)
        r = requests.get(url).json()
        return r

    def set_blind(self, blind_id, position,positionkind):
        """

        :param blind_id:
        :param position: value between 0 and 65535
        :return:
        """
        url, dta = self.pvb.get_activate_blind_data(blind_id, position,positionkind)
        r = requests.put(url, data=dta)
        return r.json()


if __name__ == "__main__":
    pv = PowerView("192.168.0.106")
    #pv.set_blind('7271',0,3)
    print(pv.set_blind('7271', 0, 1))
    time.sleep(1)
    pv.jog_shade('7271')
