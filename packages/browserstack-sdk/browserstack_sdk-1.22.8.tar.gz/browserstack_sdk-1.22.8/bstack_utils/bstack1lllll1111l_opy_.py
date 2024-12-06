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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1111l1l11l_opy_
from browserstack_sdk.bstack1111ll111_opy_ import bstack1l1l1l1l1_opy_
def _1lllll111ll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1llll1lll11_opy_:
    def __init__(self, handler):
        self._1lllll111l1_opy_ = {}
        self._1llll1lllll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1l1l1l1_opy_.version()
        if bstack1111l1l11l_opy_(pytest_version, bstack1l1l1l_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢᓳ")) >= 0:
            self._1lllll111l1_opy_[bstack1l1l1l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓴ")] = Module._register_setup_function_fixture
            self._1lllll111l1_opy_[bstack1l1l1l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᓵ")] = Module._register_setup_module_fixture
            self._1lllll111l1_opy_[bstack1l1l1l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᓶ")] = Class._register_setup_class_fixture
            self._1lllll111l1_opy_[bstack1l1l1l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᓷ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1llll1ll11l_opy_(bstack1l1l1l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᓸ"))
            Module._register_setup_module_fixture = self.bstack1llll1ll11l_opy_(bstack1l1l1l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᓹ"))
            Class._register_setup_class_fixture = self.bstack1llll1ll11l_opy_(bstack1l1l1l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᓺ"))
            Class._register_setup_method_fixture = self.bstack1llll1ll11l_opy_(bstack1l1l1l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᓻ"))
        else:
            self._1lllll111l1_opy_[bstack1l1l1l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᓼ")] = Module._inject_setup_function_fixture
            self._1lllll111l1_opy_[bstack1l1l1l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓽ")] = Module._inject_setup_module_fixture
            self._1lllll111l1_opy_[bstack1l1l1l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓾ")] = Class._inject_setup_class_fixture
            self._1lllll111l1_opy_[bstack1l1l1l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᓿ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1llll1ll11l_opy_(bstack1l1l1l_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᔀ"))
            Module._inject_setup_module_fixture = self.bstack1llll1ll11l_opy_(bstack1l1l1l_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᔁ"))
            Class._inject_setup_class_fixture = self.bstack1llll1ll11l_opy_(bstack1l1l1l_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᔂ"))
            Class._inject_setup_method_fixture = self.bstack1llll1ll11l_opy_(bstack1l1l1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᔃ"))
    def bstack1llll1ll1ll_opy_(self, bstack1llll1ll1l1_opy_, hook_type):
        bstack1lllll11lll_opy_ = id(bstack1llll1ll1l1_opy_.__class__)
        if (bstack1lllll11lll_opy_, hook_type) in self._1llll1lllll_opy_:
            return
        meth = getattr(bstack1llll1ll1l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1llll1lllll_opy_[(bstack1lllll11lll_opy_, hook_type)] = meth
            setattr(bstack1llll1ll1l1_opy_, hook_type, self.bstack1llll1ll111_opy_(hook_type, bstack1lllll11lll_opy_))
    def bstack1lllll1l111_opy_(self, instance, bstack1lllll11l1l_opy_):
        if bstack1lllll11l1l_opy_ == bstack1l1l1l_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᔄ"):
            self.bstack1llll1ll1ll_opy_(instance.obj, bstack1l1l1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᔅ"))
            self.bstack1llll1ll1ll_opy_(instance.obj, bstack1l1l1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥᔆ"))
        if bstack1lllll11l1l_opy_ == bstack1l1l1l_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᔇ"):
            self.bstack1llll1ll1ll_opy_(instance.obj, bstack1l1l1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢᔈ"))
            self.bstack1llll1ll1ll_opy_(instance.obj, bstack1l1l1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦᔉ"))
        if bstack1lllll11l1l_opy_ == bstack1l1l1l_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᔊ"):
            self.bstack1llll1ll1ll_opy_(instance.obj, bstack1l1l1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤᔋ"))
            self.bstack1llll1ll1ll_opy_(instance.obj, bstack1l1l1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨᔌ"))
        if bstack1lllll11l1l_opy_ == bstack1l1l1l_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᔍ"):
            self.bstack1llll1ll1ll_opy_(instance.obj, bstack1l1l1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨᔎ"))
            self.bstack1llll1ll1ll_opy_(instance.obj, bstack1l1l1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥᔏ"))
    @staticmethod
    def bstack1lllll11l11_opy_(hook_type, func, args):
        if hook_type in [bstack1l1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᔐ"), bstack1l1l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᔑ")]:
            _1lllll111ll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1llll1ll111_opy_(self, hook_type, bstack1lllll11lll_opy_):
        def bstack1lllll11ll1_opy_(arg=None):
            self.handler(hook_type, bstack1l1l1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᔒ"))
            result = None
            try:
                bstack1lllll11111_opy_ = self._1llll1lllll_opy_[(bstack1lllll11lll_opy_, hook_type)]
                self.bstack1lllll11l11_opy_(hook_type, bstack1lllll11111_opy_, (arg,))
                result = Result(result=bstack1l1l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᔓ"))
            except Exception as e:
                result = Result(result=bstack1l1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᔔ"), exception=e)
                self.handler(hook_type, bstack1l1l1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᔕ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᔖ"), result)
        def bstack1llll1lll1l_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1l1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᔗ"))
            result = None
            exception = None
            try:
                self.bstack1lllll11l11_opy_(hook_type, self._1llll1lllll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᔘ"))
            except Exception as e:
                result = Result(result=bstack1l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᔙ"), exception=e)
                self.handler(hook_type, bstack1l1l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᔚ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᔛ"), result)
        if hook_type in [bstack1l1l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᔜ"), bstack1l1l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᔝ")]:
            return bstack1llll1lll1l_opy_
        return bstack1lllll11ll1_opy_
    def bstack1llll1ll11l_opy_(self, bstack1lllll11l1l_opy_):
        def bstack1llll1llll1_opy_(this, *args, **kwargs):
            self.bstack1lllll1l111_opy_(this, bstack1lllll11l1l_opy_)
            self._1lllll111l1_opy_[bstack1lllll11l1l_opy_](this, *args, **kwargs)
        return bstack1llll1llll1_opy_