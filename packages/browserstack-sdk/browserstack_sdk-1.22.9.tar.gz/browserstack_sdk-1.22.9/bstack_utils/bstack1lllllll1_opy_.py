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
from browserstack_sdk.bstack1l1l1llll_opy_ import bstack1l1llll1l1_opy_
from browserstack_sdk.bstack11l1lllll1_opy_ import RobotHandler
def bstack1l1llll1ll_opy_(framework):
    if framework.lower() == bstack11ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬጢ"):
        return bstack1l1llll1l1_opy_.version()
    elif framework.lower() == bstack11ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬጣ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11ll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧጤ"):
        import behave
        return behave.__version__
    else:
        return bstack11ll11l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩጥ")