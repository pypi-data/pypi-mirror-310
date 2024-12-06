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
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111lll1ll1_opy_, bstack1l1llll11_opy_, get_host_info, bstack11111ll1ll_opy_, \
 bstack1lll1ll11l_opy_, bstack11lll1l111_opy_, bstack11l11l11ll_opy_, bstack1lllll1llll_opy_, bstack1lll1ll1l_opy_
import bstack_utils.bstack1ll11lll1_opy_ as bstack11ll11l11_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1ll111l1_opy_
from bstack_utils.percy import bstack1lll11lll1_opy_
from bstack_utils.config import Config
bstack1l1111lll1_opy_ = Config.bstack111ll1l11_opy_()
logger = logging.getLogger(__name__)
percy = bstack1lll11lll1_opy_()
@bstack11l11l11ll_opy_(class_method=False)
def bstack1ll1l11111l_opy_(bs_config, bstack11llll11l1_opy_):
  try:
    data = {
        bstack1l1l1l_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫៀ"): bstack1l1l1l_opy_ (u"ࠬࡰࡳࡰࡰࠪេ"),
        bstack1l1l1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬែ"): bs_config.get(bstack1l1l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬៃ"), bstack1l1l1l_opy_ (u"ࠨࠩោ")),
        bstack1l1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧៅ"): bs_config.get(bstack1l1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ំ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧះ"): bs_config.get(bstack1l1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧៈ")),
        bstack1l1l1l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ៉"): bs_config.get(bstack1l1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ៊"), bstack1l1l1l_opy_ (u"ࠨࠩ់")),
        bstack1l1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭៌"): bstack1lll1ll1l_opy_(),
        bstack1l1l1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ៍"): bstack11111ll1ll_opy_(bs_config),
        bstack1l1l1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧ៎"): get_host_info(),
        bstack1l1l1l_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭៏"): bstack1l1llll11_opy_(),
        bstack1l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭័"): os.environ.get(bstack1l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭៑")),
        bstack1l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ្࠭"): os.environ.get(bstack1l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧ៓"), False),
        bstack1l1l1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬ។"): bstack111lll1ll1_opy_(),
        bstack1l1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ៕"): bstack1ll111llll1_opy_(),
        bstack1l1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩ៖"): bstack1ll11l11111_opy_(bstack11llll11l1_opy_),
        bstack1l1l1l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫៗ"): bstack1llll11ll_opy_(bs_config, bstack11llll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ៘"), bstack1l1l1l_opy_ (u"ࠨࠩ៙"))),
        bstack1l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ៚"): bstack1lll1ll11l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l1l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ៛").format(str(error)))
    return None
def bstack1ll11l11111_opy_(framework):
  return {
    bstack1l1l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫៜ"): framework.get(bstack1l1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭៝"), bstack1l1l1l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭៞")),
    bstack1l1l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ៟"): framework.get(bstack1l1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ០")),
    bstack1l1l1l_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭១"): framework.get(bstack1l1l1l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ២")),
    bstack1l1l1l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭៣"): bstack1l1l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ៤"),
    bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭៥"): framework.get(bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ៦"))
  }
def bstack1llll11ll_opy_(bs_config, framework):
  bstack1llll1l11_opy_ = False
  bstack11l1l1111_opy_ = False
  bstack1ll111lll11_opy_ = False
  if bstack1l1l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ៧") in bs_config:
    bstack1ll111lll11_opy_ = True
  elif bstack1l1l1l_opy_ (u"ࠩࡤࡴࡵ࠭៨") in bs_config:
    bstack1llll1l11_opy_ = True
  else:
    bstack11l1l1111_opy_ = True
  bstack111llllll_opy_ = {
    bstack1l1l1l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ៩"): bstack1ll111l1_opy_.bstack1ll11l11l11_opy_(bs_config, framework),
    bstack1l1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ៪"): bstack11ll11l11_opy_.bstack111ll11111_opy_(bs_config),
    bstack1l1l1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ៫"): bs_config.get(bstack1l1l1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ៬"), False),
    bstack1l1l1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ៭"): bstack11l1l1111_opy_,
    bstack1l1l1l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ៮"): bstack1llll1l11_opy_,
    bstack1l1l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭៯"): bstack1ll111lll11_opy_
  }
  return bstack111llllll_opy_
@bstack11l11l11ll_opy_(class_method=False)
def bstack1ll111llll1_opy_():
  try:
    bstack1ll11l111ll_opy_ = json.loads(os.getenv(bstack1l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ៰"), bstack1l1l1l_opy_ (u"ࠫࢀࢃࠧ៱")))
    return {
        bstack1l1l1l_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ៲"): bstack1ll11l111ll_opy_
    }
  except Exception as error:
    logger.error(bstack1l1l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ៳").format(str(error)))
    return {}
def bstack1ll11llllll_opy_(array, bstack1ll11l1111l_opy_, bstack1ll11l11ll1_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll11l1111l_opy_]
    result[key] = o[bstack1ll11l11ll1_opy_]
  return result
def bstack1ll11ll1l1l_opy_(bstack11lll111ll_opy_=bstack1l1l1l_opy_ (u"ࠧࠨ៴")):
  bstack1ll11l111l1_opy_ = bstack11ll11l11_opy_.on()
  bstack1ll11l11l1l_opy_ = bstack1ll111l1_opy_.on()
  bstack1ll111lll1l_opy_ = percy.bstack1lll11111_opy_()
  if bstack1ll111lll1l_opy_ and not bstack1ll11l11l1l_opy_ and not bstack1ll11l111l1_opy_:
    return bstack11lll111ll_opy_ not in [bstack1l1l1l_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ៵"), bstack1l1l1l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭៶")]
  elif bstack1ll11l111l1_opy_ and not bstack1ll11l11l1l_opy_:
    return bstack11lll111ll_opy_ not in [bstack1l1l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ៷"), bstack1l1l1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭៸"), bstack1l1l1l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ៹")]
  return bstack1ll11l111l1_opy_ or bstack1ll11l11l1l_opy_ or bstack1ll111lll1l_opy_
@bstack11l11l11ll_opy_(class_method=False)
def bstack1ll11lllll1_opy_(bstack11lll111ll_opy_, test=None):
  bstack1ll111lllll_opy_ = bstack11ll11l11_opy_.on()
  if not bstack1ll111lllll_opy_ or bstack11lll111ll_opy_ not in [bstack1l1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ៺")] or test == None:
    return None
  return {
    bstack1l1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ៻"): bstack1ll111lllll_opy_ and bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ៼"), None) == True and bstack11ll11l11_opy_.bstack1l11lll1ll_opy_(test[bstack1l1l1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ៽")])
  }