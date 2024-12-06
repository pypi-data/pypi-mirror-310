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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11l11llll1_opy_ import RobotHandler
from bstack_utils.capture import bstack11ll1l111l_opy_
from bstack_utils.bstack11ll11l1ll_opy_ import bstack11l1l11l11_opy_, bstack11ll1111ll_opy_, bstack11ll11lll1_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1ll111l1_opy_
from bstack_utils.bstack111111ll_opy_ import bstack1l11l1ll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11lll1l111_opy_, bstack1lll1ll1l_opy_, Result, \
    bstack11l11l11ll_opy_, bstack11l11l1l11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ๽"): [],
        bstack1l1l1l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭๾"): [],
        bstack1l1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ๿"): []
    }
    bstack11l11ll1l1_opy_ = []
    bstack11l1ll1ll1_opy_ = []
    @staticmethod
    def bstack11ll111lll_opy_(log):
        if not (log[bstack1l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ຀")] and log[bstack1l1l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫກ")].strip()):
            return
        active = bstack1ll111l1_opy_.bstack11ll1l1lll_opy_()
        log = {
            bstack1l1l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪຂ"): log[bstack1l1l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ຃")],
            bstack1l1l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩຄ"): bstack11l11l1l11_opy_().isoformat() + bstack1l1l1l_opy_ (u"࡛ࠧࠩ຅"),
            bstack1l1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩຆ"): log[bstack1l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪງ")],
        }
        if active:
            if active[bstack1l1l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨຈ")] == bstack1l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩຉ"):
                log[bstack1l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬຊ")] = active[bstack1l1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭຋")]
            elif active[bstack1l1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬຌ")] == bstack1l1l1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ຍ"):
                log[bstack1l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩຎ")] = active[bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪຏ")]
        bstack1l11l1ll1_opy_.bstack1l11l1l1l1_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11l11ll111_opy_ = None
        self._11l11l1ll1_opy_ = None
        self._11ll11111l_opy_ = OrderedDict()
        self.bstack11ll11l1l1_opy_ = bstack11ll1l111l_opy_(self.bstack11ll111lll_opy_)
    @bstack11l11l11ll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11l1l1lll1_opy_()
        if not self._11ll11111l_opy_.get(attrs.get(bstack1l1l1l_opy_ (u"ࠫ࡮ࡪࠧຐ")), None):
            self._11ll11111l_opy_[attrs.get(bstack1l1l1l_opy_ (u"ࠬ࡯ࡤࠨຑ"))] = {}
        bstack11l1lll1l1_opy_ = bstack11ll11lll1_opy_(
                bstack11l1ll1lll_opy_=attrs.get(bstack1l1l1l_opy_ (u"࠭ࡩࡥࠩຒ")),
                name=name,
                bstack11ll111l11_opy_=bstack1lll1ll1l_opy_(),
                file_path=os.path.relpath(attrs[bstack1l1l1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧຓ")], start=os.getcwd()) if attrs.get(bstack1l1l1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨດ")) != bstack1l1l1l_opy_ (u"ࠩࠪຕ") else bstack1l1l1l_opy_ (u"ࠪࠫຖ"),
                framework=bstack1l1l1l_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪທ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l1l1l_opy_ (u"ࠬ࡯ࡤࠨຘ"), None)
        self._11ll11111l_opy_[attrs.get(bstack1l1l1l_opy_ (u"࠭ࡩࡥࠩນ"))][bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪບ")] = bstack11l1lll1l1_opy_
    @bstack11l11l11ll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11l1l1l1l1_opy_()
        self._11l1l1ll1l_opy_(messages)
        for bstack11l1l1l1ll_opy_ in self.bstack11l11ll1l1_opy_:
            bstack11l1l1l1ll_opy_[bstack1l1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪປ")][bstack1l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨຜ")].extend(self.store[bstack1l1l1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩຝ")])
            bstack1l11l1ll1_opy_.bstack11l11l1lll_opy_(bstack11l1l1l1ll_opy_)
        self.bstack11l11ll1l1_opy_ = []
        self.store[bstack1l1l1l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪພ")] = []
    @bstack11l11l11ll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11ll11l1l1_opy_.start()
        if not self._11ll11111l_opy_.get(attrs.get(bstack1l1l1l_opy_ (u"ࠬ࡯ࡤࠨຟ")), None):
            self._11ll11111l_opy_[attrs.get(bstack1l1l1l_opy_ (u"࠭ࡩࡥࠩຠ"))] = {}
        driver = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ມ"), None)
        bstack11ll11l1ll_opy_ = bstack11ll11lll1_opy_(
            bstack11l1ll1lll_opy_=attrs.get(bstack1l1l1l_opy_ (u"ࠨ࡫ࡧࠫຢ")),
            name=name,
            bstack11ll111l11_opy_=bstack1lll1ll1l_opy_(),
            file_path=os.path.relpath(attrs[bstack1l1l1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩຣ")], start=os.getcwd()),
            scope=RobotHandler.bstack11l1ll1l11_opy_(attrs.get(bstack1l1l1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ຤"), None)),
            framework=bstack1l1l1l_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪລ"),
            tags=attrs[bstack1l1l1l_opy_ (u"ࠬࡺࡡࡨࡵࠪ຦")],
            hooks=self.store[bstack1l1l1l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬວ")],
            bstack11ll1ll11l_opy_=bstack1l11l1ll1_opy_.bstack11ll1l1111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l1l1l_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤຨ").format(bstack1l1l1l_opy_ (u"ࠣࠢࠥຩ").join(attrs[bstack1l1l1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧສ")]), name) if attrs[bstack1l1l1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨຫ")] else name
        )
        self._11ll11111l_opy_[attrs.get(bstack1l1l1l_opy_ (u"ࠫ࡮ࡪࠧຬ"))][bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨອ")] = bstack11ll11l1ll_opy_
        threading.current_thread().current_test_uuid = bstack11ll11l1ll_opy_.bstack11l1l1111l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l1l1l_opy_ (u"࠭ࡩࡥࠩຮ"), None)
        self.bstack11ll1l11l1_opy_(bstack1l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨຯ"), bstack11ll11l1ll_opy_)
    @bstack11l11l11ll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11ll11l1l1_opy_.reset()
        bstack11l1lll11l_opy_ = bstack11l1ll1l1l_opy_.get(attrs.get(bstack1l1l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨະ")), bstack1l1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪັ"))
        self._11ll11111l_opy_[attrs.get(bstack1l1l1l_opy_ (u"ࠪ࡭ࡩ࠭າ"))][bstack1l1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧຳ")].stop(time=bstack1lll1ll1l_opy_(), duration=int(attrs.get(bstack1l1l1l_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪິ"), bstack1l1l1l_opy_ (u"࠭࠰ࠨີ"))), result=Result(result=bstack11l1lll11l_opy_, exception=attrs.get(bstack1l1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຶ")), bstack11ll1l1l11_opy_=[attrs.get(bstack1l1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩື"))]))
        self.bstack11ll1l11l1_opy_(bstack1l1l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧຸࠫ"), self._11ll11111l_opy_[attrs.get(bstack1l1l1l_opy_ (u"ࠪ࡭ࡩູ࠭"))][bstack1l1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧ຺ࠧ")], True)
        self.store[bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩົ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11l11l11ll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11l1l1lll1_opy_()
        current_test_id = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨຼ"), None)
        bstack11l11l111l_opy_ = current_test_id if bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩຽ"), None) else bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫ຾"), None)
        if attrs.get(bstack1l1l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ຿"), bstack1l1l1l_opy_ (u"ࠪࠫເ")).lower() in [bstack1l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪແ"), bstack1l1l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧໂ")]:
            hook_type = bstack11l1l1l111_opy_(attrs.get(bstack1l1l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫໃ")), bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫໄ"), None))
            hook_name = bstack1l1l1l_opy_ (u"ࠨࡽࢀࠫ໅").format(attrs.get(bstack1l1l1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩໆ"), bstack1l1l1l_opy_ (u"ࠪࠫ໇")))
            if hook_type in [bstack1l1l1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ່"), bstack1l1l1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨ້")]:
                hook_name = bstack1l1l1l_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃ໊ࠧ").format(bstack11l1l11ll1_opy_.get(hook_type), attrs.get(bstack1l1l1l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫໋ࠧ"), bstack1l1l1l_opy_ (u"ࠨࠩ໌")))
            bstack11l1lll1ll_opy_ = bstack11ll1111ll_opy_(
                bstack11l1ll1lll_opy_=bstack11l11l111l_opy_ + bstack1l1l1l_opy_ (u"ࠩ࠰ࠫໍ") + attrs.get(bstack1l1l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨ໎"), bstack1l1l1l_opy_ (u"ࠫࠬ໏")).lower(),
                name=hook_name,
                bstack11ll111l11_opy_=bstack1lll1ll1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l1l1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ໐")), start=os.getcwd()),
                framework=bstack1l1l1l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬ໑"),
                tags=attrs[bstack1l1l1l_opy_ (u"ࠧࡵࡣࡪࡷࠬ໒")],
                scope=RobotHandler.bstack11l1ll1l11_opy_(attrs.get(bstack1l1l1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ໓"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11l1lll1ll_opy_.bstack11l1l1111l_opy_()
            threading.current_thread().current_hook_id = bstack11l11l111l_opy_ + bstack1l1l1l_opy_ (u"ࠩ࠰ࠫ໔") + attrs.get(bstack1l1l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨ໕"), bstack1l1l1l_opy_ (u"ࠫࠬ໖")).lower()
            self.store[bstack1l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ໗")] = [bstack11l1lll1ll_opy_.bstack11l1l1111l_opy_()]
            if bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ໘"), None):
                self.store[bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ໙")].append(bstack11l1lll1ll_opy_.bstack11l1l1111l_opy_())
            else:
                self.store[bstack1l1l1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ໚")].append(bstack11l1lll1ll_opy_.bstack11l1l1111l_opy_())
            if bstack11l11l111l_opy_:
                self._11ll11111l_opy_[bstack11l11l111l_opy_ + bstack1l1l1l_opy_ (u"ࠩ࠰ࠫ໛") + attrs.get(bstack1l1l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨໜ"), bstack1l1l1l_opy_ (u"ࠫࠬໝ")).lower()] = { bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨໞ"): bstack11l1lll1ll_opy_ }
            bstack1l11l1ll1_opy_.bstack11ll1l11l1_opy_(bstack1l1l1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧໟ"), bstack11l1lll1ll_opy_)
        else:
            bstack11ll1ll1ll_opy_ = {
                bstack1l1l1l_opy_ (u"ࠧࡪࡦࠪ໠"): uuid4().__str__(),
                bstack1l1l1l_opy_ (u"ࠨࡶࡨࡼࡹ࠭໡"): bstack1l1l1l_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨ໢").format(attrs.get(bstack1l1l1l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ໣")), attrs.get(bstack1l1l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩ໤"), bstack1l1l1l_opy_ (u"ࠬ࠭໥"))) if attrs.get(bstack1l1l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ໦"), []) else attrs.get(bstack1l1l1l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ໧")),
                bstack1l1l1l_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨ໨"): attrs.get(bstack1l1l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ໩"), []),
                bstack1l1l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ໪"): bstack1lll1ll1l_opy_(),
                bstack1l1l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ໫"): bstack1l1l1l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭໬"),
                bstack1l1l1l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ໭"): attrs.get(bstack1l1l1l_opy_ (u"ࠧࡥࡱࡦࠫ໮"), bstack1l1l1l_opy_ (u"ࠨࠩ໯"))
            }
            if attrs.get(bstack1l1l1l_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪ໰"), bstack1l1l1l_opy_ (u"ࠪࠫ໱")) != bstack1l1l1l_opy_ (u"ࠫࠬ໲"):
                bstack11ll1ll1ll_opy_[bstack1l1l1l_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭໳")] = attrs.get(bstack1l1l1l_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ໴"))
            if not self.bstack11l1ll1ll1_opy_:
                self._11ll11111l_opy_[self._11l1llllll_opy_()][bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໵")].add_step(bstack11ll1ll1ll_opy_)
                threading.current_thread().current_step_uuid = bstack11ll1ll1ll_opy_[bstack1l1l1l_opy_ (u"ࠨ࡫ࡧࠫ໶")]
            self.bstack11l1ll1ll1_opy_.append(bstack11ll1ll1ll_opy_)
    @bstack11l11l11ll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11l1l1l1l1_opy_()
        self._11l1l1ll1l_opy_(messages)
        current_test_id = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ໷"), None)
        bstack11l11l111l_opy_ = current_test_id if current_test_id else bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭໸"), None)
        bstack11l1lll111_opy_ = bstack11l1ll1l1l_opy_.get(attrs.get(bstack1l1l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ໹")), bstack1l1l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭໺"))
        bstack11l11lllll_opy_ = attrs.get(bstack1l1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໻"))
        if bstack11l1lll111_opy_ != bstack1l1l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ໼") and not attrs.get(bstack1l1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໽")) and self._11l11ll111_opy_:
            bstack11l11lllll_opy_ = self._11l11ll111_opy_
        bstack11ll1l11ll_opy_ = Result(result=bstack11l1lll111_opy_, exception=bstack11l11lllll_opy_, bstack11ll1l1l11_opy_=[bstack11l11lllll_opy_])
        if attrs.get(bstack1l1l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ໾"), bstack1l1l1l_opy_ (u"ࠪࠫ໿")).lower() in [bstack1l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪༀ"), bstack1l1l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ༁")]:
            bstack11l11l111l_opy_ = current_test_id if current_test_id else bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ༂"), None)
            if bstack11l11l111l_opy_:
                bstack11ll1111l1_opy_ = bstack11l11l111l_opy_ + bstack1l1l1l_opy_ (u"ࠢ࠮ࠤ༃") + attrs.get(bstack1l1l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭༄"), bstack1l1l1l_opy_ (u"ࠩࠪ༅")).lower()
                self._11ll11111l_opy_[bstack11ll1111l1_opy_][bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༆")].stop(time=bstack1lll1ll1l_opy_(), duration=int(attrs.get(bstack1l1l1l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ༇"), bstack1l1l1l_opy_ (u"ࠬ࠶ࠧ༈"))), result=bstack11ll1l11ll_opy_)
                bstack1l11l1ll1_opy_.bstack11ll1l11l1_opy_(bstack1l1l1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ༉"), self._11ll11111l_opy_[bstack11ll1111l1_opy_][bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ༊")])
        else:
            bstack11l11l111l_opy_ = current_test_id if current_test_id else bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪ་"), None)
            if bstack11l11l111l_opy_ and len(self.bstack11l1ll1ll1_opy_) == 1:
                current_step_uuid = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭༌"), None)
                self._11ll11111l_opy_[bstack11l11l111l_opy_][bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭།")].bstack11ll111l1l_opy_(current_step_uuid, duration=int(attrs.get(bstack1l1l1l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ༎"), bstack1l1l1l_opy_ (u"ࠬ࠶ࠧ༏"))), result=bstack11ll1l11ll_opy_)
            else:
                self.bstack11l1llll11_opy_(attrs)
            self.bstack11l1ll1ll1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l1l1l_opy_ (u"࠭ࡨࡵ࡯࡯ࠫ༐"), bstack1l1l1l_opy_ (u"ࠧ࡯ࡱࠪ༑")) == bstack1l1l1l_opy_ (u"ࠨࡻࡨࡷࠬ༒"):
                return
            self.messages.push(message)
            bstack11l1lllll1_opy_ = []
            if bstack1ll111l1_opy_.bstack11ll1l1lll_opy_():
                bstack11l1lllll1_opy_.append({
                    bstack1l1l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ༓"): bstack1lll1ll1l_opy_(),
                    bstack1l1l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༔"): message.get(bstack1l1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༕")),
                    bstack1l1l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ༖"): message.get(bstack1l1l1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ༗")),
                    **bstack1ll111l1_opy_.bstack11ll1l1lll_opy_()
                })
                if len(bstack11l1lllll1_opy_) > 0:
                    bstack1l11l1ll1_opy_.bstack1l11l1l1l1_opy_(bstack11l1lllll1_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1l11l1ll1_opy_.bstack11l1ll111l_opy_()
    def bstack11l1llll11_opy_(self, bstack11l1ll11l1_opy_):
        if not bstack1ll111l1_opy_.bstack11ll1l1lll_opy_():
            return
        kwname = bstack1l1l1l_opy_ (u"ࠧࡼࡿࠣࡿࢂ༘࠭").format(bstack11l1ll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ༙")), bstack11l1ll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ༚"), bstack1l1l1l_opy_ (u"ࠪࠫ༛"))) if bstack11l1ll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩ༜"), []) else bstack11l1ll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ༝"))
        error_message = bstack1l1l1l_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧ༞").format(kwname, bstack11l1ll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ༟")), str(bstack11l1ll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ༠"))))
        bstack11l1llll1l_opy_ = bstack1l1l1l_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣ༡").format(kwname, bstack11l1ll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ༢")))
        bstack11l1l1l11l_opy_ = error_message if bstack11l1ll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༣")) else bstack11l1llll1l_opy_
        bstack11l1l11111_opy_ = {
            bstack1l1l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ༤"): self.bstack11l1ll1ll1_opy_[-1].get(bstack1l1l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ༥"), bstack1lll1ll1l_opy_()),
            bstack1l1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༦"): bstack11l1l1l11l_opy_,
            bstack1l1l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ༧"): bstack1l1l1l_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ༨") if bstack11l1ll11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ༩")) == bstack1l1l1l_opy_ (u"ࠫࡋࡇࡉࡍࠩ༪") else bstack1l1l1l_opy_ (u"ࠬࡏࡎࡇࡑࠪ༫"),
            **bstack1ll111l1_opy_.bstack11ll1l1lll_opy_()
        }
        bstack1l11l1ll1_opy_.bstack1l11l1l1l1_opy_([bstack11l1l11111_opy_])
    def _11l1llllll_opy_(self):
        for bstack11l1ll1lll_opy_ in reversed(self._11ll11111l_opy_):
            bstack11l1l111l1_opy_ = bstack11l1ll1lll_opy_
            data = self._11ll11111l_opy_[bstack11l1ll1lll_opy_][bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༬")]
            if isinstance(data, bstack11ll1111ll_opy_):
                if not bstack1l1l1l_opy_ (u"ࠧࡆࡃࡆࡌࠬ༭") in data.bstack11l11lll11_opy_():
                    return bstack11l1l111l1_opy_
            else:
                return bstack11l1l111l1_opy_
    def _11l1l1ll1l_opy_(self, messages):
        try:
            bstack11l1ll1111_opy_ = BuiltIn().get_variable_value(bstack1l1l1l_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢ༮")) in (bstack11l11ll1ll_opy_.DEBUG, bstack11l11ll1ll_opy_.TRACE)
            for message, bstack11l11l11l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༯"))
                level = message.get(bstack1l1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ༰"))
                if level == bstack11l11ll1ll_opy_.FAIL:
                    self._11l11ll111_opy_ = name or self._11l11ll111_opy_
                    self._11l11l1ll1_opy_ = bstack11l11l11l1_opy_.get(bstack1l1l1l_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ༱")) if bstack11l1ll1111_opy_ and bstack11l11l11l1_opy_ else self._11l11l1ll1_opy_
        except:
            pass
    @classmethod
    def bstack11ll1l11l1_opy_(self, event: str, bstack11l1l1llll_opy_: bstack11l1l11l11_opy_, bstack11l1ll11ll_opy_=False):
        if event == bstack1l1l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ༲"):
            bstack11l1l1llll_opy_.set(hooks=self.store[bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ༳")])
        if event == bstack1l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ༴"):
            event = bstack1l1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦ༵ࠪ")
        if bstack11l1ll11ll_opy_:
            bstack11l11l1l1l_opy_ = {
                bstack1l1l1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭༶"): event,
                bstack11l1l1llll_opy_.bstack11l1l11lll_opy_(): bstack11l1l1llll_opy_.bstack11l11ll11l_opy_(event)
            }
            self.bstack11l11ll1l1_opy_.append(bstack11l11l1l1l_opy_)
        else:
            bstack1l11l1ll1_opy_.bstack11ll1l11l1_opy_(event, bstack11l1l1llll_opy_)
class Messages:
    def __init__(self):
        self._11l1l1ll11_opy_ = []
    def bstack11l1l1lll1_opy_(self):
        self._11l1l1ll11_opy_.append([])
    def bstack11l1l1l1l1_opy_(self):
        return self._11l1l1ll11_opy_.pop() if self._11l1l1ll11_opy_ else list()
    def push(self, message):
        self._11l1l1ll11_opy_[-1].append(message) if self._11l1l1ll11_opy_ else self._11l1l1ll11_opy_.append([message])
class bstack11l11ll1ll_opy_:
    FAIL = bstack1l1l1l_opy_ (u"ࠪࡊࡆࡏࡌࠨ༷")
    ERROR = bstack1l1l1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ༸")
    WARNING = bstack1l1l1l_opy_ (u"ࠬ࡝ࡁࡓࡐ༹ࠪ")
    bstack11l11lll1l_opy_ = bstack1l1l1l_opy_ (u"࠭ࡉࡏࡈࡒࠫ༺")
    DEBUG = bstack1l1l1l_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭༻")
    TRACE = bstack1l1l1l_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧ༼")
    bstack11l1l111ll_opy_ = [FAIL, ERROR]
def bstack11ll111111_opy_(bstack11l1l11l1l_opy_):
    if not bstack11l1l11l1l_opy_:
        return None
    if bstack11l1l11l1l_opy_.get(bstack1l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༽"), None):
        return getattr(bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༾")], bstack1l1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ༿"), None)
    return bstack11l1l11l1l_opy_.get(bstack1l1l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪཀ"), None)
def bstack11l1l1l111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬཁ"), bstack1l1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩག")]:
        return
    if hook_type.lower() == bstack1l1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧགྷ"):
        if current_test_uuid is None:
            return bstack1l1l1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ང")
        else:
            return bstack1l1l1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨཅ")
    elif hook_type.lower() == bstack1l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ཆ"):
        if current_test_uuid is None:
            return bstack1l1l1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨཇ")
        else:
            return bstack1l1l1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ཈")