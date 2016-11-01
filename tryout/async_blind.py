from tryout.base_blind import BaseTest

from tryout.async_decorator import async_putt


class async_PowerView(BaseTest):
    def __init__(self, ip, putt_wrapper):
        BaseTest.__init__(self, ip, putt_wrapper)


if __name__ == "__main__":
    aspv = async_PowerView("192.168.0.114", async_putt)
    aspv.test()
