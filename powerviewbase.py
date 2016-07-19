class PowerViewBase:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.base_path = "http://{}/api".format(ip_address)
        self.scenes_path = "{}/scenes".format(self.base_path)
        self.shades_path = "{}/shades".format(self.base_path)
        self.rooms_path = "{}/rooms".format(self.base_path)

    def get_user_data(self):
        _str = "{}/userdata/".format(self.base_path)
        return _str

    def get_activate_scene_path(self, scene_id):
        _scene_path = "{}?sceneid={}".format(self.scenes_path, scene_id)
        return _scene_path

    def get_activate_blind_data(self, blind_id, position):
        url = "{}{}/".format(self.shades_path, blind_id)
        dta = {"shade": {"blind_id": blind_id, "positions": {"posKind1": 1, "position1": position}}}
        return (url, dta)