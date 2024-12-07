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
import threading
import logging
import bstack_utils.bstack1l11ll1l_opy_ as bstack11llll1111_opy_
from bstack_utils.helper import bstack1l111111l1_opy_
logger = logging.getLogger(__name__)
def bstack1ll111ll1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1l111l1lll_opy_(context, *args):
    tags = getattr(args[0], bstack11ll11l_opy_ (u"࠭ࡴࡢࡩࡶࠫု"), [])
    bstack1ll1l11l11_opy_ = bstack11llll1111_opy_.bstack1ll1l1l111_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll1l11l11_opy_
    try:
      bstack11l1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll111ll1_opy_(bstack11ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ူ")) else context.browser
      if bstack11l1lll1_opy_ and bstack11l1lll1_opy_.session_id and bstack1ll1l11l11_opy_ and bstack1l111111l1_opy_(
              threading.current_thread(), bstack11ll11l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧေ"), None):
          threading.current_thread().isA11yTest = bstack11llll1111_opy_.bstack1l1l1l11ll_opy_(bstack11l1lll1_opy_, bstack1ll1l11l11_opy_)
    except Exception as e:
       logger.debug(bstack11ll11l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡦ࠷࠱ࡺࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩဲ").format(str(e)))
def bstack11l1ll11_opy_(bstack11l1lll1_opy_):
    if bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧဳ"), None) and bstack1l111111l1_opy_(
      threading.current_thread(), bstack11ll11l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪဴ"), None) and not bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࠨဵ"), False):
      threading.current_thread().a11y_stop = True
      bstack11llll1111_opy_.bstack1l1ll1ll_opy_(bstack11l1lll1_opy_, name=bstack11ll11l_opy_ (u"ࠨࠢံ"), path=bstack11ll11l_opy_ (u"့ࠢࠣ"))