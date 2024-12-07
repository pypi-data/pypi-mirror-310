# coding: UTF-8
import sys
bstack11lll_opy_ = sys.version_info [0] == 2
bstack11ll111_opy_ = 2048
bstack1ll111l_opy_ = 7
def bstack11ll11l_opy_ (bstack1111l1_opy_):
    global bstack11ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack1l1l1_opy_ = bstack1111l1_opy_ [:-1]
    bstack11l11_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1_opy_)
    bstack11l1ll1_opy_ = bstack1l1l1_opy_ [:bstack11l11_opy_] + bstack1l1l1_opy_ [bstack11l11_opy_:]
    if bstack11lll_opy_:
        bstack1111111_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll111_opy_ - (bstackl_opy_ + bstack11l11l1_opy_) % bstack1ll111l_opy_) for bstackl_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack1111111_opy_ = str () .join ([chr (ord (char) - bstack11ll111_opy_ - (bstackl_opy_ + bstack11l11l1_opy_) % bstack1ll111l_opy_) for bstackl_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack1111111_opy_)
class bstack1l1ll1ll1_opy_:
    def __init__(self, handler):
        self._1ll1ll1111l_opy_ = None
        self.handler = handler
        self._1ll1ll11111_opy_ = self.bstack1ll1l1llll1_opy_()
        self.patch()
    def patch(self):
        self._1ll1ll1111l_opy_ = self._1ll1ll11111_opy_.execute
        self._1ll1ll11111_opy_.execute = self.bstack1ll1l1lllll_opy_()
    def bstack1ll1l1lllll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11ll11l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥᙚ"), driver_command, None, this, args)
            response = self._1ll1ll1111l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11ll11l_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥᙛ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1ll11111_opy_.execute = self._1ll1ll1111l_opy_
    @staticmethod
    def bstack1ll1l1llll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver