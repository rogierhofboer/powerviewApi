import json

import math
import logging
from decode import decode_base64

JOG_DATA = json.dumps({"shade": {"motion": "jog"}})


class PowerViewBase:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self._base_path = "http://{}/api".format(ip_address)
        self._scenes_path = "{}/scenes".format(self._base_path)
        self._shades_path = "{}/shades".format(self._base_path)
        self._rooms_path = "{}/rooms".format(self._base_path)
        self._user_path = "{}/userdata/".format(self._base_path)

        self.type1_shades = [6]
        self.type2_shades = [23, 44]
        self.type3_shades = [8]

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
            {"shade": {"id": blind_id, "positions": {"posKind1": positionkind, "position1": position}}})

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

    def get_shade_class_name(self, shade_type):
        raise NotImplemented


lgr = logging.getLogger(__name__)

MAXMOVEPOSITION = 65535
MAXTILTPOSITION = 32767


def to_percentage_position(value, base=MAXMOVEPOSITION):
    """
    Will convert a PowerView position value to a value between 0 and 100.

    :param value: the position received from the powerview API.
    :param base: normally two bytes. On occasions this can change.
    :return: percentage value
    """
    _multiplier = 100.0 / base
    percentage = math.ceil(value * _multiplier)
    return percentage


def to_powerview_position(percentage, base=MAXMOVEPOSITION):
    """
    Will convert a percentage position value to a value from 0 to base.
    :param percentage:
    :param base:
    :return: powerview position value
    """
    if percentage == None:
        return None
    _multiplier = base / 100.0

    value = math.ceil(percentage * _multiplier)
    return value


def get_positions(response):
    try:
        positions = response.get('shade').get('positions')
        return positions
    except AttributeError:
        lgr.debug("No position feedback from blind ")
        return False


def normalize(self,position):
    pass

class BaseShade:
    def __init__(self, name, shade_id, shades_api_path):
        self.name = name
        self.shade_id = shade_id
        self.shade_api_path = "{}/{}".format(shades_api_path, shade_id)
        self.pos1openposition = MAXMOVEPOSITION
        self.pos1closeposition = 0
        self.base = max(self.pos1openposition, self.pos1closeposition)

    def jog(self):
        raise NotImplemented

    def process_response(self, response):
        raise NotImplemented

    def open(self):
        raise NotImplemented

    def close(self):
        raise NotImplemented

    def update(self):
        raise NotImplemented

    def get_update_data(self):
        return {"refresh": True}


# url = self._get_shade_data(shade_id)
#     r = requests.get(url, params={"refresh": force_refresh}).json()
#     return r

class BaseShadeType1(BaseShade):
    """
    A basic "up" down "shade"
    """

    def __init__(self, name, shade_id, shades_api_path):
        BaseShade.__init__(self, name, shade_id, shades_api_path)
        self.position1 = 0
        self.position1_perc = 0

    def move1(self,position1,percentage=False):
        self.move(position1,percentage=percentage)

    def _get_move_data(self, position, percentage=False):
        if percentage:
            position = to_powerview_position(position)
        return {"shade": {"id": self.shade_id, "positions": {"posKind1": 1, "position1": position}}}

    def process_response(self, response):
        positions = get_positions(response)
        if positions:
            _position_kind = positions.get('posKind1')
            _position = positions.get('position1')

            if _position_kind == 1:
                self.position1 = _position
                self.position1_perc = to_percentage_position(_position)
                lgr.debug("Blind positions: position1: {}".format(self.position1))


class BaseShadeType2(BaseShade):
    """
    A tilt at the bottom type of shade.
    """

    def __init__(self, name, shade_id, shades_api_path):
        BaseShade.__init__(self, name, shade_id, shades_api_path)
        self.position1 = 0  # the movement position
        self.position1_perc = 0
        self.position2 = 0  # the tilt position
        self.position2_perc = 0
        self.tiltopenposition = MAXTILTPOSITION
        self.tiltcloseposition = 0

    def move1(self,position1,percentage=False):
        self.move(position1,None,percentage=percentage)

    def move2(self,position2,percentage=False):
        self.move(None,position2,percentage=percentage)

    def open(self):
        self.move(self.pos1openposition,None)

    def close(self):
        self.move(self.pos1closeposition,None)

    def open2(self):
        self.move(None,self.tiltopenposition)

    def close2(self):
        self.move(None,self.tiltcloseposition)

    def move(self,position1,tilt,percentage=False):
        raise NotImplemented

    def _get_move_data(self, position=None, tilt=None, percentage=False):
        if percentage:
            position = to_powerview_position(position)
            tilt = to_powerview_position(tilt, self.tiltopenposition)
        if position is None:
            return {"shade": {"id": self.shade_id,
                              "positions": {"posKind1": 3, "position1": tilt}}}
        else:
            return {"shade": {"id": self.shade_id,
                              "positions": {"posKind1": 1, "position1": position}}}

    def process_response(self, response):
        positions = get_positions(response)
        if positions:
            _position_kind = positions.get('posKind1')
            _position = positions.get('position1')

            if _position_kind == 1:
                self.position1 = _position
                self.position1_perc = to_percentage_position(_position)
                self.position2 = 0
                self.position2_perc = 0
                lgr.debug("Blind positions: position1: {}  position2: {}".
                          format(self.position1, self.position2))
            elif _position_kind == 3:
                self.position1 = 0
                self.position2 = _position
                self.position2_perc = to_percentage_position(_position, base=MAXTILTPOSITION)
                lgr.debug("Blind positions: position1: {}  position2: {}".
                          format(self.position1, self.position2))


class BaseShadeType3(BaseShade):
    """
    Like a top down bottom up shade
    """

    def __init__(self, name, shade_id, shades_api_path):
        BaseShade.__init__(self, name, shade_id, shades_api_path)
        self.position1 = 0
        self.position1_perc = 0
        self.position2 = 0
        self.position2_perc = 0
        self.pos2openposition = 0  # open meaning middle bar is at the top position.
        self.pos2closeposition = MAXMOVEPOSITION  # close meaning middle bar is at the bottom position.

        # Bottom and middle bar have different coordinate spaces
        # Bottom bar down is position at 0
        # Middle bar down is position MAXMOVEPOSITION
        # If normalize == True both bars are down at position MAXMOVEPOSITION
        self.normalize=False


    def move1(self,position1,percentage=False):
        self.move(position1,None,percentage=percentage)

    def move2(self,position2,percentage=False):
        self.move(None,position2,percentage=percentage)

    def open(self):
        self.move(self.pos1openposition,None)

    def close(self):
        self.move(self.pos1closeposition, None)

    def open2(self):
        self.move(None,self.pos2openposition)

    def close2(self):
        self.move(None,self.pos2closeposition)

    def _get_move_data(self, position1=None, position2=None, percentage=False):
        if percentage:
            position1 = to_powerview_position(position1)
            position2 = to_powerview_position(position2)
        if position1 is None:
            position1 = self.position1
        if position2 is None:
            position2 = self.position2

        return {"shade": {"id": self.shade_id,
                          "positions": {"posKind1": 1, "position1": position1,
                                        "posKind2": 2, "position2": position2}}}

    def process_response(self, response):
        positions = get_positions(response)
        if positions:
            _position_kind = positions.get('posKind1')
            _position = positions.get('position1')

            if _position_kind == 1:
                self.position1 = _position
                self.position1_perc = to_percentage_position(_position)
                lgr.debug("Blind positions: position1: {}".format(self.position1))

            _position_kind2 = positions.get('posKind2')
            _position2 = positions.get('position2')

            if _position_kind2 == 2:
                self.position2 = _position2
                self.position2_perc = to_percentage_position(_position2)
                lgr.debug("Blind positions: position2: {}".format(self.position2))
