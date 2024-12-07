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
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack111llll1ll_opy_, bstack111ll11111_opy_, bstack1l1l1111ll_opy_, bstack11l11l11ll_opy_, bstack1111l111l1_opy_, bstack11111l111l_opy_, bstack11111ll1ll_opy_, bstack1lll1l1ll_opy_
from bstack_utils.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1l1ll_opy_
import bstack_utils.bstack1l11ll1lll_opy_ as bstack1lll1l111_opy_
from bstack_utils.bstack11llll1lll_opy_ import bstack111lllll1_opy_
import bstack_utils.bstack1l11ll1l_opy_ as bstack11llll1111_opy_
from bstack_utils.bstack1ll1l1ll1l_opy_ import bstack1ll1l1ll1l_opy_
from bstack_utils.bstack11ll11ll11_opy_ import bstack11l1lll111_opy_
bstack1ll11lll1ll_opy_ = bstack11ll11l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᛏ")
logger = logging.getLogger(__name__)
class bstack1ll11l11l1_opy_:
    bstack1ll1ll1l1l1_opy_ = None
    bs_config = None
    bstack11ll1ll11_opy_ = None
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def launch(cls, bs_config, bstack11ll1ll11_opy_):
        cls.bs_config = bs_config
        cls.bstack11ll1ll11_opy_ = bstack11ll1ll11_opy_
        try:
            cls.bstack1ll11llll1l_opy_()
            bstack111l1lll1l_opy_ = bstack111llll1ll_opy_(bs_config)
            bstack111llll11l_opy_ = bstack111ll11111_opy_(bs_config)
            data = bstack1lll1l111_opy_.bstack1ll1l111l11_opy_(bs_config, bstack11ll1ll11_opy_)
            config = {
                bstack11ll11l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᛐ"): (bstack111l1lll1l_opy_, bstack111llll11l_opy_),
                bstack11ll11l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᛑ"): cls.default_headers()
            }
            response = bstack1l1l1111ll_opy_(bstack11ll11l_opy_ (u"ࠫࡕࡕࡓࡕࠩᛒ"), cls.request_url(bstack11ll11l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬᛓ")), data, config)
            if response.status_code != 200:
                bstack1ll11lll11l_opy_ = response.json()
                if bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᛔ")] == False:
                    cls.bstack1ll1l111ll1_opy_(bstack1ll11lll11l_opy_)
                    return
                cls.bstack1ll11l1ll11_opy_(bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᛕ")])
                cls.bstack1ll11ll1111_opy_(bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᛖ")])
                return None
            bstack1ll1l111111_opy_ = cls.bstack1ll11ll1ll1_opy_(response)
            return bstack1ll1l111111_opy_
        except Exception as error:
            logger.error(bstack11ll11l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢᛗ").format(str(error)))
            return None
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def stop(cls, bstack1ll11ll1l1l_opy_=None):
        if not bstack111lllll1_opy_.on() and not bstack11llll1111_opy_.on():
            return
        if os.environ.get(bstack11ll11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᛘ")) == bstack11ll11l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᛙ") or os.environ.get(bstack11ll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᛚ")) == bstack11ll11l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᛛ"):
            logger.error(bstack11ll11l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᛜ"))
            return {
                bstack11ll11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᛝ"): bstack11ll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᛞ"),
                bstack11ll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᛟ"): bstack11ll11l_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᛠ")
            }
        try:
            cls.bstack1ll1ll1l1l1_opy_.shutdown()
            data = {
                bstack11ll11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᛡ"): bstack1lll1l1ll_opy_()
            }
            if not bstack1ll11ll1l1l_opy_ is None:
                data[bstack11ll11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪᛢ")] = [{
                    bstack11ll11l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᛣ"): bstack11ll11l_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭ᛤ"),
                    bstack11ll11l_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩᛥ"): bstack1ll11ll1l1l_opy_
                }]
            config = {
                bstack11ll11l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᛦ"): cls.default_headers()
            }
            bstack1lllll1lll1_opy_ = bstack11ll11l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬᛧ").format(os.environ[bstack11ll11l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥᛨ")])
            bstack1ll11l1l1l1_opy_ = cls.request_url(bstack1lllll1lll1_opy_)
            response = bstack1l1l1111ll_opy_(bstack11ll11l_opy_ (u"࠭ࡐࡖࡖࠪᛩ"), bstack1ll11l1l1l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11ll11l_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨᛪ"))
        except Exception as error:
            logger.error(bstack11ll11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧ᛫") + str(error))
            return {
                bstack11ll11l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᛬"): bstack11ll11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ᛭"),
                bstack11ll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᛮ"): str(error)
            }
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1ll11ll1ll1_opy_(cls, response):
        bstack1ll11lll11l_opy_ = response.json()
        bstack1ll1l111111_opy_ = {}
        if bstack1ll11lll11l_opy_.get(bstack11ll11l_opy_ (u"ࠬࡰࡷࡵࠩᛯ")) is None:
            os.environ[bstack11ll11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᛰ")] = bstack11ll11l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᛱ")
        else:
            os.environ[bstack11ll11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᛲ")] = bstack1ll11lll11l_opy_.get(bstack11ll11l_opy_ (u"ࠩ࡭ࡻࡹ࠭ᛳ"), bstack11ll11l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᛴ"))
        os.environ[bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᛵ")] = bstack1ll11lll11l_opy_.get(bstack11ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᛶ"), bstack11ll11l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛷ"))
        if bstack111lllll1_opy_.bstack1ll11l1l1ll_opy_(cls.bs_config, cls.bstack11ll1ll11_opy_.get(bstack11ll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᛸ"), bstack11ll11l_opy_ (u"ࠨࠩ᛹"))) is True:
            bstack1ll1l1111l1_opy_, bstack1llll11l11_opy_, bstack1ll1l1111ll_opy_ = cls.bstack1ll11ll1l11_opy_(bstack1ll11lll11l_opy_)
            if bstack1ll1l1111l1_opy_ != None and bstack1llll11l11_opy_ != None:
                bstack1ll1l111111_opy_[bstack11ll11l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᛺")] = {
                    bstack11ll11l_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭᛻"): bstack1ll1l1111l1_opy_,
                    bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭᛼"): bstack1llll11l11_opy_,
                    bstack11ll11l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ᛽"): bstack1ll1l1111ll_opy_
                }
            else:
                bstack1ll1l111111_opy_[bstack11ll11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᛾")] = {}
        else:
            bstack1ll1l111111_opy_[bstack11ll11l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᛿")] = {}
        if bstack11llll1111_opy_.bstack111ll1ll1l_opy_(cls.bs_config) is True:
            bstack1ll11lll111_opy_, bstack1llll11l11_opy_ = cls.bstack1ll11llll11_opy_(bstack1ll11lll11l_opy_)
            if bstack1ll11lll111_opy_ != None and bstack1llll11l11_opy_ != None:
                bstack1ll1l111111_opy_[bstack11ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜀ")] = {
                    bstack11ll11l_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭ᜁ"): bstack1ll11lll111_opy_,
                    bstack11ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᜂ"): bstack1llll11l11_opy_,
                }
            else:
                bstack1ll1l111111_opy_[bstack11ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᜃ")] = {}
        else:
            bstack1ll1l111111_opy_[bstack11ll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᜄ")] = {}
        if bstack1ll1l111111_opy_[bstack11ll11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᜅ")].get(bstack11ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᜆ")) != None or bstack1ll1l111111_opy_[bstack11ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜇ")].get(bstack11ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᜈ")) != None:
            cls.bstack1ll1l111l1l_opy_(bstack1ll11lll11l_opy_.get(bstack11ll11l_opy_ (u"ࠪ࡮ࡼࡺࠧᜉ")), bstack1ll11lll11l_opy_.get(bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᜊ")))
        return bstack1ll1l111111_opy_
    @classmethod
    def bstack1ll11ll1l11_opy_(cls, bstack1ll11lll11l_opy_):
        if bstack1ll11lll11l_opy_.get(bstack11ll11l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᜋ")) == None:
            cls.bstack1ll11l1ll11_opy_()
            return [None, None, None]
        if bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᜌ")][bstack11ll11l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᜍ")] != True:
            cls.bstack1ll11l1ll11_opy_(bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᜎ")])
            return [None, None, None]
        logger.debug(bstack11ll11l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᜏ"))
        os.environ[bstack11ll11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᜐ")] = bstack11ll11l_opy_ (u"ࠫࡹࡸࡵࡦࠩᜑ")
        if bstack1ll11lll11l_opy_.get(bstack11ll11l_opy_ (u"ࠬࡰࡷࡵࠩᜒ")):
            os.environ[bstack11ll11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᜓ")] = bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠧ࡫ࡹࡷ᜔ࠫ")]
            os.environ[bstack11ll11l_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋ᜕ࠬ")] = json.dumps({
                bstack11ll11l_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ᜖"): bstack111llll1ll_opy_(cls.bs_config),
                bstack11ll11l_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬ᜗"): bstack111ll11111_opy_(cls.bs_config)
            })
        if bstack1ll11lll11l_opy_.get(bstack11ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭᜘")):
            os.environ[bstack11ll11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ᜙")] = bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ᜚")]
        if bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᜛")].get(bstack11ll11l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᜜"), {}).get(bstack11ll11l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭᜝")):
            os.environ[bstack11ll11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ᜞")] = str(bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᜟ")][bstack11ll11l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᜠ")][bstack11ll11l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᜡ")])
        return [bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠧ࡫ࡹࡷࠫᜢ")], bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᜣ")], os.environ[bstack11ll11l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᜤ")]]
    @classmethod
    def bstack1ll11llll11_opy_(cls, bstack1ll11lll11l_opy_):
        if bstack1ll11lll11l_opy_.get(bstack11ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᜥ")) == None:
            cls.bstack1ll11ll1111_opy_()
            return [None, None]
        if bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᜦ")][bstack11ll11l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᜧ")] != True:
            cls.bstack1ll11ll1111_opy_(bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᜨ")])
            return [None, None]
        if bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᜩ")].get(bstack11ll11l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᜪ")):
            logger.debug(bstack11ll11l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᜫ"))
            parsed = json.loads(os.getenv(bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᜬ"), bstack11ll11l_opy_ (u"ࠫࢀࢃࠧᜭ")))
            capabilities = bstack1lll1l111_opy_.bstack1ll11l1l11l_opy_(bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᜮ")][bstack11ll11l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᜯ")][bstack11ll11l_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜰ")], bstack11ll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᜱ"), bstack11ll11l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨᜲ"))
            bstack1ll11lll111_opy_ = capabilities[bstack11ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨᜳ")]
            os.environ[bstack11ll11l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕ᜴ࠩ")] = bstack1ll11lll111_opy_
            parsed[bstack11ll11l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᜵")] = capabilities[bstack11ll11l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᜶")]
            os.environ[bstack11ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ᜷")] = json.dumps(parsed)
            scripts = bstack1lll1l111_opy_.bstack1ll11l1l11l_opy_(bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᜸")][bstack11ll11l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ᜹")][bstack11ll11l_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ᜺")], bstack11ll11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᜻"), bstack11ll11l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭᜼"))
            bstack1ll1l1ll1l_opy_.bstack111llll111_opy_(scripts)
            commands = bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᜽")][bstack11ll11l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ᜾")][bstack11ll11l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩ᜿")].get(bstack11ll11l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᝀ"))
            bstack1ll1l1ll1l_opy_.bstack111ll1l11l_opy_(commands)
            bstack1ll1l1ll1l_opy_.store()
        return [bstack1ll11lll111_opy_, bstack1ll11lll11l_opy_[bstack11ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᝁ")]]
    @classmethod
    def bstack1ll11l1ll11_opy_(cls, response=None):
        os.environ[bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᝂ")] = bstack11ll11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᝃ")
        os.environ[bstack11ll11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᝄ")] = bstack11ll11l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᝅ")
        os.environ[bstack11ll11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᝆ")] = bstack11ll11l_opy_ (u"ࠩࡱࡹࡱࡲࠧᝇ")
        os.environ[bstack11ll11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᝈ")] = bstack11ll11l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᝉ")
        os.environ[bstack11ll11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᝊ")] = bstack11ll11l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᝋ")
        os.environ[bstack11ll11l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᝌ")] = bstack11ll11l_opy_ (u"ࠣࡰࡸࡰࡱࠨᝍ")
        cls.bstack1ll1l111ll1_opy_(response, bstack11ll11l_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤᝎ"))
        return [None, None, None]
    @classmethod
    def bstack1ll11ll1111_opy_(cls, response=None):
        os.environ[bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᝏ")] = bstack11ll11l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᝐ")
        os.environ[bstack11ll11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᝑ")] = bstack11ll11l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᝒ")
        os.environ[bstack11ll11l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᝓ")] = bstack11ll11l_opy_ (u"ࠨࡰࡸࡰࡱ࠭᝔")
        cls.bstack1ll1l111ll1_opy_(response, bstack11ll11l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤ᝕"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l111l1l_opy_(cls, bstack1ll11ll1lll_opy_, bstack1llll11l11_opy_):
        os.environ[bstack11ll11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ᝖")] = bstack1ll11ll1lll_opy_
        os.environ[bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᝗")] = bstack1llll11l11_opy_
    @classmethod
    def bstack1ll1l111ll1_opy_(cls, response=None, product=bstack11ll11l_opy_ (u"ࠧࠨ᝘")):
        if response == None:
            logger.error(product + bstack11ll11l_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣ᝙"))
        for error in response[bstack11ll11l_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ᝚")]:
            bstack1111l1l1l1_opy_ = error[bstack11ll11l_opy_ (u"ࠨ࡭ࡨࡽࠬ᝛")]
            error_message = error[bstack11ll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᝜")]
            if error_message:
                if bstack1111l1l1l1_opy_ == bstack11ll11l_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤ᝝"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11ll11l_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧ᝞") + product + bstack11ll11l_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ᝟"))
    @classmethod
    def bstack1ll11llll1l_opy_(cls):
        if cls.bstack1ll1ll1l1l1_opy_ is not None:
            return
        cls.bstack1ll1ll1l1l1_opy_ = bstack1ll1ll1l1ll_opy_(cls.bstack1ll11l1l111_opy_)
        cls.bstack1ll1ll1l1l1_opy_.start()
    @classmethod
    def bstack11l1ll1111_opy_(cls):
        if cls.bstack1ll1ll1l1l1_opy_ is None:
            return
        cls.bstack1ll1ll1l1l1_opy_.shutdown()
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1ll11l1l111_opy_(cls, bstack11l1l11l1l_opy_, bstack1ll11ll11l1_opy_=bstack11ll11l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᝠ")):
        config = {
            bstack11ll11l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᝡ"): cls.default_headers()
        }
        response = bstack1l1l1111ll_opy_(bstack11ll11l_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᝢ"), cls.request_url(bstack1ll11ll11l1_opy_), bstack11l1l11l1l_opy_, config)
        bstack111lll1lll_opy_ = response.json()
    @classmethod
    def bstack11l1l11111_opy_(cls, bstack11l1l11l1l_opy_, bstack1ll11ll11l1_opy_=bstack11ll11l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᝣ")):
        if not bstack1lll1l111_opy_.bstack1ll11l1llll_opy_(bstack11l1l11l1l_opy_[bstack11ll11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᝤ")]):
            return
        bstack1l1l11l1l1_opy_ = bstack1lll1l111_opy_.bstack1ll1l11111l_opy_(bstack11l1l11l1l_opy_[bstack11ll11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᝥ")], bstack11l1l11l1l_opy_.get(bstack11ll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᝦ")))
        if bstack1l1l11l1l1_opy_ != None:
            if bstack11l1l11l1l_opy_.get(bstack11ll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᝧ")) != None:
                bstack11l1l11l1l_opy_[bstack11ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᝨ")][bstack11ll11l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ᝩ")] = bstack1l1l11l1l1_opy_
            else:
                bstack11l1l11l1l_opy_[bstack11ll11l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᝪ")] = bstack1l1l11l1l1_opy_
        if bstack1ll11ll11l1_opy_ == bstack11ll11l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᝫ"):
            cls.bstack1ll11llll1l_opy_()
            cls.bstack1ll1ll1l1l1_opy_.add(bstack11l1l11l1l_opy_)
        elif bstack1ll11ll11l1_opy_ == bstack11ll11l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᝬ"):
            cls.bstack1ll11l1l111_opy_([bstack11l1l11l1l_opy_], bstack1ll11ll11l1_opy_)
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1l11111l1l_opy_(cls, bstack11l1ll1ll1_opy_):
        bstack1ll11lll1l1_opy_ = []
        for log in bstack11l1ll1ll1_opy_:
            bstack1ll11ll111l_opy_ = {
                bstack11ll11l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ᝭"): bstack11ll11l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨᝮ"),
                bstack11ll11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᝯ"): log[bstack11ll11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᝰ")],
                bstack11ll11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ᝱"): log[bstack11ll11l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᝲ")],
                bstack11ll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫᝳ"): {},
                bstack11ll11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᝴"): log[bstack11ll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᝵")],
            }
            if bstack11ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᝶") in log:
                bstack1ll11ll111l_opy_[bstack11ll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᝷")] = log[bstack11ll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᝸")]
            elif bstack11ll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᝹") in log:
                bstack1ll11ll111l_opy_[bstack11ll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᝺")] = log[bstack11ll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᝻")]
            bstack1ll11lll1l1_opy_.append(bstack1ll11ll111l_opy_)
        cls.bstack11l1l11111_opy_({
            bstack11ll11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ᝼"): bstack11ll11l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ᝽"),
            bstack11ll11l_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭᝾"): bstack1ll11lll1l1_opy_
        })
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1ll11llllll_opy_(cls, steps):
        bstack1ll11l1ll1l_opy_ = []
        for step in steps:
            bstack1ll11l1lll1_opy_ = {
                bstack11ll11l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ᝿"): bstack11ll11l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭ក"),
                bstack11ll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪខ"): step[bstack11ll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫគ")],
                bstack11ll11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩឃ"): step[bstack11ll11l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪង")],
                bstack11ll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩច"): step[bstack11ll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪឆ")],
                bstack11ll11l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬជ"): step[bstack11ll11l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ឈ")]
            }
            if bstack11ll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬញ") in step:
                bstack1ll11l1lll1_opy_[bstack11ll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ដ")] = step[bstack11ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧឋ")]
            elif bstack11ll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨឌ") in step:
                bstack1ll11l1lll1_opy_[bstack11ll11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩឍ")] = step[bstack11ll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪណ")]
            bstack1ll11l1ll1l_opy_.append(bstack1ll11l1lll1_opy_)
        cls.bstack11l1l11111_opy_({
            bstack11ll11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨត"): bstack11ll11l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩថ"),
            bstack11ll11l_opy_ (u"࠭࡬ࡰࡩࡶࠫទ"): bstack1ll11l1ll1l_opy_
        })
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1lllll1l1l_opy_(cls, screenshot):
        cls.bstack11l1l11111_opy_({
            bstack11ll11l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫធ"): bstack11ll11l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬន"),
            bstack11ll11l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧប"): [{
                bstack11ll11l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨផ"): bstack11ll11l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭ព"),
                bstack11ll11l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨភ"): datetime.datetime.utcnow().isoformat() + bstack11ll11l_opy_ (u"࡚࠭ࠨម"),
                bstack11ll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨយ"): screenshot[bstack11ll11l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧរ")],
                bstack11ll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩល"): screenshot[bstack11ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪវ")]
            }]
        }, bstack1ll11ll11l1_opy_=bstack11ll11l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩឝ"))
    @classmethod
    @bstack11l11l11ll_opy_(class_method=True)
    def bstack1l1l1ll11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1l11111_opy_({
            bstack11ll11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩឞ"): bstack11ll11l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪស"),
            bstack11ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩហ"): {
                bstack11ll11l_opy_ (u"ࠣࡷࡸ࡭ࡩࠨឡ"): cls.current_test_uuid(),
                bstack11ll11l_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣអ"): cls.bstack11ll1lll11_opy_(driver)
            }
        })
    @classmethod
    def bstack11ll111l1l_opy_(cls, event: str, bstack11l1l11l1l_opy_: bstack11l1lll111_opy_):
        bstack11l1ll111l_opy_ = {
            bstack11ll11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧឣ"): event,
            bstack11l1l11l1l_opy_.bstack11l1l1l1l1_opy_(): bstack11l1l11l1l_opy_.bstack11l11l1ll1_opy_(event)
        }
        cls.bstack11l1l11111_opy_(bstack11l1ll111l_opy_)
        result = getattr(bstack11l1l11l1l_opy_, bstack11ll11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫឤ"), None)
        if event == bstack11ll11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ឥ"):
            threading.current_thread().bstackTestMeta = {bstack11ll11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ឦ"): bstack11ll11l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨឧ")}
        elif event == bstack11ll11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪឨ"):
            threading.current_thread().bstackTestMeta = {bstack11ll11l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩឩ"): getattr(result, bstack11ll11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪឪ"), bstack11ll11l_opy_ (u"ࠫࠬឫ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11ll11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ឬ"), None) is None or os.environ[bstack11ll11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧឭ")] == bstack11ll11l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧឮ")) and (os.environ.get(bstack11ll11l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ឯ"), None) is None or os.environ[bstack11ll11l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧឰ")] == bstack11ll11l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣឱ")):
            return False
        return True
    @staticmethod
    def bstack1ll11ll11ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll11l11l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11ll11l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪឲ"): bstack11ll11l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨឳ"),
            bstack11ll11l_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩ឴"): bstack11ll11l_opy_ (u"ࠧࡵࡴࡸࡩࠬ឵")
        }
        if os.environ.get(bstack11ll11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩា"), None):
            headers[bstack11ll11l_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩិ")] = bstack11ll11l_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ី").format(os.environ[bstack11ll11l_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧឹ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11ll11l_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫឺ").format(bstack1ll11lll1ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11ll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪុ"), None)
    @staticmethod
    def bstack11ll1lll11_opy_(driver):
        return {
            bstack1111l111l1_opy_(): bstack11111l111l_opy_(driver)
        }
    @staticmethod
    def bstack1ll11lllll1_opy_(exception_info, report):
        return [{bstack11ll11l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪូ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111lllllll_opy_(typename):
        if bstack11ll11l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦួ") in typename:
            return bstack11ll11l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥើ")
        return bstack11ll11l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦឿ")