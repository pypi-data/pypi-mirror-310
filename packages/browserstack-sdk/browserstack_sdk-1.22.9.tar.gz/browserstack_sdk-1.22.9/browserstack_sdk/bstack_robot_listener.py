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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11l1lllll1_opy_ import RobotHandler
from bstack_utils.capture import bstack11ll1l1l11_opy_
from bstack_utils.bstack11ll11ll11_opy_ import bstack11l1lll111_opy_, bstack11ll1l1l1l_opy_, bstack11ll111ll1_opy_
from bstack_utils.bstack11llll1lll_opy_ import bstack111lllll1_opy_
from bstack_utils.bstack1111111l_opy_ import bstack1ll11l11l1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l111111l1_opy_, bstack1lll1l1ll_opy_, Result, \
    bstack11l11l11ll_opy_, bstack11l11lll11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11ll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ๽"): [],
        bstack11ll11l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭๾"): [],
        bstack11ll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ๿"): []
    }
    bstack11l1ll11ll_opy_ = []
    bstack11l1l111l1_opy_ = []
    @staticmethod
    def bstack11ll1ll1l1_opy_(log):
        if not (log[bstack11ll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ຀")] and log[bstack11ll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫກ")].strip()):
            return
        active = bstack111lllll1_opy_.bstack11ll1l11l1_opy_()
        log = {
            bstack11ll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪຂ"): log[bstack11ll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ຃")],
            bstack11ll11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩຄ"): bstack11l11lll11_opy_().isoformat() + bstack11ll11l_opy_ (u"࡛ࠧࠩ຅"),
            bstack11ll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩຆ"): log[bstack11ll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪງ")],
        }
        if active:
            if active[bstack11ll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨຈ")] == bstack11ll11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩຉ"):
                log[bstack11ll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬຊ")] = active[bstack11ll11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭຋")]
            elif active[bstack11ll11l_opy_ (u"ࠧࡵࡻࡳࡩࠬຌ")] == bstack11ll11l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ຍ"):
                log[bstack11ll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩຎ")] = active[bstack11ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪຏ")]
        bstack1ll11l11l1_opy_.bstack1l11111l1l_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11l1llll1l_opy_ = None
        self._11l11ll111_opy_ = None
        self._11l1lll11l_opy_ = OrderedDict()
        self.bstack11ll1111ll_opy_ = bstack11ll1l1l11_opy_(self.bstack11ll1ll1l1_opy_)
    @bstack11l11l11ll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11l11l1l11_opy_()
        if not self._11l1lll11l_opy_.get(attrs.get(bstack11ll11l_opy_ (u"ࠫ࡮ࡪࠧຐ")), None):
            self._11l1lll11l_opy_[attrs.get(bstack11ll11l_opy_ (u"ࠬ࡯ࡤࠨຑ"))] = {}
        bstack11l1l1ll1l_opy_ = bstack11ll111ll1_opy_(
                bstack11l1l11lll_opy_=attrs.get(bstack11ll11l_opy_ (u"࠭ࡩࡥࠩຒ")),
                name=name,
                bstack11ll111lll_opy_=bstack1lll1l1ll_opy_(),
                file_path=os.path.relpath(attrs[bstack11ll11l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧຓ")], start=os.getcwd()) if attrs.get(bstack11ll11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨດ")) != bstack11ll11l_opy_ (u"ࠩࠪຕ") else bstack11ll11l_opy_ (u"ࠪࠫຖ"),
                framework=bstack11ll11l_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪທ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11ll11l_opy_ (u"ࠬ࡯ࡤࠨຘ"), None)
        self._11l1lll11l_opy_[attrs.get(bstack11ll11l_opy_ (u"࠭ࡩࡥࠩນ"))][bstack11ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪບ")] = bstack11l1l1ll1l_opy_
    @bstack11l11l11ll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11l11lll1l_opy_()
        self._11ll111111_opy_(messages)
        for bstack11l11lllll_opy_ in self.bstack11l1ll11ll_opy_:
            bstack11l11lllll_opy_[bstack11ll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪປ")][bstack11ll11l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨຜ")].extend(self.store[bstack11ll11l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩຝ")])
            bstack1ll11l11l1_opy_.bstack11l1l11111_opy_(bstack11l11lllll_opy_)
        self.bstack11l1ll11ll_opy_ = []
        self.store[bstack11ll11l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪພ")] = []
    @bstack11l11l11ll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11ll1111ll_opy_.start()
        if not self._11l1lll11l_opy_.get(attrs.get(bstack11ll11l_opy_ (u"ࠬ࡯ࡤࠨຟ")), None):
            self._11l1lll11l_opy_[attrs.get(bstack11ll11l_opy_ (u"࠭ࡩࡥࠩຠ"))] = {}
        driver = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ມ"), None)
        bstack11ll11ll11_opy_ = bstack11ll111ll1_opy_(
            bstack11l1l11lll_opy_=attrs.get(bstack11ll11l_opy_ (u"ࠨ࡫ࡧࠫຢ")),
            name=name,
            bstack11ll111lll_opy_=bstack1lll1l1ll_opy_(),
            file_path=os.path.relpath(attrs[bstack11ll11l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩຣ")], start=os.getcwd()),
            scope=RobotHandler.bstack11l1l1l111_opy_(attrs.get(bstack11ll11l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ຤"), None)),
            framework=bstack11ll11l_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪລ"),
            tags=attrs[bstack11ll11l_opy_ (u"ࠬࡺࡡࡨࡵࠪ຦")],
            hooks=self.store[bstack11ll11l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬວ")],
            bstack11ll11lll1_opy_=bstack1ll11l11l1_opy_.bstack11ll1lll11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11ll11l_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤຨ").format(bstack11ll11l_opy_ (u"ࠣࠢࠥຩ").join(attrs[bstack11ll11l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧສ")]), name) if attrs[bstack11ll11l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨຫ")] else name
        )
        self._11l1lll11l_opy_[attrs.get(bstack11ll11l_opy_ (u"ࠫ࡮ࡪࠧຬ"))][bstack11ll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨອ")] = bstack11ll11ll11_opy_
        threading.current_thread().current_test_uuid = bstack11ll11ll11_opy_.bstack11l1l1l11l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11ll11l_opy_ (u"࠭ࡩࡥࠩຮ"), None)
        self.bstack11ll111l1l_opy_(bstack11ll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨຯ"), bstack11ll11ll11_opy_)
    @bstack11l11l11ll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11ll1111ll_opy_.reset()
        bstack11l1ll1lll_opy_ = bstack11l1l1l1ll_opy_.get(attrs.get(bstack11ll11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨະ")), bstack11ll11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪັ"))
        self._11l1lll11l_opy_[attrs.get(bstack11ll11l_opy_ (u"ࠪ࡭ࡩ࠭າ"))][bstack11ll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧຳ")].stop(time=bstack1lll1l1ll_opy_(), duration=int(attrs.get(bstack11ll11l_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪິ"), bstack11ll11l_opy_ (u"࠭࠰ࠨີ"))), result=Result(result=bstack11l1ll1lll_opy_, exception=attrs.get(bstack11ll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຶ")), bstack11ll11ll1l_opy_=[attrs.get(bstack11ll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩື"))]))
        self.bstack11ll111l1l_opy_(bstack11ll11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧຸࠫ"), self._11l1lll11l_opy_[attrs.get(bstack11ll11l_opy_ (u"ࠪ࡭ࡩູ࠭"))][bstack11ll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧ຺ࠧ")], True)
        self.store[bstack11ll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩົ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11l11l11ll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11l11l1l11_opy_()
        current_test_id = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨຼ"), None)
        bstack11l11ll1l1_opy_ = current_test_id if bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩຽ"), None) else bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫ຾"), None)
        if attrs.get(bstack11ll11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ຿"), bstack11ll11l_opy_ (u"ࠪࠫເ")).lower() in [bstack11ll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪແ"), bstack11ll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧໂ")]:
            hook_type = bstack11l1l1111l_opy_(attrs.get(bstack11ll11l_opy_ (u"࠭ࡴࡺࡲࡨࠫໃ")), bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫໄ"), None))
            hook_name = bstack11ll11l_opy_ (u"ࠨࡽࢀࠫ໅").format(attrs.get(bstack11ll11l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩໆ"), bstack11ll11l_opy_ (u"ࠪࠫ໇")))
            if hook_type in [bstack11ll11l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ່"), bstack11ll11l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨ້")]:
                hook_name = bstack11ll11l_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃ໊ࠧ").format(bstack11l1l11ll1_opy_.get(hook_type), attrs.get(bstack11ll11l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫໋ࠧ"), bstack11ll11l_opy_ (u"ࠨࠩ໌")))
            bstack11l1ll11l1_opy_ = bstack11ll1l1l1l_opy_(
                bstack11l1l11lll_opy_=bstack11l11ll1l1_opy_ + bstack11ll11l_opy_ (u"ࠩ࠰ࠫໍ") + attrs.get(bstack11ll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨ໎"), bstack11ll11l_opy_ (u"ࠫࠬ໏")).lower(),
                name=hook_name,
                bstack11ll111lll_opy_=bstack1lll1l1ll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11ll11l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ໐")), start=os.getcwd()),
                framework=bstack11ll11l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬ໑"),
                tags=attrs[bstack11ll11l_opy_ (u"ࠧࡵࡣࡪࡷࠬ໒")],
                scope=RobotHandler.bstack11l1l1l111_opy_(attrs.get(bstack11ll11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ໓"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11l1ll11l1_opy_.bstack11l1l1l11l_opy_()
            threading.current_thread().current_hook_id = bstack11l11ll1l1_opy_ + bstack11ll11l_opy_ (u"ࠩ࠰ࠫ໔") + attrs.get(bstack11ll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨ໕"), bstack11ll11l_opy_ (u"ࠫࠬ໖")).lower()
            self.store[bstack11ll11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ໗")] = [bstack11l1ll11l1_opy_.bstack11l1l1l11l_opy_()]
            if bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ໘"), None):
                self.store[bstack11ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ໙")].append(bstack11l1ll11l1_opy_.bstack11l1l1l11l_opy_())
            else:
                self.store[bstack11ll11l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ໚")].append(bstack11l1ll11l1_opy_.bstack11l1l1l11l_opy_())
            if bstack11l11ll1l1_opy_:
                self._11l1lll11l_opy_[bstack11l11ll1l1_opy_ + bstack11ll11l_opy_ (u"ࠩ࠰ࠫ໛") + attrs.get(bstack11ll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨໜ"), bstack11ll11l_opy_ (u"ࠫࠬໝ")).lower()] = { bstack11ll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨໞ"): bstack11l1ll11l1_opy_ }
            bstack1ll11l11l1_opy_.bstack11ll111l1l_opy_(bstack11ll11l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧໟ"), bstack11l1ll11l1_opy_)
        else:
            bstack11ll1l11ll_opy_ = {
                bstack11ll11l_opy_ (u"ࠧࡪࡦࠪ໠"): uuid4().__str__(),
                bstack11ll11l_opy_ (u"ࠨࡶࡨࡼࡹ࠭໡"): bstack11ll11l_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨ໢").format(attrs.get(bstack11ll11l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ໣")), attrs.get(bstack11ll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩ໤"), bstack11ll11l_opy_ (u"ࠬ࠭໥"))) if attrs.get(bstack11ll11l_opy_ (u"࠭ࡡࡳࡩࡶࠫ໦"), []) else attrs.get(bstack11ll11l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ໧")),
                bstack11ll11l_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨ໨"): attrs.get(bstack11ll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ໩"), []),
                bstack11ll11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ໪"): bstack1lll1l1ll_opy_(),
                bstack11ll11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ໫"): bstack11ll11l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭໬"),
                bstack11ll11l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ໭"): attrs.get(bstack11ll11l_opy_ (u"ࠧࡥࡱࡦࠫ໮"), bstack11ll11l_opy_ (u"ࠨࠩ໯"))
            }
            if attrs.get(bstack11ll11l_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪ໰"), bstack11ll11l_opy_ (u"ࠪࠫ໱")) != bstack11ll11l_opy_ (u"ࠫࠬ໲"):
                bstack11ll1l11ll_opy_[bstack11ll11l_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭໳")] = attrs.get(bstack11ll11l_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ໴"))
            if not self.bstack11l1l111l1_opy_:
                self._11l1lll11l_opy_[self._11l11ll1ll_opy_()][bstack11ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໵")].add_step(bstack11ll1l11ll_opy_)
                threading.current_thread().current_step_uuid = bstack11ll1l11ll_opy_[bstack11ll11l_opy_ (u"ࠨ࡫ࡧࠫ໶")]
            self.bstack11l1l111l1_opy_.append(bstack11ll1l11ll_opy_)
    @bstack11l11l11ll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11l11lll1l_opy_()
        self._11ll111111_opy_(messages)
        current_test_id = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ໷"), None)
        bstack11l11ll1l1_opy_ = current_test_id if current_test_id else bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭໸"), None)
        bstack11l11l1l1l_opy_ = bstack11l1l1l1ll_opy_.get(attrs.get(bstack11ll11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ໹")), bstack11ll11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭໺"))
        bstack11l11l11l1_opy_ = attrs.get(bstack11ll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໻"))
        if bstack11l11l1l1l_opy_ != bstack11ll11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ໼") and not attrs.get(bstack11ll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໽")) and self._11l1llll1l_opy_:
            bstack11l11l11l1_opy_ = self._11l1llll1l_opy_
        bstack11ll11l11l_opy_ = Result(result=bstack11l11l1l1l_opy_, exception=bstack11l11l11l1_opy_, bstack11ll11ll1l_opy_=[bstack11l11l11l1_opy_])
        if attrs.get(bstack11ll11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ໾"), bstack11ll11l_opy_ (u"ࠪࠫ໿")).lower() in [bstack11ll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪༀ"), bstack11ll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ༁")]:
            bstack11l11ll1l1_opy_ = current_test_id if current_test_id else bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ༂"), None)
            if bstack11l11ll1l1_opy_:
                bstack11ll11l1ll_opy_ = bstack11l11ll1l1_opy_ + bstack11ll11l_opy_ (u"ࠢ࠮ࠤ༃") + attrs.get(bstack11ll11l_opy_ (u"ࠨࡶࡼࡴࡪ࠭༄"), bstack11ll11l_opy_ (u"ࠩࠪ༅")).lower()
                self._11l1lll11l_opy_[bstack11ll11l1ll_opy_][bstack11ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༆")].stop(time=bstack1lll1l1ll_opy_(), duration=int(attrs.get(bstack11ll11l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ༇"), bstack11ll11l_opy_ (u"ࠬ࠶ࠧ༈"))), result=bstack11ll11l11l_opy_)
                bstack1ll11l11l1_opy_.bstack11ll111l1l_opy_(bstack11ll11l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ༉"), self._11l1lll11l_opy_[bstack11ll11l1ll_opy_][bstack11ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ༊")])
        else:
            bstack11l11ll1l1_opy_ = current_test_id if current_test_id else bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪ་"), None)
            if bstack11l11ll1l1_opy_ and len(self.bstack11l1l111l1_opy_) == 1:
                current_step_uuid = bstack1l111111l1_opy_(threading.current_thread(), bstack11ll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭༌"), None)
                self._11l1lll11l_opy_[bstack11l11ll1l1_opy_][bstack11ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭།")].bstack11ll1l1lll_opy_(current_step_uuid, duration=int(attrs.get(bstack11ll11l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ༎"), bstack11ll11l_opy_ (u"ࠬ࠶ࠧ༏"))), result=bstack11ll11l11l_opy_)
            else:
                self.bstack11l1l1llll_opy_(attrs)
            self.bstack11l1l111l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11ll11l_opy_ (u"࠭ࡨࡵ࡯࡯ࠫ༐"), bstack11ll11l_opy_ (u"ࠧ࡯ࡱࠪ༑")) == bstack11ll11l_opy_ (u"ࠨࡻࡨࡷࠬ༒"):
                return
            self.messages.push(message)
            bstack11l1ll1ll1_opy_ = []
            if bstack111lllll1_opy_.bstack11ll1l11l1_opy_():
                bstack11l1ll1ll1_opy_.append({
                    bstack11ll11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ༓"): bstack1lll1l1ll_opy_(),
                    bstack11ll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༔"): message.get(bstack11ll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༕")),
                    bstack11ll11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ༖"): message.get(bstack11ll11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ༗")),
                    **bstack111lllll1_opy_.bstack11ll1l11l1_opy_()
                })
                if len(bstack11l1ll1ll1_opy_) > 0:
                    bstack1ll11l11l1_opy_.bstack1l11111l1l_opy_(bstack11l1ll1ll1_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1ll11l11l1_opy_.bstack11l1ll1111_opy_()
    def bstack11l1l1llll_opy_(self, bstack11l1l1lll1_opy_):
        if not bstack111lllll1_opy_.bstack11ll1l11l1_opy_():
            return
        kwname = bstack11ll11l_opy_ (u"ࠧࡼࡿࠣࡿࢂ༘࠭").format(bstack11l1l1lll1_opy_.get(bstack11ll11l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ༙")), bstack11l1l1lll1_opy_.get(bstack11ll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ༚"), bstack11ll11l_opy_ (u"ࠪࠫ༛"))) if bstack11l1l1lll1_opy_.get(bstack11ll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩ༜"), []) else bstack11l1l1lll1_opy_.get(bstack11ll11l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ༝"))
        error_message = bstack11ll11l_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧ༞").format(kwname, bstack11l1l1lll1_opy_.get(bstack11ll11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ༟")), str(bstack11l1l1lll1_opy_.get(bstack11ll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ༠"))))
        bstack11ll11111l_opy_ = bstack11ll11l_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣ༡").format(kwname, bstack11l1l1lll1_opy_.get(bstack11ll11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ༢")))
        bstack11ll1111l1_opy_ = error_message if bstack11l1l1lll1_opy_.get(bstack11ll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༣")) else bstack11ll11111l_opy_
        bstack11l1l111ll_opy_ = {
            bstack11ll11l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ༤"): self.bstack11l1l111l1_opy_[-1].get(bstack11ll11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ༥"), bstack1lll1l1ll_opy_()),
            bstack11ll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༦"): bstack11ll1111l1_opy_,
            bstack11ll11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ༧"): bstack11ll11l_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ༨") if bstack11l1l1lll1_opy_.get(bstack11ll11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ༩")) == bstack11ll11l_opy_ (u"ࠫࡋࡇࡉࡍࠩ༪") else bstack11ll11l_opy_ (u"ࠬࡏࡎࡇࡑࠪ༫"),
            **bstack111lllll1_opy_.bstack11ll1l11l1_opy_()
        }
        bstack1ll11l11l1_opy_.bstack1l11111l1l_opy_([bstack11l1l111ll_opy_])
    def _11l11ll1ll_opy_(self):
        for bstack11l1l11lll_opy_ in reversed(self._11l1lll11l_opy_):
            bstack11l1llllll_opy_ = bstack11l1l11lll_opy_
            data = self._11l1lll11l_opy_[bstack11l1l11lll_opy_][bstack11ll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༬")]
            if isinstance(data, bstack11ll1l1l1l_opy_):
                if not bstack11ll11l_opy_ (u"ࠧࡆࡃࡆࡌࠬ༭") in data.bstack11l11ll11l_opy_():
                    return bstack11l1llllll_opy_
            else:
                return bstack11l1llllll_opy_
    def _11ll111111_opy_(self, messages):
        try:
            bstack11l11l1lll_opy_ = BuiltIn().get_variable_value(bstack11ll11l_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢ༮")) in (bstack11l1llll11_opy_.DEBUG, bstack11l1llll11_opy_.TRACE)
            for message, bstack11l1ll1l11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11ll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༯"))
                level = message.get(bstack11ll11l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ༰"))
                if level == bstack11l1llll11_opy_.FAIL:
                    self._11l1llll1l_opy_ = name or self._11l1llll1l_opy_
                    self._11l11ll111_opy_ = bstack11l1ll1l11_opy_.get(bstack11ll11l_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ༱")) if bstack11l11l1lll_opy_ and bstack11l1ll1l11_opy_ else self._11l11ll111_opy_
        except:
            pass
    @classmethod
    def bstack11ll111l1l_opy_(self, event: str, bstack11l1l11l1l_opy_: bstack11l1lll111_opy_, bstack11l1l11l11_opy_=False):
        if event == bstack11ll11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ༲"):
            bstack11l1l11l1l_opy_.set(hooks=self.store[bstack11ll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ༳")])
        if event == bstack11ll11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ༴"):
            event = bstack11ll11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦ༵ࠪ")
        if bstack11l1l11l11_opy_:
            bstack11l1ll111l_opy_ = {
                bstack11ll11l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭༶"): event,
                bstack11l1l11l1l_opy_.bstack11l1l1l1l1_opy_(): bstack11l1l11l1l_opy_.bstack11l11l1ll1_opy_(event)
            }
            self.bstack11l1ll11ll_opy_.append(bstack11l1ll111l_opy_)
        else:
            bstack1ll11l11l1_opy_.bstack11ll111l1l_opy_(event, bstack11l1l11l1l_opy_)
class Messages:
    def __init__(self):
        self._11l1lll1ll_opy_ = []
    def bstack11l11l1l11_opy_(self):
        self._11l1lll1ll_opy_.append([])
    def bstack11l11lll1l_opy_(self):
        return self._11l1lll1ll_opy_.pop() if self._11l1lll1ll_opy_ else list()
    def push(self, message):
        self._11l1lll1ll_opy_[-1].append(message) if self._11l1lll1ll_opy_ else self._11l1lll1ll_opy_.append([message])
class bstack11l1llll11_opy_:
    FAIL = bstack11ll11l_opy_ (u"ࠪࡊࡆࡏࡌࠨ༷")
    ERROR = bstack11ll11l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ༸")
    WARNING = bstack11ll11l_opy_ (u"ࠬ࡝ࡁࡓࡐ༹ࠪ")
    bstack11l1lll1l1_opy_ = bstack11ll11l_opy_ (u"࠭ࡉࡏࡈࡒࠫ༺")
    DEBUG = bstack11ll11l_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭༻")
    TRACE = bstack11ll11l_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧ༼")
    bstack11l1l1ll11_opy_ = [FAIL, ERROR]
def bstack11l1ll1l1l_opy_(bstack11l11llll1_opy_):
    if not bstack11l11llll1_opy_:
        return None
    if bstack11l11llll1_opy_.get(bstack11ll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༽"), None):
        return getattr(bstack11l11llll1_opy_[bstack11ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༾")], bstack11ll11l_opy_ (u"ࠫࡺࡻࡩࡥࠩ༿"), None)
    return bstack11l11llll1_opy_.get(bstack11ll11l_opy_ (u"ࠬࡻࡵࡪࡦࠪཀ"), None)
def bstack11l1l1111l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11ll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬཁ"), bstack11ll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩག")]:
        return
    if hook_type.lower() == bstack11ll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧགྷ"):
        if current_test_uuid is None:
            return bstack11ll11l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ང")
        else:
            return bstack11ll11l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨཅ")
    elif hook_type.lower() == bstack11ll11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ཆ"):
        if current_test_uuid is None:
            return bstack11ll11l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨཇ")
        else:
            return bstack11ll11l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ཈")