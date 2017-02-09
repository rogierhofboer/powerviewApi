import logging


from powerview_api.helpers.decode import decode_base64
from powerview_api.helpers import get_method

lgr = logging.getLogger(__name__)


class PowerViewBase:
    type1_shades = [6]
    type2_shades = [23, 44]
    type3_shades = [8]

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self._base_path = "http://{}/api".format(ip_address)
        self._scenes_path = "{}/scenes".format(self._base_path)
        self._shades_path = "{}/shades".format(self._base_path)
        self._rooms_path = "{}/rooms".format(self._base_path)
        self._user_path = "{}/userdata/".format(self._base_path)
        self._times_path = "{}/times".format(self._base_path)

        self.all_shades = []

    @get_method
    def get_user_data(self):
        return self._user_path, None

    @get_method
    def get_time(self):
        return self._times_path, None

    @get_method
    def get_shades(self):
        return self._shades_path, None

    @get_method
    def get_scenes(self):
        return self._scenes_path, None

    @get_method
    def activate_scene(self, scene_id):
        return self._scenes_path, {"sceneid": scene_id}

    @get_method
    def get_rooms(self):
        return self._rooms_path, None

    def _get_blind_path_url(self, blind_id):
        url = "{}/{}".format(self._shades_path, blind_id)
        return url

    @staticmethod
    def sanitize_shades(shades):
        try:
            for shade in shades['shadeData']:
                shade['name'] = decode_base64(shade.get('name', ''))
        except KeyError:
            lgr.debug("no shade data available")

    @staticmethod
    def sanitize_scenes(scenes):
        try:
            for scene in scenes['sceneData']:
                scene['name'] = decode_base64(scene['name'])
        except KeyError:
            lgr.debug("no scene data available")

    @staticmethod
    def sanitize_user_data(userdata):
        try:
            userdata["userData"]["hubName"] = decode_base64(
                userdata["userData"]["hubName"])
        except KeyError:
            lgr.debug("no userdata available")

    @staticmethod
    def sanitize_rooms(response):
        try:
            for room in response["roomData"]:
                room["name"] = decode_base64(room["name"])
        except KeyError:
            lgr.debug("no roomdata available")

    @staticmethod
    def get_shade_class_name(shade_type):
        raise NotImplemented

    def process_response(self, response):
        self.sanitize_scenes(response)
        self.sanitize_user_data(response)
        self.sanitize_shades(response)
        self.sanitize_rooms(response)
        return response
