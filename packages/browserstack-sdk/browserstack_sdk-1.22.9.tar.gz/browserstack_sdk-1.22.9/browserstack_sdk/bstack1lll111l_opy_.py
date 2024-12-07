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
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1ll1l1l1_opy_ = {}
        bstack11ll1llll1_opy_ = os.environ.get(bstack11ll11l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪฉ"), bstack11ll11l_opy_ (u"ࠪࠫช"))
        if not bstack11ll1llll1_opy_:
            return bstack1ll1l1l1_opy_
        try:
            bstack11ll1lll1l_opy_ = json.loads(bstack11ll1llll1_opy_)
            if bstack11ll11l_opy_ (u"ࠦࡴࡹࠢซ") in bstack11ll1lll1l_opy_:
                bstack1ll1l1l1_opy_[bstack11ll11l_opy_ (u"ࠧࡵࡳࠣฌ")] = bstack11ll1lll1l_opy_[bstack11ll11l_opy_ (u"ࠨ࡯ࡴࠤญ")]
            if bstack11ll11l_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦฎ") in bstack11ll1lll1l_opy_ or bstack11ll11l_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦฏ") in bstack11ll1lll1l_opy_:
                bstack1ll1l1l1_opy_[bstack11ll11l_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧฐ")] = bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢฑ"), bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢฒ")))
            if bstack11ll11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨณ") in bstack11ll1lll1l_opy_ or bstack11ll11l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦด") in bstack11ll1lll1l_opy_:
                bstack1ll1l1l1_opy_[bstack11ll11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧต")] = bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤถ"), bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢท")))
            if bstack11ll11l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧธ") in bstack11ll1lll1l_opy_ or bstack11ll11l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧน") in bstack11ll1lll1l_opy_:
                bstack1ll1l1l1_opy_[bstack11ll11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨบ")] = bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣป"), bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣผ")))
            if bstack11ll11l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣฝ") in bstack11ll1lll1l_opy_ or bstack11ll11l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨพ") in bstack11ll1lll1l_opy_:
                bstack1ll1l1l1_opy_[bstack11ll11l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢฟ")] = bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦภ"), bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤม")))
            if bstack11ll11l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣย") in bstack11ll1lll1l_opy_ or bstack11ll11l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨร") in bstack11ll1lll1l_opy_:
                bstack1ll1l1l1_opy_[bstack11ll11l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢฤ")] = bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦล"), bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤฦ")))
            if bstack11ll11l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢว") in bstack11ll1lll1l_opy_ or bstack11ll11l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢศ") in bstack11ll1lll1l_opy_:
                bstack1ll1l1l1_opy_[bstack11ll11l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣษ")] = bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥส"), bstack11ll1lll1l_opy_.get(bstack11ll11l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥห")))
            if bstack11ll11l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦฬ") in bstack11ll1lll1l_opy_:
                bstack1ll1l1l1_opy_[bstack11ll11l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧอ")] = bstack11ll1lll1l_opy_[bstack11ll11l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨฮ")]
        except Exception as error:
            logger.error(bstack11ll11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦฯ") +  str(error))
        return bstack1ll1l1l1_opy_