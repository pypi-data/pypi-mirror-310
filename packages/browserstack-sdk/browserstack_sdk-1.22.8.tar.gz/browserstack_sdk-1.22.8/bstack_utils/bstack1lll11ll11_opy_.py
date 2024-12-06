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
import logging
import os
import threading
from bstack_utils.helper import bstack1ll1l1lll_opy_
from bstack_utils.constants import bstack111l111l1l_opy_
logger = logging.getLogger(__name__)
class bstack1ll111l1_opy_:
    bstack1ll1ll11l11_opy_ = None
    @classmethod
    def bstack11ll111l_opy_(cls):
        if cls.on():
            logger.info(
                bstack1l1l1l_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭៾").format(os.environ[bstack1l1l1l_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠥ៿")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1l1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭᠀"), None) is None or os.environ[bstack1l1l1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧ᠁")] == bstack1l1l1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ᠂"):
            return False
        return True
    @classmethod
    def bstack1ll11l11l11_opy_(cls, bs_config, framework=bstack1l1l1l_opy_ (u"ࠣࠤ᠃")):
        if framework == bstack1l1l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ᠄"):
            return bstack1ll1l1lll_opy_(bs_config.get(bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᠅")))
        bstack1ll111ll1ll_opy_ = framework in bstack111l111l1l_opy_
        return bstack1ll1l1lll_opy_(bs_config.get(bstack1l1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᠆"), bstack1ll111ll1ll_opy_))
    @classmethod
    def bstack1ll111l1ll1_opy_(cls, framework):
        return framework in bstack111l111l1l_opy_
    @classmethod
    def bstack1ll11llll11_opy_(cls, bs_config, framework):
        return cls.bstack1ll11l11l11_opy_(bs_config, framework) is True and cls.bstack1ll111l1ll1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ᠇"), None)
    @staticmethod
    def bstack11ll1l1lll_opy_():
        if getattr(threading.current_thread(), bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ᠈"), None):
            return {
                bstack1l1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ᠉"): bstack1l1l1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭᠊"),
                bstack1l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᠋"): getattr(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ᠌"), None)
            }
        if getattr(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ᠍"), None):
            return {
                bstack1l1l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ᠎"): bstack1l1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ᠏"),
                bstack1l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᠐"): getattr(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ᠑"), None)
            }
        return None
    @staticmethod
    def bstack1ll111l1lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll111l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l1ll1l11_opy_(test, hook_name=None):
        bstack1ll111ll111_opy_ = test.parent
        if hook_name in [bstack1l1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ᠒"), bstack1l1l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ᠓"), bstack1l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ᠔"), bstack1l1l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ᠕")]:
            bstack1ll111ll111_opy_ = test
        scope = []
        while bstack1ll111ll111_opy_ is not None:
            scope.append(bstack1ll111ll111_opy_.name)
            bstack1ll111ll111_opy_ = bstack1ll111ll111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll111ll1l1_opy_(hook_type):
        if hook_type == bstack1l1l1l_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦ᠖"):
            return bstack1l1l1l_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦ᠗")
        elif hook_type == bstack1l1l1l_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧ᠘"):
            return bstack1l1l1l_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤ᠙")
    @staticmethod
    def bstack1ll111ll11l_opy_(bstack11l111lll_opy_):
        try:
            if not bstack1ll111l1_opy_.on():
                return bstack11l111lll_opy_
            if os.environ.get(bstack1l1l1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣ᠚"), None) == bstack1l1l1l_opy_ (u"ࠦࡹࡸࡵࡦࠤ᠛"):
                tests = os.environ.get(bstack1l1l1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤ᠜"), None)
                if tests is None or tests == bstack1l1l1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ᠝"):
                    return bstack11l111lll_opy_
                bstack11l111lll_opy_ = tests.split(bstack1l1l1l_opy_ (u"ࠧ࠭ࠩ᠞"))
                return bstack11l111lll_opy_
        except Exception as exc:
            print(bstack1l1l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤ᠟"), str(exc))
        return bstack11l111lll_opy_