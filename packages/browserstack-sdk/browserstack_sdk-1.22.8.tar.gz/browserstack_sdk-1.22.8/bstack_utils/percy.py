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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l11ll1lll_opy_, bstack1ll1lll11l_opy_
class bstack1lll11lll1_opy_:
  working_dir = os.getcwd()
  bstack1l1ll11ll1_opy_ = False
  config = {}
  binary_path = bstack1l1l1l_opy_ (u"ࠨࠩᖍ")
  bstack1lll11ll11l_opy_ = bstack1l1l1l_opy_ (u"ࠩࠪᖎ")
  bstack11111llll_opy_ = False
  bstack1lll1l1l1l1_opy_ = None
  bstack1lll1lll111_opy_ = {}
  bstack1llll1111ll_opy_ = 300
  bstack1lll1l1ll1l_opy_ = False
  logger = None
  bstack1lll1llllll_opy_ = False
  bstack1l11111ll1_opy_ = False
  bstack1ll1111l11_opy_ = None
  bstack1llll1111l1_opy_ = bstack1l1l1l_opy_ (u"ࠪࠫᖏ")
  bstack1lll11l1l11_opy_ = {
    bstack1l1l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᖐ") : 1,
    bstack1l1l1l_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ᖑ") : 2,
    bstack1l1l1l_opy_ (u"࠭ࡥࡥࡩࡨࠫᖒ") : 3,
    bstack1l1l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᖓ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lll1ll1l1l_opy_(self):
    bstack1lll11l1ll1_opy_ = bstack1l1l1l_opy_ (u"ࠨࠩᖔ")
    bstack1lll11ll1ll_opy_ = sys.platform
    bstack1lll1ll11l1_opy_ = bstack1l1l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᖕ")
    if re.match(bstack1l1l1l_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥᖖ"), bstack1lll11ll1ll_opy_) != None:
      bstack1lll11l1ll1_opy_ = bstack111l11l1ll_opy_ + bstack1l1l1l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧᖗ")
      self.bstack1llll1111l1_opy_ = bstack1l1l1l_opy_ (u"ࠬࡳࡡࡤࠩᖘ")
    elif re.match(bstack1l1l1l_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦᖙ"), bstack1lll11ll1ll_opy_) != None:
      bstack1lll11l1ll1_opy_ = bstack111l11l1ll_opy_ + bstack1l1l1l_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣᖚ")
      bstack1lll1ll11l1_opy_ = bstack1l1l1l_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦᖛ")
      self.bstack1llll1111l1_opy_ = bstack1l1l1l_opy_ (u"ࠩࡺ࡭ࡳ࠭ᖜ")
    else:
      bstack1lll11l1ll1_opy_ = bstack111l11l1ll_opy_ + bstack1l1l1l_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨᖝ")
      self.bstack1llll1111l1_opy_ = bstack1l1l1l_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪᖞ")
    return bstack1lll11l1ll1_opy_, bstack1lll1ll11l1_opy_
  def bstack1lll1l11111_opy_(self):
    try:
      bstack1lll1l11l1l_opy_ = [os.path.join(expanduser(bstack1l1l1l_opy_ (u"ࠧࢄࠢᖟ")), bstack1l1l1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᖠ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lll1l11l1l_opy_:
        if(self.bstack1lll1lll1ll_opy_(path)):
          return path
      raise bstack1l1l1l_opy_ (u"ࠢࡖࡰࡤࡰࡧ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᖡ")
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥᖢ").format(e))
  def bstack1lll1lll1ll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lll1ll1111_opy_(self, bstack1lll11l1ll1_opy_, bstack1lll1ll11l1_opy_):
    try:
      bstack1lll1ll1lll_opy_ = self.bstack1lll1l11111_opy_()
      bstack1lll11ll1l1_opy_ = os.path.join(bstack1lll1ll1lll_opy_, bstack1l1l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᖣ"))
      bstack1lll1lllll1_opy_ = os.path.join(bstack1lll1ll1lll_opy_, bstack1lll1ll11l1_opy_)
      if os.path.exists(bstack1lll1lllll1_opy_):
        self.logger.info(bstack1l1l1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᖤ").format(bstack1lll1lllll1_opy_))
        return bstack1lll1lllll1_opy_
      if os.path.exists(bstack1lll11ll1l1_opy_):
        self.logger.info(bstack1l1l1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᖥ").format(bstack1lll11ll1l1_opy_))
        return self.bstack1lll11l111l_opy_(bstack1lll11ll1l1_opy_, bstack1lll1ll11l1_opy_)
      self.logger.info(bstack1l1l1l_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᖦ").format(bstack1lll11l1ll1_opy_))
      response = bstack1ll1lll11l_opy_(bstack1l1l1l_opy_ (u"࠭ࡇࡆࡖࠪᖧ"), bstack1lll11l1ll1_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1lll11ll1l1_opy_, bstack1l1l1l_opy_ (u"ࠧࡸࡤࠪᖨ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1l1l_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨᖩ").format(bstack1lll11ll1l1_opy_))
        return self.bstack1lll11l111l_opy_(bstack1lll11ll1l1_opy_, bstack1lll1ll11l1_opy_)
      else:
        raise(bstack1l1l1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧᖪ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᖫ").format(e))
  def bstack1lll11ll111_opy_(self, bstack1lll11l1ll1_opy_, bstack1lll1ll11l1_opy_):
    try:
      retry = 2
      bstack1lll1lllll1_opy_ = None
      bstack1lll1l1111l_opy_ = False
      while retry > 0:
        bstack1lll1lllll1_opy_ = self.bstack1lll1ll1111_opy_(bstack1lll11l1ll1_opy_, bstack1lll1ll11l1_opy_)
        bstack1lll1l1111l_opy_ = self.bstack1lll11l1lll_opy_(bstack1lll11l1ll1_opy_, bstack1lll1ll11l1_opy_, bstack1lll1lllll1_opy_)
        if bstack1lll1l1111l_opy_:
          break
        retry -= 1
      return bstack1lll1lllll1_opy_, bstack1lll1l1111l_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᖬ").format(e))
    return bstack1lll1lllll1_opy_, False
  def bstack1lll11l1lll_opy_(self, bstack1lll11l1ll1_opy_, bstack1lll1ll11l1_opy_, bstack1lll1lllll1_opy_, bstack1lll1ll111l_opy_ = 0):
    if bstack1lll1ll111l_opy_ > 1:
      return False
    if bstack1lll1lllll1_opy_ == None or os.path.exists(bstack1lll1lllll1_opy_) == False:
      self.logger.warn(bstack1l1l1l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᖭ"))
      return False
    bstack1lll1l1l1ll_opy_ = bstack1l1l1l_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦᖮ")
    command = bstack1l1l1l_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ᖯ").format(bstack1lll1lllll1_opy_)
    bstack1lll11lllll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1lll1l1l1ll_opy_, bstack1lll11lllll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l1l1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᖰ"))
      return False
  def bstack1lll11l111l_opy_(self, bstack1lll11ll1l1_opy_, bstack1lll1ll11l1_opy_):
    try:
      working_dir = os.path.dirname(bstack1lll11ll1l1_opy_)
      shutil.unpack_archive(bstack1lll11ll1l1_opy_, working_dir)
      bstack1lll1lllll1_opy_ = os.path.join(working_dir, bstack1lll1ll11l1_opy_)
      os.chmod(bstack1lll1lllll1_opy_, 0o755)
      return bstack1lll1lllll1_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᖱ"))
  def bstack1llll111l11_opy_(self):
    try:
      bstack1lll11l11ll_opy_ = self.config.get(bstack1l1l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᖲ"))
      bstack1llll111l11_opy_ = bstack1lll11l11ll_opy_ or (bstack1lll11l11ll_opy_ is None and self.bstack1l1ll11ll1_opy_)
      if not bstack1llll111l11_opy_ or self.config.get(bstack1l1l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᖳ"), None) not in bstack1111llllll_opy_:
        return False
      self.bstack11111llll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᖴ").format(e))
  def bstack1lll1l1l111_opy_(self):
    try:
      bstack1lll1l1l111_opy_ = self.bstack1lll1lll11l_opy_
      return bstack1lll1l1l111_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᖵ").format(e))
  def init(self, bstack1l1ll11ll1_opy_, config, logger):
    self.bstack1l1ll11ll1_opy_ = bstack1l1ll11ll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1llll111l11_opy_():
      return
    self.bstack1lll1lll111_opy_ = config.get(bstack1l1l1l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᖶ"), {})
    self.bstack1lll1lll11l_opy_ = config.get(bstack1l1l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᖷ"))
    try:
      bstack1lll11l1ll1_opy_, bstack1lll1ll11l1_opy_ = self.bstack1lll1ll1l1l_opy_()
      bstack1lll1lllll1_opy_, bstack1lll1l1111l_opy_ = self.bstack1lll11ll111_opy_(bstack1lll11l1ll1_opy_, bstack1lll1ll11l1_opy_)
      if bstack1lll1l1111l_opy_:
        self.binary_path = bstack1lll1lllll1_opy_
        thread = Thread(target=self.bstack1lll1l1ll11_opy_)
        thread.start()
      else:
        self.bstack1lll1llllll_opy_ = True
        self.logger.error(bstack1l1l1l_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᖸ").format(bstack1lll1lllll1_opy_))
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᖹ").format(e))
  def bstack1lll1l1llll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1l1l_opy_ (u"ࠫࡱࡵࡧࠨᖺ"), bstack1l1l1l_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᖻ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1l1l_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᖼ").format(logfile))
      self.bstack1lll11ll11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᖽ").format(e))
  def bstack1lll1l1ll11_opy_(self):
    bstack1lll1ll11ll_opy_ = self.bstack1lll1llll11_opy_()
    if bstack1lll1ll11ll_opy_ == None:
      self.bstack1lll1llllll_opy_ = True
      self.logger.error(bstack1l1l1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᖾ"))
      return False
    command_args = [bstack1l1l1l_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᖿ") if self.bstack1l1ll11ll1_opy_ else bstack1l1l1l_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᗀ")]
    bstack1lll1l111ll_opy_ = self.bstack1lll1l11l11_opy_()
    if bstack1lll1l111ll_opy_ != None:
      command_args.append(bstack1l1l1l_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᗁ").format(bstack1lll1l111ll_opy_))
    env = os.environ.copy()
    env[bstack1l1l1l_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᗂ")] = bstack1lll1ll11ll_opy_
    env[bstack1l1l1l_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨᗃ")] = os.environ.get(bstack1l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᗄ"), bstack1l1l1l_opy_ (u"ࠨࠩᗅ"))
    bstack1lll1lll1l1_opy_ = [self.binary_path]
    self.bstack1lll1l1llll_opy_()
    self.bstack1lll1l1l1l1_opy_ = self.bstack1llll11111l_opy_(bstack1lll1lll1l1_opy_ + command_args, env)
    self.logger.debug(bstack1l1l1l_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥᗆ"))
    bstack1lll1ll111l_opy_ = 0
    while self.bstack1lll1l1l1l1_opy_.poll() == None:
      bstack1lll1l1lll1_opy_ = self.bstack1lll1l1l11l_opy_()
      if bstack1lll1l1lll1_opy_:
        self.logger.debug(bstack1l1l1l_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨᗇ"))
        self.bstack1lll1l1ll1l_opy_ = True
        return True
      bstack1lll1ll111l_opy_ += 1
      self.logger.debug(bstack1l1l1l_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢᗈ").format(bstack1lll1ll111l_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥᗉ").format(bstack1lll1ll111l_opy_))
    self.bstack1lll1llllll_opy_ = True
    return False
  def bstack1lll1l1l11l_opy_(self, bstack1lll1ll111l_opy_ = 0):
    if bstack1lll1ll111l_opy_ > 10:
      return False
    try:
      bstack1lll11l1111_opy_ = os.environ.get(bstack1l1l1l_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭ᗊ"), bstack1l1l1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨᗋ"))
      bstack1lll11l11l1_opy_ = bstack1lll11l1111_opy_ + bstack111l11ll11_opy_
      response = requests.get(bstack1lll11l11l1_opy_)
      data = response.json()
      self.bstack1ll1111l11_opy_ = data.get(bstack1l1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᗌ"), {}).get(bstack1l1l1l_opy_ (u"ࠩ࡬ࡨࠬᗍ"), None)
      return True
    except:
      self.logger.debug(bstack1l1l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣᗎ"))
      return False
  def bstack1lll1llll11_opy_(self):
    bstack1lll11lll1l_opy_ = bstack1l1l1l_opy_ (u"ࠫࡦࡶࡰࠨᗏ") if self.bstack1l1ll11ll1_opy_ else bstack1l1l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᗐ")
    bstack1lll1ll1l11_opy_ = bstack1l1l1l_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤᗑ") if self.config.get(bstack1l1l1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᗒ")) is None else True
    bstack1llllll111l_opy_ = bstack1l1l1l_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤᗓ").format(self.config[bstack1l1l1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᗔ")], bstack1lll11lll1l_opy_, bstack1lll1ll1l11_opy_)
    if self.bstack1lll1lll11l_opy_:
      bstack1llllll111l_opy_ += bstack1l1l1l_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧᗕ").format(self.bstack1lll1lll11l_opy_)
    uri = bstack1l11ll1lll_opy_(bstack1llllll111l_opy_)
    try:
      response = bstack1ll1lll11l_opy_(bstack1l1l1l_opy_ (u"ࠫࡌࡋࡔࠨᗖ"), uri, {}, {bstack1l1l1l_opy_ (u"ࠬࡧࡵࡵࡪࠪᗗ"): (self.config[bstack1l1l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᗘ")], self.config[bstack1l1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᗙ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11111llll_opy_ = data.get(bstack1l1l1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᗚ"))
        self.bstack1lll1lll11l_opy_ = data.get(bstack1l1l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧᗛ"))
        os.environ[bstack1l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᗜ")] = str(self.bstack11111llll_opy_)
        os.environ[bstack1l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᗝ")] = str(self.bstack1lll1lll11l_opy_)
        if bstack1lll1ll1l11_opy_ == bstack1l1l1l_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣᗞ") and str(self.bstack11111llll_opy_).lower() == bstack1l1l1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᗟ"):
          self.bstack1l11111ll1_opy_ = True
        if bstack1l1l1l_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᗠ") in data:
          return data[bstack1l1l1l_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᗡ")]
        else:
          raise bstack1l1l1l_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩᗢ").format(data)
      else:
        raise bstack1l1l1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥᗣ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧᗤ").format(e))
  def bstack1lll1l11l11_opy_(self):
    bstack1lll1ll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣᗥ"))
    try:
      if bstack1l1l1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᗦ") not in self.bstack1lll1lll111_opy_:
        self.bstack1lll1lll111_opy_[bstack1l1l1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᗧ")] = 2
      with open(bstack1lll1ll1ll1_opy_, bstack1l1l1l_opy_ (u"ࠨࡹࠪᗨ")) as fp:
        json.dump(self.bstack1lll1lll111_opy_, fp)
      return bstack1lll1ll1ll1_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᗩ").format(e))
  def bstack1llll11111l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llll1111l1_opy_ == bstack1l1l1l_opy_ (u"ࠪࡻ࡮ࡴࠧᗪ"):
        bstack1lll1llll1l_opy_ = [bstack1l1l1l_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬᗫ"), bstack1l1l1l_opy_ (u"ࠬ࠵ࡣࠨᗬ")]
        cmd = bstack1lll1llll1l_opy_ + cmd
      cmd = bstack1l1l1l_opy_ (u"࠭ࠠࠨᗭ").join(cmd)
      self.logger.debug(bstack1l1l1l_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦᗮ").format(cmd))
      with open(self.bstack1lll11ll11l_opy_, bstack1l1l1l_opy_ (u"ࠣࡣࠥᗯ")) as bstack1lll1l11ll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lll1l11ll1_opy_, text=True, stderr=bstack1lll1l11ll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lll1llllll_opy_ = True
      self.logger.error(bstack1l1l1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᗰ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lll1l1ll1l_opy_:
        self.logger.info(bstack1l1l1l_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦᗱ"))
        cmd = [self.binary_path, bstack1l1l1l_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢᗲ")]
        self.bstack1llll11111l_opy_(cmd)
        self.bstack1lll1l1ll1l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᗳ").format(cmd, e))
  def bstack11l1l1l1l_opy_(self):
    if not self.bstack11111llll_opy_:
      return
    try:
      bstack1lll11llll1_opy_ = 0
      while not self.bstack1lll1l1ll1l_opy_ and bstack1lll11llll1_opy_ < self.bstack1llll1111ll_opy_:
        if self.bstack1lll1llllll_opy_:
          self.logger.info(bstack1l1l1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦᗴ"))
          return
        time.sleep(1)
        bstack1lll11llll1_opy_ += 1
      os.environ[bstack1l1l1l_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ᗵ")] = str(self.bstack1lll11lll11_opy_())
      self.logger.info(bstack1l1l1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤᗶ"))
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᗷ").format(e))
  def bstack1lll11lll11_opy_(self):
    if self.bstack1l1ll11ll1_opy_:
      return
    try:
      bstack1lll1l111l1_opy_ = [platform[bstack1l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᗸ")].lower() for platform in self.config.get(bstack1l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᗹ"), [])]
      bstack1llll111111_opy_ = sys.maxsize
      bstack1lll11l1l1l_opy_ = bstack1l1l1l_opy_ (u"ࠬ࠭ᗺ")
      for browser in bstack1lll1l111l1_opy_:
        if browser in self.bstack1lll11l1l11_opy_:
          bstack1lll1l11lll_opy_ = self.bstack1lll11l1l11_opy_[browser]
        if bstack1lll1l11lll_opy_ < bstack1llll111111_opy_:
          bstack1llll111111_opy_ = bstack1lll1l11lll_opy_
          bstack1lll11l1l1l_opy_ = browser
      return bstack1lll11l1l1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᗻ").format(e))
  @classmethod
  def bstack1lll11111_opy_(self):
    return os.getenv(bstack1l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᗼ"), bstack1l1l1l_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧᗽ")).lower()
  @classmethod
  def bstack11l111111_opy_(self):
    return os.getenv(bstack1l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᗾ"), bstack1l1l1l_opy_ (u"ࠪࠫᗿ"))