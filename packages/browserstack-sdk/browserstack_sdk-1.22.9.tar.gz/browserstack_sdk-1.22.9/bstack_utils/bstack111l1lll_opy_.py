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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111l11ll1l_opy_, bstack111l11l1ll_opy_
import tempfile
import json
bstack1llll11l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᔞ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11ll11l_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᔟ"),
      datefmt=bstack11ll11l_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ᔠ"),
      stream=sys.stdout
    )
  return logger
def bstack1llll1l1lll_opy_():
  global bstack1llll11l1ll_opy_
  if os.path.exists(bstack1llll11l1ll_opy_):
    os.remove(bstack1llll11l1ll_opy_)
def bstack1111l1ll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l111l1l_opy_(config, log_level):
  bstack1llll11lll1_opy_ = log_level
  if bstack11ll11l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᔡ") in config and config[bstack11ll11l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᔢ")] in bstack111l11ll1l_opy_:
    bstack1llll11lll1_opy_ = bstack111l11ll1l_opy_[config[bstack11ll11l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᔣ")]]
  if config.get(bstack11ll11l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᔤ"), False):
    logging.getLogger().setLevel(bstack1llll11lll1_opy_)
    return bstack1llll11lll1_opy_
  global bstack1llll11l1ll_opy_
  bstack1111l1ll1_opy_()
  bstack1llll1l1ll1_opy_ = logging.Formatter(
    fmt=bstack11ll11l_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᔥ"),
    datefmt=bstack11ll11l_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬᔦ")
  )
  bstack1llll1l1l1l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1llll11l1ll_opy_)
  file_handler.setFormatter(bstack1llll1l1ll1_opy_)
  bstack1llll1l1l1l_opy_.setFormatter(bstack1llll1l1ll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1llll1l1l1l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11ll11l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ᔧ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1llll1l1l1l_opy_.setLevel(bstack1llll11lll1_opy_)
  logging.getLogger().addHandler(bstack1llll1l1l1l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1llll11lll1_opy_
def bstack1llll11ll11_opy_(config):
  try:
    bstack1llll1l111l_opy_ = set(bstack111l11l1ll_opy_)
    bstack1llll1l1l11_opy_ = bstack11ll11l_opy_ (u"ࠬ࠭ᔨ")
    with open(bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᔩ")) as bstack1llll11ll1l_opy_:
      bstack1llll1l1111_opy_ = bstack1llll11ll1l_opy_.read()
      bstack1llll1l1l11_opy_ = re.sub(bstack11ll11l_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨᔪ"), bstack11ll11l_opy_ (u"ࠨࠩᔫ"), bstack1llll1l1111_opy_, flags=re.M)
      bstack1llll1l1l11_opy_ = re.sub(
        bstack11ll11l_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬᔬ") + bstack11ll11l_opy_ (u"ࠪࢀࠬᔭ").join(bstack1llll1l111l_opy_) + bstack11ll11l_opy_ (u"ࠫ࠮࠴ࠪࠥࠩᔮ"),
        bstack11ll11l_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᔯ"),
        bstack1llll1l1l11_opy_, flags=re.M | re.I
      )
    def bstack1llll1l11l1_opy_(dic):
      bstack1llll1ll111_opy_ = {}
      for key, value in dic.items():
        if key in bstack1llll1l111l_opy_:
          bstack1llll1ll111_opy_[key] = bstack11ll11l_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᔰ")
        else:
          if isinstance(value, dict):
            bstack1llll1ll111_opy_[key] = bstack1llll1l11l1_opy_(value)
          else:
            bstack1llll1ll111_opy_[key] = value
      return bstack1llll1ll111_opy_
    bstack1llll1ll111_opy_ = bstack1llll1l11l1_opy_(config)
    return {
      bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᔱ"): bstack1llll1l1l11_opy_,
      bstack11ll11l_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᔲ"): json.dumps(bstack1llll1ll111_opy_)
    }
  except Exception as e:
    return {}
def bstack1l11111l1l_opy_(config):
  global bstack1llll11l1ll_opy_
  try:
    if config.get(bstack11ll11l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᔳ"), False):
      return
    uuid = os.getenv(bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᔴ"))
    if not uuid or uuid == bstack11ll11l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᔵ"):
      return
    bstack1llll11llll_opy_ = [bstack11ll11l_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡳࡥ࡯ࡶࡶ࠲ࡹࡾࡴࠨᔶ"), bstack11ll11l_opy_ (u"࠭ࡐࡪࡲࡩ࡭ࡱ࡫ࠧᔷ"), bstack11ll11l_opy_ (u"ࠧࡱࡻࡳࡶࡴࡰࡥࡤࡶ࠱ࡸࡴࡳ࡬ࠨᔸ"), bstack1llll11l1ll_opy_]
    bstack1111l1ll1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧᔹ") + uuid + bstack11ll11l_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪᔺ"))
    with tarfile.open(output_file, bstack11ll11l_opy_ (u"ࠥࡻ࠿࡭ࡺࠣᔻ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1llll11llll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1llll11ll11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1llll1l11ll_opy_ = data.encode()
        tarinfo.size = len(bstack1llll1l11ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1llll1l11ll_opy_))
    bstack1111ll111_opy_ = MultipartEncoder(
      fields= {
        bstack11ll11l_opy_ (u"ࠫࡩࡧࡴࡢࠩᔼ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11ll11l_opy_ (u"ࠬࡸࡢࠨᔽ")), bstack11ll11l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫᔾ")),
        bstack11ll11l_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᔿ"): uuid
      }
    )
    response = requests.post(
      bstack11ll11l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡸࡴࡱࡵࡡࡥ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥᕀ"),
      data=bstack1111ll111_opy_,
      headers={bstack11ll11l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᕁ"): bstack1111ll111_opy_.content_type},
      auth=(config[bstack11ll11l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᕂ")], config[bstack11ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᕃ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11ll11l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶ࡬ࡰࡣࡧࠤࡱࡵࡧࡴ࠼ࠣࠫᕄ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11ll11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠬᕅ") + str(e))
  finally:
    try:
      bstack1llll1l1lll_opy_()
    except:
      pass