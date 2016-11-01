from powerview_api.powerviewbase import PowerViewBase


class BaseTest(PowerViewBase):
    def __init__(self, ip,putt_wrapper):
        PowerViewBase.__init__(self, ip)
        self.wrap(putt_wrapper)

    def wrap(self,putt_wrapper):
        self.test=putt_wrapper(self.test)

    def test(self,inp):
        print(inp)