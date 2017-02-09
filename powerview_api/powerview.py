"""
Powerview api
"""
from powerview_api.helpers.powerview_base import PowerViewBase
from powerview_api.helpers.shades import ShadeType1, ShadeType2, ShadeType3
from powerview_api.helpers.wrappers import sync_api

__author__ = 'sander'


@sync_api
class PowerView(PowerViewBase):
    """
    The PowerView class representing one PowerView hub with a
    unique ip address
    """

    def __init__(self, ip_address):
        PowerViewBase.__init__(self, ip_address)

    def define_all_shades(self):
        shades = self.get_shades()
        self.all_shades = []
        for shade in shades["shadeData"]:
            self.all_shades.append(self.shade_factory(shade))

    def shade_factory(self, shadedata):
        _type = shadedata["type"]
        if _type in PowerViewBase.type1_shades:
            return ShadeType1(self._shades_path, shadedata)
        elif _type in PowerViewBase.type2_shades:
            return ShadeType2(self._shades_path, shadedata)
        elif _type in PowerViewBase.type3_shades:
            return ShadeType3(self._shades_path, shadedata)
        else:
            return ShadeType1(self._shades_path, shadedata)


if __name__ == "__main__":
    import pprint

    #pv = PowerView("192.168.0.106")
    pv = PowerView("192.168.2.4")
    userdata = pv.get_scenes()
    pv.activate_scene(61722)
    pprint.pprint(userdata)
