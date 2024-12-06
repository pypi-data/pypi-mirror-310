# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack1l11l1l_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1l1l1l_opy_ (bstack11ll111_opy_):
    global bstack11l1ll_opy_
    bstack1ll11l1_opy_ = ord (bstack11ll111_opy_ [-1])
    bstack1lllllll_opy_ = bstack11ll111_opy_ [:-1]
    bstack11lll1_opy_ = bstack1ll11l1_opy_ % len (bstack1lllllll_opy_)
    bstack11l1l_opy_ = bstack1lllllll_opy_ [:bstack11lll1_opy_] + bstack1lllllll_opy_ [bstack11lll1_opy_:]
    if bstack1_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11l1l_opy_ - (bstack1l1lll_opy_ + bstack1ll11l1_opy_) % bstack11l1l1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1l11l1l_opy_ - (bstack1l1lll_opy_ + bstack1ll11l1_opy_) % bstack11l1l1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack111l_opy_)
class bstack1ll11111_opy_:
    def __init__(self, handler):
        self._1ll1l1lllll_opy_ = None
        self.handler = handler
        self._1ll1ll11111_opy_ = self.bstack1ll1l1llll1_opy_()
        self.patch()
    def patch(self):
        self._1ll1l1lllll_opy_ = self._1ll1ll11111_opy_.execute
        self._1ll1ll11111_opy_.execute = self.bstack1ll1l1lll1l_opy_()
    def bstack1ll1l1lll1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1l1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥᙚ"), driver_command, None, this, args)
            response = self._1ll1l1lllll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1l1l_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥᙛ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1ll11111_opy_.execute = self._1ll1l1lllll_opy_
    @staticmethod
    def bstack1ll1l1llll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver