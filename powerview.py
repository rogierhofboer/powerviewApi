"""
Powerview api
"""

import base64
import json
import pprint
import requests

__author__ = 'sander'


def decode_base64(string):
    """
    Converts base64 to unicode
    """
    return base64.b64decode(string).decode('utf-8')


class PowerView:
    """
    The power view class representing one powerview hub with a
    unique ip address
    """
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.base_path = "http://{}/api".format(ip_address)
        self.scenes_path = "{}/scenes".format(self.base_path)
        self.shades_path = "{}/shades".format(self.base_path)
        self.rooms_path = "{}/rooms".format(self.base_path)

    def get_user_data(self):
        """gets user data"""
        _str = "{}/userdata/".format(self.base_path)
        _user = requests.get(_str)
        dta = _user.json()
        dta["userData"]["hubName"] = decode_base64(dta["userData"]["hubName"])
        return dta

    def get_rooms(self):
        """
        gets room data
        :return:
        """
        _room_data = requests.get(self.rooms_path).json()
        for room in _room_data["roomData"]:
            room["name"] = decode_base64(room["name"])
        return _room_data

    def get_scenes(self):
        """get scenes"""
        dta = requests.get(self.scenes_path).json()
        for scene in dta['sceneData']:
            scene['name'] = decode_base64(scene['name'])
        return dta

    def activate_scene(self, scene_id):
        """

        :param scene_id:
         The id of the scene
        :return:
        """
        _scene_path = "{}?sceneid={}".format(self.scenes_path, scene_id)
        requests.get(_scene_path)

    def set_blind(self, blind_id, position):
        """

        :param blind_id:
        :param position:
        :return:
        """
        url = "{}{}/".format(self.shades_path, blind_id)
        dta = {"shade": {"blind_id": blind_id, "positions": {"posKind1": 1, "position1": position}}}
        print("moving shade")
        print("address: {}".format(url))
        print("data:")
        pprint.pprint(dta)
        r = requests.put(url, data=json.dumps(dta))
        pprint.pprint(r.json())


if __name__ == "__main__":
    pv = PowerView("192.168.0.117")
    pv.get_scenes()
    # pv.set_blind(52214, 30000)
