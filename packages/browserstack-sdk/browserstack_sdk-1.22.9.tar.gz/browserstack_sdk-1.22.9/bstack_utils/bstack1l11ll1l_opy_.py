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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack111llll1l1_opy_ as bstack111lll1l1l_opy_
from bstack_utils.bstack1ll1l1ll1l_opy_ import bstack1ll1l1ll1l_opy_
from bstack_utils.helper import bstack1lll1l1ll_opy_, bstack11l11lll11_opy_, bstack1l1ll111_opy_, bstack111llll1ll_opy_, bstack111ll11111_opy_, bstack11l1ll1l1_opy_, get_host_info, bstack111ll1ll11_opy_, bstack1l1l1111ll_opy_, bstack11l11l11ll_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack11l11l11ll_opy_(class_method=False)
def _111ll111ll_opy_(driver, bstack11l111111l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11ll11l_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪ཮"): caps.get(bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ཯"), None),
        bstack11ll11l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ཰"): bstack11l111111l_opy_.get(bstack11ll11l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨཱ"), None),
        bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩིࠬ"): caps.get(bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩཱིࠬ"), None),
        bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰུࠪ"): caps.get(bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰཱུࠪ"), None)
    }
  except Exception as error:
    logger.debug(bstack11ll11l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧྲྀ") + str(error))
  return response
def on():
    if os.environ.get(bstack11ll11l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩཷ"), None) is None or os.environ[bstack11ll11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪླྀ")] == bstack11ll11l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦཹ"):
        return False
    return True
def bstack111ll1ll1l_opy_(config):
  return config.get(bstack11ll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿེࠧ"), False) or any([p.get(bstack11ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨཻ"), False) == True for p in config.get(bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷོࠬ"), [])])
def bstack1l1l1l1l1l_opy_(config, bstack11l1l1111_opy_):
  try:
    if not bstack1l1ll111_opy_(config):
      return False
    bstack111ll1l1ll_opy_ = config.get(bstack11ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻཽࠪ"), False)
    if int(bstack11l1l1111_opy_) < len(config.get(bstack11ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧཾ"), [])) and config[bstack11ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཿ")][bstack11l1l1111_opy_]:
      bstack111lllll11_opy_ = config[bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴྀࠩ")][bstack11l1l1111_opy_].get(bstack11ll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿཱྀࠧ"), None)
    else:
      bstack111lllll11_opy_ = config.get(bstack11ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨྂ"), None)
    if bstack111lllll11_opy_ != None:
      bstack111ll1l1ll_opy_ = bstack111lllll11_opy_
    bstack111lll11ll_opy_ = os.getenv(bstack11ll11l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧྃ")) is not None and len(os.getenv(bstack11ll11l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ྄"))) > 0 and os.getenv(bstack11ll11l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ྅")) != bstack11ll11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ྆")
    return bstack111ll1l1ll_opy_ and bstack111lll11ll_opy_
  except Exception as error:
    logger.debug(bstack11ll11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭྇") + str(error))
  return False
def bstack1ll1l1l111_opy_(test_tags):
  bstack111ll1111l_opy_ = os.getenv(bstack11ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨྈ"))
  if bstack111ll1111l_opy_ is None:
    return True
  bstack111ll1111l_opy_ = json.loads(bstack111ll1111l_opy_)
  try:
    include_tags = bstack111ll1111l_opy_[bstack11ll11l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ྉ")] if bstack11ll11l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧྊ") in bstack111ll1111l_opy_ and isinstance(bstack111ll1111l_opy_[bstack11ll11l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨྋ")], list) else []
    exclude_tags = bstack111ll1111l_opy_[bstack11ll11l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩྌ")] if bstack11ll11l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪྍ") in bstack111ll1111l_opy_ and isinstance(bstack111ll1111l_opy_[bstack11ll11l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫྎ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11ll11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢྏ") + str(error))
  return False
def bstack111ll1lll1_opy_(config, bstack111ll11lll_opy_, bstack111lll111l_opy_, bstack111ll11ll1_opy_):
  bstack111l1lll1l_opy_ = bstack111llll1ll_opy_(config)
  bstack111llll11l_opy_ = bstack111ll11111_opy_(config)
  if bstack111l1lll1l_opy_ is None or bstack111llll11l_opy_ is None:
    logger.error(bstack11ll11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩྐ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪྑ"), bstack11ll11l_opy_ (u"ࠪࡿࢂ࠭ྒ")))
    data = {
        bstack11ll11l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩྒྷ"): config[bstack11ll11l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪྔ")],
        bstack11ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩྕ"): config.get(bstack11ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪྖ"), os.path.basename(os.getcwd())),
        bstack11ll11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫྗ"): bstack1lll1l1ll_opy_(),
        bstack11ll11l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ྘"): config.get(bstack11ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ྙ"), bstack11ll11l_opy_ (u"ࠫࠬྚ")),
        bstack11ll11l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬྛ"): {
            bstack11ll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ྜ"): bstack111ll11lll_opy_,
            bstack11ll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪྜྷ"): bstack111lll111l_opy_,
            bstack11ll11l_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬྞ"): __version__,
            bstack11ll11l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫྟ"): bstack11ll11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪྠ"),
            bstack11ll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫྡ"): bstack11ll11l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧྡྷ"),
            bstack11ll11l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ྣ"): bstack111ll11ll1_opy_
        },
        bstack11ll11l_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩྤ"): settings,
        bstack11ll11l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩྥ"): bstack111ll1ll11_opy_(),
        bstack11ll11l_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩྦ"): bstack11l1ll1l1_opy_(),
        bstack11ll11l_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬྦྷ"): get_host_info(),
        bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ྨ"): bstack1l1ll111_opy_(config)
    }
    headers = {
        bstack11ll11l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫྩ"): bstack11ll11l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩྪ"),
    }
    config = {
        bstack11ll11l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬྫ"): (bstack111l1lll1l_opy_, bstack111llll11l_opy_),
        bstack11ll11l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩྫྷ"): headers
    }
    response = bstack1l1l1111ll_opy_(bstack11ll11l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧྭ"), bstack111lll1l1l_opy_ + bstack11ll11l_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪྮ"), data, config)
    bstack111lll1lll_opy_ = response.json()
    if bstack111lll1lll_opy_[bstack11ll11l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬྯ")]:
      parsed = json.loads(os.getenv(bstack11ll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ྰ"), bstack11ll11l_opy_ (u"࠭ࡻࡾࠩྱ")))
      parsed[bstack11ll11l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨྲ")] = bstack111lll1lll_opy_[bstack11ll11l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ླ")][bstack11ll11l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪྴ")]
      os.environ[bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫྵ")] = json.dumps(parsed)
      bstack1ll1l1ll1l_opy_.bstack111llll111_opy_(bstack111lll1lll_opy_[bstack11ll11l_opy_ (u"ࠫࡩࡧࡴࡢࠩྶ")][bstack11ll11l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ྷ")])
      bstack1ll1l1ll1l_opy_.bstack111ll1l11l_opy_(bstack111lll1lll_opy_[bstack11ll11l_opy_ (u"࠭ࡤࡢࡶࡤࠫྸ")][bstack11ll11l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩྐྵ")])
      bstack1ll1l1ll1l_opy_.store()
      return bstack111lll1lll_opy_[bstack11ll11l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ྺ")][bstack11ll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧྻ")], bstack111lll1lll_opy_[bstack11ll11l_opy_ (u"ࠪࡨࡦࡺࡡࠨྼ")][bstack11ll11l_opy_ (u"ࠫ࡮ࡪࠧ྽")]
    else:
      logger.error(bstack11ll11l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭྾") + bstack111lll1lll_opy_[bstack11ll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ྿")])
      if bstack111lll1lll_opy_[bstack11ll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿀")] == bstack11ll11l_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪ࿁"):
        for bstack111lll11l1_opy_ in bstack111lll1lll_opy_[bstack11ll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ࿂")]:
          logger.error(bstack111lll11l1_opy_[bstack11ll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿃")])
      return None, None
  except Exception as error:
    logger.error(bstack11ll11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧ࿄") +  str(error))
    return None, None
def bstack111l1lllll_opy_():
  if os.getenv(bstack11ll11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ࿅")) is None:
    return {
        bstack11ll11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࿆࠭"): bstack11ll11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭࿇"),
        bstack11ll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿈"): bstack11ll11l_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨ࿉")
    }
  data = {bstack11ll11l_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫ࿊"): bstack1lll1l1ll_opy_()}
  headers = {
      bstack11ll11l_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ࿋"): bstack11ll11l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭࿌") + os.getenv(bstack11ll11l_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦ࿍")),
      bstack11ll11l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭࿎"): bstack11ll11l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ࿏")
  }
  response = bstack1l1l1111ll_opy_(bstack11ll11l_opy_ (u"ࠩࡓ࡙࡙࠭࿐"), bstack111lll1l1l_opy_ + bstack11ll11l_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬ࿑"), data, { bstack11ll11l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ࿒"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11ll11l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨ࿓") + bstack11l11lll11_opy_().isoformat() + bstack11ll11l_opy_ (u"࡚࠭ࠨ࿔"))
      return {bstack11ll11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ࿕"): bstack11ll11l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ࿖"), bstack11ll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿗"): bstack11ll11l_opy_ (u"ࠪࠫ࿘")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11ll11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢ࿙") + str(error))
    return {
        bstack11ll11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ࿚"): bstack11ll11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ࿛"),
        bstack11ll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿜"): str(error)
    }
def bstack1ll11111l_opy_(caps, options, desired_capabilities={}):
  try:
    bstack111ll1llll_opy_ = caps.get(bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ࿝"), {}).get(bstack11ll11l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭࿞"), caps.get(bstack11ll11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ࿟"), bstack11ll11l_opy_ (u"ࠫࠬ࿠")))
    if bstack111ll1llll_opy_:
      logger.warn(bstack11ll11l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ࿡"))
      return False
    if options:
      bstack111ll1l1l1_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack111ll1l1l1_opy_ = desired_capabilities
    else:
      bstack111ll1l1l1_opy_ = {}
    browser = caps.get(bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ࿢"), bstack11ll11l_opy_ (u"ࠧࠨ࿣")).lower() or bstack111ll1l1l1_opy_.get(bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭࿤"), bstack11ll11l_opy_ (u"ࠩࠪ࿥")).lower()
    if browser != bstack11ll11l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ࿦"):
      logger.warn(bstack11ll11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ࿧"))
      return False
    browser_version = caps.get(bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࿨")) or caps.get(bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ࿩")) or bstack111ll1l1l1_opy_.get(bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࿪")) or bstack111ll1l1l1_opy_.get(bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ࿫"), {}).get(bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ࿬")) or bstack111ll1l1l1_opy_.get(bstack11ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ࿭"), {}).get(bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࿮"))
    if browser_version and browser_version != bstack11ll11l_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬ࿯") and int(browser_version.split(bstack11ll11l_opy_ (u"࠭࠮ࠨ࿰"))[0]) <= 98:
      logger.warn(bstack11ll11l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠻࠲ࠧ࿱"))
      return False
    if not options:
      bstack111lll1ll1_opy_ = caps.get(bstack11ll11l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭࿲")) or bstack111ll1l1l1_opy_.get(bstack11ll11l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ࿳"), {})
      if bstack11ll11l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ࿴") in bstack111lll1ll1_opy_.get(bstack11ll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩ࿵"), []):
        logger.warn(bstack11ll11l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢ࿶"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11ll11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣ࿷") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack111ll11l1l_opy_ = config.get(bstack11ll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ࿸"), {})
    bstack111ll11l1l_opy_[bstack11ll11l_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ࿹")] = os.getenv(bstack11ll11l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ࿺"))
    bstack111lll1111_opy_ = json.loads(os.getenv(bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ࿻"), bstack11ll11l_opy_ (u"ࠫࢀࢃࠧ࿼"))).get(bstack11ll11l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࿽"))
    caps[bstack11ll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭࿾")] = True
    if bstack11ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ࿿") in caps:
      caps[bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩက")][bstack11ll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩခ")] = bstack111ll11l1l_opy_
      caps[bstack11ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫဂ")][bstack11ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫဃ")][bstack11ll11l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭င")] = bstack111lll1111_opy_
    else:
      caps[bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬစ")] = bstack111ll11l1l_opy_
      caps[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ဆ")][bstack11ll11l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩဇ")] = bstack111lll1111_opy_
  except Exception as error:
    logger.debug(bstack11ll11l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥဈ") +  str(error))
def bstack1l1l1l11ll_opy_(driver, bstack111lll1l11_opy_):
  try:
    setattr(driver, bstack11ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪဉ"), True)
    session = driver.session_id
    if session:
      bstack111ll111l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111ll111l1_opy_ = False
      bstack111ll111l1_opy_ = url.scheme in [bstack11ll11l_opy_ (u"ࠦ࡭ࡺࡴࡱࠤည"), bstack11ll11l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦဋ")]
      if bstack111ll111l1_opy_:
        if bstack111lll1l11_opy_:
          logger.info(bstack11ll11l_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨဌ"))
      return bstack111lll1l11_opy_
  except Exception as e:
    logger.error(bstack11ll11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥဍ") + str(e))
    return False
def bstack1l1ll1ll_opy_(driver, name, path):
  try:
    bstack111ll11l11_opy_ = {
        bstack11ll11l_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨဎ"): threading.current_thread().current_test_uuid,
        bstack11ll11l_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧဏ"): os.environ.get(bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨတ"), bstack11ll11l_opy_ (u"ࠫࠬထ")),
        bstack11ll11l_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩဒ"): os.environ.get(bstack11ll11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧဓ"), bstack11ll11l_opy_ (u"ࠧࠨန"))
    }
    logger.debug(bstack11ll11l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫပ"))
    logger.debug(driver.execute_async_script(bstack1ll1l1ll1l_opy_.perform_scan, {bstack11ll11l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤဖ"): name}))
    logger.debug(driver.execute_async_script(bstack1ll1l1ll1l_opy_.bstack111ll1l111_opy_, bstack111ll11l11_opy_))
    logger.info(bstack11ll11l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨဗ"))
  except Exception as bstack111l1llll1_opy_:
    logger.error(bstack11ll11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨဘ") + str(path) + bstack11ll11l_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢမ") + str(bstack111l1llll1_opy_))