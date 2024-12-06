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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111l11l111_opy_, bstack11l1111l1_opy_, bstack1l1ll1l1ll_opy_, bstack1llll11ll1_opy_,
                                    bstack111l1111ll_opy_, bstack111l11111l_opy_, bstack111l11l11l_opy_, bstack1111lllll1_opy_)
from bstack_utils.messages import bstack1ll111l11_opy_, bstack1llll1lll1_opy_
from bstack_utils.proxy import bstack11ll1l111_opy_, bstack1111l111_opy_
bstack1l1111lll1_opy_ = Config.bstack111ll1l11_opy_()
logger = logging.getLogger(__name__)
def bstack111ll11lll_opy_(config):
    return config[bstack1l1l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫጦ")]
def bstack111llll111_opy_(config):
    return config[bstack1l1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ጧ")]
def bstack1llll1ll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11111lll11_opy_(obj):
    values = []
    bstack1llllllll11_opy_ = re.compile(bstack1l1l1l_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣጨ"), re.I)
    for key in obj.keys():
        if bstack1llllllll11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11111ll1ll_opy_(config):
    tags = []
    tags.extend(bstack11111lll11_opy_(os.environ))
    tags.extend(bstack11111lll11_opy_(config))
    return tags
def bstack11111l1ll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11111111ll_opy_(bstack1111lll1l1_opy_):
    if not bstack1111lll1l1_opy_:
        return bstack1l1l1l_opy_ (u"ࠬ࠭ጩ")
    return bstack1l1l1l_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢጪ").format(bstack1111lll1l1_opy_.name, bstack1111lll1l1_opy_.email)
def bstack111lll1ll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111ll111l_opy_ = repo.common_dir
        info = {
            bstack1l1l1l_opy_ (u"ࠢࡴࡪࡤࠦጫ"): repo.head.commit.hexsha,
            bstack1l1l1l_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦጬ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1l1l_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤጭ"): repo.active_branch.name,
            bstack1l1l1l_opy_ (u"ࠥࡸࡦ࡭ࠢጮ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1l1l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢጯ"): bstack11111111ll_opy_(repo.head.commit.committer),
            bstack1l1l1l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨጰ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1l1l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨጱ"): bstack11111111ll_opy_(repo.head.commit.author),
            bstack1l1l1l_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧጲ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1l1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤጳ"): repo.head.commit.message,
            bstack1l1l1l_opy_ (u"ࠤࡵࡳࡴࡺࠢጴ"): repo.git.rev_parse(bstack1l1l1l_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧጵ")),
            bstack1l1l1l_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧጶ"): bstack1111ll111l_opy_,
            bstack1l1l1l_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣጷ"): subprocess.check_output([bstack1l1l1l_opy_ (u"ࠨࡧࡪࡶࠥጸ"), bstack1l1l1l_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥጹ"), bstack1l1l1l_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦጺ")]).strip().decode(
                bstack1l1l1l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨጻ")),
            bstack1l1l1l_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧጼ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1l1l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨጽ"): repo.git.rev_list(
                bstack1l1l1l_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧጾ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111111l11_opy_ = []
        for remote in remotes:
            bstack1lllllll1ll_opy_ = {
                bstack1l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጿ"): remote.name,
                bstack1l1l1l_opy_ (u"ࠢࡶࡴ࡯ࠦፀ"): remote.url,
            }
            bstack1111111l11_opy_.append(bstack1lllllll1ll_opy_)
        bstack11111lll1l_opy_ = {
            bstack1l1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨፁ"): bstack1l1l1l_opy_ (u"ࠤࡪ࡭ࡹࠨፂ"),
            **info,
            bstack1l1l1l_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦፃ"): bstack1111111l11_opy_
        }
        bstack11111lll1l_opy_ = bstack1111l1llll_opy_(bstack11111lll1l_opy_)
        return bstack11111lll1l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢፄ").format(err))
        return {}
def bstack1111l1llll_opy_(bstack11111lll1l_opy_):
    bstack1lllll1ll11_opy_ = bstack1111l11111_opy_(bstack11111lll1l_opy_)
    if bstack1lllll1ll11_opy_ and bstack1lllll1ll11_opy_ > bstack111l1111ll_opy_:
        bstack1111ll1l11_opy_ = bstack1lllll1ll11_opy_ - bstack111l1111ll_opy_
        bstack111111l111_opy_ = bstack11111l1l1l_opy_(bstack11111lll1l_opy_[bstack1l1l1l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨፅ")], bstack1111ll1l11_opy_)
        bstack11111lll1l_opy_[bstack1l1l1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢፆ")] = bstack111111l111_opy_
        logger.info(bstack1l1l1l_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤፇ")
                    .format(bstack1111l11111_opy_(bstack11111lll1l_opy_) / 1024))
    return bstack11111lll1l_opy_
def bstack1111l11111_opy_(bstack1l1ll1l11l_opy_):
    try:
        if bstack1l1ll1l11l_opy_:
            bstack1111l11l1l_opy_ = json.dumps(bstack1l1ll1l11l_opy_)
            bstack1llllll11l1_opy_ = sys.getsizeof(bstack1111l11l1l_opy_)
            return bstack1llllll11l1_opy_
    except Exception as e:
        logger.debug(bstack1l1l1l_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣፈ").format(e))
    return -1
def bstack11111l1l1l_opy_(field, bstack11111l1111_opy_):
    try:
        bstack1111l1l1l1_opy_ = len(bytes(bstack111l11111l_opy_, bstack1l1l1l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨፉ")))
        bstack1111111ll1_opy_ = bytes(field, bstack1l1l1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩፊ"))
        bstack1lllll1l1ll_opy_ = len(bstack1111111ll1_opy_)
        bstack1lllllllll1_opy_ = ceil(bstack1lllll1l1ll_opy_ - bstack11111l1111_opy_ - bstack1111l1l1l1_opy_)
        if bstack1lllllllll1_opy_ > 0:
            bstack1111lll11l_opy_ = bstack1111111ll1_opy_[:bstack1lllllllll1_opy_].decode(bstack1l1l1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪፋ"), errors=bstack1l1l1l_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬፌ")) + bstack111l11111l_opy_
            return bstack1111lll11l_opy_
    except Exception as e:
        logger.debug(bstack1l1l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦፍ").format(e))
    return field
def bstack1l1llll11_opy_():
    env = os.environ
    if (bstack1l1l1l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧፎ") in env and len(env[bstack1l1l1l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨፏ")]) > 0) or (
            bstack1l1l1l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣፐ") in env and len(env[bstack1l1l1l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤፑ")]) > 0):
        return {
            bstack1l1l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤፒ"): bstack1l1l1l_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨፓ"),
            bstack1l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤፔ"): env.get(bstack1l1l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥፕ")),
            bstack1l1l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥፖ"): env.get(bstack1l1l1l_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦፗ")),
            bstack1l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤፘ"): env.get(bstack1l1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥፙ"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠧࡉࡉࠣፚ")) == bstack1l1l1l_opy_ (u"ࠨࡴࡳࡷࡨࠦ፛") and bstack1ll1l1lll_opy_(env.get(bstack1l1l1l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤ፜"))):
        return {
            bstack1l1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ፝"): bstack1l1l1l_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦ፞"),
            bstack1l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ፟"): env.get(bstack1l1l1l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ፠")),
            bstack1l1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ፡"): env.get(bstack1l1l1l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥ።")),
            bstack1l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፣"): env.get(bstack1l1l1l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦ፤"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠤࡆࡍࠧ፥")) == bstack1l1l1l_opy_ (u"ࠥࡸࡷࡻࡥࠣ፦") and bstack1ll1l1lll_opy_(env.get(bstack1l1l1l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦ፧"))):
        return {
            bstack1l1l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ፨"): bstack1l1l1l_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤ፩"),
            bstack1l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ፪"): env.get(bstack1l1l1l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣ፫")),
            bstack1l1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ፬"): env.get(bstack1l1l1l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ፭")),
            bstack1l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ፮"): env.get(bstack1l1l1l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ፯"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠨࡃࡊࠤ፰")) == bstack1l1l1l_opy_ (u"ࠢࡵࡴࡸࡩࠧ፱") and env.get(bstack1l1l1l_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤ፲")) == bstack1l1l1l_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦ፳"):
        return {
            bstack1l1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ፴"): bstack1l1l1l_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨ፵"),
            bstack1l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ፶"): None,
            bstack1l1l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ፷"): None,
            bstack1l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፸"): None
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦ፹")) and env.get(bstack1l1l1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧ፺")):
        return {
            bstack1l1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ፻"): bstack1l1l1l_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢ፼"),
            bstack1l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ፽"): env.get(bstack1l1l1l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦ፾")),
            bstack1l1l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ፿"): None,
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᎀ"): env.get(bstack1l1l1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᎁ"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠥࡇࡎࠨᎂ")) == bstack1l1l1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᎃ") and bstack1ll1l1lll_opy_(env.get(bstack1l1l1l_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᎄ"))):
        return {
            bstack1l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎅ"): bstack1l1l1l_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨᎆ"),
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎇ"): env.get(bstack1l1l1l_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧᎈ")),
            bstack1l1l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᎉ"): None,
            bstack1l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᎊ"): env.get(bstack1l1l1l_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᎋ"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠨࡃࡊࠤᎌ")) == bstack1l1l1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᎍ") and bstack1ll1l1lll_opy_(env.get(bstack1l1l1l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᎎ"))):
        return {
            bstack1l1l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᎏ"): bstack1l1l1l_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨ᎐"),
            bstack1l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᎑"): env.get(bstack1l1l1l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦ᎒")),
            bstack1l1l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᎓"): env.get(bstack1l1l1l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᎔")),
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᎕"): env.get(bstack1l1l1l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧ᎖"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠥࡇࡎࠨ᎗")) == bstack1l1l1l_opy_ (u"ࠦࡹࡸࡵࡦࠤ᎘") and bstack1ll1l1lll_opy_(env.get(bstack1l1l1l_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣ᎙"))):
        return {
            bstack1l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᎚"): bstack1l1l1l_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢ᎛"),
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᎜"): env.get(bstack1l1l1l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨ᎝")),
            bstack1l1l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᎞"): env.get(bstack1l1l1l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᎟")),
            bstack1l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᎠ"): env.get(bstack1l1l1l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᎡ"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠢࡄࡋࠥᎢ")) == bstack1l1l1l_opy_ (u"ࠣࡶࡵࡹࡪࠨᎣ") and bstack1ll1l1lll_opy_(env.get(bstack1l1l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᎤ"))):
        return {
            bstack1l1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᎥ"): bstack1l1l1l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᎦ"),
            bstack1l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎧ"): env.get(bstack1l1l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᎨ")),
            bstack1l1l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎩ"): env.get(bstack1l1l1l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᎪ")) or env.get(bstack1l1l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᎫ")),
            bstack1l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᎬ"): env.get(bstack1l1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᎭ"))
        }
    if bstack1ll1l1lll_opy_(env.get(bstack1l1l1l_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᎮ"))):
        return {
            bstack1l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎯ"): bstack1l1l1l_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᎰ"),
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎱ"): bstack1l1l1l_opy_ (u"ࠤࡾࢁࢀࢃࠢᎲ").format(env.get(bstack1l1l1l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭Ꮃ")), env.get(bstack1l1l1l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᎴ"))),
            bstack1l1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᎵ"): env.get(bstack1l1l1l_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᎶ")),
            bstack1l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᎷ"): env.get(bstack1l1l1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᎸ"))
        }
    if bstack1ll1l1lll_opy_(env.get(bstack1l1l1l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᎹ"))):
        return {
            bstack1l1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᎺ"): bstack1l1l1l_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨᎻ"),
            bstack1l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎼ"): bstack1l1l1l_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧᎽ").format(env.get(bstack1l1l1l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭Ꮎ")), env.get(bstack1l1l1l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᎿ")), env.get(bstack1l1l1l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᏀ")), env.get(bstack1l1l1l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᏁ"))),
            bstack1l1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᏂ"): env.get(bstack1l1l1l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᏃ")),
            bstack1l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᏄ"): env.get(bstack1l1l1l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᏅ"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᏆ")) and env.get(bstack1l1l1l_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᏇ")):
        return {
            bstack1l1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᏈ"): bstack1l1l1l_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨᏉ"),
            bstack1l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏊ"): bstack1l1l1l_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤᏋ").format(env.get(bstack1l1l1l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᏌ")), env.get(bstack1l1l1l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭Ꮝ")), env.get(bstack1l1l1l_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩᏎ"))),
            bstack1l1l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᏏ"): env.get(bstack1l1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᏐ")),
            bstack1l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏑ"): env.get(bstack1l1l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᏒ"))
        }
    if any([env.get(bstack1l1l1l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᏓ")), env.get(bstack1l1l1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᏔ")), env.get(bstack1l1l1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᏕ"))]):
        return {
            bstack1l1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᏖ"): bstack1l1l1l_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦᏗ"),
            bstack1l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏘ"): env.get(bstack1l1l1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᏙ")),
            bstack1l1l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᏚ"): env.get(bstack1l1l1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᏛ")),
            bstack1l1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᏜ"): env.get(bstack1l1l1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᏝ"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᏞ")):
        return {
            bstack1l1l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏟ"): bstack1l1l1l_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᏠ"),
            bstack1l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᏡ"): env.get(bstack1l1l1l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᏢ")),
            bstack1l1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏣ"): env.get(bstack1l1l1l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᏤ")),
            bstack1l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏥ"): env.get(bstack1l1l1l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᏦ"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᏧ")) or env.get(bstack1l1l1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᏨ")):
        return {
            bstack1l1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᏩ"): bstack1l1l1l_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᏪ"),
            bstack1l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᏫ"): env.get(bstack1l1l1l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᏬ")),
            bstack1l1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᏭ"): bstack1l1l1l_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᏮ") if env.get(bstack1l1l1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᏯ")) else None,
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᏰ"): env.get(bstack1l1l1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᏱ"))
        }
    if any([env.get(bstack1l1l1l_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᏲ")), env.get(bstack1l1l1l_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᏳ")), env.get(bstack1l1l1l_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᏴ"))]):
        return {
            bstack1l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᏵ"): bstack1l1l1l_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨ᏶"),
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᏷"): None,
            bstack1l1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏸ"): env.get(bstack1l1l1l_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᏹ")),
            bstack1l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏺ"): env.get(bstack1l1l1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᏻ"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᏼ")):
        return {
            bstack1l1l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᏽ"): bstack1l1l1l_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦ᏾"),
            bstack1l1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᏿"): env.get(bstack1l1l1l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᐀")),
            bstack1l1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᐁ"): bstack1l1l1l_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᐂ").format(env.get(bstack1l1l1l_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᐃ"))) if env.get(bstack1l1l1l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᐄ")) else None,
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐅ"): env.get(bstack1l1l1l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᐆ"))
        }
    if bstack1ll1l1lll_opy_(env.get(bstack1l1l1l_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦᐇ"))):
        return {
            bstack1l1l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᐈ"): bstack1l1l1l_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨᐉ"),
            bstack1l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᐊ"): env.get(bstack1l1l1l_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦᐋ")),
            bstack1l1l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᐌ"): env.get(bstack1l1l1l_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧᐍ")),
            bstack1l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᐎ"): env.get(bstack1l1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᐏ"))
        }
    if bstack1ll1l1lll_opy_(env.get(bstack1l1l1l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᐐ"))):
        return {
            bstack1l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐑ"): bstack1l1l1l_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᐒ"),
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐓ"): bstack1l1l1l_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᐔ").format(env.get(bstack1l1l1l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᐕ")), env.get(bstack1l1l1l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᐖ")), env.get(bstack1l1l1l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᐗ"))),
            bstack1l1l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᐘ"): env.get(bstack1l1l1l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᐙ")),
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐚ"): env.get(bstack1l1l1l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᐛ"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠥࡇࡎࠨᐜ")) == bstack1l1l1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᐝ") and env.get(bstack1l1l1l_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᐞ")) == bstack1l1l1l_opy_ (u"ࠨ࠱ࠣᐟ"):
        return {
            bstack1l1l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᐠ"): bstack1l1l1l_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣᐡ"),
            bstack1l1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᐢ"): bstack1l1l1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨᐣ").format(env.get(bstack1l1l1l_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨᐤ"))),
            bstack1l1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᐥ"): None,
            bstack1l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᐦ"): None,
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᐧ")):
        return {
            bstack1l1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᐨ"): bstack1l1l1l_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᐩ"),
            bstack1l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᐪ"): None,
            bstack1l1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᐫ"): env.get(bstack1l1l1l_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨᐬ")),
            bstack1l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᐭ"): env.get(bstack1l1l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᐮ"))
        }
    if any([env.get(bstack1l1l1l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦᐯ")), env.get(bstack1l1l1l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤᐰ")), env.get(bstack1l1l1l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣᐱ")), env.get(bstack1l1l1l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧᐲ"))]):
        return {
            bstack1l1l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᐳ"): bstack1l1l1l_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᐴ"),
            bstack1l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᐵ"): None,
            bstack1l1l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᐶ"): env.get(bstack1l1l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᐷ")) or None,
            bstack1l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᐸ"): env.get(bstack1l1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᐹ"), 0)
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᐺ")):
        return {
            bstack1l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐻ"): bstack1l1l1l_opy_ (u"ࠢࡈࡱࡆࡈࠧᐼ"),
            bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐽ"): None,
            bstack1l1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᐾ"): env.get(bstack1l1l1l_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᐿ")),
            bstack1l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᑀ"): env.get(bstack1l1l1l_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦᑁ"))
        }
    if env.get(bstack1l1l1l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᑂ")):
        return {
            bstack1l1l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᑃ"): bstack1l1l1l_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᑄ"),
            bstack1l1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᑅ"): env.get(bstack1l1l1l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᑆ")),
            bstack1l1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᑇ"): env.get(bstack1l1l1l_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᑈ")),
            bstack1l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᑉ"): env.get(bstack1l1l1l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᑊ"))
        }
    return {bstack1l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᑋ"): None}
def get_host_info():
    return {
        bstack1l1l1l_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᑌ"): platform.node(),
        bstack1l1l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᑍ"): platform.system(),
        bstack1l1l1l_opy_ (u"ࠦࡹࡿࡰࡦࠤᑎ"): platform.machine(),
        bstack1l1l1l_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᑏ"): platform.version(),
        bstack1l1l1l_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᑐ"): platform.architecture()[0]
    }
def bstack1llllll1l1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1llllll1l1l_opy_():
    if bstack1l1111lll1_opy_.get_property(bstack1l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᑑ")):
        return bstack1l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᑒ")
    return bstack1l1l1l_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᑓ")
def bstack1111l1ll1l_opy_(driver):
    info = {
        bstack1l1l1l_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᑔ"): driver.capabilities,
        bstack1l1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᑕ"): driver.session_id,
        bstack1l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᑖ"): driver.capabilities.get(bstack1l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᑗ"), None),
        bstack1l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᑘ"): driver.capabilities.get(bstack1l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᑙ"), None),
        bstack1l1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᑚ"): driver.capabilities.get(bstack1l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᑛ"), None),
    }
    if bstack1llllll1l1l_opy_() == bstack1l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᑜ"):
        if bstack1l1ll11ll1_opy_():
            info[bstack1l1l1l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᑝ")] = bstack1l1l1l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᑞ")
        elif driver.capabilities.get(bstack1l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑟ"), {}).get(bstack1l1l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᑠ"), False):
            info[bstack1l1l1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᑡ")] = bstack1l1l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᑢ")
        else:
            info[bstack1l1l1l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᑣ")] = bstack1l1l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᑤ")
    return info
def bstack1l1ll11ll1_opy_():
    if bstack1l1111lll1_opy_.get_property(bstack1l1l1l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᑥ")):
        return True
    if bstack1ll1l1lll_opy_(os.environ.get(bstack1l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᑦ"), None)):
        return True
    return False
def bstack1ll1lll11l_opy_(bstack11111111l1_opy_, url, data, config):
    headers = config.get(bstack1l1l1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᑧ"), None)
    proxies = bstack11ll1l111_opy_(config, url)
    auth = config.get(bstack1l1l1l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᑨ"), None)
    response = requests.request(
            bstack11111111l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11l1l1ll_opy_(bstack1l1ll1lll_opy_, size):
    bstack1l11ll11l1_opy_ = []
    while len(bstack1l1ll1lll_opy_) > size:
        bstack1ll1ll111_opy_ = bstack1l1ll1lll_opy_[:size]
        bstack1l11ll11l1_opy_.append(bstack1ll1ll111_opy_)
        bstack1l1ll1lll_opy_ = bstack1l1ll1lll_opy_[size:]
    bstack1l11ll11l1_opy_.append(bstack1l1ll1lll_opy_)
    return bstack1l11ll11l1_opy_
def bstack1lllll1llll_opy_(message, bstack1111ll1lll_opy_=False):
    os.write(1, bytes(message, bstack1l1l1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᑩ")))
    os.write(1, bytes(bstack1l1l1l_opy_ (u"ࠫࡡࡴࠧᑪ"), bstack1l1l1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᑫ")))
    if bstack1111ll1lll_opy_:
        with open(bstack1l1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬᑬ") + os.environ[bstack1l1l1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᑭ")] + bstack1l1l1l_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭ᑮ"), bstack1l1l1l_opy_ (u"ࠩࡤࠫᑯ")) as f:
            f.write(message + bstack1l1l1l_opy_ (u"ࠪࡠࡳ࠭ᑰ"))
def bstack1111ll1111_opy_():
    return os.environ[bstack1l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᑱ")].lower() == bstack1l1l1l_opy_ (u"ࠬࡺࡲࡶࡧࠪᑲ")
def bstack1l11ll1lll_opy_(bstack1llllll111l_opy_):
    return bstack1l1l1l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᑳ").format(bstack111l11l111_opy_, bstack1llllll111l_opy_)
def bstack1lll1ll1l_opy_():
    return bstack11l11l1l11_opy_().replace(tzinfo=None).isoformat() + bstack1l1l1l_opy_ (u"࡛ࠧࠩᑴ")
def bstack1111l111l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1l1l_opy_ (u"ࠨ࡜ࠪᑵ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1l1l_opy_ (u"ࠩ࡝ࠫᑶ")))).total_seconds() * 1000
def bstack11111ll11l_opy_(timestamp):
    return bstack1llllll11ll_opy_(timestamp).isoformat() + bstack1l1l1l_opy_ (u"ࠪ࡞ࠬᑷ")
def bstack11111ll111_opy_(bstack111111llll_opy_):
    date_format = bstack1l1l1l_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩᑸ")
    bstack1lllll1l11l_opy_ = datetime.datetime.strptime(bstack111111llll_opy_, date_format)
    return bstack1lllll1l11l_opy_.isoformat() + bstack1l1l1l_opy_ (u"ࠬࡠࠧᑹ")
def bstack11111l1l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᑺ")
    else:
        return bstack1l1l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᑻ")
def bstack1ll1l1lll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᑼ")
def bstack1111l1111l_opy_(val):
    return val.__str__().lower() == bstack1l1l1l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᑽ")
def bstack11l11l11ll_opy_(bstack1111111111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111111111_opy_ as e:
                print(bstack1l1l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᑾ").format(func.__name__, bstack1111111111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1lllll1ll1l_opy_(bstack1llllll1111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1llllll1111_opy_(cls, *args, **kwargs)
            except bstack1111111111_opy_ as e:
                print(bstack1l1l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᑿ").format(bstack1llllll1111_opy_.__name__, bstack1111111111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1lllll1ll1l_opy_
    else:
        return decorator
def bstack1lll1ll11l_opy_(bstack11l1111ll1_opy_):
    if bstack1l1l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᒀ") in bstack11l1111ll1_opy_ and bstack1111l1111l_opy_(bstack11l1111ll1_opy_[bstack1l1l1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᒁ")]):
        return False
    if bstack1l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᒂ") in bstack11l1111ll1_opy_ and bstack1111l1111l_opy_(bstack11l1111ll1_opy_[bstack1l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᒃ")]):
        return False
    return True
def bstack11llllll1l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1ll11111ll_opy_(hub_url, CONFIG):
    if bstack111l11l11_opy_() <= version.parse(bstack1l1l1l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᒄ")):
        if hub_url != bstack1l1l1l_opy_ (u"ࠪࠫᒅ"):
            return bstack1l1l1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᒆ") + hub_url + bstack1l1l1l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᒇ")
        return bstack1l1ll1l1ll_opy_
    if hub_url != bstack1l1l1l_opy_ (u"࠭ࠧᒈ"):
        return bstack1l1l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᒉ") + hub_url + bstack1l1l1l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤᒊ")
    return bstack1llll11ll1_opy_
def bstack1lllllll1l1_opy_():
    return isinstance(os.getenv(bstack1l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨᒋ")), str)
def bstack1llll111l1_opy_(url):
    return urlparse(url).hostname
def bstack11llll1l1_opy_(hostname):
    for bstack1l111l11ll_opy_ in bstack11l1111l1_opy_:
        regex = re.compile(bstack1l111l11ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1111ll1l1l_opy_(bstack1111l111ll_opy_, file_name, logger):
    bstack1lll1ll1_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l_opy_ (u"ࠪࢂࠬᒌ")), bstack1111l111ll_opy_)
    try:
        if not os.path.exists(bstack1lll1ll1_opy_):
            os.makedirs(bstack1lll1ll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1l1l_opy_ (u"ࠫࢃ࠭ᒍ")), bstack1111l111ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1l1l_opy_ (u"ࠬࡽࠧᒎ")):
                pass
            with open(file_path, bstack1l1l1l_opy_ (u"ࠨࡷࠬࠤᒏ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll111l11_opy_.format(str(e)))
def bstack1111l1ll11_opy_(file_name, key, value, logger):
    file_path = bstack1111ll1l1l_opy_(bstack1l1l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᒐ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1111ll1_opy_ = json.load(open(file_path, bstack1l1l1l_opy_ (u"ࠨࡴࡥࠫᒑ")))
        else:
            bstack1ll1111ll1_opy_ = {}
        bstack1ll1111ll1_opy_[key] = value
        with open(file_path, bstack1l1l1l_opy_ (u"ࠤࡺ࠯ࠧᒒ")) as outfile:
            json.dump(bstack1ll1111ll1_opy_, outfile)
def bstack1lll111l11_opy_(file_name, logger):
    file_path = bstack1111ll1l1l_opy_(bstack1l1l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᒓ"), file_name, logger)
    bstack1ll1111ll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1l1l_opy_ (u"ࠫࡷ࠭ᒔ")) as bstack1lllll11l_opy_:
            bstack1ll1111ll1_opy_ = json.load(bstack1lllll11l_opy_)
    return bstack1ll1111ll1_opy_
def bstack11ll11ll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᒕ") + file_path + bstack1l1l1l_opy_ (u"࠭ࠠࠨᒖ") + str(e))
def bstack111l11l11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1l1l_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᒗ")
def bstack1l11l11lll_opy_(config):
    if bstack1l1l1l_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᒘ") in config:
        del (config[bstack1l1l1l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᒙ")])
        return False
    if bstack111l11l11_opy_() < version.parse(bstack1l1l1l_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᒚ")):
        return False
    if bstack111l11l11_opy_() >= version.parse(bstack1l1l1l_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᒛ")):
        return True
    if bstack1l1l1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᒜ") in config and config[bstack1l1l1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᒝ")] is False:
        return False
    else:
        return True
def bstack11l11lll1_opy_(args_list, bstack1111llll1l_opy_):
    index = -1
    for value in bstack1111llll1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11ll1l1l11_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11ll1l1l11_opy_ = bstack11ll1l1l11_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᒞ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᒟ"), exception=exception)
    def bstack111lllll1l_opy_(self):
        if self.result != bstack1l1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᒠ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1l1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᒡ") in self.exception_type:
            return bstack1l1l1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᒢ")
        return bstack1l1l1l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᒣ")
    def bstack111111ll11_opy_(self):
        if self.result != bstack1l1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒤ"):
            return None
        if self.bstack11ll1l1l11_opy_:
            return self.bstack11ll1l1l11_opy_
        return bstack11111llll1_opy_(self.exception)
def bstack11111llll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111lll1ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11lll1l111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1lll1lll11_opy_(config, logger):
    try:
        import playwright
        bstack111111l1ll_opy_ = playwright.__file__
        bstack1llllll1lll_opy_ = os.path.split(bstack111111l1ll_opy_)
        bstack111111111l_opy_ = bstack1llllll1lll_opy_[0] + bstack1l1l1l_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᒥ")
        os.environ[bstack1l1l1l_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᒦ")] = bstack1111l111_opy_(config)
        with open(bstack111111111l_opy_, bstack1l1l1l_opy_ (u"ࠩࡵࠫᒧ")) as f:
            bstack11ll1llll_opy_ = f.read()
            bstack1llllll1l11_opy_ = bstack1l1l1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᒨ")
            bstack1111111lll_opy_ = bstack11ll1llll_opy_.find(bstack1llllll1l11_opy_)
            if bstack1111111lll_opy_ == -1:
              process = subprocess.Popen(bstack1l1l1l_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᒩ"), shell=True, cwd=bstack1llllll1lll_opy_[0])
              process.wait()
              bstack1111ll11l1_opy_ = bstack1l1l1l_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬᒪ")
              bstack1llllllll1l_opy_ = bstack1l1l1l_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥᒫ")
              bstack1111l11ll1_opy_ = bstack11ll1llll_opy_.replace(bstack1111ll11l1_opy_, bstack1llllllll1l_opy_)
              with open(bstack111111111l_opy_, bstack1l1l1l_opy_ (u"ࠧࡸࠩᒬ")) as f:
                f.write(bstack1111l11ll1_opy_)
    except Exception as e:
        logger.error(bstack1llll1lll1_opy_.format(str(e)))
def bstack1l111111l1_opy_():
  try:
    bstack1111l1l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᒭ"))
    bstack11111l11ll_opy_ = []
    if os.path.exists(bstack1111l1l1ll_opy_):
      with open(bstack1111l1l1ll_opy_) as f:
        bstack11111l11ll_opy_ = json.load(f)
      os.remove(bstack1111l1l1ll_opy_)
    return bstack11111l11ll_opy_
  except:
    pass
  return []
def bstack1l11111l_opy_(bstack111lll1l1_opy_):
  try:
    bstack11111l11ll_opy_ = []
    bstack1111l1l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᒮ"))
    if os.path.exists(bstack1111l1l1ll_opy_):
      with open(bstack1111l1l1ll_opy_) as f:
        bstack11111l11ll_opy_ = json.load(f)
    bstack11111l11ll_opy_.append(bstack111lll1l1_opy_)
    with open(bstack1111l1l1ll_opy_, bstack1l1l1l_opy_ (u"ࠪࡻࠬᒯ")) as f:
        json.dump(bstack11111l11ll_opy_, f)
  except:
    pass
def bstack11lll1l1l1_opy_(logger, bstack1111llll11_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1l1l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᒰ"), bstack1l1l1l_opy_ (u"ࠬ࠭ᒱ"))
    if test_name == bstack1l1l1l_opy_ (u"࠭ࠧᒲ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ᒳ"), bstack1l1l1l_opy_ (u"ࠨࠩᒴ"))
    bstack11111l1lll_opy_ = bstack1l1l1l_opy_ (u"ࠩ࠯ࠤࠬᒵ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111llll11_opy_:
        bstack111ll111l_opy_ = os.environ.get(bstack1l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒶ"), bstack1l1l1l_opy_ (u"ࠫ࠵࠭ᒷ"))
        bstack11ll1llll1_opy_ = {bstack1l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᒸ"): test_name, bstack1l1l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᒹ"): bstack11111l1lll_opy_, bstack1l1l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᒺ"): bstack111ll111l_opy_}
        bstack111111ll1l_opy_ = []
        bstack11111l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᒻ"))
        if os.path.exists(bstack11111l111l_opy_):
            with open(bstack11111l111l_opy_) as f:
                bstack111111ll1l_opy_ = json.load(f)
        bstack111111ll1l_opy_.append(bstack11ll1llll1_opy_)
        with open(bstack11111l111l_opy_, bstack1l1l1l_opy_ (u"ࠩࡺࠫᒼ")) as f:
            json.dump(bstack111111ll1l_opy_, f)
    else:
        bstack11ll1llll1_opy_ = {bstack1l1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᒽ"): test_name, bstack1l1l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᒾ"): bstack11111l1lll_opy_, bstack1l1l1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᒿ"): str(multiprocessing.current_process().name)}
        if bstack1l1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪᓀ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11ll1llll1_opy_)
  except Exception as e:
      logger.warn(bstack1l1l1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᓁ").format(e))
def bstack11lllll1_opy_(error_message, test_name, index, logger):
  try:
    bstack1111l11l11_opy_ = []
    bstack11ll1llll1_opy_ = {bstack1l1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᓂ"): test_name, bstack1l1l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᓃ"): error_message, bstack1l1l1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᓄ"): index}
    bstack111111l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᓅ"))
    if os.path.exists(bstack111111l1l1_opy_):
        with open(bstack111111l1l1_opy_) as f:
            bstack1111l11l11_opy_ = json.load(f)
    bstack1111l11l11_opy_.append(bstack11ll1llll1_opy_)
    with open(bstack111111l1l1_opy_, bstack1l1l1l_opy_ (u"ࠬࡽࠧᓆ")) as f:
        json.dump(bstack1111l11l11_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1l1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᓇ").format(e))
def bstack1l1ll111l1_opy_(bstack1llll11111_opy_, name, logger):
  try:
    bstack11ll1llll1_opy_ = {bstack1l1l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᓈ"): name, bstack1l1l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᓉ"): bstack1llll11111_opy_, bstack1l1l1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᓊ"): str(threading.current_thread()._name)}
    return bstack11ll1llll1_opy_
  except Exception as e:
    logger.warn(bstack1l1l1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᓋ").format(e))
  return
def bstack1lllll1lll1_opy_():
    return platform.system() == bstack1l1l1l_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬᓌ")
def bstack11111l111_opy_(bstack1111111l1l_opy_, config, logger):
    bstack11111lllll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111111l1l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦᓍ").format(e))
    return bstack11111lllll_opy_
def bstack1111l1l11l_opy_(bstack1lllllll11l_opy_, bstack1111ll11ll_opy_):
    bstack1lllll1l1l1_opy_ = version.parse(bstack1lllllll11l_opy_)
    bstack1111l11lll_opy_ = version.parse(bstack1111ll11ll_opy_)
    if bstack1lllll1l1l1_opy_ > bstack1111l11lll_opy_:
        return 1
    elif bstack1lllll1l1l1_opy_ < bstack1111l11lll_opy_:
        return -1
    else:
        return 0
def bstack11l11l1l11_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1llllll11ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l1l111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lll11llll_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack1l1l1l_opy_ (u"࠭ࡧࡦࡶࠪᓎ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1ll1l111_opy_ = caps.get(bstack1l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᓏ"))
    bstack1lllllll111_opy_ = True
    if bstack1111l1111l_opy_(caps.get(bstack1l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧᓐ"))) or bstack1111l1111l_opy_(caps.get(bstack1l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩᓑ"))):
        bstack1lllllll111_opy_ = False
    if bstack1l11l11lll_opy_({bstack1l1l1l_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥᓒ"): bstack1lllllll111_opy_}):
        bstack1l1ll1l111_opy_ = bstack1l1ll1l111_opy_ or {}
        bstack1l1ll1l111_opy_[bstack1l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᓓ")] = bstack1111l1l111_opy_(framework)
        bstack1l1ll1l111_opy_[bstack1l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᓔ")] = bstack1111ll1111_opy_()
        if getattr(options, bstack1l1l1l_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧᓕ"), None):
            options.set_capability(bstack1l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᓖ"), bstack1l1ll1l111_opy_)
        else:
            options[bstack1l1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᓗ")] = bstack1l1ll1l111_opy_
    else:
        if getattr(options, bstack1l1l1l_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᓘ"), None):
            options.set_capability(bstack1l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᓙ"), bstack1111l1l111_opy_(framework))
            options.set_capability(bstack1l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᓚ"), bstack1111ll1111_opy_())
        else:
            options[bstack1l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᓛ")] = bstack1111l1l111_opy_(framework)
            options[bstack1l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᓜ")] = bstack1111ll1111_opy_()
    return options
def bstack1111lll111_opy_(bstack1llllll1ll1_opy_, framework):
    if bstack1llllll1ll1_opy_ and len(bstack1llllll1ll1_opy_.split(bstack1l1l1l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᓝ"))) > 1:
        ws_url = bstack1llllll1ll1_opy_.split(bstack1l1l1l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᓞ"))[0]
        if bstack1l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᓟ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1llllllllll_opy_ = json.loads(urllib.parse.unquote(bstack1llllll1ll1_opy_.split(bstack1l1l1l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᓠ"))[1]))
            bstack1llllllllll_opy_ = bstack1llllllllll_opy_ or {}
            bstack1llllllllll_opy_[bstack1l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᓡ")] = str(framework) + str(__version__)
            bstack1llllllllll_opy_[bstack1l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᓢ")] = bstack1111ll1111_opy_()
            bstack1llllll1ll1_opy_ = bstack1llllll1ll1_opy_.split(bstack1l1l1l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᓣ"))[0] + bstack1l1l1l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᓤ") + urllib.parse.quote(json.dumps(bstack1llllllllll_opy_))
    return bstack1llllll1ll1_opy_
def bstack1lll1l1lll_opy_():
    global bstack1lll11l11l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1lll11l11l_opy_ = BrowserType.connect
    return bstack1lll11l11l_opy_
def bstack1ll111ll_opy_(framework_name):
    global bstack1llll1l1ll_opy_
    bstack1llll1l1ll_opy_ = framework_name
    return framework_name
def bstack1ll1111ll_opy_(self, *args, **kwargs):
    global bstack1lll11l11l_opy_
    try:
        global bstack1llll1l1ll_opy_
        if bstack1l1l1l_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᓥ") in kwargs:
            kwargs[bstack1l1l1l_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᓦ")] = bstack1111lll111_opy_(
                kwargs.get(bstack1l1l1l_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᓧ"), None),
                bstack1llll1l1ll_opy_
            )
    except Exception as e:
        logger.error(bstack1l1l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦᓨ").format(str(e)))
    return bstack1lll11l11l_opy_(self, *args, **kwargs)
def bstack111111lll1_opy_(bstack11111l11l1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11ll1l111_opy_(bstack11111l11l1_opy_, bstack1l1l1l_opy_ (u"ࠧࠨᓩ"))
        if proxies and proxies.get(bstack1l1l1l_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᓪ")):
            parsed_url = urlparse(proxies.get(bstack1l1l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᓫ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᓬ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᓭ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᓮ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᓯ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1111ll1l1_opy_(bstack11111l11l1_opy_):
    bstack1111l1lll1_opy_ = {
        bstack1111lllll1_opy_[bstack111111l11l_opy_]: bstack11111l11l1_opy_[bstack111111l11l_opy_]
        for bstack111111l11l_opy_ in bstack11111l11l1_opy_
        if bstack111111l11l_opy_ in bstack1111lllll1_opy_
    }
    bstack1111l1lll1_opy_[bstack1l1l1l_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᓰ")] = bstack111111lll1_opy_(bstack11111l11l1_opy_, bstack1l1111lll1_opy_.get_property(bstack1l1l1l_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᓱ")))
    bstack1111ll1ll1_opy_ = [element.lower() for element in bstack111l11l11l_opy_]
    bstack11111ll1l1_opy_(bstack1111l1lll1_opy_, bstack1111ll1ll1_opy_)
    return bstack1111l1lll1_opy_
def bstack11111ll1l1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1l1l_opy_ (u"ࠢࠫࠬ࠭࠮ࠧᓲ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11111ll1l1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11111ll1l1_opy_(item, keys)