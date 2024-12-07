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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1lll111l_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l1111111l_opy_ import bstack1l11ll111l_opy_
import time
import requests
def bstack1ll1ll1111_opy_():
  global CONFIG
  headers = {
        bstack11ll11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11ll11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack111lll11l_opy_(CONFIG, bstack1lllll1lll_opy_)
  try:
    response = requests.get(bstack1lllll1lll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11l1l111l_opy_ = response.json()[bstack11ll11l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1ll1ll1l_opy_.format(response.json()))
      return bstack11l1l111l_opy_
    else:
      logger.debug(bstack11l111l1_opy_.format(bstack11ll11l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11l111l1_opy_.format(e))
def bstack11llll11l1_opy_(hub_url):
  global CONFIG
  url = bstack11ll11l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11ll11l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11ll11l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11ll11l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack111lll11l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1lll1l1111_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l11ll11l_opy_.format(hub_url, e))
def bstack1l1111ll1_opy_():
  try:
    global bstack1l11ll1l1l_opy_
    bstack11l1l111l_opy_ = bstack1ll1ll1111_opy_()
    bstack1lll111ll_opy_ = []
    results = []
    for bstack11l111ll1_opy_ in bstack11l1l111l_opy_:
      bstack1lll111ll_opy_.append(bstack1ll1l1l1l_opy_(target=bstack11llll11l1_opy_,args=(bstack11l111ll1_opy_,)))
    for t in bstack1lll111ll_opy_:
      t.start()
    for t in bstack1lll111ll_opy_:
      results.append(t.join())
    bstack11l111lll_opy_ = {}
    for item in results:
      hub_url = item[bstack11ll11l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11ll11l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11l111lll_opy_[hub_url] = latency
    bstack11ll11ll_opy_ = min(bstack11l111lll_opy_, key= lambda x: bstack11l111lll_opy_[x])
    bstack1l11ll1l1l_opy_ = bstack11ll11ll_opy_
    logger.debug(bstack1l1ll1lll1_opy_.format(bstack11ll11ll_opy_))
  except Exception as e:
    logger.debug(bstack11l1l11l1_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack111l1lll_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack111l1l11_opy_, bstack1l1l1111ll_opy_, bstack111l1111_opy_, bstack1l111111l1_opy_, bstack1l1ll111_opy_, \
  Notset, bstack1l1l1lll1l_opy_, \
  bstack1111lll1l_opy_, bstack1l11l1lll_opy_, bstack111l1l1ll_opy_, bstack11l1ll1l1_opy_, bstack1lll1l1l_opy_, bstack1l1lll111_opy_, \
  bstack1l111111_opy_, \
  bstack11l111111_opy_, bstack1ll1ll11ll_opy_, bstack11ll1lll1_opy_, bstack11lll1ll_opy_, \
  bstack1ll111ll_opy_, bstack11l111l1l_opy_, bstack111111ll1_opy_, bstack1l1l1111l1_opy_
from bstack_utils.bstack1lllllll1_opy_ import bstack1l1llll1ll_opy_
from bstack_utils.bstack1ll1l1l1ll_opy_ import bstack1l1ll1ll1_opy_
from bstack_utils.bstack11111ll1l_opy_ import bstack1llll1l1l_opy_, bstack1ll11l1l_opy_
from bstack_utils.bstack1111111l_opy_ import bstack1ll11l11l1_opy_
from bstack_utils.bstack11llll1lll_opy_ import bstack111lllll1_opy_
from bstack_utils.bstack1ll1l1ll1l_opy_ import bstack1ll1l1ll1l_opy_
from bstack_utils.proxy import bstack1ll1l11lll_opy_, bstack111lll11l_opy_, bstack11l11l1ll_opy_, bstack1ll1l1lll_opy_
import bstack_utils.bstack1l11ll1l_opy_ as bstack11llll1111_opy_
from browserstack_sdk.bstack1l1l1llll_opy_ import *
from browserstack_sdk.bstack1ll1llll1l_opy_ import *
from bstack_utils.bstack11llll11l_opy_ import bstack1l1llllll_opy_
from browserstack_sdk.bstack1l11l1l1l1_opy_ import *
import requests
from bstack_utils.constants import *
def bstack1ll1lllll1_opy_():
    global bstack1l11ll1l1l_opy_
    try:
        bstack1lll111l11_opy_ = bstack111111l1l_opy_()
        bstack1l1l11ll1_opy_(bstack1lll111l11_opy_)
        hub_url = bstack1lll111l11_opy_.get(bstack11ll11l_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack11ll11l_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack11ll11l_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack11ll11l_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack11ll11l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11ll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1l11ll1l1l_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack111111l1l_opy_():
    global CONFIG
    bstack1ll11111l1_opy_ = CONFIG.get(bstack11ll11l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack11ll11l_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack11ll11l_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1ll11111l1_opy_, str):
        raise ValueError(bstack11ll11l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1lll111l11_opy_ = bstack11l11111_opy_(bstack1ll11111l1_opy_)
        return bstack1lll111l11_opy_
    except Exception as e:
        logger.error(bstack11ll11l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack11l11111_opy_(bstack1ll11111l1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11ll11l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack11ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack11ll11l_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack11llllll1_opy_ + bstack1ll11111l1_opy_
        auth = (CONFIG[bstack11ll11l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack11ll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1l1ll1llll_opy_ = json.loads(response.text)
            return bstack1l1ll1llll_opy_
    except ValueError as ve:
        logger.error(bstack11ll11l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11ll11l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l1l11ll1_opy_(bstack11ll1l1l1_opy_):
    global CONFIG
    if bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack11ll11l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack11ll11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack11ll11l_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack11ll1l1l1_opy_:
        bstack1lll111l1l_opy_ = CONFIG.get(bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack11ll11l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1lll111l1l_opy_)
        bstack1llll111l1_opy_ = bstack11ll1l1l1_opy_.get(bstack11ll11l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack111llllll_opy_ = bstack11ll11l_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1llll111l1_opy_)
        logger.debug(bstack11ll11l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack111llllll_opy_)
        bstack1lllll11l1_opy_ = {
            bstack11ll11l_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack11ll11l_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack11ll11l_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack11ll11l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack11ll11l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack111llllll_opy_
        }
        bstack1lll111l1l_opy_.update(bstack1lllll11l1_opy_)
        logger.debug(bstack11ll11l_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1lll111l1l_opy_)
        CONFIG[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1lll111l1l_opy_
        logger.debug(bstack11ll11l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1ll1l1111_opy_():
    bstack1lll111l11_opy_ = bstack111111l1l_opy_()
    if not bstack1lll111l11_opy_[bstack11ll11l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack11ll11l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1lll111l11_opy_[bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack11ll11l_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
def bstack11lll1111l_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11ll11l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack11ll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1ll111l1_opy_
        logger.debug(bstack11ll11l_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11ll11l_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack11ll11l_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1l1l1l1l_opy_ = json.loads(response.text)
                bstack11l11l1l1_opy_ = bstack1l1l1l1l_opy_.get(bstack11ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack11l11l1l1_opy_:
                    bstack1lll11lll1_opy_ = bstack11l11l1l1_opy_[0]
                    bstack1llll11l11_opy_ = bstack1lll11lll1_opy_.get(bstack11ll11l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack1lllll1111_opy_ = bstack111ll1l1l_opy_ + bstack1llll11l11_opy_
                    result.extend([bstack1llll11l11_opy_, bstack1lllll1111_opy_])
                    logger.info(bstack1ll111111l_opy_.format(bstack1lllll1111_opy_))
                    bstack1l1ll1l1l1_opy_ = CONFIG[bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack11ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1l1ll1l1l1_opy_ += bstack11ll11l_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack11ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1l1ll1l1l1_opy_ != bstack1lll11lll1_opy_.get(bstack11ll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack11ll111l1_opy_.format(bstack1lll11lll1_opy_.get(bstack11ll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1l1ll1l1l1_opy_))
                    return result
                else:
                    logger.debug(bstack11ll11l_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack11ll11l_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack11ll11l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack11ll11l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
import bstack_utils.bstack1l11ll1lll_opy_ as bstack1lll1l111_opy_
import bstack_utils.bstack11l1ll111_opy_ as bstack1ll11l1l1l_opy_
bstack1l1llll111_opy_ = bstack11ll11l_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࢹ")
bstack1l11ll11l1_opy_ = bstack11ll11l_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧࢺ")
from ._version import __version__
bstack11lll1lll_opy_ = None
CONFIG = {}
bstack1ll1l11111_opy_ = {}
bstack1lll1111l1_opy_ = {}
bstack1111l11ll_opy_ = None
bstack1lll11llll_opy_ = None
bstack11ll1ll1l_opy_ = None
bstack111l11l1l_opy_ = -1
bstack1lllll1l11_opy_ = 0
bstack1ll1lll11l_opy_ = bstack1l1l111l1_opy_
bstack111ll111_opy_ = 1
bstack1l1l1lllll_opy_ = False
bstack1l111ll11_opy_ = False
bstack111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠩࠪࢻ")
bstack1lll1l11l1_opy_ = bstack11ll11l_opy_ (u"ࠪࠫࢼ")
bstack1l1l11l1l_opy_ = False
bstack1l1l111l_opy_ = True
bstack1ll1l11l_opy_ = bstack11ll11l_opy_ (u"ࠫࠬࢽ")
bstack1ll1llll1_opy_ = []
bstack1l11ll1l1l_opy_ = bstack11ll11l_opy_ (u"ࠬ࠭ࢾ")
bstack11l11l11l_opy_ = False
bstack1l11l1l1_opy_ = None
bstack11lll1111_opy_ = None
bstack1ll11ll1ll_opy_ = None
bstack1l1l11lll_opy_ = -1
bstack111l11l11_opy_ = os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"࠭ࡾࠨࢿ")), bstack11ll11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣀ"), bstack11ll11l_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣁ"))
bstack111l1ll1l_opy_ = 0
bstack111l11111_opy_ = 0
bstack1lll11l11_opy_ = []
bstack1ll1l1l1l1_opy_ = []
bstack1ll11111ll_opy_ = []
bstack1l1l1l11_opy_ = []
bstack1ll111ll11_opy_ = bstack11ll11l_opy_ (u"ࠩࠪࣂ")
bstack1l111l11l_opy_ = bstack11ll11l_opy_ (u"ࠪࠫࣃ")
bstack11llllll11_opy_ = False
bstack1lll1ll1l1_opy_ = False
bstack1lll1ll1ll_opy_ = {}
bstack11ll1l11l_opy_ = None
bstack11l1111l_opy_ = None
bstack1lll1111ll_opy_ = None
bstack1l1111l1ll_opy_ = None
bstack1l1l1ll11_opy_ = None
bstack1l111lll1l_opy_ = None
bstack1ll1l1ll1_opy_ = None
bstack1111llll_opy_ = None
bstack11111lll_opy_ = None
bstack11l1l111_opy_ = None
bstack1l1111l11l_opy_ = None
bstack1ll1ll1l1_opy_ = None
bstack1l111l1ll_opy_ = None
bstack1111l11l1_opy_ = None
bstack1l111l11_opy_ = None
bstack11llll1l11_opy_ = None
bstack1l111l11ll_opy_ = None
bstack1l111l1l11_opy_ = None
bstack1lllll1ll1_opy_ = None
bstack1l1llll11_opy_ = None
bstack1llllll11_opy_ = None
bstack111ll11l_opy_ = None
bstack1lll1lll1_opy_ = False
bstack1l11l1ll11_opy_ = bstack11ll11l_opy_ (u"ࠦࠧࣄ")
logger = bstack111l1lll_opy_.get_logger(__name__, bstack1ll1lll11l_opy_)
bstack1l1111l111_opy_ = Config.bstack1lll1ll111_opy_()
percy = bstack11llll11ll_opy_()
bstack1lll11lll_opy_ = bstack1l11ll111l_opy_()
bstack1llllllll_opy_ = bstack1l11l1l1l1_opy_()
def bstack1l111ll1_opy_():
  global CONFIG
  global bstack11llllll11_opy_
  global bstack1l1111l111_opy_
  bstack1l1lllll11_opy_ = bstack1111l11l_opy_(CONFIG)
  if bstack1l1ll111_opy_(CONFIG):
    if (bstack11ll11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࣅ") in bstack1l1lllll11_opy_ and str(bstack1l1lllll11_opy_[bstack11ll11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࣆ")]).lower() == bstack11ll11l_opy_ (u"ࠧࡵࡴࡸࡩࠬࣇ")):
      bstack11llllll11_opy_ = True
    bstack1l1111l111_opy_.bstack1l111111ll_opy_(bstack1l1lllll11_opy_.get(bstack11ll11l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬࣈ"), False))
  else:
    bstack11llllll11_opy_ = True
    bstack1l1111l111_opy_.bstack1l111111ll_opy_(True)
def bstack1l1111llll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll111l1l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1llll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11ll11l_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨࣉ") == args[i].lower() or bstack11ll11l_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪࠦ࣊") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll1l11l_opy_
      bstack1ll1l11l_opy_ += bstack11ll11l_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠡࠩ࣋") + path
      return path
  return None
bstack1l1ll11l1l_opy_ = re.compile(bstack11ll11l_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿ࠣ࣌"))
def bstack11lllllll1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l1ll11l1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11ll11l_opy_ (u"ࠨࠤࡼࠤ࣍") + group + bstack11ll11l_opy_ (u"ࠢࡾࠤ࣎"), os.environ.get(group))
  return value
def bstack11ll11ll1_opy_():
  bstack11ll1ll1_opy_ = bstack1ll1llll_opy_()
  if bstack11ll1ll1_opy_ and os.path.exists(os.path.abspath(bstack11ll1ll1_opy_)):
    fileName = bstack11ll1ll1_opy_
  if bstack11ll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉ࣏ࠬ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࣐࠭")])) and not bstack11ll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩ࣑ࠬ") in locals():
    fileName = os.environ[bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")]
  if bstack11ll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫࣓ࠧ") in locals():
    bstack1lllllll_opy_ = os.path.abspath(fileName)
  else:
    bstack1lllllll_opy_ = bstack11ll11l_opy_ (u"࠭ࠧࣔ")
  bstack11lll1l1ll_opy_ = os.getcwd()
  bstack1l11l1l111_opy_ = bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣕ")
  bstack1lllll1l1_opy_ = bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣖ")
  while (not os.path.exists(bstack1lllllll_opy_)) and bstack11lll1l1ll_opy_ != bstack11ll11l_opy_ (u"ࠤࠥࣗ"):
    bstack1lllllll_opy_ = os.path.join(bstack11lll1l1ll_opy_, bstack1l11l1l111_opy_)
    if not os.path.exists(bstack1lllllll_opy_):
      bstack1lllllll_opy_ = os.path.join(bstack11lll1l1ll_opy_, bstack1lllll1l1_opy_)
    if bstack11lll1l1ll_opy_ != os.path.dirname(bstack11lll1l1ll_opy_):
      bstack11lll1l1ll_opy_ = os.path.dirname(bstack11lll1l1ll_opy_)
    else:
      bstack11lll1l1ll_opy_ = bstack11ll11l_opy_ (u"ࠥࠦࣘ")
  if not os.path.exists(bstack1lllllll_opy_):
    bstack1l1l1ll1l1_opy_(
      bstack111l1l1l1_opy_.format(os.getcwd()))
  try:
    with open(bstack1lllllll_opy_, bstack11ll11l_opy_ (u"ࠫࡷ࠭ࣙ")) as stream:
      yaml.add_implicit_resolver(bstack11ll11l_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣚ"), bstack1l1ll11l1l_opy_)
      yaml.add_constructor(bstack11ll11l_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࠢࣛ"), bstack11lllllll1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1lllllll_opy_, bstack11ll11l_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1l1l1ll1l1_opy_(bstack1ll1l1ll11_opy_.format(str(exc)))
def bstack1ll1l1111l_opy_(config):
  bstack111lll1l_opy_ = bstack1l11lll1l_opy_(config)
  for option in list(bstack111lll1l_opy_):
    if option.lower() in bstack11llll1ll_opy_ and option != bstack11llll1ll_opy_[option.lower()]:
      bstack111lll1l_opy_[bstack11llll1ll_opy_[option.lower()]] = bstack111lll1l_opy_[option]
      del bstack111lll1l_opy_[option]
  return config
def bstack1111lll11_opy_():
  global bstack1lll1111l1_opy_
  for key, bstack1l11ll1ll1_opy_ in bstack11l1llll_opy_.items():
    if isinstance(bstack1l11ll1ll1_opy_, list):
      for var in bstack1l11ll1ll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lll1111l1_opy_[key] = os.environ[var]
          break
    elif bstack1l11ll1ll1_opy_ in os.environ and os.environ[bstack1l11ll1ll1_opy_] and str(os.environ[bstack1l11ll1ll1_opy_]).strip():
      bstack1lll1111l1_opy_[key] = os.environ[bstack1l11ll1ll1_opy_]
  if bstack11ll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣝ") in os.environ:
    bstack1lll1111l1_opy_[bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣞ")] = {}
    bstack1lll1111l1_opy_[bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣟ")][bstack11ll11l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")] = os.environ[bstack11ll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ࣡")]
def bstack1l1l1l1l11_opy_():
  global bstack1ll1l11111_opy_
  global bstack1ll1l11l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11ll11l_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣢").lower() == val.lower():
      bstack1ll1l11111_opy_[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣣࠫ")] = {}
      bstack1ll1l11111_opy_[bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣤ")][bstack11ll11l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣥ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11llll1l1_opy_ in bstack1l1lll1l1l_opy_.items():
    if isinstance(bstack11llll1l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11llll1l1_opy_:
          if idx < len(sys.argv) and bstack11ll11l_opy_ (u"ࠪ࠱࠲ࣦ࠭") + var.lower() == val.lower() and not key in bstack1ll1l11111_opy_:
            bstack1ll1l11111_opy_[key] = sys.argv[idx + 1]
            bstack1ll1l11l_opy_ += bstack11ll11l_opy_ (u"ࠫࠥ࠳࠭ࠨࣧ") + var + bstack11ll11l_opy_ (u"ࠬࠦࠧࣨ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11ll11l_opy_ (u"࠭࠭࠮ࣩࠩ") + bstack11llll1l1_opy_.lower() == val.lower() and not key in bstack1ll1l11111_opy_:
          bstack1ll1l11111_opy_[key] = sys.argv[idx + 1]
          bstack1ll1l11l_opy_ += bstack11ll11l_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + bstack11llll1l1_opy_ + bstack11ll11l_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l111lll1_opy_(config):
  bstack1l1ll11lll_opy_ = config.keys()
  for bstack1l1111ll_opy_, bstack1llllllll1_opy_ in bstack11111llll_opy_.items():
    if bstack1llllllll1_opy_ in bstack1l1ll11lll_opy_:
      config[bstack1l1111ll_opy_] = config[bstack1llllllll1_opy_]
      del config[bstack1llllllll1_opy_]
  for bstack1l1111ll_opy_, bstack1llllllll1_opy_ in bstack11l1l1l1l_opy_.items():
    if isinstance(bstack1llllllll1_opy_, list):
      for bstack1l1111lll_opy_ in bstack1llllllll1_opy_:
        if bstack1l1111lll_opy_ in bstack1l1ll11lll_opy_:
          config[bstack1l1111ll_opy_] = config[bstack1l1111lll_opy_]
          del config[bstack1l1111lll_opy_]
          break
    elif bstack1llllllll1_opy_ in bstack1l1ll11lll_opy_:
      config[bstack1l1111ll_opy_] = config[bstack1llllllll1_opy_]
      del config[bstack1llllllll1_opy_]
  for bstack1l1111lll_opy_ in list(config):
    for bstack1lll1l111l_opy_ in bstack1lll11ll_opy_:
      if bstack1l1111lll_opy_.lower() == bstack1lll1l111l_opy_.lower() and bstack1l1111lll_opy_ != bstack1lll1l111l_opy_:
        config[bstack1lll1l111l_opy_] = config[bstack1l1111lll_opy_]
        del config[bstack1l1111lll_opy_]
  bstack1l11l11lll_opy_ = [{}]
  if not config.get(bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ࣬")):
    config[bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࣭࠭")] = [{}]
  bstack1l11l11lll_opy_ = config[bstack11ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ࣮ࠧ")]
  for platform in bstack1l11l11lll_opy_:
    for bstack1l1111lll_opy_ in list(platform):
      for bstack1lll1l111l_opy_ in bstack1lll11ll_opy_:
        if bstack1l1111lll_opy_.lower() == bstack1lll1l111l_opy_.lower() and bstack1l1111lll_opy_ != bstack1lll1l111l_opy_:
          platform[bstack1lll1l111l_opy_] = platform[bstack1l1111lll_opy_]
          del platform[bstack1l1111lll_opy_]
  for bstack1l1111ll_opy_, bstack1llllllll1_opy_ in bstack11l1l1l1l_opy_.items():
    for platform in bstack1l11l11lll_opy_:
      if isinstance(bstack1llllllll1_opy_, list):
        for bstack1l1111lll_opy_ in bstack1llllllll1_opy_:
          if bstack1l1111lll_opy_ in platform:
            platform[bstack1l1111ll_opy_] = platform[bstack1l1111lll_opy_]
            del platform[bstack1l1111lll_opy_]
            break
      elif bstack1llllllll1_opy_ in platform:
        platform[bstack1l1111ll_opy_] = platform[bstack1llllllll1_opy_]
        del platform[bstack1llllllll1_opy_]
  for bstack1l1lll1l11_opy_ in bstack1l1lll1l1_opy_:
    if bstack1l1lll1l11_opy_ in config:
      if not bstack1l1lll1l1_opy_[bstack1l1lll1l11_opy_] in config:
        config[bstack1l1lll1l1_opy_[bstack1l1lll1l11_opy_]] = {}
      config[bstack1l1lll1l1_opy_[bstack1l1lll1l11_opy_]].update(config[bstack1l1lll1l11_opy_])
      del config[bstack1l1lll1l11_opy_]
  for platform in bstack1l11l11lll_opy_:
    for bstack1l1lll1l11_opy_ in bstack1l1lll1l1_opy_:
      if bstack1l1lll1l11_opy_ in list(platform):
        if not bstack1l1lll1l1_opy_[bstack1l1lll1l11_opy_] in platform:
          platform[bstack1l1lll1l1_opy_[bstack1l1lll1l11_opy_]] = {}
        platform[bstack1l1lll1l1_opy_[bstack1l1lll1l11_opy_]].update(platform[bstack1l1lll1l11_opy_])
        del platform[bstack1l1lll1l11_opy_]
  config = bstack1ll1l1111l_opy_(config)
  return config
def bstack1ll1ll11l_opy_(config):
  global bstack1lll1l11l1_opy_
  bstack1ll11ll11l_opy_ = False
  if bstack11ll11l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦ࣯ࠩ") in config and str(config[bstack11ll11l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࣰࠪ")]).lower() != bstack11ll11l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪࣱ࠭"):
    if bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࣲࠬ") not in config or str(config[bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ࣳ")]).lower() == bstack11ll11l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
      config[bstack11ll11l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪࣵ")] = False
    else:
      bstack1lll111l11_opy_ = bstack111111l1l_opy_()
      if bstack11ll11l_opy_ (u"ࠬ࡯ࡳࡕࡴ࡬ࡥࡱࡍࡲࡪࡦࣶࠪ") in bstack1lll111l11_opy_:
        if not bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࣷ") in config:
          config[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣸ")] = {}
        config[bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣹࠬ")][bstack11ll11l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࣺࠫ")] = bstack11ll11l_opy_ (u"ࠪࡥࡹࡹ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩࣻ")
        bstack1ll11ll11l_opy_ = True
        bstack1lll1l11l1_opy_ = config[bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")].get(bstack11ll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ"))
  if bstack1l1ll111_opy_(config) and bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࣾ") in config and str(config[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ")]).lower() != bstack11ll11l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ") and not bstack1ll11ll11l_opy_:
    if not bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ँ") in config:
      config[bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧं")] = {}
    if not config[bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨः")].get(bstack11ll11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠩऄ")) and not bstack11ll11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨअ") in config[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")]:
      bstack1lll1l1ll_opy_ = datetime.datetime.now()
      bstack1lll1ll11_opy_ = bstack1lll1l1ll_opy_.strftime(bstack11ll11l_opy_ (u"ࠨࠧࡧࡣࠪࡨ࡟ࠦࡊࠨࡑࠬइ"))
      hostname = socket.gethostname()
      bstack1llll1llll_opy_ = bstack11ll11l_opy_ (u"ࠩࠪई").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11ll11l_opy_ (u"ࠪࡿࢂࡥࡻࡾࡡࡾࢁࠬउ").format(bstack1lll1ll11_opy_, hostname, bstack1llll1llll_opy_)
      config[bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऊ")][bstack11ll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऋ")] = identifier
    bstack1lll1l11l1_opy_ = config[bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")].get(bstack11ll11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऍ"))
  return config
def bstack1lll1l11ll_opy_():
  bstack11l1lllll_opy_ =  bstack11l1ll1l1_opy_()[bstack11ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠧऎ")]
  return bstack11l1lllll_opy_ if bstack11l1lllll_opy_ else -1
def bstack1lll1l1l11_opy_(bstack11l1lllll_opy_):
  global CONFIG
  if not bstack11ll11l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫए") in CONFIG[bstack11ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ")]:
    return
  CONFIG[bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ")] = CONFIG[bstack11ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ")].replace(
    bstack11ll11l_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨओ"),
    str(bstack11l1lllll_opy_)
  )
def bstack11llllll1l_opy_():
  global CONFIG
  if not bstack11ll11l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭औ") in CONFIG[bstack11ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")]:
    return
  bstack1lll1l1ll_opy_ = datetime.datetime.now()
  bstack1lll1ll11_opy_ = bstack1lll1l1ll_opy_.strftime(bstack11ll11l_opy_ (u"ࠩࠨࡨ࠲ࠫࡢ࠮ࠧࡋ࠾ࠪࡓࠧख"))
  CONFIG[bstack11ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬग")] = CONFIG[bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")].replace(
    bstack11ll11l_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫङ"),
    bstack1lll1ll11_opy_
  )
def bstack1ll11l111l_opy_():
  global CONFIG
  if bstack11ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच") in CONFIG and not bool(CONFIG[bstack11ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")]):
    del CONFIG[bstack11ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज")]
    return
  if not bstack11ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG:
    CONFIG[bstack11ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = bstack11ll11l_opy_ (u"ࠫࠨࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧट")
  if bstack11ll11l_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫठ") in CONFIG[bstack11ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")]:
    bstack11llllll1l_opy_()
    os.environ[bstack11ll11l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫढ")] = CONFIG[bstack11ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪण")]
  if not bstack11ll11l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫत") in CONFIG[bstack11ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]:
    return
  bstack11l1lllll_opy_ = bstack11ll11l_opy_ (u"ࠫࠬद")
  bstack1ll1l111l1_opy_ = bstack1lll1l11ll_opy_()
  if bstack1ll1l111l1_opy_ != -1:
    bstack11l1lllll_opy_ = bstack11ll11l_opy_ (u"ࠬࡉࡉࠡࠩध") + str(bstack1ll1l111l1_opy_)
  if bstack11l1lllll_opy_ == bstack11ll11l_opy_ (u"࠭ࠧन"):
    bstack1llll1l1_opy_ = bstack11l1ll11l_opy_(CONFIG[bstack11ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪऩ")])
    if bstack1llll1l1_opy_ != -1:
      bstack11l1lllll_opy_ = str(bstack1llll1l1_opy_)
  if bstack11l1lllll_opy_:
    bstack1lll1l1l11_opy_(bstack11l1lllll_opy_)
    os.environ[bstack11ll11l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬप")] = CONFIG[bstack11ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]
def bstack1l11l11ll_opy_(bstack1ll11ll11_opy_, bstack1l11l1111l_opy_, path):
  bstack11l11l1l_opy_ = {
    bstack11ll11l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧब"): bstack1l11l1111l_opy_
  }
  if os.path.exists(path):
    bstack111ll1l1_opy_ = json.load(open(path, bstack11ll11l_opy_ (u"ࠫࡷࡨࠧभ")))
  else:
    bstack111ll1l1_opy_ = {}
  bstack111ll1l1_opy_[bstack1ll11ll11_opy_] = bstack11l11l1l_opy_
  with open(path, bstack11ll11l_opy_ (u"ࠧࡽࠫࠣम")) as outfile:
    json.dump(bstack111ll1l1_opy_, outfile)
def bstack11l1ll11l_opy_(bstack1ll11ll11_opy_):
  bstack1ll11ll11_opy_ = str(bstack1ll11ll11_opy_)
  bstack111l1111l_opy_ = os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"࠭ࡾࠨय")), bstack11ll11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧर"))
  try:
    if not os.path.exists(bstack111l1111l_opy_):
      os.makedirs(bstack111l1111l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"ࠨࢀࠪऱ")), bstack11ll11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩल"), bstack11ll11l_opy_ (u"ࠪ࠲ࡧࡻࡩ࡭ࡦ࠰ࡲࡦࡳࡥ࠮ࡥࡤࡧ࡭࡫࠮࡫ࡵࡲࡲࠬळ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11ll11l_opy_ (u"ࠫࡼ࠭ऴ")):
        pass
      with open(file_path, bstack11ll11l_opy_ (u"ࠧࡽࠫࠣव")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11ll11l_opy_ (u"࠭ࡲࠨश")) as bstack1l1l1lll1_opy_:
      bstack111llll1_opy_ = json.load(bstack1l1l1lll1_opy_)
    if bstack1ll11ll11_opy_ in bstack111llll1_opy_:
      bstack1llll1l1l1_opy_ = bstack111llll1_opy_[bstack1ll11ll11_opy_][bstack11ll11l_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫष")]
      bstack111ll1ll1_opy_ = int(bstack1llll1l1l1_opy_) + 1
      bstack1l11l11ll_opy_(bstack1ll11ll11_opy_, bstack111ll1ll1_opy_, file_path)
      return bstack111ll1ll1_opy_
    else:
      bstack1l11l11ll_opy_(bstack1ll11ll11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1llll1l111_opy_.format(str(e)))
    return -1
def bstack1ll1lll1l1_opy_(config):
  if not config[bstack11ll11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪस")] or not config[bstack11ll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬह")]:
    return True
  else:
    return False
def bstack11l1l1l1_opy_(config, index=0):
  global bstack1l1l11l1l_opy_
  bstack1111l1l11_opy_ = {}
  caps = bstack11111ll1_opy_ + bstack111l1ll1_opy_
  if config.get(bstack11ll11l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧऺ"), False):
    bstack1111l1l11_opy_[bstack11ll11l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨऻ")] = True
    bstack1111l1l11_opy_[bstack11ll11l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")] = config.get(bstack11ll11l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪऽ"), {})
  if bstack1l1l11l1l_opy_:
    caps += bstack11l11llll_opy_
  for key in config:
    if key in caps + [bstack11ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪा")]:
      continue
    bstack1111l1l11_opy_[key] = config[key]
  if bstack11ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫि") in config:
    for bstack11lll11111_opy_ in config[bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬी")][index]:
      if bstack11lll11111_opy_ in caps:
        continue
      bstack1111l1l11_opy_[bstack11lll11111_opy_] = config[bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")][index][bstack11lll11111_opy_]
  bstack1111l1l11_opy_[bstack11ll11l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ू")] = socket.gethostname()
  if bstack11ll11l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ृ") in bstack1111l1l11_opy_:
    del (bstack1111l1l11_opy_[bstack11ll11l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧॄ")])
  return bstack1111l1l11_opy_
def bstack1lll11l1l1_opy_(config):
  global bstack1l1l11l1l_opy_
  bstack1l1llll1l_opy_ = {}
  caps = bstack111l1ll1_opy_
  if bstack1l1l11l1l_opy_:
    caps += bstack11l11llll_opy_
  for key in caps:
    if key in config:
      bstack1l1llll1l_opy_[key] = config[key]
  return bstack1l1llll1l_opy_
def bstack11lll1l11l_opy_(bstack1111l1l11_opy_, bstack1l1llll1l_opy_):
  bstack11l11111l_opy_ = {}
  for key in bstack1111l1l11_opy_.keys():
    if key in bstack11111llll_opy_:
      bstack11l11111l_opy_[bstack11111llll_opy_[key]] = bstack1111l1l11_opy_[key]
    else:
      bstack11l11111l_opy_[key] = bstack1111l1l11_opy_[key]
  for key in bstack1l1llll1l_opy_:
    if key in bstack11111llll_opy_:
      bstack11l11111l_opy_[bstack11111llll_opy_[key]] = bstack1l1llll1l_opy_[key]
    else:
      bstack11l11111l_opy_[key] = bstack1l1llll1l_opy_[key]
  return bstack11l11111l_opy_
def bstack1lll1l11l_opy_(config, index=0):
  global bstack1l1l11l1l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l11111ll1_opy_ = bstack111l1l11_opy_(bstack1l1ll1l1l_opy_, config, logger)
  bstack1l1llll1l_opy_ = bstack1lll11l1l1_opy_(config)
  bstack1l111ll1ll_opy_ = bstack111l1ll1_opy_
  bstack1l111ll1ll_opy_ += bstack1ll11lll1_opy_
  bstack1l1llll1l_opy_ = update(bstack1l1llll1l_opy_, bstack1l11111ll1_opy_)
  if bstack1l1l11l1l_opy_:
    bstack1l111ll1ll_opy_ += bstack11l11llll_opy_
  if bstack11ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॅ") in config:
    if bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ॆ") in config[bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬे")][index]:
      caps[bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨै")] = config[bstack11ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ")][index][bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ")]
    if bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧो") in config[bstack11ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index]:
      caps[bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯्ࠩ")] = str(config[bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॏ")])
    bstack1ll1111111_opy_ = bstack111l1l11_opy_(bstack1l1ll1l1l_opy_, config[bstack11ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index], logger)
    bstack1l111ll1ll_opy_ += list(bstack1ll1111111_opy_.keys())
    for bstack1lll1ll11l_opy_ in bstack1l111ll1ll_opy_:
      if bstack1lll1ll11l_opy_ in config[bstack11ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index]:
        if bstack1lll1ll11l_opy_ == bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ॒"):
          try:
            bstack1ll1111111_opy_[bstack1lll1ll11l_opy_] = str(config[bstack11ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index][bstack1lll1ll11l_opy_] * 1.0)
          except:
            bstack1ll1111111_opy_[bstack1lll1ll11l_opy_] = str(config[bstack11ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index][bstack1lll1ll11l_opy_])
        else:
          bstack1ll1111111_opy_[bstack1lll1ll11l_opy_] = config[bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ")][index][bstack1lll1ll11l_opy_]
        del (config[bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1lll1ll11l_opy_])
    bstack1l1llll1l_opy_ = update(bstack1l1llll1l_opy_, bstack1ll1111111_opy_)
  bstack1111l1l11_opy_ = bstack11l1l1l1_opy_(config, index)
  for bstack1l1111lll_opy_ in bstack111l1ll1_opy_ + list(bstack1l11111ll1_opy_.keys()):
    if bstack1l1111lll_opy_ in bstack1111l1l11_opy_:
      bstack1l1llll1l_opy_[bstack1l1111lll_opy_] = bstack1111l1l11_opy_[bstack1l1111lll_opy_]
      del (bstack1111l1l11_opy_[bstack1l1111lll_opy_])
  if bstack1l1l1lll1l_opy_(config):
    bstack1111l1l11_opy_[bstack11ll11l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫॗ")] = True
    caps.update(bstack1l1llll1l_opy_)
    caps[bstack11ll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭क़")] = bstack1111l1l11_opy_
  else:
    bstack1111l1l11_opy_[bstack11ll11l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ख़")] = False
    caps.update(bstack11lll1l11l_opy_(bstack1111l1l11_opy_, bstack1l1llll1l_opy_))
    if bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬग़") in caps:
      caps[bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩज़")] = caps[bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")]
      del (caps[bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")])
    if bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬफ़") in caps:
      caps[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧय़")] = caps[bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧॠ")]
      del (caps[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ")])
  return caps
def bstack1ll1ll111l_opy_():
  global bstack1l11ll1l1l_opy_
  global CONFIG
  if bstack1ll111l1l1_opy_() <= version.parse(bstack11ll11l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨॢ")):
    if bstack1l11ll1l1l_opy_ != bstack11ll11l_opy_ (u"ࠩࠪॣ"):
      return bstack11ll11l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ।") + bstack1l11ll1l1l_opy_ + bstack11ll11l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ॥")
    return bstack11lll1l111_opy_
  if bstack1l11ll1l1l_opy_ != bstack11ll11l_opy_ (u"ࠬ࠭०"):
    return bstack11ll11l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ१") + bstack1l11ll1l1l_opy_ + bstack11ll11l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ२")
  return bstack1llll1l1ll_opy_
def bstack1l1l1llll1_opy_(options):
  return hasattr(options, bstack11ll11l_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ३"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1lll11l1_opy_(options, bstack1ll11llll1_opy_):
  for bstack1l11llll_opy_ in bstack1ll11llll1_opy_:
    if bstack1l11llll_opy_ in [bstack11ll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ४"), bstack11ll11l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ५")]:
      continue
    if bstack1l11llll_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11llll_opy_] = update(options._experimental_options[bstack1l11llll_opy_],
                                                         bstack1ll11llll1_opy_[bstack1l11llll_opy_])
    else:
      options.add_experimental_option(bstack1l11llll_opy_, bstack1ll11llll1_opy_[bstack1l11llll_opy_])
  if bstack11ll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩ६") in bstack1ll11llll1_opy_:
    for arg in bstack1ll11llll1_opy_[bstack11ll11l_opy_ (u"ࠬࡧࡲࡨࡵࠪ७")]:
      options.add_argument(arg)
    del (bstack1ll11llll1_opy_[bstack11ll11l_opy_ (u"࠭ࡡࡳࡩࡶࠫ८")])
  if bstack11ll11l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ९") in bstack1ll11llll1_opy_:
    for ext in bstack1ll11llll1_opy_[bstack11ll11l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ॰")]:
      options.add_extension(ext)
    del (bstack1ll11llll1_opy_[bstack11ll11l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॱ")])
def bstack1l1lllll_opy_(options, bstack1l1ll1l11_opy_):
  if bstack11ll11l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩॲ") in bstack1l1ll1l11_opy_:
    for bstack1ll1l11ll_opy_ in bstack1l1ll1l11_opy_[bstack11ll11l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪॳ")]:
      if bstack1ll1l11ll_opy_ in options._preferences:
        options._preferences[bstack1ll1l11ll_opy_] = update(options._preferences[bstack1ll1l11ll_opy_], bstack1l1ll1l11_opy_[bstack11ll11l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫॴ")][bstack1ll1l11ll_opy_])
      else:
        options.set_preference(bstack1ll1l11ll_opy_, bstack1l1ll1l11_opy_[bstack11ll11l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ")][bstack1ll1l11ll_opy_])
  if bstack11ll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬॶ") in bstack1l1ll1l11_opy_:
    for arg in bstack1l1ll1l11_opy_[bstack11ll11l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ")]:
      options.add_argument(arg)
def bstack11lll111l_opy_(options, bstack1l1ll1111_opy_):
  if bstack11ll11l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪॸ") in bstack1l1ll1111_opy_:
    options.use_webview(bool(bstack1l1ll1111_opy_[bstack11ll11l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫॹ")]))
  bstack1lll11l1_opy_(options, bstack1l1ll1111_opy_)
def bstack1l1l1lll_opy_(options, bstack1l1ll111ll_opy_):
  for bstack1l1111ll1l_opy_ in bstack1l1ll111ll_opy_:
    if bstack1l1111ll1l_opy_ in [bstack11ll11l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨॺ"), bstack11ll11l_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")]:
      continue
    options.set_capability(bstack1l1111ll1l_opy_, bstack1l1ll111ll_opy_[bstack1l1111ll1l_opy_])
  if bstack11ll11l_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ") in bstack1l1ll111ll_opy_:
    for arg in bstack1l1ll111ll_opy_[bstack11ll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬॽ")]:
      options.add_argument(arg)
  if bstack11ll11l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬॾ") in bstack1l1ll111ll_opy_:
    options.bstack1lll111ll1_opy_(bool(bstack1l1ll111ll_opy_[bstack11ll11l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ॿ")]))
def bstack11ll1l1l_opy_(options, bstack1l1ll1lll_opy_):
  for bstack1l111ll1l1_opy_ in bstack1l1ll1lll_opy_:
    if bstack1l111ll1l1_opy_ in [bstack11ll11l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧঀ"), bstack11ll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ")]:
      continue
    options._options[bstack1l111ll1l1_opy_] = bstack1l1ll1lll_opy_[bstack1l111ll1l1_opy_]
  if bstack11ll11l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩং") in bstack1l1ll1lll_opy_:
    for bstack1lll11l11l_opy_ in bstack1l1ll1lll_opy_[bstack11ll11l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ")]:
      options.bstack1111ll11_opy_(
        bstack1lll11l11l_opy_, bstack1l1ll1lll_opy_[bstack11ll11l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ঄")][bstack1lll11l11l_opy_])
  if bstack11ll11l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ") in bstack1l1ll1lll_opy_:
    for arg in bstack1l1ll1lll_opy_[bstack11ll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ")]:
      options.add_argument(arg)
def bstack11111111l_opy_(options, caps):
  if not hasattr(options, bstack11ll11l_opy_ (u"ࠪࡏࡊ࡟ࠧই")):
    return
  if options.KEY == bstack11ll11l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঈ") and options.KEY in caps:
    bstack1lll11l1_opy_(options, caps[bstack11ll11l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪউ")])
  elif options.KEY == bstack11ll11l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫঊ") and options.KEY in caps:
    bstack1l1lllll_opy_(options, caps[bstack11ll11l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঋ")])
  elif options.KEY == bstack11ll11l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঌ") and options.KEY in caps:
    bstack1l1l1lll_opy_(options, caps[bstack11ll11l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ঍")])
  elif options.KEY == bstack11ll11l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ঎") and options.KEY in caps:
    bstack11lll111l_opy_(options, caps[bstack11ll11l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬএ")])
  elif options.KEY == bstack11ll11l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫঐ") and options.KEY in caps:
    bstack11ll1l1l_opy_(options, caps[bstack11ll11l_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ঑")])
def bstack1l1l1111l_opy_(caps):
  global bstack1l1l11l1l_opy_
  if isinstance(os.environ.get(bstack11ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ঒")), str):
    bstack1l1l11l1l_opy_ = eval(os.getenv(bstack11ll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩও")))
  if bstack1l1l11l1l_opy_:
    if bstack1l1111llll_opy_() < version.parse(bstack11ll11l_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨঔ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11ll11l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪক")
    if bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩখ") in caps:
      browser = caps[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ")]
    elif bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧঘ") in caps:
      browser = caps[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨঙ")]
    browser = str(browser).lower()
    if browser == bstack11ll11l_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨচ") or browser == bstack11ll11l_opy_ (u"ࠩ࡬ࡴࡦࡪࠧছ"):
      browser = bstack11ll11l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪজ")
    if browser == bstack11ll11l_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬঝ"):
      browser = bstack11ll11l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬঞ")
    if browser not in [bstack11ll11l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ট"), bstack11ll11l_opy_ (u"ࠧࡦࡦࡪࡩࠬঠ"), bstack11ll11l_opy_ (u"ࠨ࡫ࡨࠫড"), bstack11ll11l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩঢ"), bstack11ll11l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫণ")]:
      return None
    try:
      package = bstack11ll11l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ত").format(browser)
      name = bstack11ll11l_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭থ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1l1llll1_opy_(options):
        return None
      for bstack1l1111lll_opy_ in caps.keys():
        options.set_capability(bstack1l1111lll_opy_, caps[bstack1l1111lll_opy_])
      bstack11111111l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lll111l1_opy_(options, bstack111l1llll_opy_):
  if not bstack1l1l1llll1_opy_(options):
    return
  for bstack1l1111lll_opy_ in bstack111l1llll_opy_.keys():
    if bstack1l1111lll_opy_ in bstack1ll11lll1_opy_:
      continue
    if bstack1l1111lll_opy_ in options._caps and type(options._caps[bstack1l1111lll_opy_]) in [dict, list]:
      options._caps[bstack1l1111lll_opy_] = update(options._caps[bstack1l1111lll_opy_], bstack111l1llll_opy_[bstack1l1111lll_opy_])
    else:
      options.set_capability(bstack1l1111lll_opy_, bstack111l1llll_opy_[bstack1l1111lll_opy_])
  bstack11111111l_opy_(options, bstack111l1llll_opy_)
  if bstack11ll11l_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬদ") in options._caps:
    if options._caps[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬধ")] and options._caps[bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ন")].lower() != bstack11ll11l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ঩"):
      del options._caps[bstack11ll11l_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩপ")]
def bstack1llllll111_opy_(proxy_config):
  if bstack11ll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨফ") in proxy_config:
    proxy_config[bstack11ll11l_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧব")] = proxy_config[bstack11ll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪভ")]
    del (proxy_config[bstack11ll11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম")])
  if bstack11ll11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫয") in proxy_config and proxy_config[bstack11ll11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬর")].lower() != bstack11ll11l_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪ঱"):
    proxy_config[bstack11ll11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧল")] = bstack11ll11l_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬ঳")
  if bstack11ll11l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫ঴") in proxy_config:
    proxy_config[bstack11ll11l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")] = bstack11ll11l_opy_ (u"ࠨࡲࡤࡧࠬশ")
  return proxy_config
def bstack1lll11111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11ll11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨষ") in config:
    return proxy
  config[bstack11ll11l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩস")] = bstack1llllll111_opy_(config[bstack11ll11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪহ")])
  if proxy == None:
    proxy = Proxy(config[bstack11ll11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ঺")])
  return proxy
def bstack1l1ll11ll_opy_(self):
  global CONFIG
  global bstack1ll1ll1l1_opy_
  try:
    proxy = bstack11l11l1ll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11ll11l_opy_ (u"࠭࠮ࡱࡣࡦࠫ঻")):
        proxies = bstack1ll1l11lll_opy_(proxy, bstack1ll1ll111l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1l11llll_opy_ = proxies.popitem()
          if bstack11ll11l_opy_ (u"ࠢ࠻࠱࠲়ࠦ") in bstack1l1l11llll_opy_:
            return bstack1l1l11llll_opy_
          else:
            return bstack11ll11l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤঽ") + bstack1l1l11llll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11ll11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨা").format(str(e)))
  return bstack1ll1ll1l1_opy_(self)
def bstack1lllll11_opy_():
  global CONFIG
  return bstack1ll1l1lll_opy_(CONFIG) and bstack1l1lll111_opy_() and bstack1ll111l1l1_opy_() >= version.parse(bstack11lll1l1_opy_)
def bstack1ll11l11_opy_():
  global CONFIG
  return (bstack11ll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ি") in CONFIG or bstack11ll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨী") in CONFIG) and bstack1l111111_opy_()
def bstack1l11lll1l_opy_(config):
  bstack111lll1l_opy_ = {}
  if bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩু") in config:
    bstack111lll1l_opy_ = config[bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪূ")]
  if bstack11ll11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ৃ") in config:
    bstack111lll1l_opy_ = config[bstack11ll11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৄ")]
  proxy = bstack11l11l1ll_opy_(config)
  if proxy:
    if proxy.endswith(bstack11ll11l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৅")) and os.path.isfile(proxy):
      bstack111lll1l_opy_[bstack11ll11l_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৆")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11ll11l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩে")):
        proxies = bstack111lll11l_opy_(config, bstack1ll1ll111l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1l11llll_opy_ = proxies.popitem()
          if bstack11ll11l_opy_ (u"ࠧࡀ࠯࠰ࠤৈ") in bstack1l1l11llll_opy_:
            parsed_url = urlparse(bstack1l1l11llll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11ll11l_opy_ (u"ࠨ࠺࠰࠱ࠥ৉") + bstack1l1l11llll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack111lll1l_opy_[bstack11ll11l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ৊")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack111lll1l_opy_[bstack11ll11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫো")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack111lll1l_opy_[bstack11ll11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬৌ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack111lll1l_opy_[bstack11ll11l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ্࠭")] = str(parsed_url.password)
  return bstack111lll1l_opy_
def bstack1111l11l_opy_(config):
  if bstack11ll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩৎ") in config:
    return config[bstack11ll11l_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৏")]
  return {}
def bstack1ll11ll1l_opy_(caps):
  global bstack1lll1l11l1_opy_
  if bstack11ll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৐") in caps:
    caps[bstack11ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৑")][bstack11ll11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ৒")] = True
    if bstack1lll1l11l1_opy_:
      caps[bstack11ll11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৓")][bstack11ll11l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৔")] = bstack1lll1l11l1_opy_
  else:
    caps[bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ৕")] = True
    if bstack1lll1l11l1_opy_:
      caps[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৖")] = bstack1lll1l11l1_opy_
def bstack1l1lll11_opy_():
  global CONFIG
  if not bstack1l1ll111_opy_(CONFIG):
    return
  if bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪৗ") in CONFIG and bstack111111ll1_opy_(CONFIG[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৘")]):
    if (
      bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৙") in CONFIG
      and bstack111111ll1_opy_(CONFIG[bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৚")].get(bstack11ll11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧ৛")))
    ):
      logger.debug(bstack11ll11l_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧড়"))
      return
    bstack111lll1l_opy_ = bstack1l11lll1l_opy_(CONFIG)
    bstack1l11l111l1_opy_(CONFIG[bstack11ll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨঢ়")], bstack111lll1l_opy_)
def bstack1l11l111l1_opy_(key, bstack111lll1l_opy_):
  global bstack11lll1lll_opy_
  logger.info(bstack1llll11l1l_opy_)
  try:
    bstack11lll1lll_opy_ = Local()
    bstack11ll1l111_opy_ = {bstack11ll11l_opy_ (u"࠭࡫ࡦࡻࠪ৞"): key}
    bstack11ll1l111_opy_.update(bstack111lll1l_opy_)
    logger.debug(bstack1ll11l11l_opy_.format(str(bstack11ll1l111_opy_)))
    bstack11lll1lll_opy_.start(**bstack11ll1l111_opy_)
    if bstack11lll1lll_opy_.isRunning():
      logger.info(bstack1l1ll11111_opy_)
  except Exception as e:
    bstack1l1l1ll1l1_opy_(bstack1llll11111_opy_.format(str(e)))
def bstack1lllll111l_opy_():
  global bstack11lll1lll_opy_
  if bstack11lll1lll_opy_.isRunning():
    logger.info(bstack1ll1lll1ll_opy_)
    bstack11lll1lll_opy_.stop()
  bstack11lll1lll_opy_ = None
def bstack11ll1l1ll_opy_(bstack1l1ll1l111_opy_=[]):
  global CONFIG
  bstack1l1lll1ll_opy_ = []
  bstack11ll1llll_opy_ = [bstack11ll11l_opy_ (u"ࠧࡰࡵࠪয়"), bstack11ll11l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫৠ"), bstack11ll11l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ৡ"), bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬৢ"), bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩৣ"), bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৤")]
  try:
    for err in bstack1l1ll1l111_opy_:
      bstack1l111l1111_opy_ = {}
      for k in bstack11ll1llll_opy_:
        val = CONFIG[bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৥")][int(err[bstack11ll11l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭০")])].get(k)
        if val:
          bstack1l111l1111_opy_[k] = val
      if(err[bstack11ll11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ১")] != bstack11ll11l_opy_ (u"ࠩࠪ২")):
        bstack1l111l1111_opy_[bstack11ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩ৩")] = {
          err[bstack11ll11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ৪")]: err[bstack11ll11l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৫")]
        }
        bstack1l1lll1ll_opy_.append(bstack1l111l1111_opy_)
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨ৬") + str(e))
  finally:
    return bstack1l1lll1ll_opy_
def bstack1l11ll1111_opy_(file_name):
  bstack1lll11ll11_opy_ = []
  try:
    bstack111l1l1l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack111l1l1l_opy_):
      with open(bstack111l1l1l_opy_) as f:
        bstack1ll11lllll_opy_ = json.load(f)
        bstack1lll11ll11_opy_ = bstack1ll11lllll_opy_
      os.remove(bstack111l1l1l_opy_)
    return bstack1lll11ll11_opy_
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡪࡩ࡯ࡩࠣࡩࡷࡸ࡯ࡳࠢ࡯࡭ࡸࡺ࠺ࠡࠩ৭") + str(e))
    return bstack1lll11ll11_opy_
def bstack1l11111l11_opy_():
  global bstack1l11l1ll11_opy_
  global bstack1ll1llll1_opy_
  global bstack1lll11l11_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack1ll11111ll_opy_
  global bstack1l111l11l_opy_
  global CONFIG
  bstack1111ll1ll_opy_ = os.environ.get(bstack11ll11l_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ৮"))
  if bstack1111ll1ll_opy_ in [bstack11ll11l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ৯"), bstack11ll11l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩৰ")]:
    bstack1111l1lll_opy_()
  percy.shutdown()
  if bstack1l11l1ll11_opy_:
    logger.warning(bstack1l1l11l11l_opy_.format(str(bstack1l11l1ll11_opy_)))
  else:
    try:
      bstack111ll1l1_opy_ = bstack1111lll1l_opy_(bstack11ll11l_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪৱ"), logger)
      if bstack111ll1l1_opy_.get(bstack11ll11l_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪ৲")) and bstack111ll1l1_opy_.get(bstack11ll11l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫ৳")).get(bstack11ll11l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ৴")):
        logger.warning(bstack1l1l11l11l_opy_.format(str(bstack111ll1l1_opy_[bstack11ll11l_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭৵")][bstack11ll11l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ৶")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1l1ll11l_opy_)
  global bstack11lll1lll_opy_
  if bstack11lll1lll_opy_:
    bstack1lllll111l_opy_()
  try:
    for driver in bstack1ll1llll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1l11l111_opy_)
  if bstack1l111l11l_opy_ == bstack11ll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ৷"):
    bstack1ll11111ll_opy_ = bstack1l11ll1111_opy_(bstack11ll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ৸"))
  if bstack1l111l11l_opy_ == bstack11ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ৹") and len(bstack1ll1l1l1l1_opy_) == 0:
    bstack1ll1l1l1l1_opy_ = bstack1l11ll1111_opy_(bstack11ll11l_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ৺"))
    if len(bstack1ll1l1l1l1_opy_) == 0:
      bstack1ll1l1l1l1_opy_ = bstack1l11ll1111_opy_(bstack11ll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭৻"))
  bstack1l11111l1_opy_ = bstack11ll11l_opy_ (u"ࠨࠩৼ")
  if len(bstack1lll11l11_opy_) > 0:
    bstack1l11111l1_opy_ = bstack11ll1l1ll_opy_(bstack1lll11l11_opy_)
  elif len(bstack1ll1l1l1l1_opy_) > 0:
    bstack1l11111l1_opy_ = bstack11ll1l1ll_opy_(bstack1ll1l1l1l1_opy_)
  elif len(bstack1ll11111ll_opy_) > 0:
    bstack1l11111l1_opy_ = bstack11ll1l1ll_opy_(bstack1ll11111ll_opy_)
  elif len(bstack1l1l1l11_opy_) > 0:
    bstack1l11111l1_opy_ = bstack11ll1l1ll_opy_(bstack1l1l1l11_opy_)
  if bool(bstack1l11111l1_opy_):
    bstack11l11l11_opy_(bstack1l11111l1_opy_)
  else:
    bstack11l11l11_opy_()
  bstack1l11l1lll_opy_(bstack1lllll111_opy_, logger)
  bstack111l1lll_opy_.bstack1l11111l1l_opy_(CONFIG)
  if len(bstack1ll11111ll_opy_) > 0:
    sys.exit(len(bstack1ll11111ll_opy_))
def bstack1ll111111_opy_(bstack11l11l111_opy_, frame):
  global bstack1l1111l111_opy_
  logger.error(bstack1111ll1l_opy_)
  bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬ৽"), bstack11l11l111_opy_)
  if hasattr(signal, bstack11ll11l_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫ৾")):
    bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫ৿"), signal.Signals(bstack11l11l111_opy_).name)
  else:
    bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ਀"), bstack11ll11l_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪਁ"))
  bstack1111ll1ll_opy_ = os.environ.get(bstack11ll11l_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਂ"))
  if bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਃ"):
    bstack1ll11l11l1_opy_.stop(bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ਄")))
  bstack1l11111l11_opy_()
  sys.exit(1)
def bstack1l1l1ll1l1_opy_(err):
  logger.critical(bstack1ll1111ll_opy_.format(str(err)))
  bstack11l11l11_opy_(bstack1ll1111ll_opy_.format(str(err)), True)
  atexit.unregister(bstack1l11111l11_opy_)
  bstack1111l1lll_opy_()
  sys.exit(1)
def bstack111111111_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11l11l11_opy_(message, True)
  atexit.unregister(bstack1l11111l11_opy_)
  bstack1111l1lll_opy_()
  sys.exit(1)
def bstack1llll1111_opy_():
  global CONFIG
  global bstack1ll1l11111_opy_
  global bstack1lll1111l1_opy_
  global bstack1l1l111l_opy_
  CONFIG = bstack11ll11ll1_opy_()
  load_dotenv(CONFIG.get(bstack11ll11l_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫਅ")))
  bstack1111lll11_opy_()
  bstack1l1l1l1l11_opy_()
  CONFIG = bstack1l111lll1_opy_(CONFIG)
  update(CONFIG, bstack1lll1111l1_opy_)
  update(CONFIG, bstack1ll1l11111_opy_)
  CONFIG = bstack1ll1ll11l_opy_(CONFIG)
  bstack1l1l111l_opy_ = bstack1l1ll111_opy_(CONFIG)
  os.environ[bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧਆ")] = bstack1l1l111l_opy_.__str__()
  bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ਇ"), bstack1l1l111l_opy_)
  if (bstack11ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਈ") in CONFIG and bstack11ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਉ") in bstack1ll1l11111_opy_) or (
          bstack11ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਊ") in CONFIG and bstack11ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ਋") not in bstack1lll1111l1_opy_):
    if os.getenv(bstack11ll11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ਌")):
      CONFIG[bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭਍")] = os.getenv(bstack11ll11l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ਎"))
    else:
      bstack1ll11l111l_opy_()
  elif (bstack11ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਏ") not in CONFIG and bstack11ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩਐ") in CONFIG) or (
          bstack11ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਑") in bstack1lll1111l1_opy_ and bstack11ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ਒") not in bstack1ll1l11111_opy_):
    del (CONFIG[bstack11ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਓ")])
  if bstack1ll1lll1l1_opy_(CONFIG):
    bstack1l1l1ll1l1_opy_(bstack1l1l1l1111_opy_)
  bstack1lll1l1l1l_opy_()
  bstack1lll11ll1_opy_()
  if bstack1l1l11l1l_opy_:
    CONFIG[bstack11ll11l_opy_ (u"ࠫࡦࡶࡰࠨਔ")] = bstack111ll11l1_opy_(CONFIG)
    logger.info(bstack1ll1l1l11l_opy_.format(CONFIG[bstack11ll11l_opy_ (u"ࠬࡧࡰࡱࠩਕ")]))
  if not bstack1l1l111l_opy_:
    CONFIG[bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਖ")] = [{}]
def bstack1ll1l1llll_opy_(config, bstack11lllll1l1_opy_):
  global CONFIG
  global bstack1l1l11l1l_opy_
  CONFIG = config
  bstack1l1l11l1l_opy_ = bstack11lllll1l1_opy_
def bstack1lll11ll1_opy_():
  global CONFIG
  global bstack1l1l11l1l_opy_
  if bstack11ll11l_opy_ (u"ࠧࡢࡲࡳࠫਗ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack111111111_opy_(e, bstack1l11llll11_opy_)
    bstack1l1l11l1l_opy_ = True
    bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧਘ"), True)
def bstack111ll11l1_opy_(config):
  bstack1l1111l11_opy_ = bstack11ll11l_opy_ (u"ࠩࠪਙ")
  app = config[bstack11ll11l_opy_ (u"ࠪࡥࡵࡶࠧਚ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lllll1ll_opy_:
      if os.path.exists(app):
        bstack1l1111l11_opy_ = bstack1lll11111l_opy_(config, app)
      elif bstack11l11lll1_opy_(app):
        bstack1l1111l11_opy_ = app
      else:
        bstack1l1l1ll1l1_opy_(bstack11lllll111_opy_.format(app))
    else:
      if bstack11l11lll1_opy_(app):
        bstack1l1111l11_opy_ = app
      elif os.path.exists(app):
        bstack1l1111l11_opy_ = bstack1lll11111l_opy_(app)
      else:
        bstack1l1l1ll1l1_opy_(bstack1ll1111l1_opy_)
  else:
    if len(app) > 2:
      bstack1l1l1ll1l1_opy_(bstack1lll1111l_opy_)
    elif len(app) == 2:
      if bstack11ll11l_opy_ (u"ࠫࡵࡧࡴࡩࠩਛ") in app and bstack11ll11l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨਜ") in app:
        if os.path.exists(app[bstack11ll11l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫਝ")]):
          bstack1l1111l11_opy_ = bstack1lll11111l_opy_(config, app[bstack11ll11l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬਞ")], app[bstack11ll11l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫਟ")])
        else:
          bstack1l1l1ll1l1_opy_(bstack11lllll111_opy_.format(app))
      else:
        bstack1l1l1ll1l1_opy_(bstack1lll1111l_opy_)
    else:
      for key in app:
        if key in bstack11lll1ll1_opy_:
          if key == bstack11ll11l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧਠ"):
            if os.path.exists(app[key]):
              bstack1l1111l11_opy_ = bstack1lll11111l_opy_(config, app[key])
            else:
              bstack1l1l1ll1l1_opy_(bstack11lllll111_opy_.format(app))
          else:
            bstack1l1111l11_opy_ = app[key]
        else:
          bstack1l1l1ll1l1_opy_(bstack111l11ll1_opy_)
  return bstack1l1111l11_opy_
def bstack11l11lll1_opy_(bstack1l1111l11_opy_):
  import re
  bstack1l11l1l11l_opy_ = re.compile(bstack11ll11l_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥਡ"))
  bstack11ll11lll_opy_ = re.compile(bstack11ll11l_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣਢ"))
  if bstack11ll11l_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫਣ") in bstack1l1111l11_opy_ or re.fullmatch(bstack1l11l1l11l_opy_, bstack1l1111l11_opy_) or re.fullmatch(bstack11ll11lll_opy_, bstack1l1111l11_opy_):
    return True
  else:
    return False
def bstack1lll11111l_opy_(config, path, bstack1llll1l11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11ll11l_opy_ (u"࠭ࡲࡣࠩਤ")).read()).hexdigest()
  bstack1ll1l111_opy_ = bstack1l1llll11l_opy_(md5_hash)
  bstack1l1111l11_opy_ = None
  if bstack1ll1l111_opy_:
    logger.info(bstack11l1l1lll_opy_.format(bstack1ll1l111_opy_, md5_hash))
    return bstack1ll1l111_opy_
  bstack1111ll111_opy_ = MultipartEncoder(
    fields={
      bstack11ll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࠬਥ"): (os.path.basename(path), open(os.path.abspath(path), bstack11ll11l_opy_ (u"ࠨࡴࡥࠫਦ")), bstack11ll11l_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ਧ")),
      bstack11ll11l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ਨ"): bstack1llll1l11_opy_
    }
  )
  response = requests.post(bstack111ll1lll_opy_, data=bstack1111ll111_opy_,
                           headers={bstack11ll11l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ਩"): bstack1111ll111_opy_.content_type},
                           auth=(config[bstack11ll11l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧਪ")], config[bstack11ll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩਫ")]))
  try:
    res = json.loads(response.text)
    bstack1l1111l11_opy_ = res[bstack11ll11l_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨਬ")]
    logger.info(bstack11ll11l1l_opy_.format(bstack1l1111l11_opy_))
    bstack1lll1lllll_opy_(md5_hash, bstack1l1111l11_opy_)
  except ValueError as err:
    bstack1l1l1ll1l1_opy_(bstack11ll11l11_opy_.format(str(err)))
  return bstack1l1111l11_opy_
def bstack1lll1l1l1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack111ll111_opy_
  bstack1ll1l1l1_opy_ = 1
  bstack1lllllll1l_opy_ = 1
  if bstack11ll11l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨਭ") in CONFIG:
    bstack1lllllll1l_opy_ = CONFIG[bstack11ll11l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩਮ")]
  else:
    bstack1lllllll1l_opy_ = bstack1ll11l11ll_opy_(framework_name, args) or 1
  if bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ") in CONFIG:
    bstack1ll1l1l1_opy_ = len(CONFIG[bstack11ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਰ")])
  bstack111ll111_opy_ = int(bstack1lllllll1l_opy_) * int(bstack1ll1l1l1_opy_)
def bstack1ll11l11ll_opy_(framework_name, args):
  if framework_name == bstack1llllll1l_opy_ and args and bstack11ll11l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ਱") in args:
      bstack11111l11_opy_ = args.index(bstack11ll11l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫਲ"))
      return int(args[bstack11111l11_opy_ + 1]) or 1
  return 1
def bstack1l1llll11l_opy_(md5_hash):
  bstack1l111111l_opy_ = os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"ࠧࡿࠩਲ਼")), bstack11ll11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ਴"), bstack11ll11l_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪਵ"))
  if os.path.exists(bstack1l111111l_opy_):
    bstack1l1ll1111l_opy_ = json.load(open(bstack1l111111l_opy_, bstack11ll11l_opy_ (u"ࠪࡶࡧ࠭ਸ਼")))
    if md5_hash in bstack1l1ll1111l_opy_:
      bstack11l1111l1_opy_ = bstack1l1ll1111l_opy_[md5_hash]
      bstack1ll1lll11_opy_ = datetime.datetime.now()
      bstack1l1l1l1lll_opy_ = datetime.datetime.strptime(bstack11l1111l1_opy_[bstack11ll11l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ਷")], bstack11ll11l_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩਸ"))
      if (bstack1ll1lll11_opy_ - bstack1l1l1l1lll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11l1111l1_opy_[bstack11ll11l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫਹ")]):
        return None
      return bstack11l1111l1_opy_[bstack11ll11l_opy_ (u"ࠧࡪࡦࠪ਺")]
  else:
    return None
def bstack1lll1lllll_opy_(md5_hash, bstack1l1111l11_opy_):
  bstack111l1111l_opy_ = os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"ࠨࢀࠪ਻")), bstack11ll11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬਼ࠩ"))
  if not os.path.exists(bstack111l1111l_opy_):
    os.makedirs(bstack111l1111l_opy_)
  bstack1l111111l_opy_ = os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"ࠪࢂࠬ਽")), bstack11ll11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫਾ"), bstack11ll11l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ਿ"))
  bstack1ll111l11l_opy_ = {
    bstack11ll11l_opy_ (u"࠭ࡩࡥࠩੀ"): bstack1l1111l11_opy_,
    bstack11ll11l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪੁ"): datetime.datetime.strftime(datetime.datetime.now(), bstack11ll11l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬੂ")),
    bstack11ll11l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ੃"): str(__version__)
  }
  if os.path.exists(bstack1l111111l_opy_):
    bstack1l1ll1111l_opy_ = json.load(open(bstack1l111111l_opy_, bstack11ll11l_opy_ (u"ࠪࡶࡧ࠭੄")))
  else:
    bstack1l1ll1111l_opy_ = {}
  bstack1l1ll1111l_opy_[md5_hash] = bstack1ll111l11l_opy_
  with open(bstack1l111111l_opy_, bstack11ll11l_opy_ (u"ࠦࡼ࠱ࠢ੅")) as outfile:
    json.dump(bstack1l1ll1111l_opy_, outfile)
def bstack1ll11l111_opy_(self):
  return
def bstack111llll1l_opy_(self):
  return
def bstack1ll1ll1l1l_opy_(self):
  global bstack1l111l1ll_opy_
  bstack1l111l1ll_opy_(self)
def bstack1l11ll1l11_opy_():
  global bstack1ll11ll1ll_opy_
  bstack1ll11ll1ll_opy_ = True
def bstack111lll11_opy_(self):
  global bstack111ll1ll_opy_
  global bstack1111l11ll_opy_
  global bstack11l1111l_opy_
  try:
    if bstack11ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ੆") in bstack111ll1ll_opy_ and self.session_id != None and bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪੇ"), bstack11ll11l_opy_ (u"ࠧࠨੈ")) != bstack11ll11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ੉"):
      bstack1l111llll1_opy_ = bstack11ll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੊") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪੋ")
      if bstack1l111llll1_opy_ == bstack11ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫੌ"):
        bstack1ll111ll_opy_(logger)
      if self != None:
        bstack1llll1l1l_opy_(self, bstack1l111llll1_opy_, bstack11ll11l_opy_ (u"ࠬ࠲ࠠࠨ੍").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11ll11l_opy_ (u"࠭ࠧ੎")
    if bstack11ll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ੏") in bstack111ll1ll_opy_ and getattr(threading.current_thread(), bstack11ll11l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੐"), None):
      bstack1l1llll1l1_opy_.bstack1lll11ll1l_opy_(self, bstack1lll1ll1ll_opy_, logger, wait=True)
    if bstack11ll11l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩੑ") in bstack111ll1ll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1llll1l1l_opy_(self, bstack11ll11l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ੒"))
      bstack1ll11l1l1l_opy_.bstack11l1ll11_opy_(self)
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ੓") + str(e))
  bstack11l1111l_opy_(self)
  self.session_id = None
def bstack1111111l1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1l111111_opy_
    global bstack111ll1ll_opy_
    command_executor = kwargs.get(bstack11ll11l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ੔"), bstack11ll11l_opy_ (u"࠭ࠧ੕"))
    bstack1l111l1l1l_opy_ = False
    if type(command_executor) == str and bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ੖") in command_executor:
      bstack1l111l1l1l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ੗") in str(getattr(command_executor, bstack11ll11l_opy_ (u"ࠩࡢࡹࡷࡲࠧ੘"), bstack11ll11l_opy_ (u"ࠪࠫਖ਼"))):
      bstack1l111l1l1l_opy_ = True
    else:
      return bstack11ll1l11l_opy_(self, *args, **kwargs)
    if bstack1l111l1l1l_opy_:
      if kwargs.get(bstack11ll11l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬਗ਼")):
        kwargs[bstack11ll11l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ਜ਼")] = bstack1l1l111111_opy_(kwargs[bstack11ll11l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧੜ")], bstack111ll1ll_opy_)
      elif kwargs.get(bstack11ll11l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ੝")):
        kwargs[bstack11ll11l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨਫ਼")] = bstack1l1l111111_opy_(kwargs[bstack11ll11l_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ੟")], bstack111ll1ll_opy_)
  except Exception as e:
    logger.error(bstack11ll11l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ੠").format(str(e)))
  return bstack11ll1l11l_opy_(self, *args, **kwargs)
def bstack1l1ll1ll11_opy_(self, command_executor=bstack11ll11l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ੡"), *args, **kwargs):
  bstack1ll1llllll_opy_ = bstack1111111l1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack111lllll1_opy_.on():
    return bstack1ll1llllll_opy_
  try:
    logger.debug(bstack11ll11l_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩ੢").format(str(command_executor)))
    logger.debug(bstack11ll11l_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨ੣").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ੤") in command_executor._url:
      bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ੥"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ੦") in command_executor):
    bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ੧"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1111l1111_opy_ = getattr(threading.current_thread(), bstack11ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ੨"), None)
  if bstack11ll11l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ੩") in bstack111ll1ll_opy_ or bstack11ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ੪") in bstack111ll1ll_opy_:
    bstack1ll11l11l1_opy_.bstack1l1l1ll11l_opy_(self)
  if bstack11ll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ੫") in bstack111ll1ll_opy_ and bstack1111l1111_opy_ and bstack1111l1111_opy_.get(bstack11ll11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੬"), bstack11ll11l_opy_ (u"ࠩࠪ੭")) == bstack11ll11l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ੮"):
    bstack1ll11l11l1_opy_.bstack1l1l1ll11l_opy_(self)
  return bstack1ll1llllll_opy_
def bstack11111l1l1_opy_(args):
  return bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬ੯") in str(args)
def bstack1l1l1ll1ll_opy_(self, driver_command, *args, **kwargs):
  global bstack1l1llll11_opy_
  global bstack1lll1lll1_opy_
  bstack1l11lll11_opy_ = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩੰ"), None) and bstack1l111111l1_opy_(
          threading.current_thread(), bstack11ll11l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬੱ"), None)
  bstack1l1lll1lll_opy_ = getattr(self, bstack11ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧੲ"), None) != None and getattr(self, bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨੳ"), None) == True
  if not bstack1lll1lll1_opy_ and bstack1l1l111l_opy_ and bstack11ll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩੴ") in CONFIG and CONFIG[bstack11ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪੵ")] == True and bstack1ll1l1ll1l_opy_.bstack1ll1ll1ll_opy_(driver_command) and (bstack1l1lll1lll_opy_ or bstack1l11lll11_opy_) and not bstack11111l1l1_opy_(args):
    try:
      bstack1lll1lll1_opy_ = True
      logger.debug(bstack11ll11l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭੶").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11ll11l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪ੷").format(str(err)))
    bstack1lll1lll1_opy_ = False
  response = bstack1l1llll11_opy_(self, driver_command, *args, **kwargs)
  if (bstack11ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ੸") in str(bstack111ll1ll_opy_).lower() or bstack11ll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ੹") in str(bstack111ll1ll_opy_).lower()) and bstack111lllll1_opy_.on():
    try:
      if driver_command == bstack11ll11l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ੺"):
        bstack1ll11l11l1_opy_.bstack1lllll1l1l_opy_({
            bstack11ll11l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ੻"): response[bstack11ll11l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ੼")],
            bstack11ll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ੽"): bstack1ll11l11l1_opy_.current_test_uuid() if bstack1ll11l11l1_opy_.current_test_uuid() else bstack111lllll1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1l1lll111l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1111l11ll_opy_
  global bstack111l11l1l_opy_
  global bstack11ll1ll1l_opy_
  global bstack1l1l1lllll_opy_
  global bstack1l111ll11_opy_
  global bstack111ll1ll_opy_
  global bstack11ll1l11l_opy_
  global bstack1ll1llll1_opy_
  global bstack1l1l11lll_opy_
  global bstack1lll1ll1ll_opy_
  CONFIG[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ੾")] = str(bstack111ll1ll_opy_) + str(__version__)
  command_executor = bstack1ll1ll111l_opy_()
  logger.debug(bstack1lll11l1l_opy_.format(command_executor))
  proxy = bstack1lll11111_opy_(CONFIG, proxy)
  bstack11l1l1111_opy_ = 0 if bstack111l11l1l_opy_ < 0 else bstack111l11l1l_opy_
  try:
    if bstack1l1l1lllll_opy_ is True:
      bstack11l1l1111_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l111ll11_opy_ is True:
      bstack11l1l1111_opy_ = int(threading.current_thread().name)
  except:
    bstack11l1l1111_opy_ = 0
  bstack111l1llll_opy_ = bstack1lll1l11l_opy_(CONFIG, bstack11l1l1111_opy_)
  logger.debug(bstack1l111ll11l_opy_.format(str(bstack111l1llll_opy_)))
  if bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ੿") in CONFIG and bstack111111ll1_opy_(CONFIG[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ઀")]):
    bstack1ll11ll1l_opy_(bstack111l1llll_opy_)
  if bstack11llll1111_opy_.bstack1l1l1l1l1l_opy_(CONFIG, bstack11l1l1111_opy_) and bstack11llll1111_opy_.bstack1ll11111l_opy_(bstack111l1llll_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack11llll1111_opy_.set_capabilities(bstack111l1llll_opy_, CONFIG)
  if desired_capabilities:
    bstack1l1lll11l_opy_ = bstack1l111lll1_opy_(desired_capabilities)
    bstack1l1lll11l_opy_[bstack11ll11l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨઁ")] = bstack1l1l1lll1l_opy_(CONFIG)
    bstack1lllllllll_opy_ = bstack1lll1l11l_opy_(bstack1l1lll11l_opy_)
    if bstack1lllllllll_opy_:
      bstack111l1llll_opy_ = update(bstack1lllllllll_opy_, bstack111l1llll_opy_)
    desired_capabilities = None
  if options:
    bstack1lll111l1_opy_(options, bstack111l1llll_opy_)
  if not options:
    options = bstack1l1l1111l_opy_(bstack111l1llll_opy_)
  bstack1lll1ll1ll_opy_ = CONFIG.get(bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬં"))[bstack11l1l1111_opy_]
  if proxy and bstack1ll111l1l1_opy_() >= version.parse(bstack11ll11l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪઃ")):
    options.proxy(proxy)
  if options and bstack1ll111l1l1_opy_() >= version.parse(bstack11ll11l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ઄")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1ll111l1l1_opy_() < version.parse(bstack11ll11l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫઅ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack111l1llll_opy_)
  logger.info(bstack1l1l111l1l_opy_)
  if bstack1ll111l1l1_opy_() >= version.parse(bstack11ll11l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭આ")):
    bstack11ll1l11l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack1ll111l1l1_opy_() >= version.parse(bstack11ll11l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ઇ")):
    bstack11ll1l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll111l1l1_opy_() >= version.parse(bstack11ll11l_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨઈ")):
    bstack11ll1l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11ll1l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack111ll111l_opy_ = bstack11ll11l_opy_ (u"ࠩࠪઉ")
    if bstack1ll111l1l1_opy_() >= version.parse(bstack11ll11l_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫઊ")):
      bstack111ll111l_opy_ = self.caps.get(bstack11ll11l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦઋ"))
    else:
      bstack111ll111l_opy_ = self.capabilities.get(bstack11ll11l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧઌ"))
    if bstack111ll111l_opy_:
      bstack11ll1lll1_opy_(bstack111ll111l_opy_)
      if bstack1ll111l1l1_opy_() <= version.parse(bstack11ll11l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ઍ")):
        self.command_executor._url = bstack11ll11l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ઎") + bstack1l11ll1l1l_opy_ + bstack11ll11l_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧએ")
      else:
        self.command_executor._url = bstack11ll11l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦઐ") + bstack111ll111l_opy_ + bstack11ll11l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦઑ")
      logger.debug(bstack1111l1l1l_opy_.format(bstack111ll111l_opy_))
    else:
      logger.debug(bstack1ll1111l1l_opy_.format(bstack11ll11l_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ઒")))
  except Exception as e:
    logger.debug(bstack1ll1111l1l_opy_.format(e))
  if bstack11ll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫઓ") in bstack111ll1ll_opy_:
    bstack11l1l11l_opy_(bstack111l11l1l_opy_, bstack1l1l11lll_opy_)
  bstack1111l11ll_opy_ = self.session_id
  if bstack11ll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ઔ") in bstack111ll1ll_opy_ or bstack11ll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧક") in bstack111ll1ll_opy_ or bstack11ll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧખ") in bstack111ll1ll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1111l1111_opy_ = getattr(threading.current_thread(), bstack11ll11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪગ"), None)
  if bstack11ll11l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪઘ") in bstack111ll1ll_opy_ or bstack11ll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪઙ") in bstack111ll1ll_opy_:
    bstack1ll11l11l1_opy_.bstack1l1l1ll11l_opy_(self)
  if bstack11ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬચ") in bstack111ll1ll_opy_ and bstack1111l1111_opy_ and bstack1111l1111_opy_.get(bstack11ll11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭છ"), bstack11ll11l_opy_ (u"ࠧࠨજ")) == bstack11ll11l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩઝ"):
    bstack1ll11l11l1_opy_.bstack1l1l1ll11l_opy_(self)
  bstack1ll1llll1_opy_.append(self)
  if bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬઞ") in CONFIG and bstack11ll11l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨટ") in CONFIG[bstack11ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧઠ")][bstack11l1l1111_opy_]:
    bstack11ll1ll1l_opy_ = CONFIG[bstack11ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨડ")][bstack11l1l1111_opy_][bstack11ll11l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫઢ")]
  logger.debug(bstack11l1llll1_opy_.format(bstack1111l11ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1ll1l1111_opy_
    def bstack1ll111lll1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11l11l11l_opy_
      if(bstack11ll11l_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤણ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"ࠨࢀࠪત")), bstack11ll11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩથ"), bstack11ll11l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬદ")), bstack11ll11l_opy_ (u"ࠫࡼ࠭ધ")) as fp:
          fp.write(bstack11ll11l_opy_ (u"ࠧࠨન"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11ll11l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣ઩")))):
          with open(args[1], bstack11ll11l_opy_ (u"ࠧࡳࠩપ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11ll11l_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧફ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1llll111_opy_)
            if bstack11ll11l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭બ") in CONFIG and str(CONFIG[bstack11ll11l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧભ")]).lower() != bstack11ll11l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪમ"):
                bstack11111lll1_opy_ = bstack1ll1l1111_opy_()
                bstack1l11ll11l1_opy_ = bstack11ll11l_opy_ (u"ࠬ࠭ࠧࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡴࡦࡺࡨࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷ࡢࡁࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡳࡣ࡮ࡴࡤࡦࡺࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠸࡝࠼ࠌࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰ࡶࡰ࡮ࡩࡥࠩ࠲࠯ࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹ࠩ࠼ࠌࡦࡳࡳࡹࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࠪ࠽ࠍ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽ࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋࠢࠣࡸࡷࡿࠠࡼࡽࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠌࠣࠤࠥࠦࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࠽ࠍࠤࠥࢃࡽࠡࡥࡤࡸࡨ࡮ࠠࠩࡧࡻ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࡩ࡯࡯ࡵࡲࡰࡪ࠴ࡥࡳࡴࡲࡶ࠭ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠣ࠮ࠣࡩࡽ࠯࠻ࠋࠢࠣࢁࢂࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠯ࠎࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࠎࠥࠦࡽࡾࠫ࠾ࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋࡿࢀ࠿ࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࠬ࠭ࠧય").format(bstack11111lll1_opy_=bstack11111lll1_opy_)
            lines.insert(1, bstack1l11ll11l1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11ll11l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣર")), bstack11ll11l_opy_ (u"ࠧࡸࠩ઱")) as bstack111ll1l11_opy_:
              bstack111ll1l11_opy_.writelines(lines)
        CONFIG[bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪલ")] = str(bstack111ll1ll_opy_) + str(__version__)
        bstack11l1l1111_opy_ = 0 if bstack111l11l1l_opy_ < 0 else bstack111l11l1l_opy_
        try:
          if bstack1l1l1lllll_opy_ is True:
            bstack11l1l1111_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l111ll11_opy_ is True:
            bstack11l1l1111_opy_ = int(threading.current_thread().name)
        except:
          bstack11l1l1111_opy_ = 0
        CONFIG[bstack11ll11l_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤળ")] = False
        CONFIG[bstack11ll11l_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ઴")] = True
        bstack111l1llll_opy_ = bstack1lll1l11l_opy_(CONFIG, bstack11l1l1111_opy_)
        logger.debug(bstack1l111ll11l_opy_.format(str(bstack111l1llll_opy_)))
        if CONFIG.get(bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨવ")):
          bstack1ll11ll1l_opy_(bstack111l1llll_opy_)
        if bstack11ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ") in CONFIG and bstack11ll11l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫષ") in CONFIG[bstack11ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ")][bstack11l1l1111_opy_]:
          bstack11ll1ll1l_opy_ = CONFIG[bstack11ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫહ")][bstack11l1l1111_opy_][bstack11ll11l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ઺")]
        args.append(os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"ࠪࢂࠬ઻")), bstack11ll11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮઼ࠫ"), bstack11ll11l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧઽ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack111l1llll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11ll11l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣા"))
      bstack11l11l11l_opy_ = True
      return bstack1l111l11_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11lll111ll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack111l11l1l_opy_
    global bstack11ll1ll1l_opy_
    global bstack1l1l1lllll_opy_
    global bstack1l111ll11_opy_
    global bstack111ll1ll_opy_
    CONFIG[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩિ")] = str(bstack111ll1ll_opy_) + str(__version__)
    bstack11l1l1111_opy_ = 0 if bstack111l11l1l_opy_ < 0 else bstack111l11l1l_opy_
    try:
      if bstack1l1l1lllll_opy_ is True:
        bstack11l1l1111_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l111ll11_opy_ is True:
        bstack11l1l1111_opy_ = int(threading.current_thread().name)
    except:
      bstack11l1l1111_opy_ = 0
    CONFIG[bstack11ll11l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢી")] = True
    bstack111l1llll_opy_ = bstack1lll1l11l_opy_(CONFIG, bstack11l1l1111_opy_)
    logger.debug(bstack1l111ll11l_opy_.format(str(bstack111l1llll_opy_)))
    if CONFIG.get(bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ુ")):
      bstack1ll11ll1l_opy_(bstack111l1llll_opy_)
    if bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૂ") in CONFIG and bstack11ll11l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩૃ") in CONFIG[bstack11ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૄ")][bstack11l1l1111_opy_]:
      bstack11ll1ll1l_opy_ = CONFIG[bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૅ")][bstack11l1l1111_opy_][bstack11ll11l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૆")]
    import urllib
    import json
    if bstack11ll11l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬે") in CONFIG and str(CONFIG[bstack11ll11l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ૈ")]).lower() != bstack11ll11l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩૉ"):
        bstack1l1l111l11_opy_ = bstack1ll1l1111_opy_()
        bstack11111lll1_opy_ = bstack1l1l111l11_opy_ + urllib.parse.quote(json.dumps(bstack111l1llll_opy_))
    else:
        bstack11111lll1_opy_ = bstack11ll11l_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭૊") + urllib.parse.quote(json.dumps(bstack111l1llll_opy_))
    browser = self.connect(bstack11111lll1_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1ll11l11_opy_():
    global bstack11l11l11l_opy_
    global bstack111ll1ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1lll11ll_opy_
        if not bstack1l1l111l_opy_:
          global bstack111ll11l_opy_
          if not bstack111ll11l_opy_:
            from bstack_utils.helper import bstack11lll11l1_opy_, bstack1l1ll1l11l_opy_
            bstack111ll11l_opy_ = bstack11lll11l1_opy_()
            bstack1l1ll1l11l_opy_(bstack111ll1ll_opy_)
          BrowserType.connect = bstack1l1lll11ll_opy_
          return
        BrowserType.launch = bstack11lll111ll_opy_
        bstack11l11l11l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll111lll1_opy_
      bstack11l11l11l_opy_ = True
    except Exception as e:
      pass
def bstack1l11ll11_opy_(context, bstack1l1lllll1_opy_):
  try:
    context.page.evaluate(bstack11ll11l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨો"), bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪૌ")+ json.dumps(bstack1l1lllll1_opy_) + bstack11ll11l_opy_ (u"ࠢࡾࡿ્ࠥ"))
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨ૎"), e)
def bstack11lllll1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11ll11l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ૏"), bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨૐ") + json.dumps(message) + bstack11ll11l_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧ૑") + json.dumps(level) + bstack11ll11l_opy_ (u"ࠬࢃࡽࠨ૒"))
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤ૓"), e)
def bstack1l11l1ll1_opy_(self, url):
  global bstack1111l11l1_opy_
  try:
    bstack11llllll_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll111l1l_opy_.format(str(err)))
  try:
    bstack1111l11l1_opy_(self, url)
  except Exception as e:
    try:
      bstack11lll1l1l1_opy_ = str(e)
      if any(err_msg in bstack11lll1l1l1_opy_ for err_msg in bstack1l1l11l1_opy_):
        bstack11llllll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll111l1l_opy_.format(str(err)))
    raise e
def bstack11ll1lll_opy_(self):
  global bstack11lll1111_opy_
  bstack11lll1111_opy_ = self
  return
def bstack11111l11l_opy_(self):
  global bstack1l11l1l1_opy_
  bstack1l11l1l1_opy_ = self
  return
def bstack1111l1l1_opy_(test_name, bstack111l11lll_opy_):
  global CONFIG
  if percy.bstack1ll111l1ll_opy_() == bstack11ll11l_opy_ (u"ࠢࡵࡴࡸࡩࠧ૔"):
    bstack1llll1ll1l_opy_ = os.path.relpath(bstack111l11lll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1llll1ll1l_opy_)
    bstack11l11lll_opy_ = suite_name + bstack11ll11l_opy_ (u"ࠣ࠯ࠥ૕") + test_name
    threading.current_thread().percySessionName = bstack11l11lll_opy_
def bstack1ll11ll111_opy_(self, test, *args, **kwargs):
  global bstack1lll1111ll_opy_
  test_name = None
  bstack111l11lll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack111l11lll_opy_ = str(test.source)
  bstack1111l1l1_opy_(test_name, bstack111l11lll_opy_)
  bstack1lll1111ll_opy_(self, test, *args, **kwargs)
def bstack1l111l1l1_opy_(driver, bstack11l11lll_opy_):
  if not bstack11llllll11_opy_ and bstack11l11lll_opy_:
      bstack1l1l11ll11_opy_ = {
          bstack11ll11l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ૖"): bstack11ll11l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ૗"),
          bstack11ll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ૘"): {
              bstack11ll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ૙"): bstack11l11lll_opy_
          }
      }
      bstack11l1ll1ll_opy_ = bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ૚").format(json.dumps(bstack1l1l11ll11_opy_))
      driver.execute_script(bstack11l1ll1ll_opy_)
  if bstack1lll11llll_opy_:
      bstack1llll111ll_opy_ = {
          bstack11ll11l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ૛"): bstack11ll11l_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ૜"),
          bstack11ll11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ૝"): {
              bstack11ll11l_opy_ (u"ࠪࡨࡦࡺࡡࠨ૞"): bstack11l11lll_opy_ + bstack11ll11l_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭૟"),
              bstack11ll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫૠ"): bstack11ll11l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫૡ")
          }
      }
      if bstack1lll11llll_opy_.status == bstack11ll11l_opy_ (u"ࠧࡑࡃࡖࡗࠬૢ"):
          bstack1111lll1_opy_ = bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ૣ").format(json.dumps(bstack1llll111ll_opy_))
          driver.execute_script(bstack1111lll1_opy_)
          bstack1llll1l1l_opy_(driver, bstack11ll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ૤"))
      elif bstack1lll11llll_opy_.status == bstack11ll11l_opy_ (u"ࠪࡊࡆࡏࡌࠨ૥"):
          reason = bstack11ll11l_opy_ (u"ࠦࠧ૦")
          bstack111111ll_opy_ = bstack11l11lll_opy_ + bstack11ll11l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭૧")
          if bstack1lll11llll_opy_.message:
              reason = str(bstack1lll11llll_opy_.message)
              bstack111111ll_opy_ = bstack111111ll_opy_ + bstack11ll11l_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭૨") + reason
          bstack1llll111ll_opy_[bstack11ll11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ૩")] = {
              bstack11ll11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ૪"): bstack11ll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ૫"),
              bstack11ll11l_opy_ (u"ࠪࡨࡦࡺࡡࠨ૬"): bstack111111ll_opy_
          }
          bstack1111lll1_opy_ = bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ૭").format(json.dumps(bstack1llll111ll_opy_))
          driver.execute_script(bstack1111lll1_opy_)
          bstack1llll1l1l_opy_(driver, bstack11ll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ૮"), reason)
          bstack11l111l1l_opy_(reason, str(bstack1lll11llll_opy_), str(bstack111l11l1l_opy_), logger)
def bstack11l11ll1l_opy_(driver, test):
  if percy.bstack1ll111l1ll_opy_() == bstack11ll11l_opy_ (u"ࠨࡴࡳࡷࡨࠦ૯") and percy.bstack1111l1ll_opy_() == bstack11ll11l_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ૰"):
      bstack1l11lll1_opy_ = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ૱"), None)
      bstack1llll111_opy_(driver, bstack1l11lll1_opy_, test)
  if bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭૲"), None) and bstack1l111111l1_opy_(
          threading.current_thread(), bstack11ll11l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ૳"), None):
      logger.info(bstack11ll11l_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠣࠦ૴"))
      bstack11llll1111_opy_.bstack1l1ll1ll_opy_(driver, name=test.name, path=test.source)
def bstack1llll11l_opy_(test, bstack11l11lll_opy_):
    try:
      data = {}
      if test:
        data[bstack11ll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ૵")] = bstack11l11lll_opy_
      if bstack1lll11llll_opy_:
        if bstack1lll11llll_opy_.status == bstack11ll11l_opy_ (u"࠭ࡐࡂࡕࡖࠫ૶"):
          data[bstack11ll11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ૷")] = bstack11ll11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ૸")
        elif bstack1lll11llll_opy_.status == bstack11ll11l_opy_ (u"ࠩࡉࡅࡎࡒࠧૹ"):
          data[bstack11ll11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪૺ")] = bstack11ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫૻ")
          if bstack1lll11llll_opy_.message:
            data[bstack11ll11l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬૼ")] = str(bstack1lll11llll_opy_.message)
      user = CONFIG[bstack11ll11l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ૽")]
      key = CONFIG[bstack11ll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ૾")]
      url = bstack11ll11l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳ࠭૿").format(user, key, bstack1111l11ll_opy_)
      headers = {
        bstack11ll11l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ଀"): bstack11ll11l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ଁ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1llllll1ll_opy_.format(str(e)))
def bstack1lll1l1ll1_opy_(test, bstack11l11lll_opy_):
  global CONFIG
  global bstack1l11l1l1_opy_
  global bstack11lll1111_opy_
  global bstack1111l11ll_opy_
  global bstack1lll11llll_opy_
  global bstack11ll1ll1l_opy_
  global bstack1l1111l1ll_opy_
  global bstack1l1l1ll11_opy_
  global bstack1l111lll1l_opy_
  global bstack1llllll11_opy_
  global bstack1ll1llll1_opy_
  global bstack1lll1ll1ll_opy_
  try:
    if not bstack1111l11ll_opy_:
      with open(os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"ࠫࢃ࠭ଂ")), bstack11ll11l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଃ"), bstack11ll11l_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ଄"))) as f:
        bstack11lll1llll_opy_ = json.loads(bstack11ll11l_opy_ (u"ࠢࡼࠤଅ") + f.read().strip() + bstack11ll11l_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪଆ") + bstack11ll11l_opy_ (u"ࠤࢀࠦଇ"))
        bstack1111l11ll_opy_ = bstack11lll1llll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll1llll1_opy_:
    for driver in bstack1ll1llll1_opy_:
      if bstack1111l11ll_opy_ == driver.session_id:
        if test:
          bstack11l11ll1l_opy_(driver, test)
        bstack1l111l1l1_opy_(driver, bstack11l11lll_opy_)
  elif bstack1111l11ll_opy_:
    bstack1llll11l_opy_(test, bstack11l11lll_opy_)
  if bstack1l11l1l1_opy_:
    bstack1l1l1ll11_opy_(bstack1l11l1l1_opy_)
  if bstack11lll1111_opy_:
    bstack1l111lll1l_opy_(bstack11lll1111_opy_)
  if bstack1ll11ll1ll_opy_:
    bstack1llllll11_opy_()
def bstack11111111_opy_(self, test, *args, **kwargs):
  bstack11l11lll_opy_ = None
  if test:
    bstack11l11lll_opy_ = str(test.name)
  bstack1lll1l1ll1_opy_(test, bstack11l11lll_opy_)
  bstack1l1111l1ll_opy_(self, test, *args, **kwargs)
def bstack1l111ll111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll1l1ll1_opy_
  global CONFIG
  global bstack1ll1llll1_opy_
  global bstack1111l11ll_opy_
  bstack11l1lll1_opy_ = None
  try:
    if bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩଈ"), None):
      try:
        if not bstack1111l11ll_opy_:
          with open(os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"ࠫࢃ࠭ଉ")), bstack11ll11l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଊ"), bstack11ll11l_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨଋ"))) as f:
            bstack11lll1llll_opy_ = json.loads(bstack11ll11l_opy_ (u"ࠢࡼࠤଌ") + f.read().strip() + bstack11ll11l_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ଍") + bstack11ll11l_opy_ (u"ࠤࢀࠦ଎"))
            bstack1111l11ll_opy_ = bstack11lll1llll_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1ll1llll1_opy_:
        for driver in bstack1ll1llll1_opy_:
          if bstack1111l11ll_opy_ == driver.session_id:
            bstack11l1lll1_opy_ = driver
    bstack1ll1l11l11_opy_ = bstack11llll1111_opy_.bstack1ll1l1l111_opy_(test.tags)
    if bstack11l1lll1_opy_:
      threading.current_thread().isA11yTest = bstack11llll1111_opy_.bstack1l1l1l11ll_opy_(bstack11l1lll1_opy_, bstack1ll1l11l11_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll1l11l11_opy_
  except:
    pass
  bstack1ll1l1ll1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1lll11llll_opy_
  bstack1lll11llll_opy_ = self._test
def bstack1l11ll1ll_opy_():
  global bstack111l11l11_opy_
  try:
    if os.path.exists(bstack111l11l11_opy_):
      os.remove(bstack111l11l11_opy_)
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ଏ") + str(e))
def bstack1ll1l1ll_opy_():
  global bstack111l11l11_opy_
  bstack111ll1l1_opy_ = {}
  try:
    if not os.path.isfile(bstack111l11l11_opy_):
      with open(bstack111l11l11_opy_, bstack11ll11l_opy_ (u"ࠫࡼ࠭ଐ")):
        pass
      with open(bstack111l11l11_opy_, bstack11ll11l_opy_ (u"ࠧࡽࠫࠣ଑")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack111l11l11_opy_):
      bstack111ll1l1_opy_ = json.load(open(bstack111l11l11_opy_, bstack11ll11l_opy_ (u"࠭ࡲࡣࠩ଒")))
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩଓ") + str(e))
  finally:
    return bstack111ll1l1_opy_
def bstack11l1l11l_opy_(platform_index, item_index):
  global bstack111l11l11_opy_
  try:
    bstack111ll1l1_opy_ = bstack1ll1l1ll_opy_()
    bstack111ll1l1_opy_[item_index] = platform_index
    with open(bstack111l11l11_opy_, bstack11ll11l_opy_ (u"ࠣࡹ࠮ࠦଔ")) as outfile:
      json.dump(bstack111ll1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧକ") + str(e))
def bstack1l11l1lll1_opy_(bstack1l1111l1l_opy_):
  global CONFIG
  bstack1ll11lll1l_opy_ = bstack11ll11l_opy_ (u"ࠪࠫଖ")
  if not bstack11ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଗ") in CONFIG:
    logger.info(bstack11ll11l_opy_ (u"ࠬࡔ࡯ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠤࡵࡧࡳࡴࡧࡧࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡵࡩࡵࡵࡲࡵࠢࡩࡳࡷࠦࡒࡰࡤࡲࡸࠥࡸࡵ࡯ࠩଘ"))
  try:
    platform = CONFIG[bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଙ")][bstack1l1111l1l_opy_]
    if bstack11ll11l_opy_ (u"ࠧࡰࡵࠪଚ") in platform:
      bstack1ll11lll1l_opy_ += str(platform[bstack11ll11l_opy_ (u"ࠨࡱࡶࠫଛ")]) + bstack11ll11l_opy_ (u"ࠩ࠯ࠤࠬଜ")
    if bstack11ll11l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଝ") in platform:
      bstack1ll11lll1l_opy_ += str(platform[bstack11ll11l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧଞ")]) + bstack11ll11l_opy_ (u"ࠬ࠲ࠠࠨଟ")
    if bstack11ll11l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪଠ") in platform:
      bstack1ll11lll1l_opy_ += str(platform[bstack11ll11l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫଡ")]) + bstack11ll11l_opy_ (u"ࠨ࠮ࠣࠫଢ")
    if bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫଣ") in platform:
      bstack1ll11lll1l_opy_ += str(platform[bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬତ")]) + bstack11ll11l_opy_ (u"ࠫ࠱ࠦࠧଥ")
    if bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଦ") in platform:
      bstack1ll11lll1l_opy_ += str(platform[bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଧ")]) + bstack11ll11l_opy_ (u"ࠧ࠭ࠢࠪନ")
    if bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ଩") in platform:
      bstack1ll11lll1l_opy_ += str(platform[bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪପ")]) + bstack11ll11l_opy_ (u"ࠪ࠰ࠥ࠭ଫ")
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠫࡘࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡹࡸࡩ࡯ࡩࠣࡪࡴࡸࠠࡳࡧࡳࡳࡷࡺࠠࡨࡧࡱࡩࡷࡧࡴࡪࡱࡱࠫବ") + str(e))
  finally:
    if bstack1ll11lll1l_opy_[len(bstack1ll11lll1l_opy_) - 2:] == bstack11ll11l_opy_ (u"ࠬ࠲ࠠࠨଭ"):
      bstack1ll11lll1l_opy_ = bstack1ll11lll1l_opy_[:-2]
    return bstack1ll11lll1l_opy_
def bstack1l11l1111_opy_(path, bstack1ll11lll1l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l11llll1_opy_ = ET.parse(path)
    bstack1lll111111_opy_ = bstack1l11llll1_opy_.getroot()
    bstack1l1l11111l_opy_ = None
    for suite in bstack1lll111111_opy_.iter(bstack11ll11l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬମ")):
      if bstack11ll11l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧଯ") in suite.attrib:
        suite.attrib[bstack11ll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ର")] += bstack11ll11l_opy_ (u"ࠩࠣࠫ଱") + bstack1ll11lll1l_opy_
        bstack1l1l11111l_opy_ = suite
    bstack11lll11l_opy_ = None
    for robot in bstack1lll111111_opy_.iter(bstack11ll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଲ")):
      bstack11lll11l_opy_ = robot
    bstack1lll11l111_opy_ = len(bstack11lll11l_opy_.findall(bstack11ll11l_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪଳ")))
    if bstack1lll11l111_opy_ == 1:
      bstack11lll11l_opy_.remove(bstack11lll11l_opy_.findall(bstack11ll11l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ଴"))[0])
      bstack1llllll1l1_opy_ = ET.Element(bstack11ll11l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬଵ"), attrib={bstack11ll11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬଶ"): bstack11ll11l_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࡳࠨଷ"), bstack11ll11l_opy_ (u"ࠩ࡬ࡨࠬସ"): bstack11ll11l_opy_ (u"ࠪࡷ࠵࠭ହ")})
      bstack11lll11l_opy_.insert(1, bstack1llllll1l1_opy_)
      bstack1l1l11111_opy_ = None
      for suite in bstack11lll11l_opy_.iter(bstack11ll11l_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ଺")):
        bstack1l1l11111_opy_ = suite
      bstack1l1l11111_opy_.append(bstack1l1l11111l_opy_)
      bstack1ll1l1l11_opy_ = None
      for status in bstack1l1l11111l_opy_.iter(bstack11ll11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ଻")):
        bstack1ll1l1l11_opy_ = status
      bstack1l1l11111_opy_.append(bstack1ll1l1l11_opy_)
    bstack1l11llll1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷ଼ࠫ") + str(e))
def bstack1ll111l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l111l1l11_opy_
  global CONFIG
  if bstack11ll11l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦଽ") in options:
    del options[bstack11ll11l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧା")]
  bstack11l11l1l_opy_ = bstack1ll1l1ll_opy_()
  for bstack1l1l1lll11_opy_ in bstack11l11l1l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11ll11l_opy_ (u"ࠩࡳࡥࡧࡵࡴࡠࡴࡨࡷࡺࡲࡴࡴࠩି"), str(bstack1l1l1lll11_opy_), bstack11ll11l_opy_ (u"ࠪࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠧୀ"))
    bstack1l11l1111_opy_(path, bstack1l11l1lll1_opy_(bstack11l11l1l_opy_[bstack1l1l1lll11_opy_]))
  bstack1l11ll1ll_opy_()
  return bstack1l111l1l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll11l1ll_opy_(self, ff_profile_dir):
  global bstack1111llll_opy_
  if not ff_profile_dir:
    return None
  return bstack1111llll_opy_(self, ff_profile_dir)
def bstack1l1llllll1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1lll1l11l1_opy_
  bstack1ll1llll11_opy_ = []
  if bstack11ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୁ") in CONFIG:
    bstack1ll1llll11_opy_ = CONFIG[bstack11ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨୂ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11ll11l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢୃ")],
      pabot_args[bstack11ll11l_opy_ (u"ࠢࡷࡧࡵࡦࡴࡹࡥࠣୄ")],
      argfile,
      pabot_args.get(bstack11ll11l_opy_ (u"ࠣࡪ࡬ࡺࡪࠨ୅")),
      pabot_args[bstack11ll11l_opy_ (u"ࠤࡳࡶࡴࡩࡥࡴࡵࡨࡷࠧ୆")],
      platform[0],
      bstack1lll1l11l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11ll11l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࡫࡯࡬ࡦࡵࠥେ")] or [(bstack11ll11l_opy_ (u"ࠦࠧୈ"), None)]
    for platform in enumerate(bstack1ll1llll11_opy_)
  ]
def bstack11llllllll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l11111111_opy_=bstack11ll11l_opy_ (u"ࠬ࠭୉")):
  global bstack11l1l111_opy_
  self.platform_index = platform_index
  self.bstack1ll1lll111_opy_ = bstack1l11111111_opy_
  bstack11l1l111_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1lll1111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1111l11l_opy_
  global bstack1ll1l11l_opy_
  bstack1l111l11l1_opy_ = copy.deepcopy(item)
  if not bstack11ll11l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ୊") in item.options:
    bstack1l111l11l1_opy_.options[bstack11ll11l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩୋ")] = []
  bstack1l1111111_opy_ = bstack1l111l11l1_opy_.options[bstack11ll11l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪୌ")].copy()
  for v in bstack1l111l11l1_opy_.options[bstack11ll11l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨ୍ࠫ")]:
    if bstack11ll11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩ୎") in v:
      bstack1l1111111_opy_.remove(v)
    if bstack11ll11l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫ୏") in v:
      bstack1l1111111_opy_.remove(v)
    if bstack11ll11l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ୐") in v:
      bstack1l1111111_opy_.remove(v)
  bstack1l1111111_opy_.insert(0, bstack11ll11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜࠿ࢁࡽࠨ୑").format(bstack1l111l11l1_opy_.platform_index))
  bstack1l1111111_opy_.insert(0, bstack11ll11l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࠾ࢀࢃࠧ୒").format(bstack1l111l11l1_opy_.bstack1ll1lll111_opy_))
  bstack1l111l11l1_opy_.options[bstack11ll11l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ୓")] = bstack1l1111111_opy_
  if bstack1ll1l11l_opy_:
    bstack1l111l11l1_opy_.options[bstack11ll11l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ୔")].insert(0, bstack11ll11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕ࠽ࡿࢂ࠭୕").format(bstack1ll1l11l_opy_))
  return bstack1l1111l11l_opy_(caller_id, datasources, is_last, bstack1l111l11l1_opy_, outs_dir)
def bstack1l1111l1l1_opy_(command, item_index):
  if bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬୖ")):
    os.environ[bstack11ll11l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ୗ")] = json.dumps(CONFIG[bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୘")][item_index % bstack1lllll1l11_opy_])
  global bstack1ll1l11l_opy_
  if bstack1ll1l11l_opy_:
    command[0] = command[0].replace(bstack11ll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭୙"), bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ୚") + str(
      item_index) + bstack11ll11l_opy_ (u"ࠩࠣࠫ୛") + bstack1ll1l11l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11ll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଡ଼"),
                                    bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨଢ଼") + str(item_index), 1)
def bstack111llll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11111lll_opy_
  bstack1l1111l1l1_opy_(command, item_index)
  return bstack11111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11111lll_opy_
  bstack1l1111l1l1_opy_(command, item_index)
  return bstack11111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l11lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11111lll_opy_
  bstack1l1111l1l1_opy_(command, item_index)
  return bstack11111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1llll1ll_opy_(self, runner, quiet=False, capture=True):
  global bstack11111ll11_opy_
  bstack1ll1ll11l1_opy_ = bstack11111ll11_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11ll11l_opy_ (u"ࠬ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡠࡣࡵࡶࠬ୞")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11ll11l_opy_ (u"࠭ࡥࡹࡥࡢࡸࡷࡧࡣࡦࡤࡤࡧࡰࡥࡡࡳࡴࠪୟ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1ll11l1_opy_
def bstack1lll1ll1_opy_(runner, hook_name, context, element, bstack11lllll1ll_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1llllllll_opy_.bstack11lll1ll11_opy_(hook_name, element)
    bstack11lllll1ll_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1llllllll_opy_.bstack1ll11lll_opy_(element)
      if hook_name not in [bstack11ll11l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫୠ"), bstack11ll11l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫୡ")] and args and hasattr(args[0], bstack11ll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦࠩୢ")):
        args[0].error_message = bstack11ll11l_opy_ (u"ࠪࠫୣ")
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡩࡣࡱࡨࡱ࡫ࠠࡩࡱࡲ࡯ࡸࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭୤").format(str(e)))
def bstack1ll1l111ll_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    if runner.hooks.get(bstack11ll11l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ୥")).__name__ != bstack11ll11l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤ୦"):
      bstack1lll1ll1_opy_(runner, name, context, runner, bstack11lllll1ll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1ll111ll1_opy_(bstack11ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭୧")) else context.browser
      runner.driver_initialised = bstack11ll11l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ୨")
    except Exception as e:
      logger.debug(bstack11ll11l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭୩").format(str(e)))
def bstack11l1lll1l_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    bstack1lll1ll1_opy_(runner, name, context, context.feature, bstack11lllll1ll_opy_, *args)
    try:
      if not bstack11llllll11_opy_:
        bstack11l1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll111ll1_opy_(bstack11ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ୪")) else context.browser
        if is_driver_active(bstack11l1lll1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11ll11l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ୫")
          bstack1l1lllll1_opy_ = str(runner.feature.name)
          bstack1l11ll11_opy_(context, bstack1l1lllll1_opy_)
          bstack11l1lll1_opy_.execute_script(bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ୬") + json.dumps(bstack1l1lllll1_opy_) + bstack11ll11l_opy_ (u"࠭ࡽࡾࠩ୭"))
    except Exception as e:
      logger.debug(bstack11ll11l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ୮").format(str(e)))
def bstack1l1lll1ll1_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    if hasattr(context, bstack11ll11l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪ୯")):
        bstack1llllllll_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack11ll11l_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ୰")) else context.feature
    bstack1lll1ll1_opy_(runner, name, context, target, bstack11lllll1ll_opy_, *args)
def bstack1l1l1ll1_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1llllllll_opy_.start_test(context)
    bstack1lll1ll1_opy_(runner, name, context, context.scenario, bstack11lllll1ll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1ll11l1l1l_opy_.bstack1l111l1lll_opy_(context, *args)
    try:
      bstack11l1lll1_opy_ = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩୱ"), context.browser)
      if is_driver_active(bstack11l1lll1_opy_):
        bstack1ll11l11l1_opy_.bstack1l1l1ll11l_opy_(bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ୲"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11ll11l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ୳")
        if (not bstack11llllll11_opy_):
          scenario_name = args[0].name
          feature_name = bstack1l1lllll1_opy_ = str(runner.feature.name)
          bstack1l1lllll1_opy_ = feature_name + bstack11ll11l_opy_ (u"࠭ࠠ࠮ࠢࠪ୴") + scenario_name
          if runner.driver_initialised == bstack11ll11l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ୵"):
            bstack1l11ll11_opy_(context, bstack1l1lllll1_opy_)
            bstack11l1lll1_opy_.execute_script(bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭୶") + json.dumps(bstack1l1lllll1_opy_) + bstack11ll11l_opy_ (u"ࠩࢀࢁࠬ୷"))
    except Exception as e:
      logger.debug(bstack11ll11l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ୸").format(str(e)))
def bstack111111l1_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    bstack1lll1ll1_opy_(runner, name, context, args[0], bstack11lllll1ll_opy_, *args)
    try:
      bstack11l1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll111ll1_opy_(bstack11ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ୹")) else context.browser
      if is_driver_active(bstack11l1lll1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11ll11l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ୺")
        bstack1llllllll_opy_.bstack1111l111l_opy_(args[0])
        if runner.driver_initialised == bstack11ll11l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ୻"):
          feature_name = bstack1l1lllll1_opy_ = str(runner.feature.name)
          bstack1l1lllll1_opy_ = feature_name + bstack11ll11l_opy_ (u"ࠧࠡ࠯ࠣࠫ୼") + context.scenario.name
          bstack11l1lll1_opy_.execute_script(bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭୽") + json.dumps(bstack1l1lllll1_opy_) + bstack11ll11l_opy_ (u"ࠩࢀࢁࠬ୾"))
    except Exception as e:
      logger.debug(bstack11ll11l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧ୿").format(str(e)))
def bstack1l1l1l1l1_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
  bstack1llllllll_opy_.bstack1l1l1l111_opy_(args[0])
  try:
    bstack11ll111l_opy_ = args[0].status.name
    bstack11l1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ஀") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11l1lll1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11ll11l_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ஁")
        feature_name = bstack1l1lllll1_opy_ = str(runner.feature.name)
        bstack1l1lllll1_opy_ = feature_name + bstack11ll11l_opy_ (u"࠭ࠠ࠮ࠢࠪஂ") + context.scenario.name
        bstack11l1lll1_opy_.execute_script(bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬஃ") + json.dumps(bstack1l1lllll1_opy_) + bstack11ll11l_opy_ (u"ࠨࡿࢀࠫ஄"))
    if str(bstack11ll111l_opy_).lower() == bstack11ll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩஅ"):
      bstack1llll111l_opy_ = bstack11ll11l_opy_ (u"ࠪࠫஆ")
      bstack111ll11ll_opy_ = bstack11ll11l_opy_ (u"ࠫࠬஇ")
      bstack1l1l111lll_opy_ = bstack11ll11l_opy_ (u"ࠬ࠭ஈ")
      try:
        import traceback
        bstack1llll111l_opy_ = runner.exception.__class__.__name__
        bstack1l11lllll1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111ll11ll_opy_ = bstack11ll11l_opy_ (u"࠭ࠠࠨஉ").join(bstack1l11lllll1_opy_)
        bstack1l1l111lll_opy_ = bstack1l11lllll1_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1l1l11l_opy_.format(str(e)))
      bstack1llll111l_opy_ += bstack1l1l111lll_opy_
      bstack11lllll1l_opy_(context, json.dumps(str(args[0].name) + bstack11ll11l_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨஊ") + str(bstack111ll11ll_opy_)),
                          bstack11ll11l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ஋"))
      if runner.driver_initialised == bstack11ll11l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ஌"):
        bstack1ll11l1l_opy_(getattr(context, bstack11ll11l_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ஍"), None), bstack11ll11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦஎ"), bstack1llll111l_opy_)
        bstack11l1lll1_opy_.execute_script(bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪஏ") + json.dumps(str(args[0].name) + bstack11ll11l_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧஐ") + str(bstack111ll11ll_opy_)) + bstack11ll11l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧ஑"))
      if runner.driver_initialised == bstack11ll11l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨஒ"):
        bstack1llll1l1l_opy_(bstack11l1lll1_opy_, bstack11ll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩஓ"), bstack11ll11l_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢஔ") + str(bstack1llll111l_opy_))
    else:
      bstack11lllll1l_opy_(context, bstack11ll11l_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧக"), bstack11ll11l_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ஖"))
      if runner.driver_initialised == bstack11ll11l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ஗"):
        bstack1ll11l1l_opy_(getattr(context, bstack11ll11l_opy_ (u"ࠧࡱࡣࡪࡩࠬ஘"), None), bstack11ll11l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣங"))
      bstack11l1lll1_opy_.execute_script(bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧச") + json.dumps(str(args[0].name) + bstack11ll11l_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢ஛")) + bstack11ll11l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪஜ"))
      if runner.driver_initialised == bstack11ll11l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ஝"):
        bstack1llll1l1l_opy_(bstack11l1lll1_opy_, bstack11ll11l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨஞ"))
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ட").format(str(e)))
  bstack1lll1ll1_opy_(runner, name, context, args[0], bstack11lllll1ll_opy_, *args)
def bstack1ll11l1l11_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
  bstack1llllllll_opy_.end_test(args[0])
  try:
    bstack1ll11111_opy_ = args[0].status.name
    bstack11l1lll1_opy_ = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ஠"), context.browser)
    bstack1ll11l1l1l_opy_.bstack11l1ll11_opy_(bstack11l1lll1_opy_)
    if str(bstack1ll11111_opy_).lower() == bstack11ll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ஡"):
      bstack1llll111l_opy_ = bstack11ll11l_opy_ (u"ࠪࠫ஢")
      bstack111ll11ll_opy_ = bstack11ll11l_opy_ (u"ࠫࠬண")
      bstack1l1l111lll_opy_ = bstack11ll11l_opy_ (u"ࠬ࠭த")
      try:
        import traceback
        bstack1llll111l_opy_ = runner.exception.__class__.__name__
        bstack1l11lllll1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111ll11ll_opy_ = bstack11ll11l_opy_ (u"࠭ࠠࠨ஥").join(bstack1l11lllll1_opy_)
        bstack1l1l111lll_opy_ = bstack1l11lllll1_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1l1l11l_opy_.format(str(e)))
      bstack1llll111l_opy_ += bstack1l1l111lll_opy_
      bstack11lllll1l_opy_(context, json.dumps(str(args[0].name) + bstack11ll11l_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ஦") + str(bstack111ll11ll_opy_)),
                          bstack11ll11l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ஧"))
      if runner.driver_initialised == bstack11ll11l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦந") or runner.driver_initialised == bstack11ll11l_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪன"):
        bstack1ll11l1l_opy_(getattr(context, bstack11ll11l_opy_ (u"ࠫࡵࡧࡧࡦࠩப"), None), bstack11ll11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ஫"), bstack1llll111l_opy_)
        bstack11l1lll1_opy_.execute_script(bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ஬") + json.dumps(str(args[0].name) + bstack11ll11l_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ஭") + str(bstack111ll11ll_opy_)) + bstack11ll11l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨம"))
      if runner.driver_initialised == bstack11ll11l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦய") or runner.driver_initialised == bstack11ll11l_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪர"):
        bstack1llll1l1l_opy_(bstack11l1lll1_opy_, bstack11ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫற"), bstack11ll11l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤல") + str(bstack1llll111l_opy_))
    else:
      bstack11lllll1l_opy_(context, bstack11ll11l_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢள"), bstack11ll11l_opy_ (u"ࠢࡪࡰࡩࡳࠧழ"))
      if runner.driver_initialised == bstack11ll11l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥவ") or runner.driver_initialised == bstack11ll11l_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩஶ"):
        bstack1ll11l1l_opy_(getattr(context, bstack11ll11l_opy_ (u"ࠪࡴࡦ࡭ࡥࠨஷ"), None), bstack11ll11l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦஸ"))
      bstack11l1lll1_opy_.execute_script(bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪஹ") + json.dumps(str(args[0].name) + bstack11ll11l_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥ஺")) + bstack11ll11l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭஻"))
      if runner.driver_initialised == bstack11ll11l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ஼") or runner.driver_initialised == bstack11ll11l_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ஽"):
        bstack1llll1l1l_opy_(bstack11l1lll1_opy_, bstack11ll11l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥா"))
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ி").format(str(e)))
  bstack1lll1ll1_opy_(runner, name, context, context.scenario, bstack11lllll1ll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack11lll11ll_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    target = context.scenario if hasattr(context, bstack11ll11l_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧீ")) else context.feature
    bstack1lll1ll1_opy_(runner, name, context, target, bstack11lllll1ll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1lll1l11_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    try:
      bstack11l1lll1_opy_ = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬு"), context.browser)
      if context.failed is True:
        bstack1111ll11l_opy_ = []
        bstack1l11l111ll_opy_ = []
        bstack11lll1lll1_opy_ = []
        bstack1l1ll1l1_opy_ = bstack11ll11l_opy_ (u"ࠧࠨூ")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1111ll11l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l11lllll1_opy_ = traceback.format_tb(exc_tb)
            bstack1l11l11ll1_opy_ = bstack11ll11l_opy_ (u"ࠨࠢࠪ௃").join(bstack1l11lllll1_opy_)
            bstack1l11l111ll_opy_.append(bstack1l11l11ll1_opy_)
            bstack11lll1lll1_opy_.append(bstack1l11lllll1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1l1l11l_opy_.format(str(e)))
        bstack1llll111l_opy_ = bstack11ll11l_opy_ (u"ࠩࠪ௄")
        for i in range(len(bstack1111ll11l_opy_)):
          bstack1llll111l_opy_ += bstack1111ll11l_opy_[i] + bstack11lll1lll1_opy_[i] + bstack11ll11l_opy_ (u"ࠪࡠࡳ࠭௅")
        bstack1l1ll1l1_opy_ = bstack11ll11l_opy_ (u"ࠫࠥ࠭ெ").join(bstack1l11l111ll_opy_)
        if runner.driver_initialised in [bstack11ll11l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨே"), bstack11ll11l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥை")]:
          bstack11lllll1l_opy_(context, bstack1l1ll1l1_opy_, bstack11ll11l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ௉"))
          bstack1ll11l1l_opy_(getattr(context, bstack11ll11l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ொ"), None), bstack11ll11l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤோ"), bstack1llll111l_opy_)
          bstack11l1lll1_opy_.execute_script(bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨௌ") + json.dumps(bstack1l1ll1l1_opy_) + bstack11ll11l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀ்ࠫ"))
          bstack1llll1l1l_opy_(bstack11l1lll1_opy_, bstack11ll11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ௎"), bstack11ll11l_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦ௏") + str(bstack1llll111l_opy_))
          bstack1lll111lll_opy_ = bstack11lll1ll_opy_(bstack1l1ll1l1_opy_, runner.feature.name, logger)
          if (bstack1lll111lll_opy_ != None):
            bstack1l1l1l11_opy_.append(bstack1lll111lll_opy_)
      else:
        if runner.driver_initialised in [bstack11ll11l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣௐ"), bstack11ll11l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ௑")]:
          bstack11lllll1l_opy_(context, bstack11ll11l_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧ௒") + str(runner.feature.name) + bstack11ll11l_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧ௓"), bstack11ll11l_opy_ (u"ࠦ࡮ࡴࡦࡰࠤ௔"))
          bstack1ll11l1l_opy_(getattr(context, bstack11ll11l_opy_ (u"ࠬࡶࡡࡨࡧࠪ௕"), None), bstack11ll11l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ௖"))
          bstack11l1lll1_opy_.execute_script(bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬௗ") + json.dumps(bstack11ll11l_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦ௘") + str(runner.feature.name) + bstack11ll11l_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦ௙")) + bstack11ll11l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩ௚"))
          bstack1llll1l1l_opy_(bstack11l1lll1_opy_, bstack11ll11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ௛"))
          bstack1lll111lll_opy_ = bstack11lll1ll_opy_(bstack1l1ll1l1_opy_, runner.feature.name, logger)
          if (bstack1lll111lll_opy_ != None):
            bstack1l1l1l11_opy_.append(bstack1lll111lll_opy_)
    except Exception as e:
      logger.debug(bstack11ll11l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ௜").format(str(e)))
    bstack1lll1ll1_opy_(runner, name, context, context.feature, bstack11lllll1ll_opy_, *args)
def bstack11ll11111_opy_(runner, name, context, bstack11lllll1ll_opy_, *args):
    bstack1lll1ll1_opy_(runner, name, context, runner, bstack11lllll1ll_opy_, *args)
def bstack1ll11l1lll_opy_(self, name, context, *args):
  if bstack1l1l111l_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1lllll1l11_opy_
    bstack111l1l11l_opy_ = CONFIG[bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௝")][platform_index]
    os.environ[bstack11ll11l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ௞")] = json.dumps(bstack111l1l11l_opy_)
  global bstack11lllll1ll_opy_
  if not hasattr(self, bstack11ll11l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡩࡩ࠭௟")):
    self.driver_initialised = None
  bstack1lllllll11_opy_ = {
      bstack11ll11l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭௠"): bstack1ll1l111ll_opy_,
      bstack11ll11l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫ௡"): bstack11l1lll1l_opy_,
      bstack11ll11l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡹࡧࡧࠨ௢"): bstack1l1lll1ll1_opy_,
      bstack11ll11l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ௣"): bstack1l1l1ll1_opy_,
      bstack11ll11l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠫ௤"): bstack111111l1_opy_,
      bstack11ll11l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫ௥"): bstack1l1l1l1l1_opy_,
      bstack11ll11l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ௦"): bstack1ll11l1l11_opy_,
      bstack11ll11l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡶࡤ࡫ࠬ௧"): bstack11lll11ll_opy_,
      bstack11ll11l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪ௨"): bstack1lll1l11_opy_,
      bstack11ll11l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧ௩"): bstack11ll11111_opy_
  }
  handler = bstack1lllllll11_opy_.get(name, bstack11lllll1ll_opy_)
  handler(self, name, context, bstack11lllll1ll_opy_, *args)
  if name in [bstack11ll11l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ௪"), bstack11ll11l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ௫"), bstack11ll11l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ௬")]:
    try:
      bstack11l1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll111ll1_opy_(bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ௭")) else context.browser
      bstack1l11l11111_opy_ = (
        (name == bstack11ll11l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ௮") and self.driver_initialised == bstack11ll11l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ௯")) or
        (name == bstack11ll11l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫ௰") and self.driver_initialised == bstack11ll11l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ௱")) or
        (name == bstack11ll11l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ௲") and self.driver_initialised in [bstack11ll11l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ௳"), bstack11ll11l_opy_ (u"ࠣ࡫ࡱࡷࡹ࡫ࡰࠣ௴")]) or
        (name == bstack11ll11l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭௵") and self.driver_initialised == bstack11ll11l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௶"))
      )
      if bstack1l11l11111_opy_:
        self.driver_initialised = None
        bstack11l1lll1_opy_.quit()
    except Exception:
      pass
def bstack11l1111ll_opy_(config, startdir):
  return bstack11ll11l_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤ௷").format(bstack11ll11l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ௸"))
notset = Notset()
def bstack11l1ll1l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11llll1l11_opy_
  if str(name).lower() == bstack11ll11l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭௹"):
    return bstack11ll11l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ௺")
  else:
    return bstack11llll1l11_opy_(self, name, default, skip)
def bstack111lll111_opy_(item, when):
  global bstack1l111l11ll_opy_
  try:
    bstack1l111l11ll_opy_(item, when)
  except Exception as e:
    pass
def bstack11lll11l11_opy_():
  return
def bstack111l1ll11_opy_(type, name, status, reason, bstack1l1l1ll111_opy_, bstack11111l1ll_opy_):
  bstack1l1l11ll11_opy_ = {
    bstack11ll11l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ௻"): type,
    bstack11ll11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ௼"): {}
  }
  if type == bstack11ll11l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ௽"):
    bstack1l1l11ll11_opy_[bstack11ll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ௾")][bstack11ll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ௿")] = bstack1l1l1ll111_opy_
    bstack1l1l11ll11_opy_[bstack11ll11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩఀ")][bstack11ll11l_opy_ (u"ࠧࡥࡣࡷࡥࠬఁ")] = json.dumps(str(bstack11111l1ll_opy_))
  if type == bstack11ll11l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩం"):
    bstack1l1l11ll11_opy_[bstack11ll11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬః")][bstack11ll11l_opy_ (u"ࠪࡲࡦࡳࡥࠨఄ")] = name
  if type == bstack11ll11l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧఅ"):
    bstack1l1l11ll11_opy_[bstack11ll11l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨఆ")][bstack11ll11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ఇ")] = status
    if status == bstack11ll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧఈ"):
      bstack1l1l11ll11_opy_[bstack11ll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫఉ")][bstack11ll11l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩఊ")] = json.dumps(str(reason))
  bstack11l1ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨఋ").format(json.dumps(bstack1l1l11ll11_opy_))
  return bstack11l1ll1ll_opy_
def bstack1lllll11l_opy_(driver_command, response):
    if driver_command == bstack11ll11l_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨఌ"):
        bstack1ll11l11l1_opy_.bstack1lllll1l1l_opy_({
            bstack11ll11l_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ఍"): response[bstack11ll11l_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬఎ")],
            bstack11ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧఏ"): bstack1ll11l11l1_opy_.current_test_uuid()
        })
def bstack1l1l1ll1l_opy_(item, call, rep):
  global bstack1lllll1ll1_opy_
  global bstack1ll1llll1_opy_
  global bstack11llllll11_opy_
  name = bstack11ll11l_opy_ (u"ࠨࠩఐ")
  try:
    if rep.when == bstack11ll11l_opy_ (u"ࠩࡦࡥࡱࡲࠧ఑"):
      bstack1111l11ll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11llllll11_opy_:
          name = str(rep.nodeid)
          bstack1l11111ll_opy_ = bstack111l1ll11_opy_(bstack11ll11l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫఒ"), name, bstack11ll11l_opy_ (u"ࠫࠬఓ"), bstack11ll11l_opy_ (u"ࠬ࠭ఔ"), bstack11ll11l_opy_ (u"࠭ࠧక"), bstack11ll11l_opy_ (u"ࠧࠨఖ"))
          threading.current_thread().bstack1l1l11l11_opy_ = name
          for driver in bstack1ll1llll1_opy_:
            if bstack1111l11ll_opy_ == driver.session_id:
              driver.execute_script(bstack1l11111ll_opy_)
      except Exception as e:
        logger.debug(bstack11ll11l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨగ").format(str(e)))
      try:
        bstack1l1llllll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11ll11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪఘ"):
          status = bstack11ll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪఙ") if rep.outcome.lower() == bstack11ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫచ") else bstack11ll11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬఛ")
          reason = bstack11ll11l_opy_ (u"࠭ࠧజ")
          if status == bstack11ll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧఝ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11ll11l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ఞ") if status == bstack11ll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩట") else bstack11ll11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩఠ")
          data = name + bstack11ll11l_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭డ") if status == bstack11ll11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬఢ") else name + bstack11ll11l_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩణ") + reason
          bstack1l1l11lll1_opy_ = bstack111l1ll11_opy_(bstack11ll11l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩత"), bstack11ll11l_opy_ (u"ࠨࠩథ"), bstack11ll11l_opy_ (u"ࠩࠪద"), bstack11ll11l_opy_ (u"ࠪࠫధ"), level, data)
          for driver in bstack1ll1llll1_opy_:
            if bstack1111l11ll_opy_ == driver.session_id:
              driver.execute_script(bstack1l1l11lll1_opy_)
      except Exception as e:
        logger.debug(bstack11ll11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨన").format(str(e)))
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ఩").format(str(e)))
  bstack1lllll1ll1_opy_(item, call, rep)
def bstack1llll111_opy_(driver, bstack1ll1lll1l_opy_, test=None):
  global bstack111l11l1l_opy_
  if test != None:
    bstack11llll1l1l_opy_ = getattr(test, bstack11ll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫప"), None)
    bstack1111l111_opy_ = getattr(test, bstack11ll11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬఫ"), None)
    PercySDK.screenshot(driver, bstack1ll1lll1l_opy_, bstack11llll1l1l_opy_=bstack11llll1l1l_opy_, bstack1111l111_opy_=bstack1111l111_opy_, bstack1l1ll11l1_opy_=bstack111l11l1l_opy_)
  else:
    PercySDK.screenshot(driver, bstack1ll1lll1l_opy_)
def bstack1l11l1llll_opy_(driver):
  if bstack1lll11lll_opy_.bstack11111l111_opy_() is True or bstack1lll11lll_opy_.capturing() is True:
    return
  bstack1lll11lll_opy_.bstack1ll1l1lll1_opy_()
  while not bstack1lll11lll_opy_.bstack11111l111_opy_():
    bstack1l11lll11l_opy_ = bstack1lll11lll_opy_.bstack11lll1l1l_opy_()
    bstack1llll111_opy_(driver, bstack1l11lll11l_opy_)
  bstack1lll11lll_opy_.bstack1lll1l1lll_opy_()
def bstack1ll111llll_opy_(sequence, driver_command, response = None, bstack1ll1lllll_opy_ = None, args = None):
    try:
      if sequence != bstack11ll11l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨబ"):
        return
      if percy.bstack1ll111l1ll_opy_() == bstack11ll11l_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣభ"):
        return
      bstack1l11lll11l_opy_ = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭మ"), None)
      for command in bstack11l11ll11_opy_:
        if command == driver_command:
          for driver in bstack1ll1llll1_opy_:
            bstack1l11l1llll_opy_(driver)
      bstack1l1l111ll1_opy_ = percy.bstack1111l1ll_opy_()
      if driver_command in bstack1ll1111ll1_opy_[bstack1l1l111ll1_opy_]:
        bstack1lll11lll_opy_.bstack1l1lllllll_opy_(bstack1l11lll11l_opy_, driver_command)
    except Exception as e:
      pass
def bstack1ll1l11ll1_opy_(framework_name):
  if bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨయ")):
      return
  bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩర"), True)
  global bstack111ll1ll_opy_
  global bstack11l11l11l_opy_
  global bstack1lll1ll1l1_opy_
  bstack111ll1ll_opy_ = framework_name
  logger.info(bstack11lll11lll_opy_.format(bstack111ll1ll_opy_.split(bstack11ll11l_opy_ (u"࠭࠭ࠨఱ"))[0]))
  bstack1l111ll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1l111l_opy_:
      Service.start = bstack1ll11l111_opy_
      Service.stop = bstack111llll1l_opy_
      webdriver.Remote.get = bstack1l11l1ll1_opy_
      WebDriver.close = bstack1ll1ll1l1l_opy_
      WebDriver.quit = bstack111lll11_opy_
      webdriver.Remote.__init__ = bstack1l1lll111l_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1l1l111l_opy_:
        webdriver.Remote.__init__ = bstack1l1ll1ll11_opy_
    WebDriver.execute = bstack1l1l1ll1ll_opy_
    bstack11l11l11l_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1l111l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l11ll1l11_opy_
  except Exception as e:
    pass
  bstack1l1ll11l11_opy_()
  if not bstack11l11l11l_opy_:
    bstack111111111_opy_(bstack11ll11l_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤల"), bstack1llll1lll_opy_)
  if bstack1lllll11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._1l1ll1l1ll_opy_ = bstack1l1ll11ll_opy_
    except Exception as e:
      logger.error(bstack1l11l1l1ll_opy_.format(str(e)))
  if bstack1ll11l11_opy_():
    bstack11l111111_opy_(CONFIG, logger)
  if (bstack11ll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧళ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1ll111l1ll_opy_() == bstack11ll11l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢఴ"):
          bstack1l1ll1ll1_opy_(bstack1ll111llll_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll11l1ll_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11111l11l_opy_
      except Exception as e:
        logger.warn(bstack11l1l1l11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11ll1lll_opy_
      except Exception as e:
        logger.debug(bstack11llll1l_opy_ + str(e))
    except Exception as e:
      bstack111111111_opy_(e, bstack11l1l1l11_opy_)
    Output.start_test = bstack1ll11ll111_opy_
    Output.end_test = bstack11111111_opy_
    TestStatus.__init__ = bstack1l111ll111_opy_
    QueueItem.__init__ = bstack11llllllll_opy_
    pabot._create_items = bstack1l1llllll1_opy_
    try:
      from pabot import __version__ as bstack11llll11_opy_
      if version.parse(bstack11llll11_opy_) >= version.parse(bstack11ll11l_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪవ")):
        pabot._run = bstack1l11lll1ll_opy_
      elif version.parse(bstack11llll11_opy_) >= version.parse(bstack11ll11l_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫశ")):
        pabot._run = bstack1l1l11ll_opy_
      else:
        pabot._run = bstack111llll11_opy_
    except Exception as e:
      pabot._run = bstack111llll11_opy_
    pabot._create_command_for_execution = bstack1l1lll1111_opy_
    pabot._report_results = bstack1ll111l11_opy_
  if bstack11ll11l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬష") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111111111_opy_(e, bstack1l11l1ll_opy_)
    Runner.run_hook = bstack1ll11l1lll_opy_
    Step.run = bstack1llll1ll_opy_
  if bstack11ll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭స") in str(framework_name).lower():
    if not bstack1l1l111l_opy_:
      return
    try:
      if percy.bstack1ll111l1ll_opy_() == bstack11ll11l_opy_ (u"ࠢࡵࡴࡸࡩࠧహ"):
          bstack1l1ll1ll1_opy_(bstack1ll111llll_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l1111ll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11lll11l11_opy_
      Config.getoption = bstack11l1ll1l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1l1ll1l_opy_
    except Exception as e:
      pass
def bstack11lllll11l_opy_():
  global CONFIG
  if bstack11ll11l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ఺") in CONFIG and int(CONFIG[bstack11ll11l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ఻")]) > 1:
    logger.warn(bstack1111111ll_opy_)
def bstack111l11l1_opy_(arg, bstack11llll111_opy_, bstack1lll11ll11_opy_=None):
  global CONFIG
  global bstack1l11ll1l1l_opy_
  global bstack1l1l11l1l_opy_
  global bstack1l1l111l_opy_
  global bstack1l1111l111_opy_
  bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ఼ࠪ")
  if bstack11llll111_opy_ and isinstance(bstack11llll111_opy_, str):
    bstack11llll111_opy_ = eval(bstack11llll111_opy_)
  CONFIG = bstack11llll111_opy_[bstack11ll11l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫఽ")]
  bstack1l11ll1l1l_opy_ = bstack11llll111_opy_[bstack11ll11l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ా")]
  bstack1l1l11l1l_opy_ = bstack11llll111_opy_[bstack11ll11l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨి")]
  bstack1l1l111l_opy_ = bstack11llll111_opy_[bstack11ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪీ")]
  bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩు"), bstack1l1l111l_opy_)
  os.environ[bstack11ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫూ")] = bstack1111ll1ll_opy_
  os.environ[bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩృ")] = json.dumps(CONFIG)
  os.environ[bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫౄ")] = bstack1l11ll1l1l_opy_
  os.environ[bstack11ll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭౅")] = str(bstack1l1l11l1l_opy_)
  os.environ[bstack11ll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬె")] = str(True)
  if bstack111l1l1ll_opy_(arg, [bstack11ll11l_opy_ (u"ࠧ࠮ࡰࠪే"), bstack11ll11l_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩై")]) != -1:
    os.environ[bstack11ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ౉")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111l1lll1_opy_)
    return
  bstack11l111l11_opy_()
  global bstack111ll111_opy_
  global bstack111l11l1l_opy_
  global bstack1lll1l11l1_opy_
  global bstack1ll1l11l_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack1lll1ll1l1_opy_
  global bstack1l1l1lllll_opy_
  arg.append(bstack11ll11l_opy_ (u"ࠥ࠱࡜ࠨొ"))
  arg.append(bstack11ll11l_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢో"))
  arg.append(bstack11ll11l_opy_ (u"ࠧ࠳ࡗࠣౌ"))
  arg.append(bstack11ll11l_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰ్ࠧ"))
  global bstack11ll1l11l_opy_
  global bstack11l1111l_opy_
  global bstack1l1llll11_opy_
  global bstack1ll1l1ll1_opy_
  global bstack1111llll_opy_
  global bstack11l1l111_opy_
  global bstack1l1111l11l_opy_
  global bstack1l111l1ll_opy_
  global bstack1111l11l1_opy_
  global bstack1ll1ll1l1_opy_
  global bstack11llll1l11_opy_
  global bstack1l111l11ll_opy_
  global bstack1lllll1ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll1l11l_opy_ = webdriver.Remote.__init__
    bstack11l1111l_opy_ = WebDriver.quit
    bstack1l111l1ll_opy_ = WebDriver.close
    bstack1111l11l1_opy_ = WebDriver.get
    bstack1l1llll11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1ll1l1lll_opy_(CONFIG) and bstack1l1lll111_opy_():
    if bstack1ll111l1l1_opy_() < version.parse(bstack11lll1l1_opy_):
      logger.error(bstack11lllll1_opy_.format(bstack1ll111l1l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll1ll1l1_opy_ = RemoteConnection._1l1ll1l1ll_opy_
      except Exception as e:
        logger.error(bstack1l11l1l1ll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack11llll1l11_opy_ = Config.getoption
    from _pytest import runner
    bstack1l111l11ll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11lll11ll1_opy_)
  try:
    from pytest_bdd import reporting
    bstack1lllll1ll1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11ll11l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ౎"))
  bstack1lll1l11l1_opy_ = CONFIG.get(bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ౏"), {}).get(bstack11ll11l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ౐"))
  bstack1l1l1lllll_opy_ = True
  bstack1ll1l11ll1_opy_(bstack1ll1ll1ll1_opy_)
  os.environ[bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ౑")] = CONFIG[bstack11ll11l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭౒")]
  os.environ[bstack11ll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ౓")] = CONFIG[bstack11ll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ౔")]
  os.environ[bstack11ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐౕࠪ")] = bstack1l1l111l_opy_.__str__()
  from _pytest.config import main as bstack111lll1ll_opy_
  bstack111l111l1_opy_ = []
  try:
    bstack1ll11l1l1_opy_ = bstack111lll1ll_opy_(arg)
    if bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸౖࠬ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1lllll1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111l111l1_opy_.append(bstack1l1lllll1l_opy_)
    try:
      bstack111l111l_opy_ = (bstack111l111l1_opy_, int(bstack1ll11l1l1_opy_))
      bstack1lll11ll11_opy_.append(bstack111l111l_opy_)
    except:
      bstack1lll11ll11_opy_.append((bstack111l111l1_opy_, bstack1ll11l1l1_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack111l111l1_opy_.append({bstack11ll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౗"): bstack11ll11l_opy_ (u"ࠪࡔࡷࡵࡣࡦࡵࡶࠤࠬౘ") + os.environ.get(bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫౙ")), bstack11ll11l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫౚ"): traceback.format_exc(), bstack11ll11l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ౛"): int(os.environ.get(bstack11ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ౜")))})
    bstack1lll11ll11_opy_.append((bstack111l111l1_opy_, 1))
def bstack1l111lllll_opy_(arg):
  global bstack111l11111_opy_
  bstack1ll1l11ll1_opy_(bstack1l11l1ll1l_opy_)
  os.environ[bstack11ll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩౝ")] = str(bstack1l1l11l1l_opy_)
  from behave.__main__ import main as bstack1l1l1111_opy_
  status_code = bstack1l1l1111_opy_(arg)
  if status_code != 0:
    bstack111l11111_opy_ = status_code
def bstack1l111l1ll1_opy_():
  logger.info(bstack111lll1l1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11ll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ౞"), help=bstack11ll11l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫ౟"))
  parser.add_argument(bstack11ll11l_opy_ (u"ࠫ࠲ࡻࠧౠ"), bstack11ll11l_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩౡ"), help=bstack11ll11l_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬౢ"))
  parser.add_argument(bstack11ll11l_opy_ (u"ࠧ࠮࡭ࠪౣ"), bstack11ll11l_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧ౤"), help=bstack11ll11l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪ౥"))
  parser.add_argument(bstack11ll11l_opy_ (u"ࠪ࠱࡫࠭౦"), bstack11ll11l_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ౧"), help=bstack11ll11l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ౨"))
  bstack1ll11ll1_opy_ = parser.parse_args()
  try:
    bstack11lll11l1l_opy_ = bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪ౩")
    if bstack1ll11ll1_opy_.framework and bstack1ll11ll1_opy_.framework not in (bstack11ll11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ౪"), bstack11ll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ౫")):
      bstack11lll11l1l_opy_ = bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ౬")
    bstack1l11l111l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lll11l1l_opy_)
    bstack11ll11l1_opy_ = open(bstack1l11l111l_opy_, bstack11ll11l_opy_ (u"ࠪࡶࠬ౭"))
    bstack1lll1lll1l_opy_ = bstack11ll11l1_opy_.read()
    bstack11ll11l1_opy_.close()
    if bstack1ll11ll1_opy_.username:
      bstack1lll1lll1l_opy_ = bstack1lll1lll1l_opy_.replace(bstack11ll11l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ౮"), bstack1ll11ll1_opy_.username)
    if bstack1ll11ll1_opy_.key:
      bstack1lll1lll1l_opy_ = bstack1lll1lll1l_opy_.replace(bstack11ll11l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ౯"), bstack1ll11ll1_opy_.key)
    if bstack1ll11ll1_opy_.framework:
      bstack1lll1lll1l_opy_ = bstack1lll1lll1l_opy_.replace(bstack11ll11l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ౰"), bstack1ll11ll1_opy_.framework)
    file_name = bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ౱")
    file_path = os.path.abspath(file_name)
    bstack11llll1ll1_opy_ = open(file_path, bstack11ll11l_opy_ (u"ࠨࡹࠪ౲"))
    bstack11llll1ll1_opy_.write(bstack1lll1lll1l_opy_)
    bstack11llll1ll1_opy_.close()
    logger.info(bstack11lll111_opy_)
    try:
      os.environ[bstack11ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ౳")] = bstack1ll11ll1_opy_.framework if bstack1ll11ll1_opy_.framework != None else bstack11ll11l_opy_ (u"ࠥࠦ౴")
      config = yaml.safe_load(bstack1lll1lll1l_opy_)
      config[bstack11ll11l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ౵")] = bstack11ll11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫ౶")
      bstack1l1l1l111l_opy_(bstack11ll1lllll_opy_, config)
    except Exception as e:
      logger.debug(bstack1ll111l111_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1llll11ll_opy_.format(str(e)))
def bstack1l1l1l111l_opy_(bstack11ll1111_opy_, config, bstack1ll1ll1l_opy_={}):
  global bstack1l1l111l_opy_
  global bstack1l111l11l_opy_
  global bstack1l1111l111_opy_
  if not config:
    return
  bstack1ll1ll111_opy_ = bstack1l1ll111l1_opy_ if not bstack1l1l111l_opy_ else (
    bstack1l111lll11_opy_ if bstack11ll11l_opy_ (u"࠭ࡡࡱࡲࠪ౷") in config else (
        bstack1l1l1l1ll1_opy_ if config.get(bstack11ll11l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ౸")) else bstack1l11l11l1_opy_
    )
)
  bstack1l1111lll1_opy_ = False
  bstack1lll1ll1l_opy_ = False
  if bstack1l1l111l_opy_ is True:
      if bstack11ll11l_opy_ (u"ࠨࡣࡳࡴࠬ౹") in config:
          bstack1l1111lll1_opy_ = True
      else:
          bstack1lll1ll1l_opy_ = True
  bstack1l1l11l1l1_opy_ = bstack1lll1l111_opy_.bstack1llll1111l_opy_(config, bstack1l111l11l_opy_)
  data = {
    bstack11ll11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ౺"): config[bstack11ll11l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ౻")],
    bstack11ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ౼"): config[bstack11ll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ౽")],
    bstack11ll11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ౾"): bstack11ll1111_opy_,
    bstack11ll11l_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ౿"): os.environ.get(bstack11ll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪಀ"), bstack1l111l11l_opy_),
    bstack11ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫಁ"): bstack1ll111ll11_opy_,
    bstack11ll11l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬಂ"): bstack1ll1ll11ll_opy_(),
    bstack11ll11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧಃ"): {
      bstack11ll11l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ಄"): str(config[bstack11ll11l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ಅ")]) if bstack11ll11l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧಆ") in config else bstack11ll11l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤಇ"),
      bstack11ll11l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫಈ"): sys.version,
      bstack11ll11l_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬಉ"): bstack1lll1llll1_opy_(os.getenv(bstack11ll11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨಊ"), bstack11ll11l_opy_ (u"ࠧࠨಋ"))),
      bstack11ll11l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨಌ"): bstack11ll11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ಍"),
      bstack11ll11l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩಎ"): bstack1ll1ll111_opy_,
      bstack11ll11l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧಏ"): bstack1l1l11l1l1_opy_,
      bstack11ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࠩಐ"): os.environ[bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ಑")],
      bstack11ll11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨಒ"): bstack1l1llll1ll_opy_(os.environ.get(bstack11ll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨಓ"), bstack1l111l11l_opy_)),
      bstack11ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪಔ"): config[bstack11ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫಕ")] if config[bstack11ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬಖ")] else bstack11ll11l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦಗ"),
      bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ಘ"): str(config[bstack11ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಙ")]) if bstack11ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨಚ") in config else bstack11ll11l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣಛ"),
      bstack11ll11l_opy_ (u"ࠨࡱࡶࠫಜ"): sys.platform,
      bstack11ll11l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫಝ"): socket.gethostname(),
      bstack11ll11l_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬಞ"): bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ಟ"))
    }
  }
  if not bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬಠ")) is None:
    data[bstack11ll11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩಡ")][bstack11ll11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡏࡨࡸࡦࡪࡡࡵࡣࠪಢ")] = {
      bstack11ll11l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨಣ"): bstack11ll11l_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧತ"),
      bstack11ll11l_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪಥ"): bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫದ")),
      bstack11ll11l_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࡓࡻ࡭ࡣࡧࡵࠫಧ"): bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩನ"))
    }
  if bstack11ll1111_opy_ == bstack11l1l1ll_opy_:
    data[bstack11ll11l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ಩")][bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬࠭ಪ")] = bstack1l1l1111l1_opy_(config)
    data[bstack11ll11l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬಫ")][bstack11ll11l_opy_ (u"ࠪ࡭ࡸࡖࡥࡳࡥࡼࡅࡺࡺ࡯ࡆࡰࡤࡦࡱ࡫ࡤࠨಬ")] = percy.bstack11lll111l1_opy_
    data[bstack11ll11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧಭ")][bstack11ll11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡆࡺ࡯࡬ࡥࡋࡧࠫಮ")] = percy.bstack1lll1111_opy_
  update(data[bstack11ll11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩಯ")], bstack1ll1ll1l_opy_)
  try:
    response = bstack1l1l1111ll_opy_(bstack11ll11l_opy_ (u"ࠧࡑࡑࡖࡘࠬರ"), bstack111l1111_opy_(bstack1l11ll1l1_opy_), data, {
      bstack11ll11l_opy_ (u"ࠨࡣࡸࡸ࡭࠭ಱ"): (config[bstack11ll11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫಲ")], config[bstack11ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ಳ")])
    })
    if response:
      logger.debug(bstack1ll1ll11_opy_.format(bstack11ll1111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1llll1ll1_opy_.format(str(e)))
def bstack1lll1llll1_opy_(framework):
  return bstack11ll11l_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣ಴").format(str(framework), __version__) if framework else bstack11ll11l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨವ").format(
    __version__)
def bstack11l111l11_opy_():
  global CONFIG
  global bstack1ll1lll11l_opy_
  if bool(CONFIG):
    return
  try:
    bstack1llll1111_opy_()
    logger.debug(bstack11lllllll_opy_.format(str(CONFIG)))
    bstack1ll1lll11l_opy_ = bstack111l1lll_opy_.bstack1l111l1l_opy_(CONFIG, bstack1ll1lll11l_opy_)
    bstack1l111ll1_opy_()
  except Exception as e:
    logger.error(bstack11ll11l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥಶ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l111l111_opy_
  atexit.register(bstack1l11111l11_opy_)
  signal.signal(signal.SIGINT, bstack1ll111111_opy_)
  signal.signal(signal.SIGTERM, bstack1ll111111_opy_)
def bstack1l111l111_opy_(exctype, value, traceback):
  global bstack1ll1llll1_opy_
  try:
    for driver in bstack1ll1llll1_opy_:
      bstack1llll1l1l_opy_(driver, bstack11ll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧಷ"), bstack11ll11l_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦಸ") + str(value))
  except Exception:
    pass
  bstack11l11l11_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11l11l11_opy_(message=bstack11ll11l_opy_ (u"ࠩࠪಹ"), bstack1111lllll_opy_ = False):
  global CONFIG
  bstack1lll1l1l1_opy_ = bstack11ll11l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬ಺") if bstack1111lllll_opy_ else bstack11ll11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ಻")
  try:
    if message:
      bstack1ll1ll1l_opy_ = {
        bstack1lll1l1l1_opy_ : str(message)
      }
      bstack1l1l1l111l_opy_(bstack11l1l1ll_opy_, CONFIG, bstack1ll1ll1l_opy_)
    else:
      bstack1l1l1l111l_opy_(bstack11l1l1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll11l1111_opy_.format(str(e)))
def bstack1l11l1l1l_opy_(bstack1llll11lll_opy_, size):
  bstack1l1ll11ll1_opy_ = []
  while len(bstack1llll11lll_opy_) > size:
    bstack1llll11l1_opy_ = bstack1llll11lll_opy_[:size]
    bstack1l1ll11ll1_opy_.append(bstack1llll11l1_opy_)
    bstack1llll11lll_opy_ = bstack1llll11lll_opy_[size:]
  bstack1l1ll11ll1_opy_.append(bstack1llll11lll_opy_)
  return bstack1l1ll11ll1_opy_
def bstack1ll11ll1l1_opy_(args):
  if bstack11ll11l_opy_ (u"ࠬ࠳࡭ࠨ಼") in args and bstack11ll11l_opy_ (u"࠭ࡰࡥࡤࠪಽ") in args:
    return True
  return False
def run_on_browserstack(bstack1ll111ll1l_opy_=None, bstack1lll11ll11_opy_=None, bstack11111l1l_opy_=False):
  global CONFIG
  global bstack1l11ll1l1l_opy_
  global bstack1l1l11l1l_opy_
  global bstack1l111l11l_opy_
  global bstack1l1111l111_opy_
  bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠧࠨಾ")
  bstack1l11l1lll_opy_(bstack1lllll111_opy_, logger)
  if bstack1ll111ll1l_opy_ and isinstance(bstack1ll111ll1l_opy_, str):
    bstack1ll111ll1l_opy_ = eval(bstack1ll111ll1l_opy_)
  if bstack1ll111ll1l_opy_:
    CONFIG = bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨಿ")]
    bstack1l11ll1l1l_opy_ = bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪೀ")]
    bstack1l1l11l1l_opy_ = bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬು")]
    bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ೂ"), bstack1l1l11l1l_opy_)
    bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬೃ")
  bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨೄ"), uuid4().__str__())
  logger.debug(bstack11ll11l_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥ࠿ࠪ೅") + bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪೆ")))
  if not bstack11111l1l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111l1lll1_opy_)
      return
    if sys.argv[1] == bstack11ll11l_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬೇ") or sys.argv[1] == bstack11ll11l_opy_ (u"ࠪ࠱ࡻ࠭ೈ"):
      logger.info(bstack11ll11l_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫ೉").format(__version__))
      return
    if sys.argv[1] == bstack11ll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫೊ"):
      bstack1l111l1ll1_opy_()
      return
  args = sys.argv
  bstack11l111l11_opy_()
  global bstack111ll111_opy_
  global bstack1lllll1l11_opy_
  global bstack1l1l1lllll_opy_
  global bstack1l111ll11_opy_
  global bstack111l11l1l_opy_
  global bstack1lll1l11l1_opy_
  global bstack1ll1l11l_opy_
  global bstack1lll11l11_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack1lll1ll1l1_opy_
  global bstack111l1ll1l_opy_
  bstack1lllll1l11_opy_ = len(CONFIG.get(bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩೋ"), []))
  if not bstack1111ll1ll_opy_:
    if args[1] == bstack11ll11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧೌ") or args[1] == bstack11ll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴್ࠩ"):
      bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ೎")
      args = args[2:]
    elif args[1] == bstack11ll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ೏"):
      bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೐")
      args = args[2:]
    elif args[1] == bstack11ll11l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ೑"):
      bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ೒")
      args = args[2:]
    elif args[1] == bstack11ll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ೓"):
      bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ೔")
      args = args[2:]
    elif args[1] == bstack11ll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩೕ"):
      bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪೖ")
      args = args[2:]
    elif args[1] == bstack11ll11l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ೗"):
      bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ೘")
      args = args[2:]
    else:
      if not bstack11ll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ೙") in CONFIG or str(CONFIG[bstack11ll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೚")]).lower() in [bstack11ll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ೛"), bstack11ll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ೜")]:
        bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪೝ")
        args = args[1:]
      elif str(CONFIG[bstack11ll11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧೞ")]).lower() == bstack11ll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ೟"):
        bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬೠ")
        args = args[1:]
      elif str(CONFIG[bstack11ll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪೡ")]).lower() == bstack11ll11l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧೢ"):
        bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨೣ")
        args = args[1:]
      elif str(CONFIG[bstack11ll11l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭೤")]).lower() == bstack11ll11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ೥"):
        bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ೦")
        args = args[1:]
      elif str(CONFIG[bstack11ll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ೧")]).lower() == bstack11ll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ೨"):
        bstack1111ll1ll_opy_ = bstack11ll11l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ೩")
        args = args[1:]
      else:
        os.environ[bstack11ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ೪")] = bstack1111ll1ll_opy_
        bstack1l1l1ll1l1_opy_(bstack1l11l11l_opy_)
  os.environ[bstack11ll11l_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫ೫")] = bstack1111ll1ll_opy_
  bstack1l111l11l_opy_ = bstack1111ll1ll_opy_
  global bstack1l111l11_opy_
  global bstack111ll11l_opy_
  if bstack1ll111ll1l_opy_:
    try:
      os.environ[bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭೬")] = bstack1111ll1ll_opy_
      bstack1l1l1l111l_opy_(bstack1l1111l1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1ll1l11l1l_opy_.format(str(e)))
  global bstack11ll1l11l_opy_
  global bstack11l1111l_opy_
  global bstack1lll1111ll_opy_
  global bstack1l1111l1ll_opy_
  global bstack1l111lll1l_opy_
  global bstack1l1l1ll11_opy_
  global bstack1ll1l1ll1_opy_
  global bstack1111llll_opy_
  global bstack11111lll_opy_
  global bstack11l1l111_opy_
  global bstack1l1111l11l_opy_
  global bstack1l111l1ll_opy_
  global bstack11lllll1ll_opy_
  global bstack11111ll11_opy_
  global bstack1111l11l1_opy_
  global bstack1ll1ll1l1_opy_
  global bstack11llll1l11_opy_
  global bstack1l111l11ll_opy_
  global bstack1l111l1l11_opy_
  global bstack1lllll1ll1_opy_
  global bstack1l1llll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll1l11l_opy_ = webdriver.Remote.__init__
    bstack11l1111l_opy_ = WebDriver.quit
    bstack1l111l1ll_opy_ = WebDriver.close
    bstack1111l11l1_opy_ = WebDriver.get
    bstack1l1llll11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l111l11_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11lll11l1_opy_
    bstack111ll11l_opy_ = bstack11lll11l1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1llllll11_opy_
    from QWeb.keywords import browser
    bstack1llllll11_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll1l1lll_opy_(CONFIG) and bstack1l1lll111_opy_():
    if bstack1ll111l1l1_opy_() < version.parse(bstack11lll1l1_opy_):
      logger.error(bstack11lllll1_opy_.format(bstack1ll111l1l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll1ll1l1_opy_ = RemoteConnection._1l1ll1l1ll_opy_
      except Exception as e:
        logger.error(bstack1l11l1l1ll_opy_.format(str(e)))
  if not CONFIG.get(bstack11ll11l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ೭"), False) and not bstack1ll111ll1l_opy_:
    logger.info(bstack11l111ll_opy_)
  if bstack11ll11l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ೮") in CONFIG and str(CONFIG[bstack11ll11l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ೯")]).lower() != bstack11ll11l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ೰"):
    bstack1ll1lllll1_opy_()
  elif bstack1111ll1ll_opy_ != bstack11ll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩೱ") or (bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪೲ") and not bstack1ll111ll1l_opy_):
    bstack1l1111ll1_opy_()
  if (bstack1111ll1ll_opy_ in [bstack11ll11l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪೳ"), bstack11ll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ೴"), bstack11ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ೵")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll11l1ll_opy_
        bstack1l1l1ll11_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l1l1l11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l111lll1l_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11llll1l_opy_ + str(e))
    except Exception as e:
      bstack111111111_opy_(e, bstack11l1l1l11_opy_)
    if bstack1111ll1ll_opy_ != bstack11ll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ೶"):
      bstack1l11ll1ll_opy_()
    bstack1lll1111ll_opy_ = Output.start_test
    bstack1l1111l1ll_opy_ = Output.end_test
    bstack1ll1l1ll1_opy_ = TestStatus.__init__
    bstack11111lll_opy_ = pabot._run
    bstack11l1l111_opy_ = QueueItem.__init__
    bstack1l1111l11l_opy_ = pabot._create_command_for_execution
    bstack1l111l1l11_opy_ = pabot._report_results
  if bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ೷"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111111111_opy_(e, bstack1l11l1ll_opy_)
    bstack11lllll1ll_opy_ = Runner.run_hook
    bstack11111ll11_opy_ = Step.run
  if bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ೸"):
    try:
      from _pytest.config import Config
      bstack11llll1l11_opy_ = Config.getoption
      from _pytest import runner
      bstack1l111l11ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11lll11ll1_opy_)
    try:
      from pytest_bdd import reporting
      bstack1lllll1ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11ll11l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ೹"))
  try:
    framework_name = bstack11ll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೺") if bstack1111ll1ll_opy_ in [bstack11ll11l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ೻"), bstack11ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೼"), bstack11ll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ೽")] else bstack1111ll1l1_opy_(bstack1111ll1ll_opy_)
    bstack11ll1ll11_opy_ = {
      bstack11ll11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩ೾"): bstack11ll11l_opy_ (u"ࠩࡾ࠴ࢂ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ೿").format(framework_name) if bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪഀ") and bstack1lll1l1l_opy_() else framework_name,
      bstack11ll11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨഁ"): bstack1l1llll1ll_opy_(framework_name),
      bstack11ll11l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪം"): __version__,
      bstack11ll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧഃ"): bstack1111ll1ll_opy_
    }
    if bstack1111ll1ll_opy_ in bstack1l11ll111_opy_:
      if bstack1l1l111l_opy_ and bstack11ll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧഄ") in CONFIG and CONFIG[bstack11ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨഅ")] == True:
        if bstack11ll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩആ") in CONFIG:
          os.environ[bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫഇ")] = os.getenv(bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬഈ"), json.dumps(CONFIG[bstack11ll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬഉ")]))
          CONFIG[bstack11ll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ഊ")].pop(bstack11ll11l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬഋ"), None)
          CONFIG[bstack11ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨഌ")].pop(bstack11ll11l_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ഍"), None)
        bstack11ll1ll11_opy_[bstack11ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪഎ")] = {
          bstack11ll11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩഏ"): bstack11ll11l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧഐ"),
          bstack11ll11l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ഑"): str(bstack1ll111l1l1_opy_())
        }
    if bstack1111ll1ll_opy_ not in [bstack11ll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨഒ")]:
      bstack1l11ll11ll_opy_ = bstack1ll11l11l1_opy_.launch(CONFIG, bstack11ll1ll11_opy_)
  except Exception as e:
    logger.debug(bstack111lllll_opy_.format(bstack11ll11l_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩഓ"), str(e)))
  if bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩഔ"):
    bstack1l1l1lllll_opy_ = True
    if bstack1ll111ll1l_opy_ and bstack11111l1l_opy_:
      bstack1lll1l11l1_opy_ = CONFIG.get(bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧക"), {}).get(bstack11ll11l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഖ"))
      bstack1ll1l11ll1_opy_(bstack1llll11ll1_opy_)
    elif bstack1ll111ll1l_opy_:
      bstack1lll1l11l1_opy_ = CONFIG.get(bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩഗ"), {}).get(bstack11ll11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨഘ"))
      global bstack1ll1llll1_opy_
      try:
        if bstack1ll11ll1l1_opy_(bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪങ")]) and multiprocessing.current_process().name == bstack11ll11l_opy_ (u"ࠨ࠲ࠪച"):
          bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬഛ")].remove(bstack11ll11l_opy_ (u"ࠪ࠱ࡲ࠭ജ"))
          bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧഝ")].remove(bstack11ll11l_opy_ (u"ࠬࡶࡤࡣࠩഞ"))
          bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩട")] = bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪഠ")][0]
          with open(bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫഡ")], bstack11ll11l_opy_ (u"ࠩࡵࠫഢ")) as f:
            bstack111111l11_opy_ = f.read()
          bstack1l1lll11l1_opy_ = bstack11ll11l_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨണ").format(str(bstack1ll111ll1l_opy_))
          bstack11l1lll11_opy_ = bstack1l1lll11l1_opy_ + bstack111111l11_opy_
          bstack111111lll_opy_ = bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧത")] + bstack11ll11l_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧഥ")
          with open(bstack111111lll_opy_, bstack11ll11l_opy_ (u"࠭ࡷࠨദ")):
            pass
          with open(bstack111111lll_opy_, bstack11ll11l_opy_ (u"ࠢࡸ࠭ࠥധ")) as f:
            f.write(bstack11l1lll11_opy_)
          import subprocess
          bstack1l1lll1l_opy_ = subprocess.run([bstack11ll11l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣന"), bstack111111lll_opy_])
          if os.path.exists(bstack111111lll_opy_):
            os.unlink(bstack111111lll_opy_)
          os._exit(bstack1l1lll1l_opy_.returncode)
        else:
          if bstack1ll11ll1l1_opy_(bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬഩ")]):
            bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭പ")].remove(bstack11ll11l_opy_ (u"ࠫ࠲ࡳࠧഫ"))
            bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨബ")].remove(bstack11ll11l_opy_ (u"࠭ࡰࡥࡤࠪഭ"))
            bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪമ")] = bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫയ")][0]
          bstack1ll1l11ll1_opy_(bstack1llll11ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬര")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11ll11l_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬറ")] = bstack11ll11l_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ല")
          mod_globals[bstack11ll11l_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧള")] = os.path.abspath(bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩഴ")])
          exec(open(bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪവ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11ll11l_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨശ").format(str(e)))
          for driver in bstack1ll1llll1_opy_:
            bstack1lll11ll11_opy_.append({
              bstack11ll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧഷ"): bstack1ll111ll1l_opy_[bstack11ll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭സ")],
              bstack11ll11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪഹ"): str(e),
              bstack11ll11l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫഺ"): multiprocessing.current_process().name
            })
            bstack1llll1l1l_opy_(driver, bstack11ll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ഻࠭"), bstack11ll11l_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰ഼ࠥ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll1llll1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1l11l1l_opy_, CONFIG, logger)
      bstack1l1lll11_opy_()
      bstack11lllll11l_opy_()
      bstack11llll111_opy_ = {
        bstack11ll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫഽ"): args[0],
        bstack11ll11l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩാ"): CONFIG,
        bstack11ll11l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫി"): bstack1l11ll1l1l_opy_,
        bstack11ll11l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ീ"): bstack1l1l11l1l_opy_
      }
      percy.bstack1lll1lll11_opy_()
      if bstack11ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨു") in CONFIG:
        bstack111ll1111_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l1l111_opy_ = manager.list()
        if bstack1ll11ll1l1_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩൂ")]):
            if index == 0:
              bstack11llll111_opy_[bstack11ll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪൃ")] = args
            bstack111ll1111_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11llll111_opy_, bstack111l1l111_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫൄ")]):
            bstack111ll1111_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11llll111_opy_, bstack111l1l111_opy_)))
        for t in bstack111ll1111_opy_:
          t.start()
        for t in bstack111ll1111_opy_:
          t.join()
        bstack1lll11l11_opy_ = list(bstack111l1l111_opy_)
      else:
        if bstack1ll11ll1l1_opy_(args):
          bstack11llll111_opy_[bstack11ll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ൅")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11llll111_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll1l11ll1_opy_(bstack1llll11ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11ll11l_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬെ")] = bstack11ll11l_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭േ")
          mod_globals[bstack11ll11l_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧൈ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ൉") or bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ൊ"):
    percy.init(bstack1l1l11l1l_opy_, CONFIG, logger)
    percy.bstack1lll1lll11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack111111111_opy_(e, bstack11l1l1l11_opy_)
    bstack1l1lll11_opy_()
    bstack1ll1l11ll1_opy_(bstack1llllll1l_opy_)
    if bstack1l1l111l_opy_:
      bstack1lll1l1l1l_opy_(bstack1llllll1l_opy_, args)
      if bstack11ll11l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ോ") in args:
        i = args.index(bstack11ll11l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧൌ"))
        args.pop(i)
        args.pop(i)
      if bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ്࠭") not in CONFIG:
        CONFIG[bstack11ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧൎ")] = [{}]
        bstack1lllll1l11_opy_ = 1
      if bstack111ll111_opy_ == 0:
        bstack111ll111_opy_ = 1
      args.insert(0, str(bstack111ll111_opy_))
      args.insert(0, str(bstack11ll11l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ൏")))
    if bstack1ll11l11l1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l1llll1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11ll1111l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11ll11l_opy_ (u"ࠨࡒࡐࡄࡒࡘࡤࡕࡐࡕࡋࡒࡒࡘࠨ൐"),
        ).parse_args(bstack1l1llll1_opy_)
        bstack11l1l11ll_opy_ = args.index(bstack1l1llll1_opy_[0]) if len(bstack1l1llll1_opy_) > 0 else len(args)
        args.insert(bstack11l1l11ll_opy_, str(bstack11ll11l_opy_ (u"ࠧ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠫ൑")))
        args.insert(bstack11l1l11ll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳ࠰ࡳࡽࠬ൒"))))
        if bstack111111ll1_opy_(os.environ.get(bstack11ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧ൓"))) and str(os.environ.get(bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧൔ"), bstack11ll11l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩൕ"))) != bstack11ll11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪൖ"):
          for bstack1l1l1l11l1_opy_ in bstack11ll1111l_opy_:
            args.remove(bstack1l1l1l11l1_opy_)
          bstack1l11l11l1l_opy_ = os.environ.get(bstack11ll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪൗ")).split(bstack11ll11l_opy_ (u"ࠧ࠭ࠩ൘"))
          for bstack1l11llllll_opy_ in bstack1l11l11l1l_opy_:
            args.append(bstack1l11llllll_opy_)
      except Exception as e:
        logger.error(bstack11ll11l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡵࡶࡤࡧ࡭࡯࡮ࡨࠢ࡯࡭ࡸࡺࡥ࡯ࡧࡵࠤ࡫ࡵࡲࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࠦ൙").format(e))
    pabot.main(args)
  elif bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ൚"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack111111111_opy_(e, bstack11l1l1l11_opy_)
    for a in args:
      if bstack11ll11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩ൛") in a:
        bstack111l11l1l_opy_ = int(a.split(bstack11ll11l_opy_ (u"ࠫ࠿࠭൜"))[1])
      if bstack11ll11l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ൝") in a:
        bstack1lll1l11l1_opy_ = str(a.split(bstack11ll11l_opy_ (u"࠭࠺ࠨ൞"))[1])
      if bstack11ll11l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧൟ") in a:
        bstack1ll1l11l_opy_ = str(a.split(bstack11ll11l_opy_ (u"ࠨ࠼ࠪൠ"))[1])
    bstack1l11lllll_opy_ = None
    if bstack11ll11l_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨൡ") in args:
      i = args.index(bstack11ll11l_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩൢ"))
      args.pop(i)
      bstack1l11lllll_opy_ = args.pop(i)
    if bstack1l11lllll_opy_ is not None:
      global bstack1l1l11lll_opy_
      bstack1l1l11lll_opy_ = bstack1l11lllll_opy_
    bstack1ll1l11ll1_opy_(bstack1llllll1l_opy_)
    run_cli(args)
    if bstack11ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨൣ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1lllll1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll11ll11_opy_.append(bstack1l1lllll1l_opy_)
  elif bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ൤"):
    percy.init(bstack1l1l11l1l_opy_, CONFIG, logger)
    percy.bstack1lll1lll11_opy_()
    bstack1l11llll1l_opy_ = bstack1l1llll1l1_opy_(args, logger, CONFIG, bstack1l1l111l_opy_)
    bstack1l11llll1l_opy_.bstack1lll1llll_opy_()
    bstack1l1lll11_opy_()
    bstack1l111ll11_opy_ = True
    bstack1lll1ll1l1_opy_ = bstack1l11llll1l_opy_.bstack1l11lll111_opy_()
    bstack1l11llll1l_opy_.bstack11llll111_opy_(bstack11llllll11_opy_)
    bstack1ll1ll1l11_opy_ = bstack1l11llll1l_opy_.bstack11lll1l11_opy_(bstack111l11l1_opy_, {
      bstack11ll11l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ൥"): bstack1l11ll1l1l_opy_,
      bstack11ll11l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ൦"): bstack1l1l11l1l_opy_,
      bstack11ll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ൧"): bstack1l1l111l_opy_
    })
    try:
      bstack111l111l1_opy_, bstack1l11l111_opy_ = map(list, zip(*bstack1ll1ll1l11_opy_))
      bstack1ll1l1l1l1_opy_ = bstack111l111l1_opy_[0]
      for status_code in bstack1l11l111_opy_:
        if status_code != 0:
          bstack111l1ll1l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11ll11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡩࡷࡸ࡯ࡳࡵࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠳ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠽ࠤࢀࢃࠢ൨").format(str(e)))
  elif bstack1111ll1ll_opy_ == bstack11ll11l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ൩"):
    try:
      from behave.__main__ import main as bstack1l1l1111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack111111111_opy_(e, bstack1l11l1ll_opy_)
    bstack1l1lll11_opy_()
    bstack1l111ll11_opy_ = True
    bstack1ll11llll_opy_ = 1
    if bstack11ll11l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ൪") in CONFIG:
      bstack1ll11llll_opy_ = CONFIG[bstack11ll11l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ൫")]
    if bstack11ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ൬") in CONFIG:
      bstack1l1l11ll1l_opy_ = int(bstack1ll11llll_opy_) * int(len(CONFIG[bstack11ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ൭")]))
    else:
      bstack1l1l11ll1l_opy_ = int(bstack1ll11llll_opy_)
    config = Configuration(args)
    bstack11llll111l_opy_ = config.paths
    if len(bstack11llll111l_opy_) == 0:
      import glob
      pattern = bstack11ll11l_opy_ (u"ࠨࠬ࠭࠳࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠧ൮")
      bstack11ll1l11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11ll1l11_opy_)
      config = Configuration(args)
      bstack11llll111l_opy_ = config.paths
    bstack1ll1111l11_opy_ = [os.path.normpath(item) for item in bstack11llll111l_opy_]
    bstack1l111lll_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll1lll1_opy_ = [item for item in bstack1l111lll_opy_ if item not in bstack1ll1111l11_opy_]
    import platform as pf
    if pf.system().lower() == bstack11ll11l_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪ൯"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1111l11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll11l1ll1_opy_)))
                    for bstack1ll11l1ll1_opy_ in bstack1ll1111l11_opy_]
    bstack11l1l1ll1_opy_ = []
    for spec in bstack1ll1111l11_opy_:
      bstack1l111l111l_opy_ = []
      bstack1l111l111l_opy_ += bstack1ll1lll1_opy_
      bstack1l111l111l_opy_.append(spec)
      bstack11l1l1ll1_opy_.append(bstack1l111l111l_opy_)
    execution_items = []
    for bstack1l111l111l_opy_ in bstack11l1l1ll1_opy_:
      if bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭൰") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ൱")]):
          item = {}
          item[bstack11ll11l_opy_ (u"ࠬࡧࡲࡨࠩ൲")] = bstack11ll11l_opy_ (u"࠭ࠠࠨ൳").join(bstack1l111l111l_opy_)
          item[bstack11ll11l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭൴")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11ll11l_opy_ (u"ࠨࡣࡵ࡫ࠬ൵")] = bstack11ll11l_opy_ (u"ࠩࠣࠫ൶").join(bstack1l111l111l_opy_)
        item[bstack11ll11l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ൷")] = 0
        execution_items.append(item)
    bstack1l11111l_opy_ = bstack1l11l1l1l_opy_(execution_items, bstack1l1l11ll1l_opy_)
    for execution_item in bstack1l11111l_opy_:
      bstack111ll1111_opy_ = []
      for item in execution_item:
        bstack111ll1111_opy_.append(bstack1ll1l1l1l_opy_(name=str(item[bstack11ll11l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ൸")]),
                                             target=bstack1l111lllll_opy_,
                                             args=(item[bstack11ll11l_opy_ (u"ࠬࡧࡲࡨࠩ൹")],)))
      for t in bstack111ll1111_opy_:
        t.start()
      for t in bstack111ll1111_opy_:
        t.join()
  else:
    bstack1l1l1ll1l1_opy_(bstack1l11l11l_opy_)
  if not bstack1ll111ll1l_opy_:
    bstack1111l1lll_opy_()
  bstack111l1lll_opy_.bstack1111l1ll1_opy_()
def browserstack_initialize(bstack1l1l111ll_opy_=None):
  run_on_browserstack(bstack1l1l111ll_opy_, None, True)
def bstack1111l1lll_opy_():
  global CONFIG
  global bstack1l111l11l_opy_
  global bstack111l1ll1l_opy_
  global bstack111l11111_opy_
  global bstack1l1111l111_opy_
  bstack1ll11l11l1_opy_.stop()
  bstack111lllll1_opy_.bstack11lllll11_opy_()
  if bstack11ll11l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪൺ") in CONFIG and str(CONFIG[bstack11ll11l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫൻ")]).lower() != bstack11ll11l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧർ"):
    bstack11ll111ll_opy_, bstack1lllll1111_opy_ = bstack11lll1111l_opy_()
  else:
    bstack11ll111ll_opy_, bstack1lllll1111_opy_ = get_build_link()
  bstack11lll1ll1l_opy_(bstack11ll111ll_opy_)
  if bstack11ll111ll_opy_ is not None and bstack1lll1l11ll_opy_() != -1:
    sessions = bstack1111llll1_opy_(bstack11ll111ll_opy_)
    bstack1ll1111l_opy_(sessions, bstack1lllll1111_opy_)
  if bstack1l111l11l_opy_ == bstack11ll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩൽ") and bstack111l1ll1l_opy_ != 0:
    sys.exit(bstack111l1ll1l_opy_)
  if bstack1l111l11l_opy_ == bstack11ll11l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪൾ") and bstack111l11111_opy_ != 0:
    sys.exit(bstack111l11111_opy_)
def bstack11lll1ll1l_opy_(new_id):
    global bstack1ll111ll11_opy_
    bstack1ll111ll11_opy_ = new_id
def bstack1111ll1l1_opy_(bstack1lll11l1ll_opy_):
  if bstack1lll11l1ll_opy_:
    return bstack1lll11l1ll_opy_.capitalize()
  else:
    return bstack11ll11l_opy_ (u"ࠫࠬൿ")
def bstack1l1l11l1ll_opy_(bstack1lllll11ll_opy_):
  if bstack11ll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ඀") in bstack1lllll11ll_opy_ and bstack1lllll11ll_opy_[bstack11ll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫඁ")] != bstack11ll11l_opy_ (u"ࠧࠨං"):
    return bstack1lllll11ll_opy_[bstack11ll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ඃ")]
  else:
    bstack11l11lll_opy_ = bstack11ll11l_opy_ (u"ࠤࠥ඄")
    if bstack11ll11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪඅ") in bstack1lllll11ll_opy_ and bstack1lllll11ll_opy_[bstack11ll11l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫආ")] != None:
      bstack11l11lll_opy_ += bstack1lllll11ll_opy_[bstack11ll11l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬඇ")] + bstack11ll11l_opy_ (u"ࠨࠬࠡࠤඈ")
      if bstack1lllll11ll_opy_[bstack11ll11l_opy_ (u"ࠧࡰࡵࠪඉ")] == bstack11ll11l_opy_ (u"ࠣ࡫ࡲࡷࠧඊ"):
        bstack11l11lll_opy_ += bstack11ll11l_opy_ (u"ࠤ࡬ࡓࡘࠦࠢඋ")
      bstack11l11lll_opy_ += (bstack1lllll11ll_opy_[bstack11ll11l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧඌ")] or bstack11ll11l_opy_ (u"ࠫࠬඍ"))
      return bstack11l11lll_opy_
    else:
      bstack11l11lll_opy_ += bstack1111ll1l1_opy_(bstack1lllll11ll_opy_[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ඎ")]) + bstack11ll11l_opy_ (u"ࠨࠠࠣඏ") + (
              bstack1lllll11ll_opy_[bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩඐ")] or bstack11ll11l_opy_ (u"ࠨࠩඑ")) + bstack11ll11l_opy_ (u"ࠤ࠯ࠤࠧඒ")
      if bstack1lllll11ll_opy_[bstack11ll11l_opy_ (u"ࠪࡳࡸ࠭ඓ")] == bstack11ll11l_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧඔ"):
        bstack11l11lll_opy_ += bstack11ll11l_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥඕ")
      bstack11l11lll_opy_ += bstack1lllll11ll_opy_[bstack11ll11l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪඖ")] or bstack11ll11l_opy_ (u"ࠧࠨ඗")
      return bstack11l11lll_opy_
def bstack1ll1l111l_opy_(bstack1llllll11l_opy_):
  if bstack1llllll11l_opy_ == bstack11ll11l_opy_ (u"ࠣࡦࡲࡲࡪࠨ඘"):
    return bstack11ll11l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ඙")
  elif bstack1llllll11l_opy_ == bstack11ll11l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥක"):
    return bstack11ll11l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧඛ")
  elif bstack1llllll11l_opy_ == bstack11ll11l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧග"):
    return bstack11ll11l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ඝ")
  elif bstack1llllll11l_opy_ == bstack11ll11l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨඞ"):
    return bstack11ll11l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪඟ")
  elif bstack1llllll11l_opy_ == bstack11ll11l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥච"):
    return bstack11ll11l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨඡ")
  elif bstack1llllll11l_opy_ == bstack11ll11l_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧජ"):
    return bstack11ll11l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ඣ")
  else:
    return bstack11ll11l_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪඤ") + bstack1111ll1l1_opy_(
      bstack1llllll11l_opy_) + bstack11ll11l_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ඥ")
def bstack1l11l1l11_opy_(session):
  return bstack11ll11l_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨඦ").format(
    session[bstack11ll11l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ට")], bstack1l1l11l1ll_opy_(session), bstack1ll1l111l_opy_(session[bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩඨ")]),
    bstack1ll1l111l_opy_(session[bstack11ll11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫඩ")]),
    bstack1111ll1l1_opy_(session[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ඪ")] or session[bstack11ll11l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ණ")] or bstack11ll11l_opy_ (u"ࠧࠨඬ")) + bstack11ll11l_opy_ (u"ࠣࠢࠥත") + (session[bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫථ")] or bstack11ll11l_opy_ (u"ࠪࠫද")),
    session[bstack11ll11l_opy_ (u"ࠫࡴࡹࠧධ")] + bstack11ll11l_opy_ (u"ࠧࠦࠢන") + session[bstack11ll11l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ඲")], session[bstack11ll11l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩඳ")] or bstack11ll11l_opy_ (u"ࠨࠩප"),
    session[bstack11ll11l_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ඵ")] if session[bstack11ll11l_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧබ")] else bstack11ll11l_opy_ (u"ࠫࠬභ"))
def bstack1ll1111l_opy_(sessions, bstack1lllll1111_opy_):
  try:
    bstack1ll111lll_opy_ = bstack11ll11l_opy_ (u"ࠧࠨම")
    if not os.path.exists(bstack11l11ll1_opy_):
      os.mkdir(bstack11l11ll1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll11l_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫඹ")), bstack11ll11l_opy_ (u"ࠧࡳࠩය")) as f:
      bstack1ll111lll_opy_ = f.read()
    bstack1ll111lll_opy_ = bstack1ll111lll_opy_.replace(bstack11ll11l_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬර"), str(len(sessions)))
    bstack1ll111lll_opy_ = bstack1ll111lll_opy_.replace(bstack11ll11l_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩ඼"), bstack1lllll1111_opy_)
    bstack1ll111lll_opy_ = bstack1ll111lll_opy_.replace(bstack11ll11l_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫල"),
                                              sessions[0].get(bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨ඾")) if sessions[0] else bstack11ll11l_opy_ (u"ࠬ࠭඿"))
    with open(os.path.join(bstack11l11ll1_opy_, bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪව")), bstack11ll11l_opy_ (u"ࠧࡸࠩශ")) as stream:
      stream.write(bstack1ll111lll_opy_.split(bstack11ll11l_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬෂ"))[0])
      for session in sessions:
        stream.write(bstack1l11l1l11_opy_(session))
      stream.write(bstack1ll111lll_opy_.split(bstack11ll11l_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ස"))[1])
    logger.info(bstack11ll11l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭හ").format(bstack11l11ll1_opy_));
  except Exception as e:
    logger.debug(bstack1llll1l11l_opy_.format(str(e)))
def bstack1111llll1_opy_(bstack11ll111ll_opy_):
  global CONFIG
  try:
    host = bstack11ll11l_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧළ") if bstack11ll11l_opy_ (u"ࠬࡧࡰࡱࠩෆ") in CONFIG else bstack11ll11l_opy_ (u"࠭ࡡࡱ࡫ࠪ෇")
    user = CONFIG[bstack11ll11l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ෈")]
    key = CONFIG[bstack11ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ෉")]
    bstack1l111llll_opy_ = bstack11ll11l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ්") if bstack11ll11l_opy_ (u"ࠪࡥࡵࡶࠧ෋") in CONFIG else (bstack11ll11l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ෌") if CONFIG.get(bstack11ll11l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ෍")) else bstack11ll11l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ෎"))
    url = bstack11ll11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬා").format(user, key, host, bstack1l111llll_opy_,
                                                                                bstack11ll111ll_opy_)
    headers = {
      bstack11ll11l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧැ"): bstack11ll11l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬෑ"),
    }
    proxies = bstack111lll11l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11ll11l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨි")], response.json()))
  except Exception as e:
    logger.debug(bstack1lll1lll_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1ll111ll11_opy_
  try:
    if bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧී") in CONFIG:
      host = bstack11ll11l_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨු") if bstack11ll11l_opy_ (u"࠭ࡡࡱࡲࠪ෕") in CONFIG else bstack11ll11l_opy_ (u"ࠧࡢࡲ࡬ࠫූ")
      user = CONFIG[bstack11ll11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ෗")]
      key = CONFIG[bstack11ll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬෘ")]
      bstack1l111llll_opy_ = bstack11ll11l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩෙ") if bstack11ll11l_opy_ (u"ࠫࡦࡶࡰࠨේ") in CONFIG else bstack11ll11l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧෛ")
      url = bstack11ll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭ො").format(user, key, host, bstack1l111llll_opy_)
      headers = {
        bstack11ll11l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ෝ"): bstack11ll11l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫෞ"),
      }
      if bstack11ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫෟ") in CONFIG:
        params = {bstack11ll11l_opy_ (u"ࠪࡲࡦࡳࡥࠨ෠"): CONFIG[bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ෡")], bstack11ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ෢"): CONFIG[bstack11ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ෣")]}
      else:
        params = {bstack11ll11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ෤"): CONFIG[bstack11ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ෥")]}
      proxies = bstack111lll11l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1ll1ll1lll_opy_ = response.json()[0][bstack11ll11l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬ෦")]
        if bstack1ll1ll1lll_opy_:
          bstack1lllll1111_opy_ = bstack1ll1ll1lll_opy_[bstack11ll11l_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ෧")].split(bstack11ll11l_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪ෨"))[0] + bstack11ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭෩") + bstack1ll1ll1lll_opy_[
            bstack11ll11l_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ෪")]
          logger.info(bstack1ll111111l_opy_.format(bstack1lllll1111_opy_))
          bstack1ll111ll11_opy_ = bstack1ll1ll1lll_opy_[bstack11ll11l_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ෫")]
          bstack1l1ll1l1l1_opy_ = CONFIG[bstack11ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ෬")]
          if bstack11ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ෭") in CONFIG:
            bstack1l1ll1l1l1_opy_ += bstack11ll11l_opy_ (u"ࠪࠤࠬ෮") + CONFIG[bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭෯")]
          if bstack1l1ll1l1l1_opy_ != bstack1ll1ll1lll_opy_[bstack11ll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ෰")]:
            logger.debug(bstack11ll111l1_opy_.format(bstack1ll1ll1lll_opy_[bstack11ll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෱")], bstack1l1ll1l1l1_opy_))
          return [bstack1ll1ll1lll_opy_[bstack11ll11l_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪෲ")], bstack1lllll1111_opy_]
    else:
      logger.warn(bstack1ll11lll11_opy_)
  except Exception as e:
    logger.debug(bstack1ll1111lll_opy_.format(str(e)))
  return [None, None]
def bstack11llllll_opy_(url, bstack1l11lll1l1_opy_=False):
  global CONFIG
  global bstack1l11l1ll11_opy_
  if not bstack1l11l1ll11_opy_:
    hostname = bstack1l111ll1l_opy_(url)
    is_private = bstack1llll1ll11_opy_(hostname)
    if (bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬෳ") in CONFIG and not bstack111111ll1_opy_(CONFIG[bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭෴")])) and (is_private or bstack1l11lll1l1_opy_):
      bstack1l11l1ll11_opy_ = hostname
def bstack1l111ll1l_opy_(url):
  return urlparse(url).hostname
def bstack1llll1ll11_opy_(hostname):
  for bstack1l11111lll_opy_ in bstack1l1ll111l_opy_:
    regex = re.compile(bstack1l11111lll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1ll111ll1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack111l11l1l_opy_
  bstack111l111ll_opy_ = not (bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ෵"), None) and bstack1l111111l1_opy_(
          threading.current_thread(), bstack11ll11l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ෶"), None))
  bstack1ll1l11l1_opy_ = getattr(driver, bstack11ll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ෷"), None) != True
  if not bstack11llll1111_opy_.bstack1l1l1l1l1l_opy_(CONFIG, bstack111l11l1l_opy_) or (bstack1ll1l11l1_opy_ and bstack111l111ll_opy_):
    logger.warning(bstack11ll11l_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ෸"))
    return {}
  try:
    logger.debug(bstack11ll11l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ෹"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1ll1l1ll1l_opy_.bstack1l11l11l11_opy_)
    return results
  except Exception:
    logger.error(bstack11ll11l_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥ෺"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack111l11l1l_opy_
  bstack111l111ll_opy_ = not (bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭෻"), None) and bstack1l111111l1_opy_(
          threading.current_thread(), bstack11ll11l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ෼"), None))
  bstack1ll1l11l1_opy_ = getattr(driver, bstack11ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ෽"), None) != True
  if not bstack11llll1111_opy_.bstack1l1l1l1l1l_opy_(CONFIG, bstack111l11l1l_opy_) or (bstack1ll1l11l1_opy_ and bstack111l111ll_opy_):
    logger.warning(bstack11ll11l_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤ෾"))
    return {}
  try:
    logger.debug(bstack11ll11l_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫ෿"))
    logger.debug(perform_scan(driver))
    bstack1l1l1l1ll_opy_ = driver.execute_async_script(bstack1ll1l1ll1l_opy_.bstack111l11ll_opy_)
    return bstack1l1l1l1ll_opy_
  except Exception:
    logger.error(bstack11ll11l_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣ฀"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack111l11l1l_opy_
  bstack111l111ll_opy_ = not (bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬก"), None) and bstack1l111111l1_opy_(
          threading.current_thread(), bstack11ll11l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨข"), None))
  bstack1ll1l11l1_opy_ = getattr(driver, bstack11ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪฃ"), None) != True
  if not bstack11llll1111_opy_.bstack1l1l1l1l1l_opy_(CONFIG, bstack111l11l1l_opy_) or (bstack1ll1l11l1_opy_ and bstack111l111ll_opy_):
    logger.warning(bstack11ll11l_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨค"))
    return {}
  try:
    bstack1l1111ll11_opy_ = driver.execute_async_script(bstack1ll1l1ll1l_opy_.perform_scan, {bstack11ll11l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬฅ"): kwargs.get(bstack11ll11l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧฆ"), None) or bstack11ll11l_opy_ (u"ࠧࠨง")})
    return bstack1l1111ll11_opy_
  except Exception:
    logger.error(bstack11ll11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢจ"))
    return {}