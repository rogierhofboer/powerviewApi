import base64
import json
import pprint

__author__ = 'sander'

import requests


def decode_base64(str):
    return base64.b64decode(str).decode('utf-8')


class PowerView():
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.base_path = "http://{}/api".format(ip_address)
        self.scenes_path = "{}/scenes/".format(self.base_path)
        self.shades_path = "{}/shades/".format(self.base_path)

    def get_user_data(self):
        _user_data = "{}/userdata/".format(self.base_path)
        r = requests.get(_user_data)
        dta = r.json()
        dta["userData"]["hubName"] = decode_base64(dta["userData"]["hubName"])
        return dta

    def get_scenes(self):
        print("requesting : {}".format(self.scenes_path))
        # headers={'Content-Type':"application/json",'user-agent':'test-app'}
        r = requests.get(self.scenes_path)
        dta = r.json()
        for scene in dta['sceneData']:
            # str = base64.b64decode(scene['name'])
            scene['name'] = decode_base64(scene['name'])
            # print("Scene : id: {} -- name: {}".format(scene['id'], scene['name']))
            # pprint.pprint(dta)
        return dta

    def set_blind(self, id, position):
        url = "{}{}/".format(self.shades_path, id)
        dta = {"shade": {"id": id, "positions": {"posKind1": 1, "position1": position}}}
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
