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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111111l1ll_opy_, bstack1l111ll1l_opy_, bstack1l111111l1_opy_, bstack1llll1ll11_opy_, \
    bstack11111ll11l_opy_
def bstack1l11111l11_opy_(bstack1ll1l1ll1l1_opy_):
    for driver in bstack1ll1l1ll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1l1l_opy_(driver, status, reason=bstack11ll11l_opy_ (u"ࠬ࠭ᙜ")):
    bstack1l1111l111_opy_ = Config.bstack1lll1ll111_opy_()
    if bstack1l1111l111_opy_.bstack11l1111ll1_opy_():
        return
    bstack1l11111ll_opy_ = bstack111l1ll11_opy_(bstack11ll11l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᙝ"), bstack11ll11l_opy_ (u"ࠧࠨᙞ"), status, reason, bstack11ll11l_opy_ (u"ࠨࠩᙟ"), bstack11ll11l_opy_ (u"ࠩࠪᙠ"))
    driver.execute_script(bstack1l11111ll_opy_)
def bstack1ll11l1l_opy_(page, status, reason=bstack11ll11l_opy_ (u"ࠪࠫᙡ")):
    try:
        if page is None:
            return
        bstack1l1111l111_opy_ = Config.bstack1lll1ll111_opy_()
        if bstack1l1111l111_opy_.bstack11l1111ll1_opy_():
            return
        bstack1l11111ll_opy_ = bstack111l1ll11_opy_(bstack11ll11l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᙢ"), bstack11ll11l_opy_ (u"ࠬ࠭ᙣ"), status, reason, bstack11ll11l_opy_ (u"࠭ࠧᙤ"), bstack11ll11l_opy_ (u"ࠧࠨᙥ"))
        page.evaluate(bstack11ll11l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᙦ"), bstack1l11111ll_opy_)
    except Exception as e:
        print(bstack11ll11l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢᙧ"), e)
def bstack111l1ll11_opy_(type, name, status, reason, bstack1l1l1ll111_opy_, bstack11111l1ll_opy_):
    bstack1l1l11ll11_opy_ = {
        bstack11ll11l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᙨ"): type,
        bstack11ll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᙩ"): {}
    }
    if type == bstack11ll11l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᙪ"):
        bstack1l1l11ll11_opy_[bstack11ll11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᙫ")][bstack11ll11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᙬ")] = bstack1l1l1ll111_opy_
        bstack1l1l11ll11_opy_[bstack11ll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᙭")][bstack11ll11l_opy_ (u"ࠩࡧࡥࡹࡧࠧ᙮")] = json.dumps(str(bstack11111l1ll_opy_))
    if type == bstack11ll11l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᙯ"):
        bstack1l1l11ll11_opy_[bstack11ll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᙰ")][bstack11ll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᙱ")] = name
    if type == bstack11ll11l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᙲ"):
        bstack1l1l11ll11_opy_[bstack11ll11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᙳ")][bstack11ll11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᙴ")] = status
        if status == bstack11ll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᙵ") and str(reason) != bstack11ll11l_opy_ (u"ࠥࠦᙶ"):
            bstack1l1l11ll11_opy_[bstack11ll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᙷ")][bstack11ll11l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᙸ")] = json.dumps(str(reason))
    bstack11l1ll1ll_opy_ = bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᙹ").format(json.dumps(bstack1l1l11ll11_opy_))
    return bstack11l1ll1ll_opy_
def bstack11llllll_opy_(url, config, logger, bstack1l11lll1l1_opy_=False):
    hostname = bstack1l111ll1l_opy_(url)
    is_private = bstack1llll1ll11_opy_(hostname)
    try:
        if is_private or bstack1l11lll1l1_opy_:
            file_path = bstack111111l1ll_opy_(bstack11ll11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᙺ"), bstack11ll11l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᙻ"), logger)
            if os.environ.get(bstack11ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᙼ")) and eval(
                    os.environ.get(bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᙽ"))):
                return
            if (bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᙾ") in config and not config[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᙿ")]):
                os.environ[bstack11ll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ ")] = str(True)
                bstack1ll1l1lll11_opy_ = {bstack11ll11l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩᚁ"): hostname}
                bstack11111ll11l_opy_(bstack11ll11l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᚂ"), bstack11ll11l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧᚃ"), bstack1ll1l1lll11_opy_, logger)
    except Exception as e:
        pass
def bstack1ll11ll1l_opy_(caps, bstack1ll1l1ll1ll_opy_):
    if bstack11ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᚄ") in caps:
        caps[bstack11ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚅ")][bstack11ll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᚆ")] = True
        if bstack1ll1l1ll1ll_opy_:
            caps[bstack11ll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᚇ")][bstack11ll11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᚈ")] = bstack1ll1l1ll1ll_opy_
    else:
        caps[bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ᚉ")] = True
        if bstack1ll1l1ll1ll_opy_:
            caps[bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᚊ")] = bstack1ll1l1ll1ll_opy_
def bstack1ll1ll1llll_opy_(bstack11l1ll1lll_opy_):
    bstack1ll1l1lll1l_opy_ = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᚋ"), bstack11ll11l_opy_ (u"ࠫࠬᚌ"))
    if bstack1ll1l1lll1l_opy_ == bstack11ll11l_opy_ (u"ࠬ࠭ᚍ") or bstack1ll1l1lll1l_opy_ == bstack11ll11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᚎ"):
        threading.current_thread().testStatus = bstack11l1ll1lll_opy_
    else:
        if bstack11l1ll1lll_opy_ == bstack11ll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᚏ"):
            threading.current_thread().testStatus = bstack11l1ll1lll_opy_