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
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111ll1ll11_opy_, bstack11l1ll1l1_opy_, get_host_info, bstack1111111ll1_opy_, \
 bstack1l1ll111_opy_, bstack1l111111l1_opy_, bstack11l11l11ll_opy_, bstack11111ll1ll_opy_, bstack1lll1l1ll_opy_
import bstack_utils.bstack1l11ll1l_opy_ as bstack11llll1111_opy_
from bstack_utils.bstack11llll1lll_opy_ import bstack111lllll1_opy_
from bstack_utils.percy import bstack11llll11ll_opy_
from bstack_utils.config import Config
bstack1l1111l111_opy_ = Config.bstack1lll1ll111_opy_()
logger = logging.getLogger(__name__)
percy = bstack11llll11ll_opy_()
@bstack11l11l11ll_opy_(class_method=False)
def bstack1ll1l111l11_opy_(bs_config, bstack11ll1ll11_opy_):
  try:
    data = {
        bstack11ll11l_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫៀ"): bstack11ll11l_opy_ (u"ࠬࡰࡳࡰࡰࠪេ"),
        bstack11ll11l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬែ"): bs_config.get(bstack11ll11l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬៃ"), bstack11ll11l_opy_ (u"ࠨࠩោ")),
        bstack11ll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧៅ"): bs_config.get(bstack11ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ំ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧះ"): bs_config.get(bstack11ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧៈ")),
        bstack11ll11l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ៉"): bs_config.get(bstack11ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ៊"), bstack11ll11l_opy_ (u"ࠨࠩ់")),
        bstack11ll11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭៌"): bstack1lll1l1ll_opy_(),
        bstack11ll11l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ៍"): bstack1111111ll1_opy_(bs_config),
        bstack11ll11l_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧ៎"): get_host_info(),
        bstack11ll11l_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭៏"): bstack11l1ll1l1_opy_(),
        bstack11ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭័"): os.environ.get(bstack11ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭៑")),
        bstack11ll11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ្࠭"): os.environ.get(bstack11ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧ៓"), False),
        bstack11ll11l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬ។"): bstack111ll1ll11_opy_(),
        bstack11ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ៕"): bstack1ll11l11lll_opy_(),
        bstack11ll11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩ៖"): bstack1ll11l11ll1_opy_(bstack11ll1ll11_opy_),
        bstack11ll11l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫៗ"): bstack1llll1111l_opy_(bs_config, bstack11ll1ll11_opy_.get(bstack11ll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ៘"), bstack11ll11l_opy_ (u"ࠨࠩ៙"))),
        bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ៚"): bstack1l1ll111_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11ll11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ៛").format(str(error)))
    return None
def bstack1ll11l11ll1_opy_(framework):
  return {
    bstack11ll11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫៜ"): framework.get(bstack11ll11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭៝"), bstack11ll11l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭៞")),
    bstack11ll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ៟"): framework.get(bstack11ll11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ០")),
    bstack11ll11l_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭១"): framework.get(bstack11ll11l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ២")),
    bstack11ll11l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭៣"): bstack11ll11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ៤"),
    bstack11ll11l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭៥"): framework.get(bstack11ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ៦"))
  }
def bstack1llll1111l_opy_(bs_config, framework):
  bstack1l1111lll1_opy_ = False
  bstack1lll1ll1l_opy_ = False
  bstack1ll11l1111l_opy_ = False
  if bstack11ll11l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ៧") in bs_config:
    bstack1ll11l1111l_opy_ = True
  elif bstack11ll11l_opy_ (u"ࠩࡤࡴࡵ࠭៨") in bs_config:
    bstack1l1111lll1_opy_ = True
  else:
    bstack1lll1ll1l_opy_ = True
  bstack1l1l11l1l1_opy_ = {
    bstack11ll11l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ៩"): bstack111lllll1_opy_.bstack1ll11l111l1_opy_(bs_config, framework),
    bstack11ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ៪"): bstack11llll1111_opy_.bstack111ll1ll1l_opy_(bs_config),
    bstack11ll11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ៫"): bs_config.get(bstack11ll11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ៬"), False),
    bstack11ll11l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ៭"): bstack1lll1ll1l_opy_,
    bstack11ll11l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ៮"): bstack1l1111lll1_opy_,
    bstack11ll11l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭៯"): bstack1ll11l1111l_opy_
  }
  return bstack1l1l11l1l1_opy_
@bstack11l11l11ll_opy_(class_method=False)
def bstack1ll11l11lll_opy_():
  try:
    bstack1ll11l111ll_opy_ = json.loads(os.getenv(bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ៰"), bstack11ll11l_opy_ (u"ࠫࢀࢃࠧ៱")))
    return {
        bstack11ll11l_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ៲"): bstack1ll11l111ll_opy_
    }
  except Exception as error:
    logger.error(bstack11ll11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ៳").format(str(error)))
    return {}
def bstack1ll11l1l11l_opy_(array, bstack1ll111llll1_opy_, bstack1ll111lll1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll111llll1_opy_]
    result[key] = o[bstack1ll111lll1l_opy_]
  return result
def bstack1ll11l1llll_opy_(bstack11ll1111_opy_=bstack11ll11l_opy_ (u"ࠧࠨ៴")):
  bstack1ll11l11l11_opy_ = bstack11llll1111_opy_.on()
  bstack1ll11l11111_opy_ = bstack111lllll1_opy_.on()
  bstack1ll11l11l1l_opy_ = percy.bstack1ll111l1ll_opy_()
  if bstack1ll11l11l1l_opy_ and not bstack1ll11l11111_opy_ and not bstack1ll11l11l11_opy_:
    return bstack11ll1111_opy_ not in [bstack11ll11l_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ៵"), bstack11ll11l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭៶")]
  elif bstack1ll11l11l11_opy_ and not bstack1ll11l11111_opy_:
    return bstack11ll1111_opy_ not in [bstack11ll11l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ៷"), bstack11ll11l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭៸"), bstack11ll11l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ៹")]
  return bstack1ll11l11l11_opy_ or bstack1ll11l11111_opy_ or bstack1ll11l11l1l_opy_
@bstack11l11l11ll_opy_(class_method=False)
def bstack1ll1l11111l_opy_(bstack11ll1111_opy_, test=None):
  bstack1ll111lllll_opy_ = bstack11llll1111_opy_.on()
  if not bstack1ll111lllll_opy_ or bstack11ll1111_opy_ not in [bstack11ll11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ៺")] or test == None:
    return None
  return {
    bstack11ll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ៻"): bstack1ll111lllll_opy_ and bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ៼"), None) == True and bstack11llll1111_opy_.bstack1ll1l1l111_opy_(test[bstack11ll11l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ៽")])
  }