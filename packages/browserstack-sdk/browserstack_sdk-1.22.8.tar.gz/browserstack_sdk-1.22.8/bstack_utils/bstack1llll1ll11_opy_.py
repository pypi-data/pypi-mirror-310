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
import threading
import logging
import bstack_utils.bstack1ll11lll1_opy_ as bstack11ll11l11_opy_
from bstack_utils.helper import bstack11lll1l111_opy_
logger = logging.getLogger(__name__)
def bstack1ll1111l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1ll11111l_opy_(context, *args):
    tags = getattr(args[0], bstack1l1l1l_opy_ (u"࠭ࡴࡢࡩࡶࠫု"), [])
    bstack11llll1111_opy_ = bstack11ll11l11_opy_.bstack1l11lll1ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack11llll1111_opy_
    try:
      bstack11ll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1111l_opy_(bstack1l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ူ")) else context.browser
      if bstack11ll1111_opy_ and bstack11ll1111_opy_.session_id and bstack11llll1111_opy_ and bstack11lll1l111_opy_(
              threading.current_thread(), bstack1l1l1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧေ"), None):
          threading.current_thread().isA11yTest = bstack11ll11l11_opy_.bstack1l111lll1_opy_(bstack11ll1111_opy_, bstack11llll1111_opy_)
    except Exception as e:
       logger.debug(bstack1l1l1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡦ࠷࠱ࡺࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩဲ").format(str(e)))
def bstack11llll1l_opy_(bstack11ll1111_opy_):
    if bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧဳ"), None) and bstack11lll1l111_opy_(
      threading.current_thread(), bstack1l1l1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪဴ"), None) and not bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࠨဵ"), False):
      threading.current_thread().a11y_stop = True
      bstack11ll11l11_opy_.bstack1lll11lll_opy_(bstack11ll1111_opy_, name=bstack1l1l1l_opy_ (u"ࠨࠢံ"), path=bstack1l1l1l_opy_ (u"့ࠢࠣ"))