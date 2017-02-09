import math
import logging

from powerview_api.helpers import add_api_path, get_method, put_method


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
    if percentage is None:
        return None
    _multiplier = base / 100.0

    value = math.ceil(percentage * _multiplier)
    return value


def get_positions(response: dict) -> dict:
    try:
        positions = response.get('shade').get('positions')
        return positions
    except AttributeError:
        lgr.debug("No position feedback from blind ")
        return {}


def normalize(self, position):
    pass


class BaseShade:
    def __init__(self, shades_api_path, shade_data):
        self.name = shade_data['name']
        self.shade_id = shade_data['id']
        self.shade_type = shade_data['type']
        self.shade_api_path = "{}/{}".format(shades_api_path, self.shade_id)
        self.pos1openposition = MAXMOVEPOSITION
        self.pos1closeposition = 0
        self.position1 = 0
        self.position1_perc = 0
        self.base = max(self.pos1openposition, self.pos1closeposition)
        self.shade_data = shade_data

    def jog(self):
        raise NotImplemented

    def __repr__(self):
        return self.shade_data

    @put_method
    @add_api_path
    def move1(self, position1, percentage=False):
        return self._get_move_data(position1, percentage)

    @put_method
    @add_api_path
    def open(self):
        return self._get_move_data(self.pos1openposition)

    @put_method
    @add_api_path
    def close(self):
        return self._get_move_data(self.pos1closeposition)

    def move2(self, position2, percentage=False):
        raise NotImplemented

    @get_method
    def update(self):
        return self.shade_api_path, {"refresh": True}

    @staticmethod
    def get_update_data():
        return {"refresh": True}

    def _get_move_data(self, position, percentage=False):
        raise NotImplemented


class BaseShadeType1(BaseShade):
    """
    A basic "up" down "shade"
    """

    def __init__(self, shades_api_path, shade_data):
        BaseShade.__init__(self, shades_api_path, shade_data)

    def _get_move_data(self, position, percentage=False):
        if percentage:
            position = to_powerview_position(position)
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
                lgr.debug(
                    "Blind positions: position1: {}".format(self.position1))


class BaseShadeType2(BaseShade):
    """
    A tilt at the bottom type of shade.
    """

    def __init__(self, shades_api_path, shade_data):
        BaseShade.__init__(self, shades_api_path, shade_data)
        self.position2 = 0  # the tilt position
        self.position2_perc = 0
        self.tiltopenposition = MAXTILTPOSITION
        self.tiltcloseposition = 0

    @put_method
    @add_api_path
    def move2(self, position2, percentage=False):
        return self._get_move_data(position2)

    @put_method
    @add_api_path
    def open2(self):
        return self._get_move_data(tilt=self.tiltopenposition)

    @put_method
    @add_api_path
    def close2(self):
        return self._get_move_data(tilt=self.tiltcloseposition)

    def _get_move_data(self, position=None, tilt=None, percentage=False):
        if percentage:
            position = to_powerview_position(position)
            tilt = to_powerview_position(tilt, self.tiltopenposition)
        if position is None:
            return {"shade": {"id": self.shade_id,
                              "positions": {"posKind1": 3, "position1": tilt}}}
        else:
            return {"shade": {"id": self.shade_id,
                              "positions": {"posKind1": 1,
                                            "position1": position}}}

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
                self.position2_perc = to_percentage_position(
                    _position, base=MAXTILTPOSITION)
                lgr.debug("Blind positions: position1: {}  position2: {}".
                          format(self.position1, self.position2))


class BaseShadeType3(BaseShade):
    """
    Like a top down bottom up shade
    """

    def __init__(self, shades_api_path, shade_data):
        BaseShade.__init__(self, shades_api_path, shade_data)
        self.position2 = 0
        self.position2_perc = 0
        # open meaning middle bar is at the top position.
        self.pos2openposition = 0
        # close meaning middle bar is at the bottom position.
        self.pos2closeposition = MAXMOVEPOSITION

        # Bottom and middle bar have different coordinate spaces
        # Bottom bar down is position at 0
        # Middle bar down is position MAXMOVEPOSITION
        # If normalize == True both bars are down at position MAXMOVEPOSITION
        self.normalize = False

    @put_method
    @add_api_path
    def move2(self, position2, percentage=False):
        return self._get_move_data(None, position2, percentage=percentage)

    @put_method
    @add_api_path
    def open2(self):
        return self._get_move_data(None, self.pos2openposition)

    @put_method
    @add_api_path
    def close2(self):
        return self._get_move_data(None, self.pos2closeposition)

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
                                        "posKind2": 2,
                                        "position2": position2}}}

    def process_response(self, response):
        positions = get_positions(response)
        if positions:
            _position_kind = positions.get('posKind1')
            _position = positions.get('position1')

            if _position_kind == 1:
                self.position1 = _position
                self.position1_perc = to_percentage_position(_position)
                lgr.debug(
                    "Blind positions: position1: {}".format(self.position1))

            _position_kind2 = positions.get('posKind2')
            _position2 = positions.get('position2')

            if _position_kind2 == 2:
                self.position2 = _position2
                self.position2_perc = to_percentage_position(_position2)
                lgr.debug(
                    "Blind positions: position2: {}".format(self.position2))
