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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11ll11l1ll_opy_ import bstack11ll1111ll_opy_, bstack11ll11lll1_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1ll111l1_opy_
from bstack_utils.helper import bstack11lll1l111_opy_, bstack1lll1ll1l_opy_, Result
from bstack_utils.bstack111111ll_opy_ import bstack1l11l1ll1_opy_
from bstack_utils.capture import bstack11ll1l111l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1llll1l1l_opy_:
    def __init__(self):
        self.bstack11ll11l1l1_opy_ = bstack11ll1l111l_opy_(self.bstack11ll111lll_opy_)
        self.tests = {}
    @staticmethod
    def bstack11ll111lll_opy_(log):
        if not (log[bstack1l1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧะ")] and log[bstack1l1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨั")].strip()):
            return
        active = bstack1ll111l1_opy_.bstack11ll1l1lll_opy_()
        log = {
            bstack1l1l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧา"): log[bstack1l1l1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨำ")],
            bstack1l1l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ิ"): bstack1lll1ll1l_opy_(),
            bstack1l1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬี"): log[bstack1l1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ึ")],
        }
        if active:
            if active[bstack1l1l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫื")] == bstack1l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ุࠬ"):
                log[bstack1l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨู")] = active[bstack1l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥฺࠩ")]
            elif active[bstack1l1l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨ฻")] == bstack1l1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ฼"):
                log[bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ฽")] = active[bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭฾")]
        bstack1l11l1ll1_opy_.bstack1l11l1l1l1_opy_([log])
    def start_test(self, attrs):
        bstack11ll11ll1l_opy_ = uuid4().__str__()
        self.tests[bstack11ll11ll1l_opy_] = {}
        self.bstack11ll11l1l1_opy_.start()
        driver = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭฿"), None)
        bstack11ll11l1ll_opy_ = bstack11ll11lll1_opy_(
            name=attrs.scenario.name,
            uuid=bstack11ll11ll1l_opy_,
            bstack11ll111l11_opy_=bstack1lll1ll1l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l1l1l_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤเ"),
            framework=bstack1l1l1l_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩแ"),
            scope=[attrs.feature.name],
            bstack11ll1ll11l_opy_=bstack1l11l1ll1_opy_.bstack11ll1l1111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11ll11ll1l_opy_][bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭โ")] = bstack11ll11l1ll_opy_
        threading.current_thread().current_test_uuid = bstack11ll11ll1l_opy_
        bstack1l11l1ll1_opy_.bstack11ll1l11l1_opy_(bstack1l1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬใ"), bstack11ll11l1ll_opy_)
    def end_test(self, attrs):
        bstack11ll11l11l_opy_ = {
            bstack1l1l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥไ"): attrs.feature.name,
            bstack1l1l1l_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦๅ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11ll11l1ll_opy_ = self.tests[current_test_uuid][bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪๆ")]
        meta = {
            bstack1l1l1l_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤ็"): bstack11ll11l11l_opy_,
            bstack1l1l1l_opy_ (u"ࠤࡶࡸࡪࡶࡳ่ࠣ"): bstack11ll11l1ll_opy_.meta.get(bstack1l1l1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴ้ࠩ"), []),
            bstack1l1l1l_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ๊"): {
                bstack1l1l1l_opy_ (u"ࠧࡴࡡ࡮ࡧ๋ࠥ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11ll11l1ll_opy_.bstack11ll1l1ll1_opy_(meta)
        bstack11ll11l1ll_opy_.bstack11ll1l1l1l_opy_(bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ์"), []))
        bstack11ll11ll11_opy_, exception = self._11ll11l111_opy_(attrs)
        bstack11ll1l11ll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11ll1l1l11_opy_=[bstack11ll11ll11_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪํ")].stop(time=bstack1lll1ll1l_opy_(), duration=int(attrs.duration)*1000, result=bstack11ll1l11ll_opy_)
        bstack1l11l1ll1_opy_.bstack11ll1l11l1_opy_(bstack1l1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ๎"), self.tests[threading.current_thread().current_test_uuid][bstack1l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ๏")])
    def bstack1lllll1l1l_opy_(self, attrs):
        bstack11ll1ll1ll_opy_ = {
            bstack1l1l1l_opy_ (u"ࠪ࡭ࡩ࠭๐"): uuid4().__str__(),
            bstack1l1l1l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬ๑"): attrs.keyword,
            bstack1l1l1l_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ๒"): [],
            bstack1l1l1l_opy_ (u"࠭ࡴࡦࡺࡷࠫ๓"): attrs.name,
            bstack1l1l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ๔"): bstack1lll1ll1l_opy_(),
            bstack1l1l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ๕"): bstack1l1l1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ๖"),
            bstack1l1l1l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ๗"): bstack1l1l1l_opy_ (u"ࠫࠬ๘")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ๙")].add_step(bstack11ll1ll1ll_opy_)
        threading.current_thread().current_step_uuid = bstack11ll1ll1ll_opy_[bstack1l1l1l_opy_ (u"࠭ࡩࡥࠩ๚")]
    def bstack1l111l1l11_opy_(self, attrs):
        current_test_id = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ๛"), None)
        current_step_uuid = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬ๜"), None)
        bstack11ll11ll11_opy_, exception = self._11ll11l111_opy_(attrs)
        bstack11ll1l11ll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11ll1l1l11_opy_=[bstack11ll11ll11_opy_])
        self.tests[current_test_id][bstack1l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ๝")].bstack11ll111l1l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11ll1l11ll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l1l1lll1l_opy_(self, name, attrs):
        try:
            bstack11ll1ll111_opy_ = uuid4().__str__()
            self.tests[bstack11ll1ll111_opy_] = {}
            self.bstack11ll11l1l1_opy_.start()
            scopes = []
            driver = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ๞"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ๟")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11ll1ll111_opy_)
            if name in [bstack1l1l1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ๠"), bstack1l1l1l_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ๡")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l1l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ๢"), bstack1l1l1l_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣ๣")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l1l1l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ๤")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11ll1111ll_opy_(
                name=name,
                uuid=bstack11ll1ll111_opy_,
                bstack11ll111l11_opy_=bstack1lll1ll1l_opy_(),
                file_path=file_path,
                framework=bstack1l1l1l_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥ๥"),
                bstack11ll1ll11l_opy_=bstack1l11l1ll1_opy_.bstack11ll1l1111_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l1l1l_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ๦"),
                hook_type=name
            )
            self.tests[bstack11ll1ll111_opy_][bstack1l1l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣ๧")] = hook_data
            current_test_id = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥ๨"), None)
            if current_test_id:
                hook_data.bstack11ll111ll1_opy_(current_test_id)
            if name == bstack1l1l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ๩"):
                threading.current_thread().before_all_hook_uuid = bstack11ll1ll111_opy_
            threading.current_thread().current_hook_uuid = bstack11ll1ll111_opy_
            bstack1l11l1ll1_opy_.bstack11ll1l11l1_opy_(bstack1l1l1l_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤ๪"), hook_data)
        except Exception as e:
            logger.debug(bstack1l1l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳࠣ๫"), name, e)
    def bstack111l1lll_opy_(self, attrs):
        bstack11ll1111l1_opy_ = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ๬"), None)
        hook_data = self.tests[bstack11ll1111l1_opy_][bstack1l1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ๭")]
        status = bstack1l1l1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ๮")
        exception = None
        bstack11ll11ll11_opy_ = None
        if hook_data.name == bstack1l1l1l_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ๯"):
            self.bstack11ll11l1l1_opy_.reset()
            bstack11ll11llll_opy_ = self.tests[bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ๰"), None)][bstack1l1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ๱")].result.result
            if bstack11ll11llll_opy_ == bstack1l1l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ๲"):
                if attrs.hook_failures == 1:
                    status = bstack1l1l1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ๳")
                elif attrs.hook_failures == 2:
                    status = bstack1l1l1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ๴")
            elif attrs.bstack11ll1ll1l1_opy_:
                status = bstack1l1l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ๵")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l1l1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ๶") and attrs.hook_failures == 1:
                status = bstack1l1l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ๷")
            elif hasattr(attrs, bstack1l1l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ๸")) and attrs.error_message:
                status = bstack1l1l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ๹")
            bstack11ll11ll11_opy_, exception = self._11ll11l111_opy_(attrs)
        bstack11ll1l11ll_opy_ = Result(result=status, exception=exception, bstack11ll1l1l11_opy_=[bstack11ll11ll11_opy_])
        hook_data.stop(time=bstack1lll1ll1l_opy_(), duration=0, result=bstack11ll1l11ll_opy_)
        bstack1l11l1ll1_opy_.bstack11ll1l11l1_opy_(bstack1l1l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ๺"), self.tests[bstack11ll1111l1_opy_][bstack1l1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ๻")])
        threading.current_thread().current_hook_uuid = None
    def _11ll11l111_opy_(self, attrs):
        try:
            import traceback
            bstack1ll1ll11ll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11ll11ll11_opy_ = bstack1ll1ll11ll_opy_[-1] if bstack1ll1ll11ll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l1l1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡵࡷࡳࡲࠦࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠤ๼"))
            bstack11ll11ll11_opy_ = None
            exception = None
        return bstack11ll11ll11_opy_, exception