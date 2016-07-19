"""
Powerview api
"""
import asyncio
import logging
import pprint
import aiohttp

from decode import decode_base64
from powerviewbase import PowerViewBase

__author__ = 'sander'
lgr = logging.getLogger(__name__)

class PowerViewAsync:
    """
    The power view class representing one powerview hub with a
    unique ip address
    """

    def __init__(self, ip_address, session):
        self.pvb = PowerViewBase(ip_address)
        self.session = session

    @asyncio.coroutine
    def get_user_data(self):
        """gets user data"""
        _str = self.pvb.get_user_data()
        resp = yield from self.session.get(_str)
        assert resp.status == 200
        try:
            dta = yield from resp.json()
            dta["userData"]["hubName"] = decode_base64(dta["userData"]["hubName"])
            return dta
        finally:
            yield from resp.release()

    @asyncio.coroutine
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
        resp =yield from self.session.get(self.pvb.rooms_path)
        try:
            _room_data = yield from resp.json()
            for room in _room_data["roomData"]:
                room["name"] = decode_base64(room["name"])
            return _room_data
        finally:
            yield from resp.release()

    @asyncio.coroutine
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
        resp = yield from self.session.get(self.pvb.scenes_path)
        try:
            dta = yield from resp.json()
            for scene in dta['sceneData']:
                scene['name'] = decode_base64(scene['name'])
            return dta
        finally:
            yield from resp.release()

    @asyncio.coroutine
    def activate_scene(self, scene_id):
        """

        :param scene_id:
         The id of the scene
        :return:
        """
        _scene_path = self.pvb.get_activate_scene_path(scene_id)
        resp = yield from self.session.get(_scene_path)
        yield from resp.release()
        return

    @asyncio.coroutine
    def get_shades(self):
        resp = yield from self.session.get(self.pvb.shades_path)
        assert resp.status == 200
        try:
            js = yield from resp.json()
            self.pvb.sanitize_shades(js)
            lgr.debug(js)
            return js
        finally:
            yield from resp.release()

    @asyncio.coroutine
    def set_blind(self, blind_id, position):
        """

        :param blind_id:
        :param position:
        :return:
        """
        url, dta = self.pvb.get_activate_blind_data(blind_id, position)
        print("moving shade")
        print("address: {}".format(url))
        print("data:")
        #pprint.pprint(dta)
        resp = yield from self.session.put(url,data=dta)
        try:
            r = yield from resp.json()
            # pprint.pprint(r.json())
            return r
        finally:
            yield from resp.release()


if __name__ == "__main__":
    lgr.level=logging.DEBUG
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop)
    pv = PowerViewAsync("192.168.2.4", session)
    loop.run_until_complete(pv.get_shades())
    session.close()
    # pv.set_blind(52214, 30000)
