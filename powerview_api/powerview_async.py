"""
PowerView asyncio api
"""
import asyncio
import logging
import pprint

from powerview_api.helpers.shades_async import ShadeType1, ShadeType2, \
    ShadeType3
from powerview_api.helpers.wrappers_async import async_api
from powerview_api.helpers.powerview_base import PowerViewBase

__author__ = 'sander'
lgr = logging.getLogger(__name__)


@async_api
class PowerViewAsync(PowerViewBase):
    """
    The PowerView class representing one PowerView hub with a
    unique ip address
    """

    def __init__(self, ip_address, session):
        self.session = session
        PowerViewBase.__init__(self, ip_address)

    def define_all_shades(self):
        shades = self.get_shades()
        self.all_shades = []
        for shade in shades["shadeData"]:
            self.all_shades.append(self.shade_factory(shade))

    def shade_factory(self, shadedata):
        _type = shadedata["type"]
        if _type in PowerViewBase.type1_shades:
            return ShadeType1(self._shades_path, shadedata, self.session)
        elif _type in PowerViewBase.type2_shades:
            return ShadeType2(self._shades_path, shadedata, self.session)
        elif _type in PowerViewBase.type3_shades:
            return ShadeType3(self._shades_path, shadedata, self.session)
        else:
            return ShadeType1(self._shades_path, shadedata, self.session)


@asyncio.coroutine
def test(pv):
    # result = yield from pv.get_user_data()
    result = yield from pv.get_scenes()
    pprint.pprint(result)
    yield from pv.activate_scene(61722)


if __name__ == "__main__":
    import aiohttp

    lgr.level = logging.DEBUG
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop)
    # pv = PowerViewAsync("192.168.0.104", session)
    pv = PowerViewAsync("192.168.2.4", session)

    loop.run_until_complete(test(pv))
    session.close()
    # pv.set_blind(52214, 30000)
