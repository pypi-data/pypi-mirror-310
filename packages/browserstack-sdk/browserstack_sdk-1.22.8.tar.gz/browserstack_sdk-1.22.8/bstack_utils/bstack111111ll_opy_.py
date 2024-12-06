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
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack111ll11lll_opy_, bstack111llll111_opy_, bstack1ll1lll11l_opy_, bstack11l11l11ll_opy_, bstack1llllll1l1l_opy_, bstack1111l1ll1l_opy_, bstack1lllll1llll_opy_, bstack1lll1ll1l_opy_
from bstack_utils.bstack1ll1ll11l11_opy_ import bstack1ll1ll11l1l_opy_
import bstack_utils.bstack1ll11lll_opy_ as bstack1l11lll1l1_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1ll111l1_opy_
import bstack_utils.bstack1ll11lll1_opy_ as bstack11ll11l11_opy_
from bstack_utils.bstack1lll1l11l_opy_ import bstack1lll1l11l_opy_
from bstack_utils.bstack11ll11l1ll_opy_ import bstack11l1l11l11_opy_
bstack1ll11ll1ll1_opy_ = bstack1l1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᛏ")
logger = logging.getLogger(__name__)
class bstack1l11l1ll1_opy_:
    bstack1ll1ll11l11_opy_ = None
    bs_config = None
    bstack11llll11l1_opy_ = None
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def launch(cls, bs_config, bstack11llll11l1_opy_):
        cls.bs_config = bs_config
        cls.bstack11llll11l1_opy_ = bstack11llll11l1_opy_
        try:
            cls.bstack1ll1l111111_opy_()
            bstack111ll1l1l1_opy_ = bstack111ll11lll_opy_(bs_config)
            bstack111ll11l11_opy_ = bstack111llll111_opy_(bs_config)
            data = bstack1l11lll1l1_opy_.bstack1ll1l11111l_opy_(bs_config, bstack11llll11l1_opy_)
            config = {
                bstack1l1l1l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᛐ"): (bstack111ll1l1l1_opy_, bstack111ll11l11_opy_),
                bstack1l1l1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᛑ"): cls.default_headers()
            }
            response = bstack1ll1lll11l_opy_(bstack1l1l1l_opy_ (u"ࠫࡕࡕࡓࡕࠩᛒ"), cls.request_url(bstack1l1l1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬᛓ")), data, config)
            if response.status_code != 200:
                bstack1ll11l1ll11_opy_ = response.json()
                if bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᛔ")] == False:
                    cls.bstack1ll1l1111ll_opy_(bstack1ll11l1ll11_opy_)
                    return
                cls.bstack1ll11l1llll_opy_(bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᛕ")])
                cls.bstack1ll11l1lll1_opy_(bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᛖ")])
                return None
            bstack1ll11l11lll_opy_ = cls.bstack1ll11llll1l_opy_(response)
            return bstack1ll11l11lll_opy_
        except Exception as error:
            logger.error(bstack1l1l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢᛗ").format(str(error)))
            return None
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def stop(cls, bstack1ll11l1l1ll_opy_=None):
        if not bstack1ll111l1_opy_.on() and not bstack11ll11l11_opy_.on():
            return
        if os.environ.get(bstack1l1l1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᛘ")) == bstack1l1l1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᛙ") or os.environ.get(bstack1l1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᛚ")) == bstack1l1l1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᛛ"):
            logger.error(bstack1l1l1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᛜ"))
            return {
                bstack1l1l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᛝ"): bstack1l1l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᛞ"),
                bstack1l1l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᛟ"): bstack1l1l1l_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᛠ")
            }
        try:
            cls.bstack1ll1ll11l11_opy_.shutdown()
            data = {
                bstack1l1l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᛡ"): bstack1lll1ll1l_opy_()
            }
            if not bstack1ll11l1l1ll_opy_ is None:
                data[bstack1l1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪᛢ")] = [{
                    bstack1l1l1l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᛣ"): bstack1l1l1l_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭ᛤ"),
                    bstack1l1l1l_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩᛥ"): bstack1ll11l1l1ll_opy_
                }]
            config = {
                bstack1l1l1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᛦ"): cls.default_headers()
            }
            bstack1llllll111l_opy_ = bstack1l1l1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬᛧ").format(os.environ[bstack1l1l1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥᛨ")])
            bstack1ll11ll111l_opy_ = cls.request_url(bstack1llllll111l_opy_)
            response = bstack1ll1lll11l_opy_(bstack1l1l1l_opy_ (u"࠭ࡐࡖࡖࠪᛩ"), bstack1ll11ll111l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1l1l_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨᛪ"))
        except Exception as error:
            logger.error(bstack1l1l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧ᛫") + str(error))
            return {
                bstack1l1l1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᛬"): bstack1l1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ᛭"),
                bstack1l1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᛮ"): str(error)
            }
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1ll11llll1l_opy_(cls, response):
        bstack1ll11l1ll11_opy_ = response.json()
        bstack1ll11l11lll_opy_ = {}
        if bstack1ll11l1ll11_opy_.get(bstack1l1l1l_opy_ (u"ࠬࡰࡷࡵࠩᛯ")) is None:
            os.environ[bstack1l1l1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᛰ")] = bstack1l1l1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᛱ")
        else:
            os.environ[bstack1l1l1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᛲ")] = bstack1ll11l1ll11_opy_.get(bstack1l1l1l_opy_ (u"ࠩ࡭ࡻࡹ࠭ᛳ"), bstack1l1l1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᛴ"))
        os.environ[bstack1l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᛵ")] = bstack1ll11l1ll11_opy_.get(bstack1l1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᛶ"), bstack1l1l1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛷ"))
        if bstack1ll111l1_opy_.bstack1ll11llll11_opy_(cls.bs_config, cls.bstack11llll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᛸ"), bstack1l1l1l_opy_ (u"ࠨࠩ᛹"))) is True:
            bstack1ll1l1111l1_opy_, bstack1lll1111l1_opy_, bstack1ll11lll1l1_opy_ = cls.bstack1ll11ll1111_opy_(bstack1ll11l1ll11_opy_)
            if bstack1ll1l1111l1_opy_ != None and bstack1lll1111l1_opy_ != None:
                bstack1ll11l11lll_opy_[bstack1l1l1l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᛺")] = {
                    bstack1l1l1l_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭᛻"): bstack1ll1l1111l1_opy_,
                    bstack1l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭᛼"): bstack1lll1111l1_opy_,
                    bstack1l1l1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ᛽"): bstack1ll11lll1l1_opy_
                }
            else:
                bstack1ll11l11lll_opy_[bstack1l1l1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᛾")] = {}
        else:
            bstack1ll11l11lll_opy_[bstack1l1l1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᛿")] = {}
        if bstack11ll11l11_opy_.bstack111ll11111_opy_(cls.bs_config) is True:
            bstack1ll11l1ll1l_opy_, bstack1lll1111l1_opy_ = cls.bstack1ll11lll111_opy_(bstack1ll11l1ll11_opy_)
            if bstack1ll11l1ll1l_opy_ != None and bstack1lll1111l1_opy_ != None:
                bstack1ll11l11lll_opy_[bstack1l1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜀ")] = {
                    bstack1l1l1l_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭ᜁ"): bstack1ll11l1ll1l_opy_,
                    bstack1l1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᜂ"): bstack1lll1111l1_opy_,
                }
            else:
                bstack1ll11l11lll_opy_[bstack1l1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᜃ")] = {}
        else:
            bstack1ll11l11lll_opy_[bstack1l1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᜄ")] = {}
        if bstack1ll11l11lll_opy_[bstack1l1l1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᜅ")].get(bstack1l1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᜆ")) != None or bstack1ll11l11lll_opy_[bstack1l1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜇ")].get(bstack1l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᜈ")) != None:
            cls.bstack1ll11l1l111_opy_(bstack1ll11l1ll11_opy_.get(bstack1l1l1l_opy_ (u"ࠪ࡮ࡼࡺࠧᜉ")), bstack1ll11l1ll11_opy_.get(bstack1l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᜊ")))
        return bstack1ll11l11lll_opy_
    @classmethod
    def bstack1ll11ll1111_opy_(cls, bstack1ll11l1ll11_opy_):
        if bstack1ll11l1ll11_opy_.get(bstack1l1l1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᜋ")) == None:
            cls.bstack1ll11l1llll_opy_()
            return [None, None, None]
        if bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᜌ")][bstack1l1l1l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᜍ")] != True:
            cls.bstack1ll11l1llll_opy_(bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᜎ")])
            return [None, None, None]
        logger.debug(bstack1l1l1l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᜏ"))
        os.environ[bstack1l1l1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᜐ")] = bstack1l1l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᜑ")
        if bstack1ll11l1ll11_opy_.get(bstack1l1l1l_opy_ (u"ࠬࡰࡷࡵࠩᜒ")):
            os.environ[bstack1l1l1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᜓ")] = bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠧ࡫ࡹࡷ᜔ࠫ")]
            os.environ[bstack1l1l1l_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋ᜕ࠬ")] = json.dumps({
                bstack1l1l1l_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ᜖"): bstack111ll11lll_opy_(cls.bs_config),
                bstack1l1l1l_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬ᜗"): bstack111llll111_opy_(cls.bs_config)
            })
        if bstack1ll11l1ll11_opy_.get(bstack1l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭᜘")):
            os.environ[bstack1l1l1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ᜙")] = bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ᜚")]
        if bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᜛")].get(bstack1l1l1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᜜"), {}).get(bstack1l1l1l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭᜝")):
            os.environ[bstack1l1l1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ᜞")] = str(bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᜟ")][bstack1l1l1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᜠ")][bstack1l1l1l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᜡ")])
        return [bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠧ࡫ࡹࡷࠫᜢ")], bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᜣ")], os.environ[bstack1l1l1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᜤ")]]
    @classmethod
    def bstack1ll11lll111_opy_(cls, bstack1ll11l1ll11_opy_):
        if bstack1ll11l1ll11_opy_.get(bstack1l1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᜥ")) == None:
            cls.bstack1ll11l1lll1_opy_()
            return [None, None]
        if bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᜦ")][bstack1l1l1l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᜧ")] != True:
            cls.bstack1ll11l1lll1_opy_(bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᜨ")])
            return [None, None]
        if bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᜩ")].get(bstack1l1l1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᜪ")):
            logger.debug(bstack1l1l1l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᜫ"))
            parsed = json.loads(os.getenv(bstack1l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᜬ"), bstack1l1l1l_opy_ (u"ࠫࢀࢃࠧᜭ")))
            capabilities = bstack1l11lll1l1_opy_.bstack1ll11llllll_opy_(bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᜮ")][bstack1l1l1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᜯ")][bstack1l1l1l_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜰ")], bstack1l1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᜱ"), bstack1l1l1l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨᜲ"))
            bstack1ll11l1ll1l_opy_ = capabilities[bstack1l1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨᜳ")]
            os.environ[bstack1l1l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕ᜴ࠩ")] = bstack1ll11l1ll1l_opy_
            parsed[bstack1l1l1l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᜵")] = capabilities[bstack1l1l1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᜶")]
            os.environ[bstack1l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ᜷")] = json.dumps(parsed)
            scripts = bstack1l11lll1l1_opy_.bstack1ll11llllll_opy_(bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᜸")][bstack1l1l1l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ᜹")][bstack1l1l1l_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ᜺")], bstack1l1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᜻"), bstack1l1l1l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭᜼"))
            bstack1lll1l11l_opy_.bstack111ll1111l_opy_(scripts)
            commands = bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᜽")][bstack1l1l1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ᜾")][bstack1l1l1l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩ᜿")].get(bstack1l1l1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᝀ"))
            bstack1lll1l11l_opy_.bstack111ll111l1_opy_(commands)
            bstack1lll1l11l_opy_.store()
        return [bstack1ll11l1ll1l_opy_, bstack1ll11l1ll11_opy_[bstack1l1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᝁ")]]
    @classmethod
    def bstack1ll11l1llll_opy_(cls, response=None):
        os.environ[bstack1l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᝂ")] = bstack1l1l1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᝃ")
        os.environ[bstack1l1l1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᝄ")] = bstack1l1l1l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᝅ")
        os.environ[bstack1l1l1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᝆ")] = bstack1l1l1l_opy_ (u"ࠩࡱࡹࡱࡲࠧᝇ")
        os.environ[bstack1l1l1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᝈ")] = bstack1l1l1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᝉ")
        os.environ[bstack1l1l1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᝊ")] = bstack1l1l1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᝋ")
        os.environ[bstack1l1l1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᝌ")] = bstack1l1l1l_opy_ (u"ࠣࡰࡸࡰࡱࠨᝍ")
        cls.bstack1ll1l1111ll_opy_(response, bstack1l1l1l_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤᝎ"))
        return [None, None, None]
    @classmethod
    def bstack1ll11l1lll1_opy_(cls, response=None):
        os.environ[bstack1l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᝏ")] = bstack1l1l1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᝐ")
        os.environ[bstack1l1l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᝑ")] = bstack1l1l1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᝒ")
        os.environ[bstack1l1l1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᝓ")] = bstack1l1l1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭᝔")
        cls.bstack1ll1l1111ll_opy_(response, bstack1l1l1l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤ᝕"))
        return [None, None, None]
    @classmethod
    def bstack1ll11l1l111_opy_(cls, bstack1ll1l111l11_opy_, bstack1lll1111l1_opy_):
        os.environ[bstack1l1l1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ᝖")] = bstack1ll1l111l11_opy_
        os.environ[bstack1l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᝗")] = bstack1lll1111l1_opy_
    @classmethod
    def bstack1ll1l1111ll_opy_(cls, response=None, product=bstack1l1l1l_opy_ (u"ࠧࠨ᝘")):
        if response == None:
            logger.error(product + bstack1l1l1l_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣ᝙"))
        for error in response[bstack1l1l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ᝚")]:
            bstack1111111111_opy_ = error[bstack1l1l1l_opy_ (u"ࠨ࡭ࡨࡽࠬ᝛")]
            error_message = error[bstack1l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᝜")]
            if error_message:
                if bstack1111111111_opy_ == bstack1l1l1l_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤ᝝"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1l1l_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧ᝞") + product + bstack1l1l1l_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ᝟"))
    @classmethod
    def bstack1ll1l111111_opy_(cls):
        if cls.bstack1ll1ll11l11_opy_ is not None:
            return
        cls.bstack1ll1ll11l11_opy_ = bstack1ll1ll11l1l_opy_(cls.bstack1ll11ll11l1_opy_)
        cls.bstack1ll1ll11l11_opy_.start()
    @classmethod
    def bstack11l1ll111l_opy_(cls):
        if cls.bstack1ll1ll11l11_opy_ is None:
            return
        cls.bstack1ll1ll11l11_opy_.shutdown()
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1ll11ll11l1_opy_(cls, bstack11l1l1llll_opy_, bstack1ll11lll11l_opy_=bstack1l1l1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᝠ")):
        config = {
            bstack1l1l1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᝡ"): cls.default_headers()
        }
        response = bstack1ll1lll11l_opy_(bstack1l1l1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᝢ"), cls.request_url(bstack1ll11lll11l_opy_), bstack11l1l1llll_opy_, config)
        bstack111ll111ll_opy_ = response.json()
    @classmethod
    def bstack11l11l1lll_opy_(cls, bstack11l1l1llll_opy_, bstack1ll11lll11l_opy_=bstack1l1l1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᝣ")):
        if not bstack1l11lll1l1_opy_.bstack1ll11ll1l1l_opy_(bstack11l1l1llll_opy_[bstack1l1l1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᝤ")]):
            return
        bstack111llllll_opy_ = bstack1l11lll1l1_opy_.bstack1ll11lllll1_opy_(bstack11l1l1llll_opy_[bstack1l1l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᝥ")], bstack11l1l1llll_opy_.get(bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᝦ")))
        if bstack111llllll_opy_ != None:
            if bstack11l1l1llll_opy_.get(bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᝧ")) != None:
                bstack11l1l1llll_opy_[bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᝨ")][bstack1l1l1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ᝩ")] = bstack111llllll_opy_
            else:
                bstack11l1l1llll_opy_[bstack1l1l1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᝪ")] = bstack111llllll_opy_
        if bstack1ll11lll11l_opy_ == bstack1l1l1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᝫ"):
            cls.bstack1ll1l111111_opy_()
            cls.bstack1ll1ll11l11_opy_.add(bstack11l1l1llll_opy_)
        elif bstack1ll11lll11l_opy_ == bstack1l1l1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᝬ"):
            cls.bstack1ll11ll11l1_opy_([bstack11l1l1llll_opy_], bstack1ll11lll11l_opy_)
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1l11l1l1l1_opy_(cls, bstack11l1lllll1_opy_):
        bstack1ll11lll1ll_opy_ = []
        for log in bstack11l1lllll1_opy_:
            bstack1ll11l1l11l_opy_ = {
                bstack1l1l1l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ᝭"): bstack1l1l1l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨᝮ"),
                bstack1l1l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᝯ"): log[bstack1l1l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᝰ")],
                bstack1l1l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ᝱"): log[bstack1l1l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᝲ")],
                bstack1l1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫᝳ"): {},
                bstack1l1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᝴"): log[bstack1l1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᝵")],
            }
            if bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᝶") in log:
                bstack1ll11l1l11l_opy_[bstack1l1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᝷")] = log[bstack1l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᝸")]
            elif bstack1l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᝹") in log:
                bstack1ll11l1l11l_opy_[bstack1l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᝺")] = log[bstack1l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᝻")]
            bstack1ll11lll1ll_opy_.append(bstack1ll11l1l11l_opy_)
        cls.bstack11l11l1lll_opy_({
            bstack1l1l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ᝼"): bstack1l1l1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ᝽"),
            bstack1l1l1l_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭᝾"): bstack1ll11lll1ll_opy_
        })
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1ll11ll11ll_opy_(cls, steps):
        bstack1ll11ll1lll_opy_ = []
        for step in steps:
            bstack1ll11l1l1l1_opy_ = {
                bstack1l1l1l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ᝿"): bstack1l1l1l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭ក"),
                bstack1l1l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪខ"): step[bstack1l1l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫគ")],
                bstack1l1l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩឃ"): step[bstack1l1l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪង")],
                bstack1l1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩច"): step[bstack1l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪឆ")],
                bstack1l1l1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬជ"): step[bstack1l1l1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ឈ")]
            }
            if bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬញ") in step:
                bstack1ll11l1l1l1_opy_[bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ដ")] = step[bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧឋ")]
            elif bstack1l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨឌ") in step:
                bstack1ll11l1l1l1_opy_[bstack1l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩឍ")] = step[bstack1l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪណ")]
            bstack1ll11ll1lll_opy_.append(bstack1ll11l1l1l1_opy_)
        cls.bstack11l11l1lll_opy_({
            bstack1l1l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨត"): bstack1l1l1l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩថ"),
            bstack1l1l1l_opy_ (u"࠭࡬ࡰࡩࡶࠫទ"): bstack1ll11ll1lll_opy_
        })
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1ll11l1111_opy_(cls, screenshot):
        cls.bstack11l11l1lll_opy_({
            bstack1l1l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫធ"): bstack1l1l1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬន"),
            bstack1l1l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧប"): [{
                bstack1l1l1l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨផ"): bstack1l1l1l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭ព"),
                bstack1l1l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨភ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1l_opy_ (u"࡚࠭ࠨម"),
                bstack1l1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨយ"): screenshot[bstack1l1l1l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧរ")],
                bstack1l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩល"): screenshot[bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪវ")]
            }]
        }, bstack1ll11lll11l_opy_=bstack1l1l1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩឝ"))
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1ll1llllll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l11l1lll_opy_({
            bstack1l1l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩឞ"): bstack1l1l1l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪស"),
            bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩហ"): {
                bstack1l1l1l_opy_ (u"ࠣࡷࡸ࡭ࡩࠨឡ"): cls.current_test_uuid(),
                bstack1l1l1l_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣអ"): cls.bstack11ll1l1111_opy_(driver)
            }
        })
    @classmethod
    def bstack11ll1l11l1_opy_(cls, event: str, bstack11l1l1llll_opy_: bstack11l1l11l11_opy_):
        bstack11l11l1l1l_opy_ = {
            bstack1l1l1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧឣ"): event,
            bstack11l1l1llll_opy_.bstack11l1l11lll_opy_(): bstack11l1l1llll_opy_.bstack11l11ll11l_opy_(event)
        }
        cls.bstack11l11l1lll_opy_(bstack11l11l1l1l_opy_)
        result = getattr(bstack11l1l1llll_opy_, bstack1l1l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫឤ"), None)
        if event == bstack1l1l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ឥ"):
            threading.current_thread().bstackTestMeta = {bstack1l1l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ឦ"): bstack1l1l1l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨឧ")}
        elif event == bstack1l1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪឨ"):
            threading.current_thread().bstackTestMeta = {bstack1l1l1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩឩ"): getattr(result, bstack1l1l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪឪ"), bstack1l1l1l_opy_ (u"ࠫࠬឫ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1l1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ឬ"), None) is None or os.environ[bstack1l1l1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧឭ")] == bstack1l1l1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧឮ")) and (os.environ.get(bstack1l1l1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ឯ"), None) is None or os.environ[bstack1l1l1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧឰ")] == bstack1l1l1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣឱ")):
            return False
        return True
    @staticmethod
    def bstack1ll11ll1l11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11l1ll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1l1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪឲ"): bstack1l1l1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨឳ"),
            bstack1l1l1l_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩ឴"): bstack1l1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ឵")
        }
        if os.environ.get(bstack1l1l1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩា"), None):
            headers[bstack1l1l1l_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩិ")] = bstack1l1l1l_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ី").format(os.environ[bstack1l1l1l_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧឹ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1l1l_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫឺ").format(bstack1ll11ll1ll1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪុ"), None)
    @staticmethod
    def bstack11ll1l1111_opy_(driver):
        return {
            bstack1llllll1l1l_opy_(): bstack1111l1ll1l_opy_(driver)
        }
    @staticmethod
    def bstack1ll1l111l1l_opy_(exception_info, report):
        return [{bstack1l1l1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪូ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111lllll1l_opy_(typename):
        if bstack1l1l1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦួ") in typename:
            return bstack1l1l1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥើ")
        return bstack1l1l1l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦឿ")