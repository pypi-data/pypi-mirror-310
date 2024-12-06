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
from collections import deque
from bstack_utils.constants import *
class bstack1l111lll11_opy_:
    def __init__(self):
        self._1lll11111ll_opy_ = deque()
        self._1lll111lll1_opy_ = {}
        self._1lll111l1l1_opy_ = False
    def bstack1lll1111l11_opy_(self, test_name, bstack1lll11111l1_opy_):
        bstack1lll1111l1l_opy_ = self._1lll111lll1_opy_.get(test_name, {})
        return bstack1lll1111l1l_opy_.get(bstack1lll11111l1_opy_, 0)
    def bstack1lll1111ll1_opy_(self, test_name, bstack1lll11111l1_opy_):
        bstack1lll111l11l_opy_ = self.bstack1lll1111l11_opy_(test_name, bstack1lll11111l1_opy_)
        self.bstack1lll111l1ll_opy_(test_name, bstack1lll11111l1_opy_)
        return bstack1lll111l11l_opy_
    def bstack1lll111l1ll_opy_(self, test_name, bstack1lll11111l1_opy_):
        if test_name not in self._1lll111lll1_opy_:
            self._1lll111lll1_opy_[test_name] = {}
        bstack1lll1111l1l_opy_ = self._1lll111lll1_opy_[test_name]
        bstack1lll111l11l_opy_ = bstack1lll1111l1l_opy_.get(bstack1lll11111l1_opy_, 0)
        bstack1lll1111l1l_opy_[bstack1lll11111l1_opy_] = bstack1lll111l11l_opy_ + 1
    def bstack1l1llll111_opy_(self, bstack1lll111l111_opy_, bstack1lll1111lll_opy_):
        bstack1lll111llll_opy_ = self.bstack1lll1111ll1_opy_(bstack1lll111l111_opy_, bstack1lll1111lll_opy_)
        event_name = bstack111l111lll_opy_[bstack1lll1111lll_opy_]
        bstack1lll111ll11_opy_ = bstack1l1l1l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᘀ").format(bstack1lll111l111_opy_, event_name, bstack1lll111llll_opy_)
        self._1lll11111ll_opy_.append(bstack1lll111ll11_opy_)
    def bstack1l11l1l1_opy_(self):
        return len(self._1lll11111ll_opy_) == 0
    def bstack1l1llll1l_opy_(self):
        bstack1lll111ll1l_opy_ = self._1lll11111ll_opy_.popleft()
        return bstack1lll111ll1l_opy_
    def capturing(self):
        return self._1lll111l1l1_opy_
    def bstack11l11111l_opy_(self):
        self._1lll111l1l1_opy_ = True
    def bstack1ll1ll1l1l_opy_(self):
        self._1lll111l1l1_opy_ = False