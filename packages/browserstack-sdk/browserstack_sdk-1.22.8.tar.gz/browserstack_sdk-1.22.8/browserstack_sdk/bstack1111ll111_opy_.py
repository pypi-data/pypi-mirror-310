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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1ll11lll1_opy_ as bstack11ll11l11_opy_
from browserstack_sdk.bstack1l111111ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1l1l11_opy_
class bstack1l1l1l1l1_opy_:
    def __init__(self, args, logger, bstack11l1111ll1_opy_, bstack11l1111l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1111ll1_opy_ = bstack11l1111ll1_opy_
        self.bstack11l1111l11_opy_ = bstack11l1111l11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l111lll_opy_ = []
        self.bstack11l111111l_opy_ = None
        self.bstack11lll11lll_opy_ = []
        self.bstack11l11111l1_opy_ = self.bstack1ll1ll1ll1_opy_()
        self.bstack1l1ll11111_opy_ = -1
    def bstack1lllll1ll1_opy_(self, bstack11l11111ll_opy_):
        self.parse_args()
        self.bstack11l111ll1l_opy_()
        self.bstack11l111l111_opy_(bstack11l11111ll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11l1111l1l_opy_():
        import importlib
        if getattr(importlib, bstack1l1l1l_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬཉ"), False):
            bstack11l111lll1_opy_ = importlib.find_loader(bstack1l1l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪཊ"))
        else:
            bstack11l111lll1_opy_ = importlib.util.find_spec(bstack1l1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫཋ"))
    def bstack11l111llll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1ll11111_opy_ = -1
        if self.bstack11l1111l11_opy_ and bstack1l1l1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪཌ") in self.bstack11l1111ll1_opy_:
            self.bstack1l1ll11111_opy_ = int(self.bstack11l1111ll1_opy_[bstack1l1l1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫཌྷ")])
        try:
            bstack11l111ll11_opy_ = [bstack1l1l1l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧཎ"), bstack1l1l1l_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩཏ"), bstack1l1l1l_opy_ (u"ࠧ࠮ࡲࠪཐ")]
            if self.bstack1l1ll11111_opy_ >= 0:
                bstack11l111ll11_opy_.extend([bstack1l1l1l_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩད"), bstack1l1l1l_opy_ (u"ࠩ࠰ࡲࠬདྷ")])
            for arg in bstack11l111ll11_opy_:
                self.bstack11l111llll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11l111ll1l_opy_(self):
        bstack11l111111l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11l111111l_opy_ = bstack11l111111l_opy_
        return bstack11l111111l_opy_
    def bstack11l1ll111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11l1111l1l_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1l1l11_opy_)
    def bstack11l111l111_opy_(self, bstack11l11111ll_opy_):
        bstack1l1111lll1_opy_ = Config.bstack111ll1l11_opy_()
        if bstack11l11111ll_opy_:
            self.bstack11l111111l_opy_.append(bstack1l1l1l_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧན"))
            self.bstack11l111111l_opy_.append(bstack1l1l1l_opy_ (u"࡙ࠫࡸࡵࡦࠩཔ"))
        if bstack1l1111lll1_opy_.bstack11l111l1l1_opy_():
            self.bstack11l111111l_opy_.append(bstack1l1l1l_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫཕ"))
            self.bstack11l111111l_opy_.append(bstack1l1l1l_opy_ (u"࠭ࡔࡳࡷࡨࠫབ"))
        self.bstack11l111111l_opy_.append(bstack1l1l1l_opy_ (u"ࠧ࠮ࡲࠪབྷ"))
        self.bstack11l111111l_opy_.append(bstack1l1l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭མ"))
        self.bstack11l111111l_opy_.append(bstack1l1l1l_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫཙ"))
        self.bstack11l111111l_opy_.append(bstack1l1l1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪཚ"))
        if self.bstack1l1ll11111_opy_ > 1:
            self.bstack11l111111l_opy_.append(bstack1l1l1l_opy_ (u"ࠫ࠲ࡴࠧཛ"))
            self.bstack11l111111l_opy_.append(str(self.bstack1l1ll11111_opy_))
    def bstack11l1111111_opy_(self):
        bstack11lll11lll_opy_ = []
        for spec in self.bstack11l111lll_opy_:
            bstack1l11lll111_opy_ = [spec]
            bstack1l11lll111_opy_ += self.bstack11l111111l_opy_
            bstack11lll11lll_opy_.append(bstack1l11lll111_opy_)
        self.bstack11lll11lll_opy_ = bstack11lll11lll_opy_
        return bstack11lll11lll_opy_
    def bstack1ll1ll1ll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11l11111l1_opy_ = True
            return True
        except Exception as e:
            self.bstack11l11111l1_opy_ = False
        return self.bstack11l11111l1_opy_
    def bstack11lll1ll11_opy_(self, bstack11l1111lll_opy_, bstack1lllll1ll1_opy_):
        bstack1lllll1ll1_opy_[bstack1l1l1l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬཛྷ")] = self.bstack11l1111ll1_opy_
        multiprocessing.set_start_method(bstack1l1l1l_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬཝ"))
        bstack1l11111l1l_opy_ = []
        manager = multiprocessing.Manager()
        bstack11l1l11ll_opy_ = manager.list()
        if bstack1l1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪཞ") in self.bstack11l1111ll1_opy_:
            for index, platform in enumerate(self.bstack11l1111ll1_opy_[bstack1l1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫཟ")]):
                bstack1l11111l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11l1111lll_opy_,
                                                            args=(self.bstack11l111111l_opy_, bstack1lllll1ll1_opy_, bstack11l1l11ll_opy_)))
            bstack11l111l1ll_opy_ = len(self.bstack11l1111ll1_opy_[bstack1l1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬའ")])
        else:
            bstack1l11111l1l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11l1111lll_opy_,
                                                        args=(self.bstack11l111111l_opy_, bstack1lllll1ll1_opy_, bstack11l1l11ll_opy_)))
            bstack11l111l1ll_opy_ = 1
        i = 0
        for t in bstack1l11111l1l_opy_:
            os.environ[bstack1l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪཡ")] = str(i)
            if bstack1l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧར") in self.bstack11l1111ll1_opy_:
                os.environ[bstack1l1l1l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ལ")] = json.dumps(self.bstack11l1111ll1_opy_[bstack1l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩཤ")][i % bstack11l111l1ll_opy_])
            i += 1
            t.start()
        for t in bstack1l11111l1l_opy_:
            t.join()
        return list(bstack11l1l11ll_opy_)
    @staticmethod
    def bstack11lll1ll1l_opy_(driver, bstack11l111l11l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫཥ"), None)
        if item and getattr(item, bstack1l1l1l_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࠪས"), None) and not getattr(item, bstack1l1l1l_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡳࡵࡥࡤࡰࡰࡨࠫཧ"), False):
            logger.info(
                bstack1l1l1l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠤཨ"))
            bstack11l11l1111_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11ll11l11_opy_.bstack1lll11lll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)