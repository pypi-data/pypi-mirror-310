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
class bstack111l1l1ll1_opy_(object):
  bstack1lll1ll1_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l_opy_ (u"࠭ࡾࠨယ")), bstack1l1l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧရ"))
  bstack111l1l1lll_opy_ = os.path.join(bstack1lll1ll1_opy_, bstack1l1l1l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨလ"))
  bstack111l1ll111_opy_ = None
  perform_scan = None
  bstack11lllll1l1_opy_ = None
  bstack111l1l1l1_opy_ = None
  bstack111ll1lll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1l1l_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫဝ")):
      cls.instance = super(bstack111l1l1ll1_opy_, cls).__new__(cls)
      cls.instance.bstack111l1ll1l1_opy_()
    return cls.instance
  def bstack111l1ll1l1_opy_(self):
    try:
      with open(self.bstack111l1l1lll_opy_, bstack1l1l1l_opy_ (u"ࠪࡶࠬသ")) as bstack1lllll11l_opy_:
        bstack111l1ll1ll_opy_ = bstack1lllll11l_opy_.read()
        data = json.loads(bstack111l1ll1ll_opy_)
        if bstack1l1l1l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ဟ") in data:
          self.bstack111ll111l1_opy_(data[bstack1l1l1l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧဠ")])
        if bstack1l1l1l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧအ") in data:
          self.bstack111ll1111l_opy_(data[bstack1l1l1l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨဢ")])
    except:
      pass
  def bstack111ll1111l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1l1l1l_opy_ (u"ࠨࡵࡦࡥࡳ࠭ဣ")]
      self.bstack11lllll1l1_opy_ = scripts[bstack1l1l1l_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ဤ")]
      self.bstack111l1l1l1_opy_ = scripts[bstack1l1l1l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧဥ")]
      self.bstack111ll1lll1_opy_ = scripts[bstack1l1l1l_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩဦ")]
  def bstack111ll111l1_opy_(self, bstack111l1ll111_opy_):
    if bstack111l1ll111_opy_ != None and len(bstack111l1ll111_opy_) != 0:
      self.bstack111l1ll111_opy_ = bstack111l1ll111_opy_
  def store(self):
    try:
      with open(self.bstack111l1l1lll_opy_, bstack1l1l1l_opy_ (u"ࠬࡽࠧဧ")) as file:
        json.dump({
          bstack1l1l1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣဨ"): self.bstack111l1ll111_opy_,
          bstack1l1l1l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣဩ"): {
            bstack1l1l1l_opy_ (u"ࠣࡵࡦࡥࡳࠨဪ"): self.perform_scan,
            bstack1l1l1l_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨါ"): self.bstack11lllll1l1_opy_,
            bstack1l1l1l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢာ"): self.bstack111l1l1l1_opy_,
            bstack1l1l1l_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤိ"): self.bstack111ll1lll1_opy_
          }
        }, file)
    except:
      pass
  def bstack11ll111l1_opy_(self, bstack111l1ll11l_opy_):
    try:
      return any(command.get(bstack1l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪီ")) == bstack111l1ll11l_opy_ for command in self.bstack111l1ll111_opy_)
    except:
      return False
bstack1lll1l11l_opy_ = bstack111l1l1ll1_opy_()