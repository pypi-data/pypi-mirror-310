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
class bstack111l1ll1l1_opy_(object):
  bstack111l1111l_opy_ = os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"࠭ࡾࠨယ")), bstack11ll11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧရ"))
  bstack111l1l1lll_opy_ = os.path.join(bstack111l1111l_opy_, bstack11ll11l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨလ"))
  bstack111l1ll11l_opy_ = None
  perform_scan = None
  bstack1l11l11l11_opy_ = None
  bstack111l11ll_opy_ = None
  bstack111ll1l111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11ll11l_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫဝ")):
      cls.instance = super(bstack111l1ll1l1_opy_, cls).__new__(cls)
      cls.instance.bstack111l1ll1ll_opy_()
    return cls.instance
  def bstack111l1ll1ll_opy_(self):
    try:
      with open(self.bstack111l1l1lll_opy_, bstack11ll11l_opy_ (u"ࠪࡶࠬသ")) as bstack1l1l1lll1_opy_:
        bstack111l1lll11_opy_ = bstack1l1l1lll1_opy_.read()
        data = json.loads(bstack111l1lll11_opy_)
        if bstack11ll11l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ဟ") in data:
          self.bstack111ll1l11l_opy_(data[bstack11ll11l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧဠ")])
        if bstack11ll11l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧအ") in data:
          self.bstack111llll111_opy_(data[bstack11ll11l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨဢ")])
    except:
      pass
  def bstack111llll111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack11ll11l_opy_ (u"ࠨࡵࡦࡥࡳ࠭ဣ")]
      self.bstack1l11l11l11_opy_ = scripts[bstack11ll11l_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ဤ")]
      self.bstack111l11ll_opy_ = scripts[bstack11ll11l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧဥ")]
      self.bstack111ll1l111_opy_ = scripts[bstack11ll11l_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩဦ")]
  def bstack111ll1l11l_opy_(self, bstack111l1ll11l_opy_):
    if bstack111l1ll11l_opy_ != None and len(bstack111l1ll11l_opy_) != 0:
      self.bstack111l1ll11l_opy_ = bstack111l1ll11l_opy_
  def store(self):
    try:
      with open(self.bstack111l1l1lll_opy_, bstack11ll11l_opy_ (u"ࠬࡽࠧဧ")) as file:
        json.dump({
          bstack11ll11l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣဨ"): self.bstack111l1ll11l_opy_,
          bstack11ll11l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣဩ"): {
            bstack11ll11l_opy_ (u"ࠣࡵࡦࡥࡳࠨဪ"): self.perform_scan,
            bstack11ll11l_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨါ"): self.bstack1l11l11l11_opy_,
            bstack11ll11l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢာ"): self.bstack111l11ll_opy_,
            bstack11ll11l_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤိ"): self.bstack111ll1l111_opy_
          }
        }, file)
    except:
      pass
  def bstack1ll1ll1ll_opy_(self, bstack111l1ll111_opy_):
    try:
      return any(command.get(bstack11ll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪီ")) == bstack111l1ll111_opy_ for command in self.bstack111l1ll11l_opy_)
    except:
      return False
bstack1ll1l1ll1l_opy_ = bstack111l1ll1l1_opy_()