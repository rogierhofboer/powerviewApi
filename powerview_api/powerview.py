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
    # _shade = next(
    # (shade for shade in shades["shadeData"] if shade["id"] == 32653))
    # shade = pv.shade_factory(_shade)
    # #shade.close()
    # shade.move(None,shade.tiltcloseposition)

    # shade = pv.shade_factory(shades["shadeData"][0])
    # shade.jog()
    # shade.move(shade.pos1openposition,shade.pos2openposition)
    # shade.open()
    # shade.move2(1000)
    # shade.move(1000,10000)
    # pv.set_blind('7271',0,3)
    # pprint.pprint(pv.get_shade_data('11155', force_refresh=True)['shade'])
