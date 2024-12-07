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
import builtins
import logging
class bstack11ll1l1l11_opy_:
    def __init__(self, handler):
        self._111l1l1l1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111l1l11ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11ll11l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭း"), bstack11ll11l_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨ္"), bstack11ll11l_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪ်ࠫ"), bstack11ll11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪျ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111l1l1l11_opy_
        self._111l1l1ll1_opy_()
    def _111l1l1l11_opy_(self, *args, **kwargs):
        self._111l1l1l1l_opy_(*args, **kwargs)
        message = bstack11ll11l_opy_ (u"ࠬࠦࠧြ").join(map(str, args)) + bstack11ll11l_opy_ (u"࠭࡜࡯ࠩွ")
        self._log_message(bstack11ll11l_opy_ (u"ࠧࡊࡐࡉࡓࠬှ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11ll11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧဿ"): level, bstack11ll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ၀"): msg})
    def _111l1l1ll1_opy_(self):
        for level, bstack111l1l11l1_opy_ in self._111l1l11ll_opy_.items():
            setattr(logging, level, self._111l1l111l_opy_(level, bstack111l1l11l1_opy_))
    def _111l1l111l_opy_(self, level, bstack111l1l11l1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111l1l11l1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111l1l1l1l_opy_
        for level, bstack111l1l11l1_opy_ in self._111l1l11ll_opy_.items():
            setattr(logging, level, bstack111l1l11l1_opy_)