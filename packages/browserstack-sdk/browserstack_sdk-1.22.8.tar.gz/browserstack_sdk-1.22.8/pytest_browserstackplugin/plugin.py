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
import atexit
import datetime
import inspect
import logging
import os
import signal
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l11l1111l_opy_, bstack11lll11l1_opy_, update, bstack1lll1l111l_opy_,
                                       bstack11lll1111_opy_, bstack1l1ll11l_opy_, bstack11lll1l1l_opy_, bstack1ll111l11l_opy_,
                                       bstack1l1l1lll_opy_, bstack11lll11ll_opy_, bstack1l11l11l11_opy_, bstack1lll1lll1_opy_,
                                       bstack1llllllll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1ll11l1l_opy_)
from browserstack_sdk.bstack1111ll111_opy_ import bstack1l1l1l1l1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1lllll1_opy_
from bstack_utils.capture import bstack11ll1l111l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11l1l1l11_opy_, bstack1l1ll1ll1l_opy_, bstack1ll1l1ll1_opy_, \
    bstack1l1llll1_opy_
from bstack_utils.helper import bstack11lll1l111_opy_, bstack1llllll11ll_opy_, bstack11l11l1l11_opy_, bstack1llllll1l1_opy_, bstack1111ll1111_opy_, bstack1lll1ll1l_opy_, \
    bstack11111l1l11_opy_, \
    bstack11111l1ll1_opy_, bstack111l11l11_opy_, bstack1ll11111ll_opy_, bstack1lllllll1l1_opy_, bstack11llllll1l_opy_, Notset, \
    bstack1l11l11lll_opy_, bstack1111l111l1_opy_, bstack11111llll1_opy_, Result, bstack11111ll11l_opy_, bstack1111lll1ll_opy_, bstack11l11l11ll_opy_, \
    bstack1l11111l_opy_, bstack11lll1l1l1_opy_, bstack1ll1l1lll_opy_, bstack1lllll1lll1_opy_
from bstack_utils.bstack1lllll1111l_opy_ import bstack1llll1lll11_opy_
from bstack_utils.messages import bstack11ll1lllll_opy_, bstack1l1llllll1_opy_, bstack11111l1l1_opy_, bstack1ll1l111_opy_, bstack1l1l1l11_opy_, \
    bstack1llll1lll1_opy_, bstack1ll1lllll1_opy_, bstack1l11l11l1_opy_, bstack1ll1ll1l11_opy_, bstack1111l1ll1_opy_, \
    bstack11llll11_opy_, bstack1llll11l11_opy_
from bstack_utils.proxy import bstack1111l111_opy_, bstack1ll1lll1ll_opy_
from bstack_utils.bstack1l1l111ll_opy_ import bstack1ll1llll11l_opy_, bstack1ll1lll1111_opy_, bstack1ll1lll11l1_opy_, bstack1ll1ll1ll1l_opy_, \
    bstack1ll1lll1l1l_opy_, bstack1ll1llll1l1_opy_, bstack1ll1ll1llll_opy_, bstack1l11l11ll_opy_, bstack1ll1lll1l11_opy_
from bstack_utils.bstack11ll1l11_opy_ import bstack1ll11111_opy_
from bstack_utils.bstack1l1l11l1l_opy_ import bstack111ll1111_opy_, bstack1lll1lll1l_opy_, bstack1ll1l1111l_opy_, \
    bstack11ll11l1l_opy_, bstack11l111l11_opy_
from bstack_utils.bstack11ll11l1ll_opy_ import bstack11ll11lll1_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1ll111l1_opy_
import bstack_utils.bstack1ll11lll1_opy_ as bstack11ll11l11_opy_
from bstack_utils.bstack111111ll_opy_ import bstack1l11l1ll1_opy_
from bstack_utils.bstack1lll1l11l_opy_ import bstack1lll1l11l_opy_
from browserstack_sdk.__init__ import bstack1l1ll11l1_opy_
bstack1l11l11l_opy_ = None
bstack1lll11l1_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack1l11l1l1ll_opy_ = None
bstack1llll1ll_opy_ = None
bstack1l11l1l111_opy_ = None
bstack1ll1llll11_opy_ = None
bstack1l11lllll1_opy_ = None
bstack1ll1ll1ll_opy_ = None
bstack1l1l1l1111_opy_ = None
bstack11ll111ll_opy_ = None
bstack1l1111l11_opy_ = None
bstack1l1l1ll1l1_opy_ = None
bstack1llll1l1ll_opy_ = bstack1l1l1l_opy_ (u"ࠩࠪᠠ")
CONFIG = {}
bstack1111l1l1_opy_ = False
bstack111llll1_opy_ = bstack1l1l1l_opy_ (u"ࠪࠫᠡ")
bstack1l1l1l1ll_opy_ = bstack1l1l1l_opy_ (u"ࠫࠬᠢ")
bstack1ll11l1ll1_opy_ = False
bstack11l1lll1l_opy_ = []
bstack11l1ll11_opy_ = bstack11l1l1l11_opy_
bstack1ll111111l1_opy_ = bstack1l1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᠣ")
bstack1llll1lll_opy_ = {}
bstack1l1lll11l_opy_ = False
logger = bstack1l1lllll1_opy_.get_logger(__name__, bstack11l1ll11_opy_)
store = {
    bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᠤ"): []
}
bstack1l1lllll1l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11ll11111l_opy_ = {}
current_test_uuid = None
def bstack111111lll_opy_(page, bstack11ll1l1l_opy_):
    try:
        page.evaluate(bstack1l1l1l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᠥ"),
                      bstack1l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬᠦ") + json.dumps(
                          bstack11ll1l1l_opy_) + bstack1l1l1l_opy_ (u"ࠤࢀࢁࠧᠧ"))
    except Exception as e:
        print(bstack1l1l1l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣᠨ"), e)
def bstack111l1111l_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1l1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᠩ"), bstack1l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪᠪ") + json.dumps(
            message) + bstack1l1l1l_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩᠫ") + json.dumps(level) + bstack1l1l1l_opy_ (u"ࠧࡾࡿࠪᠬ"))
    except Exception as e:
        print(bstack1l1l1l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦᠭ"), e)
def pytest_configure(config):
    bstack1l1111lll1_opy_ = Config.bstack111ll1l11_opy_()
    config.args = bstack1ll111l1_opy_.bstack1ll111ll11l_opy_(config.args)
    bstack1l1111lll1_opy_.bstack1lll1llll_opy_(bstack1ll1l1lll_opy_(config.getoption(bstack1l1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᠮ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1l1lllllll1_opy_ = item.config.getoption(bstack1l1l1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᠯ"))
    plugins = item.config.getoption(bstack1l1l1l_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧᠰ"))
    report = outcome.get_result()
    bstack1l1llllll1l_opy_(item, call, report)
    if bstack1l1l1l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥᠱ") not in plugins or bstack11llllll1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1l1l_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢᠲ"), None)
    page = getattr(item, bstack1l1l1l_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨᠳ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll111l11ll_opy_(item, report, summary, bstack1l1lllllll1_opy_)
    if (page is not None):
        bstack1ll111l11l1_opy_(item, report, summary, bstack1l1lllllll1_opy_)
def bstack1ll111l11ll_opy_(item, report, summary, bstack1l1lllllll1_opy_):
    if report.when == bstack1l1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᠴ") and report.skipped:
        bstack1ll1lll1l11_opy_(report)
    if report.when in [bstack1l1l1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᠵ"), bstack1l1l1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᠶ")]:
        return
    if not bstack1111ll1111_opy_():
        return
    try:
        if (str(bstack1l1lllllll1_opy_).lower() != bstack1l1l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᠷ")):
            item._driver.execute_script(
                bstack1l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪᠸ") + json.dumps(
                    report.nodeid) + bstack1l1l1l_opy_ (u"࠭ࡽࡾࠩᠹ"))
        os.environ[bstack1l1l1l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᠺ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1l1l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣᠻ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᠼ")))
    bstack1llll111ll_opy_ = bstack1l1l1l_opy_ (u"ࠥࠦᠽ")
    bstack1ll1lll1l11_opy_(report)
    if not passed:
        try:
            bstack1llll111ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1l1l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᠾ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1llll111ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1l1l_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᠿ")))
        bstack1llll111ll_opy_ = bstack1l1l1l_opy_ (u"ࠨࠢᡀ")
        if not passed:
            try:
                bstack1llll111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᡁ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1llll111ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬᡂ")
                    + json.dumps(bstack1l1l1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥᡃ"))
                    + bstack1l1l1l_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᡄ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᡅ")
                    + json.dumps(str(bstack1llll111ll_opy_))
                    + bstack1l1l1l_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᡆ")
                )
        except Exception as e:
            summary.append(bstack1l1l1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦᡇ").format(e))
def bstack1ll1111llll_opy_(test_name, error_message):
    try:
        bstack1ll111l111l_opy_ = []
        bstack111ll111l_opy_ = os.environ.get(bstack1l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᡈ"), bstack1l1l1l_opy_ (u"ࠨ࠲ࠪᡉ"))
        bstack11ll1llll1_opy_ = {bstack1l1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᡊ"): test_name, bstack1l1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᡋ"): error_message, bstack1l1l1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᡌ"): bstack111ll111l_opy_}
        bstack1l1lllll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᡍ"))
        if os.path.exists(bstack1l1lllll111_opy_):
            with open(bstack1l1lllll111_opy_) as f:
                bstack1ll111l111l_opy_ = json.load(f)
        bstack1ll111l111l_opy_.append(bstack11ll1llll1_opy_)
        with open(bstack1l1lllll111_opy_, bstack1l1l1l_opy_ (u"࠭ࡷࠨᡎ")) as f:
            json.dump(bstack1ll111l111l_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬᡏ") + str(e))
def bstack1ll111l11l1_opy_(item, report, summary, bstack1l1lllllll1_opy_):
    if report.when in [bstack1l1l1l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᡐ"), bstack1l1l1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᡑ")]:
        return
    if (str(bstack1l1lllllll1_opy_).lower() != bstack1l1l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᡒ")):
        bstack111111lll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᡓ")))
    bstack1llll111ll_opy_ = bstack1l1l1l_opy_ (u"ࠧࠨᡔ")
    bstack1ll1lll1l11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1llll111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᡕ").format(e)
                )
        try:
            if passed:
                bstack11l111l11_opy_(getattr(item, bstack1l1l1l_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᡖ"), None), bstack1l1l1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᡗ"))
            else:
                error_message = bstack1l1l1l_opy_ (u"ࠩࠪᡘ")
                if bstack1llll111ll_opy_:
                    bstack111l1111l_opy_(item._page, str(bstack1llll111ll_opy_), bstack1l1l1l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᡙ"))
                    bstack11l111l11_opy_(getattr(item, bstack1l1l1l_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᡚ"), None), bstack1l1l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᡛ"), str(bstack1llll111ll_opy_))
                    error_message = str(bstack1llll111ll_opy_)
                else:
                    bstack11l111l11_opy_(getattr(item, bstack1l1l1l_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᡜ"), None), bstack1l1l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᡝ"))
                bstack1ll1111llll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1l1l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧᡞ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1l1l1l_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᡟ"), default=bstack1l1l1l_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᡠ"), help=bstack1l1l1l_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᡡ"))
    parser.addoption(bstack1l1l1l_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᡢ"), default=bstack1l1l1l_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧᡣ"), help=bstack1l1l1l_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨᡤ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1l1l_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥᡥ"), action=bstack1l1l1l_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣᡦ"), default=bstack1l1l1l_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥᡧ"),
                         help=bstack1l1l1l_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥᡨ"))
def bstack11ll111lll_opy_(log):
    if not (log[bstack1l1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᡩ")] and log[bstack1l1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᡪ")].strip()):
        return
    active = bstack11ll1l1lll_opy_()
    log = {
        bstack1l1l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᡫ"): log[bstack1l1l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᡬ")],
        bstack1l1l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᡭ"): bstack11l11l1l11_opy_().isoformat() + bstack1l1l1l_opy_ (u"ࠪ࡞ࠬᡮ"),
        bstack1l1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᡯ"): log[bstack1l1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᡰ")],
    }
    if active:
        if active[bstack1l1l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᡱ")] == bstack1l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᡲ"):
            log[bstack1l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᡳ")] = active[bstack1l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᡴ")]
        elif active[bstack1l1l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᡵ")] == bstack1l1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᡶ"):
            log[bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᡷ")] = active[bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᡸ")]
    bstack1l11l1ll1_opy_.bstack1l11l1l1l1_opy_([log])
def bstack11ll1l1lll_opy_():
    if len(store[bstack1l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ᡹")]) > 0 and store[bstack1l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ᡺")][-1]:
        return {
            bstack1l1l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ᡻"): bstack1l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ᡼"),
            bstack1l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᡽"): store[bstack1l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ᡾")][-1]
        }
    if store.get(bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ᡿"), None):
        return {
            bstack1l1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᢀ"): bstack1l1l1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᢁ"),
            bstack1l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᢂ"): store[bstack1l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᢃ")]
        }
    return None
bstack11ll11l1l1_opy_ = bstack11ll1l111l_opy_(bstack11ll111lll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        item._1ll111l1l1l_opy_ = True
        bstack11llll1111_opy_ = bstack11ll11l11_opy_.bstack1l11lll1ll_opy_(bstack11111l1ll1_opy_(item.own_markers))
        item._a11y_test_case = bstack11llll1111_opy_
        if bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᢄ"), None):
            driver = getattr(item, bstack1l1l1l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᢅ"), None)
            item._a11y_started = bstack11ll11l11_opy_.bstack1l111lll1_opy_(driver, bstack11llll1111_opy_)
        if not bstack1l11l1ll1_opy_.on() or bstack1ll111111l1_opy_ != bstack1l1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᢆ"):
            return
        global current_test_uuid, bstack11ll11l1l1_opy_
        bstack11ll11l1l1_opy_.start()
        bstack11l1l11l1l_opy_ = {
            bstack1l1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᢇ"): uuid4().__str__(),
            bstack1l1l1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᢈ"): bstack11l11l1l11_opy_().isoformat() + bstack1l1l1l_opy_ (u"ࠩ࡝ࠫᢉ")
        }
        current_test_uuid = bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᢊ")]
        store[bstack1l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᢋ")] = bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᢌ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11ll11111l_opy_[item.nodeid] = {**_11ll11111l_opy_[item.nodeid], **bstack11l1l11l1l_opy_}
        bstack1ll111l1l11_opy_(item, _11ll11111l_opy_[item.nodeid], bstack1l1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᢍ"))
    except Exception as err:
        print(bstack1l1l1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩᢎ"), str(err))
def pytest_runtest_setup(item):
    global bstack1l1lllll1l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1lllllll1l1_opy_():
        atexit.register(bstack1l1lll1l1_opy_)
        if not bstack1l1lllll1l1_opy_:
            try:
                bstack1ll11111l11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1lllll1lll1_opy_():
                    bstack1ll11111l11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll11111l11_opy_:
                    signal.signal(s, bstack1ll11111ll1_opy_)
                bstack1l1lllll1l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1l1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤᢏ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll1llll11l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᢐ")
    try:
        if not bstack1l11l1ll1_opy_.on():
            return
        bstack11ll11l1l1_opy_.start()
        uuid = uuid4().__str__()
        bstack11l1l11l1l_opy_ = {
            bstack1l1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᢑ"): uuid,
            bstack1l1l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᢒ"): bstack11l11l1l11_opy_().isoformat() + bstack1l1l1l_opy_ (u"ࠬࡠࠧᢓ"),
            bstack1l1l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᢔ"): bstack1l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᢕ"),
            bstack1l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᢖ"): bstack1l1l1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᢗ"),
            bstack1l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᢘ"): bstack1l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᢙ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᢚ")] = item
        store[bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᢛ")] = [uuid]
        if not _11ll11111l_opy_.get(item.nodeid, None):
            _11ll11111l_opy_[item.nodeid] = {bstack1l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᢜ"): [], bstack1l1l1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᢝ"): []}
        _11ll11111l_opy_[item.nodeid][bstack1l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᢞ")].append(bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᢟ")])
        _11ll11111l_opy_[item.nodeid + bstack1l1l1l_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫᢠ")] = bstack11l1l11l1l_opy_
        bstack1ll111111ll_opy_(item, bstack11l1l11l1l_opy_, bstack1l1l1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᢡ"))
    except Exception as err:
        print(bstack1l1l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᢢ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1llll1lll_opy_
        bstack111ll111l_opy_ = 0
        if bstack1ll11l1ll1_opy_ is True:
            bstack111ll111l_opy_ = int(os.environ.get(bstack1l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᢣ")))
        if bstack1lll11lll1_opy_.bstack1lll11111_opy_() == bstack1l1l1l_opy_ (u"ࠣࡶࡵࡹࡪࠨᢤ"):
            if bstack1lll11lll1_opy_.bstack11l111111_opy_() == bstack1l1l1l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᢥ"):
                bstack1ll1111l1l1_opy_ = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᢦ"), None)
                bstack1l1ll1l1l_opy_ = bstack1ll1111l1l1_opy_ + bstack1l1l1l_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᢧ")
                driver = getattr(item, bstack1l1l1l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᢨ"), None)
                bstack1ll111ll1_opy_ = getattr(item, bstack1l1l1l_opy_ (u"࠭࡮ࡢ࡯ࡨᢩࠫ"), None)
                bstack1lll1l11_opy_ = getattr(item, bstack1l1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᢪ"), None)
                PercySDK.screenshot(driver, bstack1l1ll1l1l_opy_, bstack1ll111ll1_opy_=bstack1ll111ll1_opy_, bstack1lll1l11_opy_=bstack1lll1l11_opy_, bstack11ll11lll_opy_=bstack111ll111l_opy_)
        if getattr(item, bstack1l1l1l_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ᢫"), False):
            bstack1l1l1l1l1_opy_.bstack11lll1ll1l_opy_(getattr(item, bstack1l1l1l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ᢬"), None), bstack1llll1lll_opy_, logger, item)
        if not bstack1l11l1ll1_opy_.on():
            return
        bstack11l1l11l1l_opy_ = {
            bstack1l1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᢭"): uuid4().__str__(),
            bstack1l1l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᢮"): bstack11l11l1l11_opy_().isoformat() + bstack1l1l1l_opy_ (u"ࠬࡠࠧ᢯"),
            bstack1l1l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᢰ"): bstack1l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᢱ"),
            bstack1l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᢲ"): bstack1l1l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᢳ"),
            bstack1l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᢴ"): bstack1l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᢵ")
        }
        _11ll11111l_opy_[item.nodeid + bstack1l1l1l_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᢶ")] = bstack11l1l11l1l_opy_
        bstack1ll111111ll_opy_(item, bstack11l1l11l1l_opy_, bstack1l1l1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᢷ"))
    except Exception as err:
        print(bstack1l1l1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭ᢸ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l11l1ll1_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1ll1ll1ll1l_opy_(fixturedef.argname):
        store[bstack1l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧᢹ")] = request.node
    elif bstack1ll1lll1l1l_opy_(fixturedef.argname):
        store[bstack1l1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧᢺ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1l1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᢻ"): fixturedef.argname,
            bstack1l1l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᢼ"): bstack11111l1l11_opy_(outcome),
            bstack1l1l1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᢽ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᢾ")]
        if not _11ll11111l_opy_.get(current_test_item.nodeid, None):
            _11ll11111l_opy_[current_test_item.nodeid] = {bstack1l1l1l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᢿ"): []}
        _11ll11111l_opy_[current_test_item.nodeid][bstack1l1l1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᣀ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1l1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬᣁ"), str(err))
if bstack11llllll1l_opy_() and bstack1l11l1ll1_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11ll11111l_opy_[request.node.nodeid][bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᣂ")].bstack1lllll1l1l_opy_(id(step))
        except Exception as err:
            print(bstack1l1l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩᣃ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11ll11111l_opy_[request.node.nodeid][bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᣄ")].bstack11ll111l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᣅ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11ll11l1ll_opy_: bstack11ll11lll1_opy_ = _11ll11111l_opy_[request.node.nodeid][bstack1l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᣆ")]
            bstack11ll11l1ll_opy_.bstack11ll111l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬᣇ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll111111l1_opy_
        try:
            if not bstack1l11l1ll1_opy_.on() or bstack1ll111111l1_opy_ != bstack1l1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᣈ"):
                return
            global bstack11ll11l1l1_opy_
            bstack11ll11l1l1_opy_.start()
            driver = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩᣉ"), None)
            if not _11ll11111l_opy_.get(request.node.nodeid, None):
                _11ll11111l_opy_[request.node.nodeid] = {}
            bstack11ll11l1ll_opy_ = bstack11ll11lll1_opy_.bstack1ll1l1l1ll1_opy_(
                scenario, feature, request.node,
                name=bstack1ll1llll1l1_opy_(request.node, scenario),
                bstack11ll111l11_opy_=bstack1lll1ll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1l1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ᣊ"),
                tags=bstack1ll1ll1llll_opy_(feature, scenario),
                bstack11ll1ll11l_opy_=bstack1l11l1ll1_opy_.bstack11ll1l1111_opy_(driver) if driver and driver.session_id else {}
            )
            _11ll11111l_opy_[request.node.nodeid][bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᣋ")] = bstack11ll11l1ll_opy_
            bstack1l1lllll11l_opy_(bstack11ll11l1ll_opy_.uuid)
            bstack1l11l1ll1_opy_.bstack11ll1l11l1_opy_(bstack1l1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᣌ"), bstack11ll11l1ll_opy_)
        except Exception as err:
            print(bstack1l1l1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩᣍ"), str(err))
def bstack1ll1111lll1_opy_(bstack11ll1ll111_opy_):
    if bstack11ll1ll111_opy_ in store[bstack1l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᣎ")]:
        store[bstack1l1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᣏ")].remove(bstack11ll1ll111_opy_)
def bstack1l1lllll11l_opy_(bstack11ll11ll1l_opy_):
    store[bstack1l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᣐ")] = bstack11ll11ll1l_opy_
    threading.current_thread().current_test_uuid = bstack11ll11ll1l_opy_
@bstack1l11l1ll1_opy_.bstack1ll11ll1l11_opy_
def bstack1l1llllll1l_opy_(item, call, report):
    global bstack1ll111111l1_opy_
    bstack1l1l11l1ll_opy_ = bstack1lll1ll1l_opy_()
    if hasattr(report, bstack1l1l1l_opy_ (u"ࠫࡸࡺ࡯ࡱࠩᣑ")):
        bstack1l1l11l1ll_opy_ = bstack11111ll11l_opy_(report.stop)
    elif hasattr(report, bstack1l1l1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫᣒ")):
        bstack1l1l11l1ll_opy_ = bstack11111ll11l_opy_(report.start)
    try:
        if getattr(report, bstack1l1l1l_opy_ (u"࠭ࡷࡩࡧࡱࠫᣓ"), bstack1l1l1l_opy_ (u"ࠧࠨᣔ")) == bstack1l1l1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᣕ"):
            bstack11ll11l1l1_opy_.reset()
        if getattr(report, bstack1l1l1l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᣖ"), bstack1l1l1l_opy_ (u"ࠪࠫᣗ")) == bstack1l1l1l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᣘ"):
            if bstack1ll111111l1_opy_ == bstack1l1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᣙ"):
                _11ll11111l_opy_[item.nodeid][bstack1l1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᣚ")] = bstack1l1l11l1ll_opy_
                bstack1ll111l1l11_opy_(item, _11ll11111l_opy_[item.nodeid], bstack1l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᣛ"), report, call)
                store[bstack1l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᣜ")] = None
            elif bstack1ll111111l1_opy_ == bstack1l1l1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᣝ"):
                bstack11ll11l1ll_opy_ = _11ll11111l_opy_[item.nodeid][bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᣞ")]
                bstack11ll11l1ll_opy_.set(hooks=_11ll11111l_opy_[item.nodeid].get(bstack1l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᣟ"), []))
                exception, bstack11ll1l1l11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11ll1l1l11_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1l1l_opy_ (u"ࠬࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠫᣠ"), bstack1l1l1l_opy_ (u"࠭ࠧᣡ"))]
                bstack11ll11l1ll_opy_.stop(time=bstack1l1l11l1ll_opy_, result=Result(result=getattr(report, bstack1l1l1l_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨᣢ"), bstack1l1l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᣣ")), exception=exception, bstack11ll1l1l11_opy_=bstack11ll1l1l11_opy_))
                bstack1l11l1ll1_opy_.bstack11ll1l11l1_opy_(bstack1l1l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᣤ"), _11ll11111l_opy_[item.nodeid][bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᣥ")])
        elif getattr(report, bstack1l1l1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᣦ"), bstack1l1l1l_opy_ (u"ࠬ࠭ᣧ")) in [bstack1l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᣨ"), bstack1l1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᣩ")]:
            bstack11ll1111l1_opy_ = item.nodeid + bstack1l1l1l_opy_ (u"ࠨ࠯ࠪᣪ") + getattr(report, bstack1l1l1l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᣫ"), bstack1l1l1l_opy_ (u"ࠪࠫᣬ"))
            if getattr(report, bstack1l1l1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᣭ"), False):
                hook_type = bstack1l1l1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᣮ") if getattr(report, bstack1l1l1l_opy_ (u"࠭ࡷࡩࡧࡱࠫᣯ"), bstack1l1l1l_opy_ (u"ࠧࠨᣰ")) == bstack1l1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᣱ") else bstack1l1l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᣲ")
                _11ll11111l_opy_[bstack11ll1111l1_opy_] = {
                    bstack1l1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᣳ"): uuid4().__str__(),
                    bstack1l1l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᣴ"): bstack1l1l11l1ll_opy_,
                    bstack1l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᣵ"): hook_type
                }
            _11ll11111l_opy_[bstack11ll1111l1_opy_][bstack1l1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᣶")] = bstack1l1l11l1ll_opy_
            bstack1ll1111lll1_opy_(_11ll11111l_opy_[bstack11ll1111l1_opy_][bstack1l1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᣷")])
            bstack1ll111111ll_opy_(item, _11ll11111l_opy_[bstack11ll1111l1_opy_], bstack1l1l1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ᣸"), report, call)
            if getattr(report, bstack1l1l1l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ᣹"), bstack1l1l1l_opy_ (u"ࠪࠫ᣺")) == bstack1l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ᣻"):
                if getattr(report, bstack1l1l1l_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭᣼"), bstack1l1l1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᣽")) == bstack1l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᣾"):
                    bstack11l1l11l1l_opy_ = {
                        bstack1l1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᣿"): uuid4().__str__(),
                        bstack1l1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᤀ"): bstack1lll1ll1l_opy_(),
                        bstack1l1l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᤁ"): bstack1lll1ll1l_opy_()
                    }
                    _11ll11111l_opy_[item.nodeid] = {**_11ll11111l_opy_[item.nodeid], **bstack11l1l11l1l_opy_}
                    bstack1ll111l1l11_opy_(item, _11ll11111l_opy_[item.nodeid], bstack1l1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᤂ"))
                    bstack1ll111l1l11_opy_(item, _11ll11111l_opy_[item.nodeid], bstack1l1l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᤃ"), report, call)
    except Exception as err:
        print(bstack1l1l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫᤄ"), str(err))
def bstack1ll1111ll11_opy_(test, bstack11l1l11l1l_opy_, result=None, call=None, bstack11lll111ll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11ll11l1ll_opy_ = {
        bstack1l1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᤅ"): bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᤆ")],
        bstack1l1l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᤇ"): bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࠨᤈ"),
        bstack1l1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᤉ"): test.name,
        bstack1l1l1l_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᤊ"): {
            bstack1l1l1l_opy_ (u"࠭࡬ࡢࡰࡪࠫᤋ"): bstack1l1l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᤌ"),
            bstack1l1l1l_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᤍ"): inspect.getsource(test.obj)
        },
        bstack1l1l1l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᤎ"): test.name,
        bstack1l1l1l_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᤏ"): test.name,
        bstack1l1l1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᤐ"): bstack1ll111l1_opy_.bstack11l1ll1l11_opy_(test),
        bstack1l1l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᤑ"): file_path,
        bstack1l1l1l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᤒ"): file_path,
        bstack1l1l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᤓ"): bstack1l1l1l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᤔ"),
        bstack1l1l1l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᤕ"): file_path,
        bstack1l1l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᤖ"): bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᤗ")],
        bstack1l1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᤘ"): bstack1l1l1l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᤙ"),
        bstack1l1l1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᤚ"): {
            bstack1l1l1l_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᤛ"): test.nodeid
        },
        bstack1l1l1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᤜ"): bstack11111l1ll1_opy_(test.own_markers)
    }
    if bstack11lll111ll_opy_ in [bstack1l1l1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᤝ"), bstack1l1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᤞ")]:
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠬࡳࡥࡵࡣࠪ᤟")] = {
            bstack1l1l1l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᤠ"): bstack11l1l11l1l_opy_.get(bstack1l1l1l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᤡ"), [])
        }
    if bstack11lll111ll_opy_ == bstack1l1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᤢ"):
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᤣ")] = bstack1l1l1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᤤ")
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᤥ")] = bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᤦ")]
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᤧ")] = bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᤨ")]
    if result:
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᤩ")] = result.outcome
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᤪ")] = result.duration * 1000
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᤫ")] = bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᤬")]
        if result.failed:
            bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ᤭")] = bstack1l11l1ll1_opy_.bstack111lllll1l_opy_(call.excinfo.typename)
            bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ᤮")] = bstack1l11l1ll1_opy_.bstack1ll1l111l1l_opy_(call.excinfo, result)
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭᤯")] = bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᤰ")]
    if outcome:
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᤱ")] = bstack11111l1l11_opy_(outcome)
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᤲ")] = 0
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᤳ")] = bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᤴ")]
        if bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᤵ")] == bstack1l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᤶ"):
            bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᤷ")] = bstack1l1l1l_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᤸ")  # bstack1ll11111lll_opy_
            bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨ᤹ࠫ")] = [{bstack1l1l1l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ᤺"): [bstack1l1l1l_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳ᤻ࠩ")]}]
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ᤼")] = bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭᤽")]
    return bstack11ll11l1ll_opy_
def bstack1ll11111l1l_opy_(test, bstack11l1lll1ll_opy_, bstack11lll111ll_opy_, result, call, outcome, bstack1ll111l1111_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11l1lll1ll_opy_[bstack1l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ᤾")]
    hook_name = bstack11l1lll1ll_opy_[bstack1l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ᤿")]
    hook_data = {
        bstack1l1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᥀"): bstack11l1lll1ll_opy_[bstack1l1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ᥁")],
        bstack1l1l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ᥂"): bstack1l1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ᥃"),
        bstack1l1l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᥄"): bstack1l1l1l_opy_ (u"ࠨࡽࢀࠫ᥅").format(bstack1ll1lll1111_opy_(hook_name)),
        bstack1l1l1l_opy_ (u"ࠩࡥࡳࡩࡿࠧ᥆"): {
            bstack1l1l1l_opy_ (u"ࠪࡰࡦࡴࡧࠨ᥇"): bstack1l1l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ᥈"),
            bstack1l1l1l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ᥉"): None
        },
        bstack1l1l1l_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ᥊"): test.name,
        bstack1l1l1l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ᥋"): bstack1ll111l1_opy_.bstack11l1ll1l11_opy_(test, hook_name),
        bstack1l1l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ᥌"): file_path,
        bstack1l1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ᥍"): file_path,
        bstack1l1l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᥎"): bstack1l1l1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ᥏"),
        bstack1l1l1l_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᥐ"): file_path,
        bstack1l1l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᥑ"): bstack11l1lll1ll_opy_[bstack1l1l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᥒ")],
        bstack1l1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᥓ"): bstack1l1l1l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᥔ") if bstack1ll111111l1_opy_ == bstack1l1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᥕ") else bstack1l1l1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᥖ"),
        bstack1l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᥗ"): hook_type
    }
    bstack1ll1l11l11l_opy_ = bstack11ll111111_opy_(_11ll11111l_opy_.get(test.nodeid, None))
    if bstack1ll1l11l11l_opy_:
        hook_data[bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫᥘ")] = bstack1ll1l11l11l_opy_
    if result:
        hook_data[bstack1l1l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᥙ")] = result.outcome
        hook_data[bstack1l1l1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᥚ")] = result.duration * 1000
        hook_data[bstack1l1l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᥛ")] = bstack11l1lll1ll_opy_[bstack1l1l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᥜ")]
        if result.failed:
            hook_data[bstack1l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᥝ")] = bstack1l11l1ll1_opy_.bstack111lllll1l_opy_(call.excinfo.typename)
            hook_data[bstack1l1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᥞ")] = bstack1l11l1ll1_opy_.bstack1ll1l111l1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᥟ")] = bstack11111l1l11_opy_(outcome)
        hook_data[bstack1l1l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᥠ")] = 100
        hook_data[bstack1l1l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᥡ")] = bstack11l1lll1ll_opy_[bstack1l1l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᥢ")]
        if hook_data[bstack1l1l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᥣ")] == bstack1l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᥤ"):
            hook_data[bstack1l1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᥥ")] = bstack1l1l1l_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᥦ")  # bstack1ll11111lll_opy_
            hook_data[bstack1l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᥧ")] = [{bstack1l1l1l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᥨ"): [bstack1l1l1l_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᥩ")]}]
    if bstack1ll111l1111_opy_:
        hook_data[bstack1l1l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᥪ")] = bstack1ll111l1111_opy_.result
        hook_data[bstack1l1l1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᥫ")] = bstack1111l111l1_opy_(bstack11l1lll1ll_opy_[bstack1l1l1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᥬ")], bstack11l1lll1ll_opy_[bstack1l1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᥭ")])
        hook_data[bstack1l1l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᥮")] = bstack11l1lll1ll_opy_[bstack1l1l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᥯")]
        if hook_data[bstack1l1l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᥰ")] == bstack1l1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᥱ"):
            hook_data[bstack1l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᥲ")] = bstack1l11l1ll1_opy_.bstack111lllll1l_opy_(bstack1ll111l1111_opy_.exception_type)
            hook_data[bstack1l1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᥳ")] = [{bstack1l1l1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᥴ"): bstack11111llll1_opy_(bstack1ll111l1111_opy_.exception)}]
    return hook_data
def bstack1ll111l1l11_opy_(test, bstack11l1l11l1l_opy_, bstack11lll111ll_opy_, result=None, call=None, outcome=None):
    bstack11ll11l1ll_opy_ = bstack1ll1111ll11_opy_(test, bstack11l1l11l1l_opy_, result, call, bstack11lll111ll_opy_, outcome)
    driver = getattr(test, bstack1l1l1l_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ᥵"), None)
    if bstack11lll111ll_opy_ == bstack1l1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ᥶") and driver:
        bstack11ll11l1ll_opy_[bstack1l1l1l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ᥷")] = bstack1l11l1ll1_opy_.bstack11ll1l1111_opy_(driver)
    if bstack11lll111ll_opy_ == bstack1l1l1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ᥸"):
        bstack11lll111ll_opy_ = bstack1l1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭᥹")
    bstack11l11l1l1l_opy_ = {
        bstack1l1l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ᥺"): bstack11lll111ll_opy_,
        bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ᥻"): bstack11ll11l1ll_opy_
    }
    bstack1l11l1ll1_opy_.bstack11l11l1lll_opy_(bstack11l11l1l1l_opy_)
    if bstack11lll111ll_opy_ == bstack1l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ᥼"):
        threading.current_thread().bstackTestMeta = {bstack1l1l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ᥽"): bstack1l1l1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ᥾")}
    elif bstack11lll111ll_opy_ == bstack1l1l1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ᥿"):
        threading.current_thread().bstackTestMeta = {bstack1l1l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᦀ"): getattr(result, bstack1l1l1l_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭ᦁ"), bstack1l1l1l_opy_ (u"࠭ࠧᦂ"))}
def bstack1ll111111ll_opy_(test, bstack11l1l11l1l_opy_, bstack11lll111ll_opy_, result=None, call=None, outcome=None, bstack1ll111l1111_opy_=None):
    hook_data = bstack1ll11111l1l_opy_(test, bstack11l1l11l1l_opy_, bstack11lll111ll_opy_, result, call, outcome, bstack1ll111l1111_opy_)
    bstack11l11l1l1l_opy_ = {
        bstack1l1l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᦃ"): bstack11lll111ll_opy_,
        bstack1l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᦄ"): hook_data
    }
    bstack1l11l1ll1_opy_.bstack11l11l1lll_opy_(bstack11l11l1l1l_opy_)
def bstack11ll111111_opy_(bstack11l1l11l1l_opy_):
    if not bstack11l1l11l1l_opy_:
        return None
    if bstack11l1l11l1l_opy_.get(bstack1l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᦅ"), None):
        return getattr(bstack11l1l11l1l_opy_[bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᦆ")], bstack1l1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᦇ"), None)
    return bstack11l1l11l1l_opy_.get(bstack1l1l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᦈ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l11l1ll1_opy_.on():
            return
        places = [bstack1l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᦉ"), bstack1l1l1l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᦊ"), bstack1l1l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᦋ")]
        bstack11l1lllll1_opy_ = []
        for bstack1l1llllll11_opy_ in places:
            records = caplog.get_records(bstack1l1llllll11_opy_)
            bstack1ll11111111_opy_ = bstack1l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᦌ") if bstack1l1llllll11_opy_ == bstack1l1l1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᦍ") else bstack1l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᦎ")
            bstack1ll1111l111_opy_ = request.node.nodeid + (bstack1l1l1l_opy_ (u"ࠬ࠭ᦏ") if bstack1l1llllll11_opy_ == bstack1l1l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᦐ") else bstack1l1l1l_opy_ (u"ࠧ࠮ࠩᦑ") + bstack1l1llllll11_opy_)
            bstack11ll11ll1l_opy_ = bstack11ll111111_opy_(_11ll11111l_opy_.get(bstack1ll1111l111_opy_, None))
            if not bstack11ll11ll1l_opy_:
                continue
            for record in records:
                if bstack1111lll1ll_opy_(record.message):
                    continue
                bstack11l1lllll1_opy_.append({
                    bstack1l1l1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᦒ"): bstack1llllll11ll_opy_(record.created).isoformat() + bstack1l1l1l_opy_ (u"ࠩ࡝ࠫᦓ"),
                    bstack1l1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᦔ"): record.levelname,
                    bstack1l1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᦕ"): record.message,
                    bstack1ll11111111_opy_: bstack11ll11ll1l_opy_
                })
        if len(bstack11l1lllll1_opy_) > 0:
            bstack1l11l1ll1_opy_.bstack1l11l1l1l1_opy_(bstack11l1lllll1_opy_)
    except Exception as err:
        print(bstack1l1l1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩᦖ"), str(err))
def bstack1111111ll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1lll11l_opy_
    bstack1l11ll11ll_opy_ = bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᦗ"), None) and bstack11lll1l111_opy_(
            threading.current_thread(), bstack1l1l1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᦘ"), None)
    bstack1111ll1ll_opy_ = getattr(driver, bstack1l1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨᦙ"), None) != None and getattr(driver, bstack1l1l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᦚ"), None) == True
    if sequence == bstack1l1l1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᦛ") and driver != None:
      if not bstack1l1lll11l_opy_ and bstack1111ll1111_opy_() and bstack1l1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᦜ") in CONFIG and CONFIG[bstack1l1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᦝ")] == True and bstack1lll1l11l_opy_.bstack11ll111l1_opy_(driver_command) and (bstack1111ll1ll_opy_ or bstack1l11ll11ll_opy_) and not bstack1l1ll11l1l_opy_(args):
        try:
          bstack1l1lll11l_opy_ = True
          logger.debug(bstack1l1l1l_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨᦞ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1l1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬᦟ").format(str(err)))
        bstack1l1lll11l_opy_ = False
    if sequence == bstack1l1l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᦠ"):
        if driver_command == bstack1l1l1l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᦡ"):
            bstack1l11l1ll1_opy_.bstack1ll11l1111_opy_({
                bstack1l1l1l_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᦢ"): response[bstack1l1l1l_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪᦣ")],
                bstack1l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᦤ"): store[bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᦥ")]
            })
def bstack1l1lll1l1_opy_():
    global bstack11l1lll1l_opy_
    bstack1l1lllll1_opy_.bstack1l111ll1l_opy_()
    logging.shutdown()
    bstack1l11l1ll1_opy_.bstack11l1ll111l_opy_()
    for driver in bstack11l1lll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll11111ll1_opy_(*args):
    global bstack11l1lll1l_opy_
    bstack1l11l1ll1_opy_.bstack11l1ll111l_opy_()
    for driver in bstack11l1lll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1l1111l1_opy_(self, *args, **kwargs):
    bstack11lllllll_opy_ = bstack1l11l11l_opy_(self, *args, **kwargs)
    bstack111llll11_opy_ = getattr(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨᦦ"), None)
    if bstack111llll11_opy_ and bstack111llll11_opy_.get(bstack1l1l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᦧ"), bstack1l1l1l_opy_ (u"ࠩࠪᦨ")) == bstack1l1l1l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᦩ"):
        bstack1l11l1ll1_opy_.bstack1ll1llllll_opy_(self)
    return bstack11lllllll_opy_
def bstack1l1111lll_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1111lll1_opy_ = Config.bstack111ll1l11_opy_()
    if bstack1l1111lll1_opy_.get_property(bstack1l1l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨᦪ")):
        return
    bstack1l1111lll1_opy_.bstack1l1111l1l_opy_(bstack1l1l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩᦫ"), True)
    global bstack1llll1l1ll_opy_
    global bstack11l11l1l1_opy_
    bstack1llll1l1ll_opy_ = framework_name
    logger.info(bstack1llll11l11_opy_.format(bstack1llll1l1ll_opy_.split(bstack1l1l1l_opy_ (u"࠭࠭ࠨ᦬"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1111ll1111_opy_():
            Service.start = bstack11lll1l1l_opy_
            Service.stop = bstack1ll111l11l_opy_
            webdriver.Remote.__init__ = bstack1ll1lll1_opy_
            webdriver.Remote.get = bstack11l1111l_opy_
            if not isinstance(os.getenv(bstack1l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ᦭")), str):
                return
            WebDriver.close = bstack1l1l1lll_opy_
            WebDriver.quit = bstack1ll111llll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack1111ll1111_opy_() and bstack1l11l1ll1_opy_.on():
            webdriver.Remote.__init__ = bstack1l1l1111l1_opy_
        bstack11l11l1l1_opy_ = True
    except Exception as e:
        pass
    bstack1lll1l1l1l_opy_()
    if os.environ.get(bstack1l1l1l_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭᦮")):
        bstack11l11l1l1_opy_ = eval(os.environ.get(bstack1l1l1l_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ᦯")))
    if not bstack11l11l1l1_opy_:
        bstack1l11l11l11_opy_(bstack1l1l1l_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧᦰ"), bstack11llll11_opy_)
    if bstack1l1llll1ll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1l1l11ll1l_opy_ = bstack1l11ll1ll_opy_
        except Exception as e:
            logger.error(bstack1llll1lll1_opy_.format(str(e)))
    if bstack1l1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᦱ") in str(framework_name).lower():
        if not bstack1111ll1111_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11lll1111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1ll11l_opy_
            Config.getoption = bstack11lll1l11l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll1l1lll1_opy_
        except Exception as e:
            pass
def bstack1ll111llll_opy_(self):
    global bstack1llll1l1ll_opy_
    global bstack1l1lll111_opy_
    global bstack1lll11l1_opy_
    try:
        if bstack1l1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᦲ") in bstack1llll1l1ll_opy_ and self.session_id != None and bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᦳ"), bstack1l1l1l_opy_ (u"ࠧࠨᦴ")) != bstack1l1l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᦵ"):
            bstack1l11ll111_opy_ = bstack1l1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᦶ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᦷ")
            bstack11lll1l1l1_opy_(logger, True)
            if self != None:
                bstack11ll11l1l_opy_(self, bstack1l11ll111_opy_, bstack1l1l1l_opy_ (u"ࠫ࠱ࠦࠧᦸ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᦹ"), None)
        if item is not None and bstack11lll1l111_opy_(threading.current_thread(), bstack1l1l1l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᦺ"), None):
            bstack1l1l1l1l1_opy_.bstack11lll1ll1l_opy_(self, bstack1llll1lll_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1l1l_opy_ (u"ࠧࠨᦻ")
    except Exception as e:
        logger.debug(bstack1l1l1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤᦼ") + str(e))
    bstack1lll11l1_opy_(self)
    self.session_id = None
def bstack1ll1lll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1lll111_opy_
    global bstack1l1l1llll1_opy_
    global bstack1ll11l1ll1_opy_
    global bstack1llll1l1ll_opy_
    global bstack1l11l11l_opy_
    global bstack11l1lll1l_opy_
    global bstack111llll1_opy_
    global bstack1l1l1l1ll_opy_
    global bstack1llll1lll_opy_
    CONFIG[bstack1l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᦽ")] = str(bstack1llll1l1ll_opy_) + str(__version__)
    command_executor = bstack1ll11111ll_opy_(bstack111llll1_opy_, CONFIG)
    logger.debug(bstack1ll1l111_opy_.format(command_executor))
    proxy = bstack1llllllll_opy_(CONFIG, proxy)
    bstack111ll111l_opy_ = 0
    try:
        if bstack1ll11l1ll1_opy_ is True:
            bstack111ll111l_opy_ = int(os.environ.get(bstack1l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᦾ")))
    except:
        bstack111ll111l_opy_ = 0
    bstack11111ll1_opy_ = bstack1l11l1111l_opy_(CONFIG, bstack111ll111l_opy_)
    logger.debug(bstack1l11l11l1_opy_.format(str(bstack11111ll1_opy_)))
    bstack1llll1lll_opy_ = CONFIG.get(bstack1l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᦿ"))[bstack111ll111l_opy_]
    if bstack1l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᧀ") in CONFIG and CONFIG[bstack1l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᧁ")]:
        bstack1ll1l1111l_opy_(bstack11111ll1_opy_, bstack1l1l1l1ll_opy_)
    if bstack11ll11l11_opy_.bstack1lll1l1l11_opy_(CONFIG, bstack111ll111l_opy_) and bstack11ll11l11_opy_.bstack1l1l111ll1_opy_(bstack11111ll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        bstack11ll11l11_opy_.set_capabilities(bstack11111ll1_opy_, CONFIG)
    if desired_capabilities:
        bstack111l1l11l_opy_ = bstack11lll11l1_opy_(desired_capabilities)
        bstack111l1l11l_opy_[bstack1l1l1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᧂ")] = bstack1l11l11lll_opy_(CONFIG)
        bstack11ll1lll1_opy_ = bstack1l11l1111l_opy_(bstack111l1l11l_opy_)
        if bstack11ll1lll1_opy_:
            bstack11111ll1_opy_ = update(bstack11ll1lll1_opy_, bstack11111ll1_opy_)
        desired_capabilities = None
    if options:
        bstack11lll11ll_opy_(options, bstack11111ll1_opy_)
    if not options:
        options = bstack1lll1l111l_opy_(bstack11111ll1_opy_)
    if proxy and bstack111l11l11_opy_() >= version.parse(bstack1l1l1l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᧃ")):
        options.proxy(proxy)
    if options and bstack111l11l11_opy_() >= version.parse(bstack1l1l1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᧄ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111l11l11_opy_() < version.parse(bstack1l1l1l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᧅ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11111ll1_opy_)
    logger.info(bstack11111l1l1_opy_)
    if bstack111l11l11_opy_() >= version.parse(bstack1l1l1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᧆ")):
        bstack1l11l11l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l11l11_opy_() >= version.parse(bstack1l1l1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᧇ")):
        bstack1l11l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l11l11_opy_() >= version.parse(bstack1l1l1l_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ᧈ")):
        bstack1l11l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l11l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack111lll1l1_opy_ = bstack1l1l1l_opy_ (u"ࠧࠨᧉ")
        if bstack111l11l11_opy_() >= version.parse(bstack1l1l1l_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩ᧊")):
            bstack111lll1l1_opy_ = self.caps.get(bstack1l1l1l_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ᧋"))
        else:
            bstack111lll1l1_opy_ = self.capabilities.get(bstack1l1l1l_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ᧌"))
        if bstack111lll1l1_opy_:
            bstack1l11111l_opy_(bstack111lll1l1_opy_)
            if bstack111l11l11_opy_() <= version.parse(bstack1l1l1l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ᧍")):
                self.command_executor._url = bstack1l1l1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ᧎") + bstack111llll1_opy_ + bstack1l1l1l_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ᧏")
            else:
                self.command_executor._url = bstack1l1l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ᧐") + bstack111lll1l1_opy_ + bstack1l1l1l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ᧑")
            logger.debug(bstack1l1llllll1_opy_.format(bstack111lll1l1_opy_))
        else:
            logger.debug(bstack11ll1lllll_opy_.format(bstack1l1l1l_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ᧒")))
    except Exception as e:
        logger.debug(bstack11ll1lllll_opy_.format(e))
    bstack1l1lll111_opy_ = self.session_id
    if bstack1l1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᧓") in bstack1llll1l1ll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ᧔"), None)
        if item:
            bstack1ll1111l11l_opy_ = getattr(item, bstack1l1l1l_opy_ (u"ࠬࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࡡࡶࡸࡦࡸࡴࡦࡦࠪ᧕"), False)
            if not getattr(item, bstack1l1l1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ᧖"), None) and bstack1ll1111l11l_opy_:
                setattr(store[bstack1l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᧗")], bstack1l1l1l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ᧘"), self)
        bstack111llll11_opy_ = getattr(threading.current_thread(), bstack1l1l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ᧙"), None)
        if bstack111llll11_opy_ and bstack111llll11_opy_.get(bstack1l1l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ᧚"), bstack1l1l1l_opy_ (u"ࠫࠬ᧛")) == bstack1l1l1l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭᧜"):
            bstack1l11l1ll1_opy_.bstack1ll1llllll_opy_(self)
    bstack11l1lll1l_opy_.append(self)
    if bstack1l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᧝") in CONFIG and bstack1l1l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᧞") in CONFIG[bstack1l1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᧟")][bstack111ll111l_opy_]:
        bstack1l1l1llll1_opy_ = CONFIG[bstack1l1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᧠")][bstack111ll111l_opy_][bstack1l1l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᧡")]
    logger.debug(bstack1111l1ll1_opy_.format(bstack1l1lll111_opy_))
def bstack11l1111l_opy_(self, url):
    global bstack1ll1ll1ll_opy_
    global CONFIG
    try:
        bstack1lll1lll1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll1ll1l11_opy_.format(str(err)))
    try:
        bstack1ll1ll1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack1lll11ll_opy_ = str(e)
            if any(err_msg in bstack1lll11ll_opy_ for err_msg in bstack1ll1l1ll1_opy_):
                bstack1lll1lll1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll1ll1l11_opy_.format(str(err)))
        raise e
def bstack1l1lll11ll_opy_(item, when):
    global bstack1l1111l11_opy_
    try:
        bstack1l1111l11_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll1l1lll1_opy_(item, call, rep):
    global bstack1l1l1ll1l1_opy_
    global bstack11l1lll1l_opy_
    name = bstack1l1l1l_opy_ (u"ࠫࠬ᧢")
    try:
        if rep.when == bstack1l1l1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ᧣"):
            bstack1l1lll111_opy_ = threading.current_thread().bstackSessionId
            bstack1l1lllllll1_opy_ = item.config.getoption(bstack1l1l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᧤"))
            try:
                if (str(bstack1l1lllllll1_opy_).lower() != bstack1l1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ᧥")):
                    name = str(rep.nodeid)
                    bstack1llllll11_opy_ = bstack111ll1111_opy_(bstack1l1l1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ᧦"), name, bstack1l1l1l_opy_ (u"ࠩࠪ᧧"), bstack1l1l1l_opy_ (u"ࠪࠫ᧨"), bstack1l1l1l_opy_ (u"ࠫࠬ᧩"), bstack1l1l1l_opy_ (u"ࠬ࠭᧪"))
                    os.environ[bstack1l1l1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ᧫")] = name
                    for driver in bstack11l1lll1l_opy_:
                        if bstack1l1lll111_opy_ == driver.session_id:
                            driver.execute_script(bstack1llllll11_opy_)
            except Exception as e:
                logger.debug(bstack1l1l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ᧬").format(str(e)))
            try:
                bstack1l11l11ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ᧭"):
                    status = bstack1l1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᧮") if rep.outcome.lower() == bstack1l1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᧯") else bstack1l1l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᧰")
                    reason = bstack1l1l1l_opy_ (u"ࠬ࠭᧱")
                    if status == bstack1l1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᧲"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1l1l_opy_ (u"ࠧࡪࡰࡩࡳࠬ᧳") if status == bstack1l1l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᧴") else bstack1l1l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᧵")
                    data = name + bstack1l1l1l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ᧶") if status == bstack1l1l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᧷") else name + bstack1l1l1l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ᧸") + reason
                    bstack1lll111111_opy_ = bstack111ll1111_opy_(bstack1l1l1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ᧹"), bstack1l1l1l_opy_ (u"ࠧࠨ᧺"), bstack1l1l1l_opy_ (u"ࠨࠩ᧻"), bstack1l1l1l_opy_ (u"ࠩࠪ᧼"), level, data)
                    for driver in bstack11l1lll1l_opy_:
                        if bstack1l1lll111_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll111111_opy_)
            except Exception as e:
                logger.debug(bstack1l1l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ᧽").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨ᧾").format(str(e)))
    bstack1l1l1ll1l1_opy_(item, call, rep)
notset = Notset()
def bstack11lll1l11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11ll111ll_opy_
    if str(name).lower() == bstack1l1l1l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬ᧿"):
        return bstack1l1l1l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧᨀ")
    else:
        return bstack11ll111ll_opy_(self, name, default, skip)
def bstack1l11ll1ll_opy_(self):
    global CONFIG
    global bstack1ll1llll11_opy_
    try:
        proxy = bstack1111l111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1l1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᨁ")):
                proxies = bstack1ll1lll1ll_opy_(proxy, bstack1ll11111ll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll111l1l1_opy_ = proxies.popitem()
                    if bstack1l1l1l_opy_ (u"ࠣ࠼࠲࠳ࠧᨂ") in bstack1ll111l1l1_opy_:
                        return bstack1ll111l1l1_opy_
                    else:
                        return bstack1l1l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᨃ") + bstack1ll111l1l1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢᨄ").format(str(e)))
    return bstack1ll1llll11_opy_(self)
def bstack1l1llll1ll_opy_():
    return (bstack1l1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᨅ") in CONFIG or bstack1l1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᨆ") in CONFIG) and bstack1llllll1l1_opy_() and bstack111l11l11_opy_() >= version.parse(
        bstack1l1ll1ll1l_opy_)
def bstack1lll1l1l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1l1llll1_opy_
    global bstack1ll11l1ll1_opy_
    global bstack1llll1l1ll_opy_
    CONFIG[bstack1l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᨇ")] = str(bstack1llll1l1ll_opy_) + str(__version__)
    bstack111ll111l_opy_ = 0
    try:
        if bstack1ll11l1ll1_opy_ is True:
            bstack111ll111l_opy_ = int(os.environ.get(bstack1l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᨈ")))
    except:
        bstack111ll111l_opy_ = 0
    CONFIG[bstack1l1l1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᨉ")] = True
    bstack11111ll1_opy_ = bstack1l11l1111l_opy_(CONFIG, bstack111ll111l_opy_)
    logger.debug(bstack1l11l11l1_opy_.format(str(bstack11111ll1_opy_)))
    if CONFIG.get(bstack1l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᨊ")):
        bstack1ll1l1111l_opy_(bstack11111ll1_opy_, bstack1l1l1l1ll_opy_)
    if bstack1l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᨋ") in CONFIG and bstack1l1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᨌ") in CONFIG[bstack1l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᨍ")][bstack111ll111l_opy_]:
        bstack1l1l1llll1_opy_ = CONFIG[bstack1l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᨎ")][bstack111ll111l_opy_][bstack1l1l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᨏ")]
    import urllib
    import json
    if bstack1l1l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᨐ") in CONFIG and str(CONFIG[bstack1l1l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᨑ")]).lower() != bstack1l1l1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᨒ"):
        bstack1l1l11l11l_opy_ = bstack1l1ll11l1_opy_()
        bstack11111111l_opy_ = bstack1l1l11l11l_opy_ + urllib.parse.quote(json.dumps(bstack11111ll1_opy_))
    else:
        bstack11111111l_opy_ = bstack1l1l1l_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭ᨓ") + urllib.parse.quote(json.dumps(bstack11111ll1_opy_))
    browser = self.connect(bstack11111111l_opy_)
    return browser
def bstack1lll1l1l1l_opy_():
    global bstack11l11l1l1_opy_
    global bstack1llll1l1ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1111ll_opy_
        if not bstack1111ll1111_opy_():
            global bstack1lll11l11l_opy_
            if not bstack1lll11l11l_opy_:
                from bstack_utils.helper import bstack1lll1l1lll_opy_, bstack1ll111ll_opy_
                bstack1lll11l11l_opy_ = bstack1lll1l1lll_opy_()
                bstack1ll111ll_opy_(bstack1llll1l1ll_opy_)
            BrowserType.connect = bstack1ll1111ll_opy_
            return
        BrowserType.launch = bstack1lll1l1l_opy_
        bstack11l11l1l1_opy_ = True
    except Exception as e:
        pass
def bstack1ll1111111l_opy_():
    global CONFIG
    global bstack1111l1l1_opy_
    global bstack111llll1_opy_
    global bstack1l1l1l1ll_opy_
    global bstack1ll11l1ll1_opy_
    global bstack11l1ll11_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫᨔ")))
    bstack1111l1l1_opy_ = eval(os.environ.get(bstack1l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧᨕ")))
    bstack111llll1_opy_ = os.environ.get(bstack1l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧᨖ"))
    bstack1lll1lll1_opy_(CONFIG, bstack1111l1l1_opy_)
    bstack11l1ll11_opy_ = bstack1l1lllll1_opy_.bstack111l11l1l_opy_(CONFIG, bstack11l1ll11_opy_)
    global bstack1l11l11l_opy_
    global bstack1lll11l1_opy_
    global bstack1l1lll1l11_opy_
    global bstack1l11l1l1ll_opy_
    global bstack1llll1ll_opy_
    global bstack1l11l1l111_opy_
    global bstack1l11lllll1_opy_
    global bstack1ll1ll1ll_opy_
    global bstack1ll1llll11_opy_
    global bstack11ll111ll_opy_
    global bstack1l1111l11_opy_
    global bstack1l1l1ll1l1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l11l11l_opy_ = webdriver.Remote.__init__
        bstack1lll11l1_opy_ = WebDriver.quit
        bstack1l11lllll1_opy_ = WebDriver.close
        bstack1ll1ll1ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᨗ") in CONFIG or bstack1l1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾᨘ࠭") in CONFIG) and bstack1llllll1l1_opy_():
        if bstack111l11l11_opy_() < version.parse(bstack1l1ll1ll1l_opy_):
            logger.error(bstack1ll1lllll1_opy_.format(bstack111l11l11_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1ll1llll11_opy_ = RemoteConnection._1l1l11ll1l_opy_
            except Exception as e:
                logger.error(bstack1llll1lll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11ll111ll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1111l11_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1l1l11_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1l1ll1l1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1l1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫᨙ"))
    bstack1l1l1l1ll_opy_ = CONFIG.get(bstack1l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᨚ"), {}).get(bstack1l1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᨛ"))
    bstack1ll11l1ll1_opy_ = True
    bstack1l1111lll_opy_(bstack1l1llll1_opy_)
if (bstack1lllllll1l1_opy_()):
    bstack1ll1111111l_opy_()
@bstack11l11l11ll_opy_(class_method=False)
def bstack1ll1111l1ll_opy_(hook_name, event, bstack1l1llllllll_opy_=None):
    if hook_name not in [bstack1l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ᨜"), bstack1l1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ᨝"), bstack1l1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ᨞"), bstack1l1l1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ᨟"), bstack1l1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᨠ"), bstack1l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᨡ"), bstack1l1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᨢ"), bstack1l1l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᨣ")]:
        return
    node = store[bstack1l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᨤ")]
    if hook_name in [bstack1l1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᨥ"), bstack1l1l1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᨦ")]:
        node = store[bstack1l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩᨧ")]
    elif hook_name in [bstack1l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᨨ"), bstack1l1l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᨩ")]:
        node = store[bstack1l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᨪ")]
    if event == bstack1l1l1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᨫ"):
        hook_type = bstack1ll1lll11l1_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11l1lll1ll_opy_ = {
            bstack1l1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᨬ"): uuid,
            bstack1l1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᨭ"): bstack1lll1ll1l_opy_(),
            bstack1l1l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᨮ"): bstack1l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᨯ"),
            bstack1l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᨰ"): hook_type,
            bstack1l1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᨱ"): hook_name
        }
        store[bstack1l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᨲ")].append(uuid)
        bstack1ll1111ll1l_opy_ = node.nodeid
        if hook_type == bstack1l1l1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᨳ"):
            if not _11ll11111l_opy_.get(bstack1ll1111ll1l_opy_, None):
                _11ll11111l_opy_[bstack1ll1111ll1l_opy_] = {bstack1l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᨴ"): []}
            _11ll11111l_opy_[bstack1ll1111ll1l_opy_][bstack1l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᨵ")].append(bstack11l1lll1ll_opy_[bstack1l1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᨶ")])
        _11ll11111l_opy_[bstack1ll1111ll1l_opy_ + bstack1l1l1l_opy_ (u"ࠬ࠳ࠧᨷ") + hook_name] = bstack11l1lll1ll_opy_
        bstack1ll111111ll_opy_(node, bstack11l1lll1ll_opy_, bstack1l1l1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᨸ"))
    elif event == bstack1l1l1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᨹ"):
        bstack11ll1111l1_opy_ = node.nodeid + bstack1l1l1l_opy_ (u"ࠨ࠯ࠪᨺ") + hook_name
        _11ll11111l_opy_[bstack11ll1111l1_opy_][bstack1l1l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᨻ")] = bstack1lll1ll1l_opy_()
        bstack1ll1111lll1_opy_(_11ll11111l_opy_[bstack11ll1111l1_opy_][bstack1l1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᨼ")])
        bstack1ll111111ll_opy_(node, _11ll11111l_opy_[bstack11ll1111l1_opy_], bstack1l1l1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᨽ"), bstack1ll111l1111_opy_=bstack1l1llllllll_opy_)
def bstack1l1lllll1ll_opy_():
    global bstack1ll111111l1_opy_
    if bstack11llllll1l_opy_():
        bstack1ll111111l1_opy_ = bstack1l1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᨾ")
    else:
        bstack1ll111111l1_opy_ = bstack1l1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᨿ")
@bstack1l11l1ll1_opy_.bstack1ll11ll1l11_opy_
def bstack1l1llll1lll_opy_():
    bstack1l1lllll1ll_opy_()
    if bstack1llllll1l1_opy_():
        bstack1ll11111_opy_(bstack1111111ll_opy_)
    try:
        bstack1llll1lll11_opy_(bstack1ll1111l1ll_opy_)
    except Exception as e:
        logger.debug(bstack1l1l1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣᩀ").format(e))
bstack1l1llll1lll_opy_()