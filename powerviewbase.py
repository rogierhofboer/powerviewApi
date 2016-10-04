import json

from decode import decode_base64


class PowerViewBase:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self._base_path = "http://{}/api".format(ip_address)
        self._scenes_path = "{}/scenes".format(self._base_path)
        self._shades_path = "{}/shades".format(self._base_path)
        self._rooms_path = "{}/rooms".format(self._base_path)
        self._user_path = "{}/userdata/".format(self._base_path)
        self._jog_body = {"shade": {"motion": "jog"}}

    def move_blind(self, blind_id, position, positionkind):
        raise NotImplemented

    def get_user_data(self):
        raise NotImplemented

    def jog_shade(self, shade_id):
        raise NotImplemented

    def get_shades(self):
        raise NotImplemented

    def get_shade_data(self):
        raise NotImplemented

    def get_scenes(self):
        raise NotImplemented

    def activate_scene(self, scene_id):
        raise NotImplemented

    def get_rooms(self):
        raise NotImplemented

    def _get_activate_scene_data(self, scene_id):
        _scene_path = "{}?sceneid={}".format(self._scenes_path, scene_id)
        return _scene_path

    def _get_blind_path_url(self, blind_id):
        url = "{}/{}".format(self._shades_path, blind_id)
        return url

    def _get_jog_data(self, shade_id):
        """
        :param shade_id:
        :return: The url and body to put in the request.
        """
        return self._get_blind_path_url(shade_id), self._jog_body

    def _get_position_body(self, position, blind_id, positionkind):
        return json.dumps(
            {"shade": {"blind_id": blind_id, "positions": {"posKind1": positionkind, "position1": position}}})

    def _get_shade_data(self, shade_id):
        return "{}/{}".format(self._shades_path, shade_id)

    def get_activate_blind_data(self, blind_id, position, positionkind):
        url = self._get_blind_path_url(blind_id)
        body = self._get_position_body(position, blind_id, positionkind)
        return (url, body)

    def sanitize_shades(self, shades):
        for shade in shades['shadeData']:
            shade['name'] = decode_base64(shade.get('name', ''))

    def sanitize_scenes(self, scenes):
        for scene in scenes['sceneData']:
            scene['name'] = decode_base64(scene['name'])

    def sanitize_user_data(self, userdata):
        userdata["userData"]["hubName"] = decode_base64(userdata["userData"]["hubName"])


class BaseShade:
    def __init__(self, name, shade_id, shades_api_path):
        self.name = name
        self.shade_id = shade_id
        self.shade_api_path = "{}/{}".format(shades_api_path, shade_id)


class ShadeType1(BaseShade):
    """
    A basic "up" down "shade"
    """
    def __init__(self,name,shade_id,shades_api_path):
        BaseShade.__init__(self,name,shade_id,shades_api_path)

    def move1(self,position):
        pass



class ShadeType2(BaseShade):
    def __init__(self):
        pass
