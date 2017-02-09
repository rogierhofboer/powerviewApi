""" sync / threaded version of shade classes"""
from powerview_api.helpers.wrappers_async import async_api
from powerview_api.helpers.shades_base import BaseShadeType1, BaseShadeType2, \
    BaseShadeType3


@async_api
class ShadeType1(BaseShadeType1):
    def __init__(self, shades_api_path, shade_data, session):
        self.session = session
        BaseShadeType1.__init__(self, shades_api_path, shade_data)


@async_api
class ShadeType2(BaseShadeType2):
    def __init__(self, shades_api_path, shade_data, session):
        self.session = session
        BaseShadeType2.__init__(self, shades_api_path, shade_data)


@async_api
class ShadeType3(BaseShadeType3):
    def __init__(self, shades_api_path, shade_data, session):
        self.session = session
        BaseShadeType3.__init__(self, shades_api_path, shade_data)
