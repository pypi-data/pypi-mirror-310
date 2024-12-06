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
from browserstack_sdk.bstack1111ll111_opy_ import bstack1l1l1l1l1_opy_
from browserstack_sdk.bstack11l11llll1_opy_ import RobotHandler
def bstack11llll1l11_opy_(framework):
    if framework.lower() == bstack1l1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬጢ"):
        return bstack1l1l1l1l1_opy_.version()
    elif framework.lower() == bstack1l1l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬጣ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1l1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧጤ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1l1l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩጥ")