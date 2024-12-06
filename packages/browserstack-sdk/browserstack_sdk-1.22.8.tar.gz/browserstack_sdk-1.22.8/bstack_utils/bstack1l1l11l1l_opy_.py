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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack1111ll1l1l_opy_, bstack1llll111l1_opy_, bstack11lll1l111_opy_, bstack11llll1l1_opy_, \
    bstack1111l1ll11_opy_
def bstack1l1lll1l1_opy_(bstack1ll1l1ll1ll_opy_):
    for driver in bstack1ll1l1ll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11ll11l1l_opy_(driver, status, reason=bstack1l1l1l_opy_ (u"ࠬ࠭ᙜ")):
    bstack1l1111lll1_opy_ = Config.bstack111ll1l11_opy_()
    if bstack1l1111lll1_opy_.bstack11l111l1l1_opy_():
        return
    bstack1llllll11_opy_ = bstack111ll1111_opy_(bstack1l1l1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᙝ"), bstack1l1l1l_opy_ (u"ࠧࠨᙞ"), status, reason, bstack1l1l1l_opy_ (u"ࠨࠩᙟ"), bstack1l1l1l_opy_ (u"ࠩࠪᙠ"))
    driver.execute_script(bstack1llllll11_opy_)
def bstack11l111l11_opy_(page, status, reason=bstack1l1l1l_opy_ (u"ࠪࠫᙡ")):
    try:
        if page is None:
            return
        bstack1l1111lll1_opy_ = Config.bstack111ll1l11_opy_()
        if bstack1l1111lll1_opy_.bstack11l111l1l1_opy_():
            return
        bstack1llllll11_opy_ = bstack111ll1111_opy_(bstack1l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᙢ"), bstack1l1l1l_opy_ (u"ࠬ࠭ᙣ"), status, reason, bstack1l1l1l_opy_ (u"࠭ࠧᙤ"), bstack1l1l1l_opy_ (u"ࠧࠨᙥ"))
        page.evaluate(bstack1l1l1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᙦ"), bstack1llllll11_opy_)
    except Exception as e:
        print(bstack1l1l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢᙧ"), e)
def bstack111ll1111_opy_(type, name, status, reason, bstack111ll1lll_opy_, bstack1111l1lll_opy_):
    bstack1ll1l1l1ll_opy_ = {
        bstack1l1l1l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᙨ"): type,
        bstack1l1l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᙩ"): {}
    }
    if type == bstack1l1l1l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᙪ"):
        bstack1ll1l1l1ll_opy_[bstack1l1l1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᙫ")][bstack1l1l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᙬ")] = bstack111ll1lll_opy_
        bstack1ll1l1l1ll_opy_[bstack1l1l1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᙭")][bstack1l1l1l_opy_ (u"ࠩࡧࡥࡹࡧࠧ᙮")] = json.dumps(str(bstack1111l1lll_opy_))
    if type == bstack1l1l1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᙯ"):
        bstack1ll1l1l1ll_opy_[bstack1l1l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᙰ")][bstack1l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᙱ")] = name
    if type == bstack1l1l1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᙲ"):
        bstack1ll1l1l1ll_opy_[bstack1l1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᙳ")][bstack1l1l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᙴ")] = status
        if status == bstack1l1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᙵ") and str(reason) != bstack1l1l1l_opy_ (u"ࠥࠦᙶ"):
            bstack1ll1l1l1ll_opy_[bstack1l1l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᙷ")][bstack1l1l1l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᙸ")] = json.dumps(str(reason))
    bstack1ll1l1l11l_opy_ = bstack1l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᙹ").format(json.dumps(bstack1ll1l1l1ll_opy_))
    return bstack1ll1l1l11l_opy_
def bstack1lll1lll1l_opy_(url, config, logger, bstack1lll11l1l1_opy_=False):
    hostname = bstack1llll111l1_opy_(url)
    is_private = bstack11llll1l1_opy_(hostname)
    try:
        if is_private or bstack1lll11l1l1_opy_:
            file_path = bstack1111ll1l1l_opy_(bstack1l1l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᙺ"), bstack1l1l1l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᙻ"), logger)
            if os.environ.get(bstack1l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᙼ")) and eval(
                    os.environ.get(bstack1l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᙽ"))):
                return
            if (bstack1l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᙾ") in config and not config[bstack1l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᙿ")]):
                os.environ[bstack1l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ ")] = str(True)
                bstack1ll1l1lll11_opy_ = {bstack1l1l1l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩᚁ"): hostname}
                bstack1111l1ll11_opy_(bstack1l1l1l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᚂ"), bstack1l1l1l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧᚃ"), bstack1ll1l1lll11_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1l1111l_opy_(caps, bstack1ll1l1ll11l_opy_):
    if bstack1l1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᚄ") in caps:
        caps[bstack1l1l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚅ")][bstack1l1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᚆ")] = True
        if bstack1ll1l1ll11l_opy_:
            caps[bstack1l1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᚇ")][bstack1l1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᚈ")] = bstack1ll1l1ll11l_opy_
    else:
        caps[bstack1l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ᚉ")] = True
        if bstack1ll1l1ll11l_opy_:
            caps[bstack1l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᚊ")] = bstack1ll1l1ll11l_opy_
def bstack1ll1lll1lll_opy_(bstack11l1lll11l_opy_):
    bstack1ll1l1ll1l1_opy_ = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᚋ"), bstack1l1l1l_opy_ (u"ࠫࠬᚌ"))
    if bstack1ll1l1ll1l1_opy_ == bstack1l1l1l_opy_ (u"ࠬ࠭ᚍ") or bstack1ll1l1ll1l1_opy_ == bstack1l1l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᚎ"):
        threading.current_thread().testStatus = bstack11l1lll11l_opy_
    else:
        if bstack11l1lll11l_opy_ == bstack1l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᚏ"):
            threading.current_thread().testStatus = bstack11l1lll11l_opy_