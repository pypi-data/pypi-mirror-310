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
import re
from bstack_utils.bstack11111ll1l_opy_ import bstack1ll1ll1llll_opy_
def bstack1ll1lll1l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll11l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᘧ")):
        return bstack11ll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᘨ")
    elif fixture_name.startswith(bstack11ll11l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᘩ")):
        return bstack11ll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᘪ")
    elif fixture_name.startswith(bstack11ll11l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᘫ")):
        return bstack11ll11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᘬ")
    elif fixture_name.startswith(bstack11ll11l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᘭ")):
        return bstack11ll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᘮ")
def bstack1ll1llll1l1_opy_(fixture_name):
    return bool(re.match(bstack11ll11l_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᘯ"), fixture_name))
def bstack1ll1llll1ll_opy_(fixture_name):
    return bool(re.match(bstack11ll11l_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᘰ"), fixture_name))
def bstack1ll1ll1lll1_opy_(fixture_name):
    return bool(re.match(bstack11ll11l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᘱ"), fixture_name))
def bstack1ll1lll1111_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll11l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᘲ")):
        return bstack11ll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᘳ"), bstack11ll11l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᘴ")
    elif fixture_name.startswith(bstack11ll11l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᘵ")):
        return bstack11ll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᘶ"), bstack11ll11l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᘷ")
    elif fixture_name.startswith(bstack11ll11l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᘸ")):
        return bstack11ll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᘹ"), bstack11ll11l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᘺ")
    elif fixture_name.startswith(bstack11ll11l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᘻ")):
        return bstack11ll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᘼ"), bstack11ll11l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᘽ")
    return None, None
def bstack1ll1lll1l11_opy_(hook_name):
    if hook_name in [bstack11ll11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᘾ"), bstack11ll11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᘿ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll1lll11ll_opy_(hook_name):
    if hook_name in [bstack11ll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᙀ"), bstack11ll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᙁ")]:
        return bstack11ll11l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᙂ")
    elif hook_name in [bstack11ll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᙃ"), bstack11ll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᙄ")]:
        return bstack11ll11l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᙅ")
    elif hook_name in [bstack11ll11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᙆ"), bstack11ll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᙇ")]:
        return bstack11ll11l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᙈ")
    elif hook_name in [bstack11ll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᙉ"), bstack11ll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᙊ")]:
        return bstack11ll11l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᙋ")
    return hook_name
def bstack1ll1llll11l_opy_(node, scenario):
    if hasattr(node, bstack11ll11l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᙌ")):
        parts = node.nodeid.rsplit(bstack11ll11l_opy_ (u"ࠦࡠࠨᙍ"))
        params = parts[-1]
        return bstack11ll11l_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᙎ").format(scenario.name, params)
    return scenario.name
def bstack1ll1llll111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11ll11l_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᙏ")):
            examples = list(node.callspec.params[bstack11ll11l_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᙐ")].values())
        return examples
    except:
        return []
def bstack1ll1lll1ll1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll1lll111l_opy_(report):
    try:
        status = bstack11ll11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᙑ")
        if report.passed or (report.failed and hasattr(report, bstack11ll11l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᙒ"))):
            status = bstack11ll11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᙓ")
        elif report.skipped:
            status = bstack11ll11l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᙔ")
        bstack1ll1ll1llll_opy_(status)
    except:
        pass
def bstack1l1llllll_opy_(status):
    try:
        bstack1ll1lll1lll_opy_ = bstack11ll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᙕ")
        if status == bstack11ll11l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᙖ"):
            bstack1ll1lll1lll_opy_ = bstack11ll11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᙗ")
        elif status == bstack11ll11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᙘ"):
            bstack1ll1lll1lll_opy_ = bstack11ll11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᙙ")
        bstack1ll1ll1llll_opy_(bstack1ll1lll1lll_opy_)
    except:
        pass
def bstack1ll1lll11l1_opy_(item=None, report=None, summary=None, extra=None):
    return