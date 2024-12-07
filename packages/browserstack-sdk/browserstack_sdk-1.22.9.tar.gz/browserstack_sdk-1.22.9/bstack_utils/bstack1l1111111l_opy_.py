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
from collections import deque
from bstack_utils.constants import *
class bstack1l11ll111l_opy_:
    def __init__(self):
        self._1lll111lll1_opy_ = deque()
        self._1lll111ll11_opy_ = {}
        self._1lll1111lll_opy_ = False
    def bstack1lll1111ll1_opy_(self, test_name, bstack1lll111l1l1_opy_):
        bstack1lll111llll_opy_ = self._1lll111ll11_opy_.get(test_name, {})
        return bstack1lll111llll_opy_.get(bstack1lll111l1l1_opy_, 0)
    def bstack1lll111ll1l_opy_(self, test_name, bstack1lll111l1l1_opy_):
        bstack1lll111l1ll_opy_ = self.bstack1lll1111ll1_opy_(test_name, bstack1lll111l1l1_opy_)
        self.bstack1lll111l11l_opy_(test_name, bstack1lll111l1l1_opy_)
        return bstack1lll111l1ll_opy_
    def bstack1lll111l11l_opy_(self, test_name, bstack1lll111l1l1_opy_):
        if test_name not in self._1lll111ll11_opy_:
            self._1lll111ll11_opy_[test_name] = {}
        bstack1lll111llll_opy_ = self._1lll111ll11_opy_[test_name]
        bstack1lll111l1ll_opy_ = bstack1lll111llll_opy_.get(bstack1lll111l1l1_opy_, 0)
        bstack1lll111llll_opy_[bstack1lll111l1l1_opy_] = bstack1lll111l1ll_opy_ + 1
    def bstack1l1lllllll_opy_(self, bstack1lll1111l11_opy_, bstack1lll1111l1l_opy_):
        bstack1lll11111ll_opy_ = self.bstack1lll111ll1l_opy_(bstack1lll1111l11_opy_, bstack1lll1111l1l_opy_)
        event_name = bstack111l11ll11_opy_[bstack1lll1111l1l_opy_]
        bstack1lll111l111_opy_ = bstack11ll11l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᘀ").format(bstack1lll1111l11_opy_, event_name, bstack1lll11111ll_opy_)
        self._1lll111lll1_opy_.append(bstack1lll111l111_opy_)
    def bstack11111l111_opy_(self):
        return len(self._1lll111lll1_opy_) == 0
    def bstack11lll1l1l_opy_(self):
        bstack1lll11l1111_opy_ = self._1lll111lll1_opy_.popleft()
        return bstack1lll11l1111_opy_
    def capturing(self):
        return self._1lll1111lll_opy_
    def bstack1ll1l1lll1_opy_(self):
        self._1lll1111lll_opy_ = True
    def bstack1lll1l1lll_opy_(self):
        self._1lll1111lll_opy_ = False