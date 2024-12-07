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
from bstack_utils.constants import (bstack111l111lll_opy_, bstack1l1ll111l_opy_, bstack11lll1l111_opy_, bstack1llll1l1ll_opy_,
                                    bstack111l1111ll_opy_, bstack111l111l1l_opy_, bstack111l11l1ll_opy_, bstack111l11l111_opy_)
from bstack_utils.messages import bstack1llll1l111_opy_, bstack1l11l1l1ll_opy_
from bstack_utils.proxy import bstack111lll11l_opy_, bstack11l11l1ll_opy_
bstack1l1111l111_opy_ = Config.bstack1lll1ll111_opy_()
logger = logging.getLogger(__name__)
def bstack111llll1ll_opy_(config):
    return config[bstack11ll11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫጦ")]
def bstack111ll11111_opy_(config):
    return config[bstack11ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ጧ")]
def bstack1l111111_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1lllllll11l_opy_(obj):
    values = []
    bstack111111l1l1_opy_ = re.compile(bstack11ll11l_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣጨ"), re.I)
    for key in obj.keys():
        if bstack111111l1l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1111111ll1_opy_(config):
    tags = []
    tags.extend(bstack1lllllll11l_opy_(os.environ))
    tags.extend(bstack1lllllll11l_opy_(config))
    return tags
def bstack1lllllllll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1llllll1l11_opy_(bstack1111l1l11l_opy_):
    if not bstack1111l1l11l_opy_:
        return bstack11ll11l_opy_ (u"ࠬ࠭ጩ")
    return bstack11ll11l_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢጪ").format(bstack1111l1l11l_opy_.name, bstack1111l1l11l_opy_.email)
def bstack111ll1ll11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111lll1l1_opy_ = repo.common_dir
        info = {
            bstack11ll11l_opy_ (u"ࠢࡴࡪࡤࠦጫ"): repo.head.commit.hexsha,
            bstack11ll11l_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦጬ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11ll11l_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤጭ"): repo.active_branch.name,
            bstack11ll11l_opy_ (u"ࠥࡸࡦ࡭ࠢጮ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11ll11l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢጯ"): bstack1llllll1l11_opy_(repo.head.commit.committer),
            bstack11ll11l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨጰ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11ll11l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨጱ"): bstack1llllll1l11_opy_(repo.head.commit.author),
            bstack11ll11l_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧጲ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11ll11l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤጳ"): repo.head.commit.message,
            bstack11ll11l_opy_ (u"ࠤࡵࡳࡴࡺࠢጴ"): repo.git.rev_parse(bstack11ll11l_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧጵ")),
            bstack11ll11l_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧጶ"): bstack1111lll1l1_opy_,
            bstack11ll11l_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣጷ"): subprocess.check_output([bstack11ll11l_opy_ (u"ࠨࡧࡪࡶࠥጸ"), bstack11ll11l_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥጹ"), bstack11ll11l_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦጺ")]).strip().decode(
                bstack11ll11l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨጻ")),
            bstack11ll11l_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧጼ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11ll11l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨጽ"): repo.git.rev_list(
                bstack11ll11l_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧጾ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111111l11_opy_ = []
        for remote in remotes:
            bstack1111ll1l1l_opy_ = {
                bstack11ll11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጿ"): remote.name,
                bstack11ll11l_opy_ (u"ࠢࡶࡴ࡯ࠦፀ"): remote.url,
            }
            bstack1111111l11_opy_.append(bstack1111ll1l1l_opy_)
        bstack111111ll11_opy_ = {
            bstack11ll11l_opy_ (u"ࠣࡰࡤࡱࡪࠨፁ"): bstack11ll11l_opy_ (u"ࠤࡪ࡭ࡹࠨፂ"),
            **info,
            bstack11ll11l_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦፃ"): bstack1111111l11_opy_
        }
        bstack111111ll11_opy_ = bstack1111l11111_opy_(bstack111111ll11_opy_)
        return bstack111111ll11_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11ll11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢፄ").format(err))
        return {}
def bstack1111l11111_opy_(bstack111111ll11_opy_):
    bstack11111111ll_opy_ = bstack1111ll11l1_opy_(bstack111111ll11_opy_)
    if bstack11111111ll_opy_ and bstack11111111ll_opy_ > bstack111l1111ll_opy_:
        bstack111111ll1l_opy_ = bstack11111111ll_opy_ - bstack111l1111ll_opy_
        bstack1llllllll11_opy_ = bstack1llllllllll_opy_(bstack111111ll11_opy_[bstack11ll11l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨፅ")], bstack111111ll1l_opy_)
        bstack111111ll11_opy_[bstack11ll11l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢፆ")] = bstack1llllllll11_opy_
        logger.info(bstack11ll11l_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤፇ")
                    .format(bstack1111ll11l1_opy_(bstack111111ll11_opy_) / 1024))
    return bstack111111ll11_opy_
def bstack1111ll11l1_opy_(bstack11l11l1l_opy_):
    try:
        if bstack11l11l1l_opy_:
            bstack111111llll_opy_ = json.dumps(bstack11l11l1l_opy_)
            bstack1llllll11l1_opy_ = sys.getsizeof(bstack111111llll_opy_)
            return bstack1llllll11l1_opy_
    except Exception as e:
        logger.debug(bstack11ll11l_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣፈ").format(e))
    return -1
def bstack1llllllllll_opy_(field, bstack11111lllll_opy_):
    try:
        bstack1111l1l1ll_opy_ = len(bytes(bstack111l111l1l_opy_, bstack11ll11l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨፉ")))
        bstack1111lll11l_opy_ = bytes(field, bstack11ll11l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩፊ"))
        bstack111111lll1_opy_ = len(bstack1111lll11l_opy_)
        bstack11111lll1l_opy_ = ceil(bstack111111lll1_opy_ - bstack11111lllll_opy_ - bstack1111l1l1ll_opy_)
        if bstack11111lll1l_opy_ > 0:
            bstack1llllll1l1l_opy_ = bstack1111lll11l_opy_[:bstack11111lll1l_opy_].decode(bstack11ll11l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪፋ"), errors=bstack11ll11l_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬፌ")) + bstack111l111l1l_opy_
            return bstack1llllll1l1l_opy_
    except Exception as e:
        logger.debug(bstack11ll11l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦፍ").format(e))
    return field
def bstack11l1ll1l1_opy_():
    env = os.environ
    if (bstack11ll11l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧፎ") in env and len(env[bstack11ll11l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨፏ")]) > 0) or (
            bstack11ll11l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣፐ") in env and len(env[bstack11ll11l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤፑ")]) > 0):
        return {
            bstack11ll11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤፒ"): bstack11ll11l_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨፓ"),
            bstack11ll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤፔ"): env.get(bstack11ll11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥፕ")),
            bstack11ll11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥፖ"): env.get(bstack11ll11l_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦፗ")),
            bstack11ll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤፘ"): env.get(bstack11ll11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥፙ"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠧࡉࡉࠣፚ")) == bstack11ll11l_opy_ (u"ࠨࡴࡳࡷࡨࠦ፛") and bstack111111ll1_opy_(env.get(bstack11ll11l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤ፜"))):
        return {
            bstack11ll11l_opy_ (u"ࠣࡰࡤࡱࡪࠨ፝"): bstack11ll11l_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦ፞"),
            bstack11ll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ፟"): env.get(bstack11ll11l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ፠")),
            bstack11ll11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ፡"): env.get(bstack11ll11l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥ።")),
            bstack11ll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፣"): env.get(bstack11ll11l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦ፤"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠤࡆࡍࠧ፥")) == bstack11ll11l_opy_ (u"ࠥࡸࡷࡻࡥࠣ፦") and bstack111111ll1_opy_(env.get(bstack11ll11l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦ፧"))):
        return {
            bstack11ll11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ፨"): bstack11ll11l_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤ፩"),
            bstack11ll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ፪"): env.get(bstack11ll11l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣ፫")),
            bstack11ll11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ፬"): env.get(bstack11ll11l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ፭")),
            bstack11ll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ፮"): env.get(bstack11ll11l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ፯"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠨࡃࡊࠤ፰")) == bstack11ll11l_opy_ (u"ࠢࡵࡴࡸࡩࠧ፱") and env.get(bstack11ll11l_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤ፲")) == bstack11ll11l_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦ፳"):
        return {
            bstack11ll11l_opy_ (u"ࠥࡲࡦࡳࡥࠣ፴"): bstack11ll11l_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨ፵"),
            bstack11ll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ፶"): None,
            bstack11ll11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ፷"): None,
            bstack11ll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፸"): None
        }
    if env.get(bstack11ll11l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦ፹")) and env.get(bstack11ll11l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧ፺")):
        return {
            bstack11ll11l_opy_ (u"ࠥࡲࡦࡳࡥࠣ፻"): bstack11ll11l_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢ፼"),
            bstack11ll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ፽"): env.get(bstack11ll11l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦ፾")),
            bstack11ll11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ፿"): None,
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᎀ"): env.get(bstack11ll11l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᎁ"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠥࡇࡎࠨᎂ")) == bstack11ll11l_opy_ (u"ࠦࡹࡸࡵࡦࠤᎃ") and bstack111111ll1_opy_(env.get(bstack11ll11l_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᎄ"))):
        return {
            bstack11ll11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎅ"): bstack11ll11l_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨᎆ"),
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎇ"): env.get(bstack11ll11l_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧᎈ")),
            bstack11ll11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᎉ"): None,
            bstack11ll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᎊ"): env.get(bstack11ll11l_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᎋ"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠨࡃࡊࠤᎌ")) == bstack11ll11l_opy_ (u"ࠢࡵࡴࡸࡩࠧᎍ") and bstack111111ll1_opy_(env.get(bstack11ll11l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᎎ"))):
        return {
            bstack11ll11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᎏ"): bstack11ll11l_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨ᎐"),
            bstack11ll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᎑"): env.get(bstack11ll11l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦ᎒")),
            bstack11ll11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᎓"): env.get(bstack11ll11l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᎔")),
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᎕"): env.get(bstack11ll11l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧ᎖"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠥࡇࡎࠨ᎗")) == bstack11ll11l_opy_ (u"ࠦࡹࡸࡵࡦࠤ᎘") and bstack111111ll1_opy_(env.get(bstack11ll11l_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣ᎙"))):
        return {
            bstack11ll11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᎚"): bstack11ll11l_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢ᎛"),
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᎜"): env.get(bstack11ll11l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨ᎝")),
            bstack11ll11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᎞"): env.get(bstack11ll11l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᎟")),
            bstack11ll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᎠ"): env.get(bstack11ll11l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᎡ"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠢࡄࡋࠥᎢ")) == bstack11ll11l_opy_ (u"ࠣࡶࡵࡹࡪࠨᎣ") and bstack111111ll1_opy_(env.get(bstack11ll11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᎤ"))):
        return {
            bstack11ll11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᎥ"): bstack11ll11l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᎦ"),
            bstack11ll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎧ"): env.get(bstack11ll11l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᎨ")),
            bstack11ll11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎩ"): env.get(bstack11ll11l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᎪ")) or env.get(bstack11ll11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᎫ")),
            bstack11ll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᎬ"): env.get(bstack11ll11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᎭ"))
        }
    if bstack111111ll1_opy_(env.get(bstack11ll11l_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᎮ"))):
        return {
            bstack11ll11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎯ"): bstack11ll11l_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᎰ"),
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎱ"): bstack11ll11l_opy_ (u"ࠤࡾࢁࢀࢃࠢᎲ").format(env.get(bstack11ll11l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭Ꮃ")), env.get(bstack11ll11l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᎴ"))),
            bstack11ll11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᎵ"): env.get(bstack11ll11l_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᎶ")),
            bstack11ll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᎷ"): env.get(bstack11ll11l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᎸ"))
        }
    if bstack111111ll1_opy_(env.get(bstack11ll11l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᎹ"))):
        return {
            bstack11ll11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᎺ"): bstack11ll11l_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨᎻ"),
            bstack11ll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎼ"): bstack11ll11l_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧᎽ").format(env.get(bstack11ll11l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭Ꮎ")), env.get(bstack11ll11l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᎿ")), env.get(bstack11ll11l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᏀ")), env.get(bstack11ll11l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᏁ"))),
            bstack11ll11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᏂ"): env.get(bstack11ll11l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᏃ")),
            bstack11ll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᏄ"): env.get(bstack11ll11l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᏅ"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᏆ")) and env.get(bstack11ll11l_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᏇ")):
        return {
            bstack11ll11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᏈ"): bstack11ll11l_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨᏉ"),
            bstack11ll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏊ"): bstack11ll11l_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤᏋ").format(env.get(bstack11ll11l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᏌ")), env.get(bstack11ll11l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭Ꮝ")), env.get(bstack11ll11l_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩᏎ"))),
            bstack11ll11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᏏ"): env.get(bstack11ll11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᏐ")),
            bstack11ll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏑ"): env.get(bstack11ll11l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᏒ"))
        }
    if any([env.get(bstack11ll11l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᏓ")), env.get(bstack11ll11l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᏔ")), env.get(bstack11ll11l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᏕ"))]):
        return {
            bstack11ll11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᏖ"): bstack11ll11l_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦᏗ"),
            bstack11ll11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏘ"): env.get(bstack11ll11l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᏙ")),
            bstack11ll11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᏚ"): env.get(bstack11ll11l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᏛ")),
            bstack11ll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᏜ"): env.get(bstack11ll11l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᏝ"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᏞ")):
        return {
            bstack11ll11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏟ"): bstack11ll11l_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᏠ"),
            bstack11ll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᏡ"): env.get(bstack11ll11l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᏢ")),
            bstack11ll11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏣ"): env.get(bstack11ll11l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᏤ")),
            bstack11ll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏥ"): env.get(bstack11ll11l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᏦ"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᏧ")) or env.get(bstack11ll11l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᏨ")):
        return {
            bstack11ll11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᏩ"): bstack11ll11l_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᏪ"),
            bstack11ll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᏫ"): env.get(bstack11ll11l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᏬ")),
            bstack11ll11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᏭ"): bstack11ll11l_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᏮ") if env.get(bstack11ll11l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᏯ")) else None,
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᏰ"): env.get(bstack11ll11l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᏱ"))
        }
    if any([env.get(bstack11ll11l_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᏲ")), env.get(bstack11ll11l_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᏳ")), env.get(bstack11ll11l_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᏴ"))]):
        return {
            bstack11ll11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᏵ"): bstack11ll11l_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨ᏶"),
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᏷"): None,
            bstack11ll11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏸ"): env.get(bstack11ll11l_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᏹ")),
            bstack11ll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏺ"): env.get(bstack11ll11l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᏻ"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᏼ")):
        return {
            bstack11ll11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᏽ"): bstack11ll11l_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦ᏾"),
            bstack11ll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᏿"): env.get(bstack11ll11l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᐀")),
            bstack11ll11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᐁ"): bstack11ll11l_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᐂ").format(env.get(bstack11ll11l_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᐃ"))) if env.get(bstack11ll11l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᐄ")) else None,
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐅ"): env.get(bstack11ll11l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᐆ"))
        }
    if bstack111111ll1_opy_(env.get(bstack11ll11l_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦᐇ"))):
        return {
            bstack11ll11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᐈ"): bstack11ll11l_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨᐉ"),
            bstack11ll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᐊ"): env.get(bstack11ll11l_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦᐋ")),
            bstack11ll11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᐌ"): env.get(bstack11ll11l_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧᐍ")),
            bstack11ll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᐎ"): env.get(bstack11ll11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᐏ"))
        }
    if bstack111111ll1_opy_(env.get(bstack11ll11l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᐐ"))):
        return {
            bstack11ll11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐑ"): bstack11ll11l_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᐒ"),
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐓ"): bstack11ll11l_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᐔ").format(env.get(bstack11ll11l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᐕ")), env.get(bstack11ll11l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᐖ")), env.get(bstack11ll11l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᐗ"))),
            bstack11ll11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᐘ"): env.get(bstack11ll11l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᐙ")),
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐚ"): env.get(bstack11ll11l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᐛ"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠥࡇࡎࠨᐜ")) == bstack11ll11l_opy_ (u"ࠦࡹࡸࡵࡦࠤᐝ") and env.get(bstack11ll11l_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᐞ")) == bstack11ll11l_opy_ (u"ࠨ࠱ࠣᐟ"):
        return {
            bstack11ll11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᐠ"): bstack11ll11l_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣᐡ"),
            bstack11ll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᐢ"): bstack11ll11l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨᐣ").format(env.get(bstack11ll11l_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨᐤ"))),
            bstack11ll11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᐥ"): None,
            bstack11ll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᐦ"): None,
        }
    if env.get(bstack11ll11l_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᐧ")):
        return {
            bstack11ll11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᐨ"): bstack11ll11l_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᐩ"),
            bstack11ll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᐪ"): None,
            bstack11ll11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᐫ"): env.get(bstack11ll11l_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨᐬ")),
            bstack11ll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᐭ"): env.get(bstack11ll11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᐮ"))
        }
    if any([env.get(bstack11ll11l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦᐯ")), env.get(bstack11ll11l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤᐰ")), env.get(bstack11ll11l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣᐱ")), env.get(bstack11ll11l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧᐲ"))]):
        return {
            bstack11ll11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᐳ"): bstack11ll11l_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᐴ"),
            bstack11ll11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᐵ"): None,
            bstack11ll11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᐶ"): env.get(bstack11ll11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᐷ")) or None,
            bstack11ll11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᐸ"): env.get(bstack11ll11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᐹ"), 0)
        }
    if env.get(bstack11ll11l_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᐺ")):
        return {
            bstack11ll11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐻ"): bstack11ll11l_opy_ (u"ࠢࡈࡱࡆࡈࠧᐼ"),
            bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐽ"): None,
            bstack11ll11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᐾ"): env.get(bstack11ll11l_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᐿ")),
            bstack11ll11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᑀ"): env.get(bstack11ll11l_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦᑁ"))
        }
    if env.get(bstack11ll11l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᑂ")):
        return {
            bstack11ll11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᑃ"): bstack11ll11l_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᑄ"),
            bstack11ll11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᑅ"): env.get(bstack11ll11l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᑆ")),
            bstack11ll11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᑇ"): env.get(bstack11ll11l_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᑈ")),
            bstack11ll11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᑉ"): env.get(bstack11ll11l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᑊ"))
        }
    return {bstack11ll11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᑋ"): None}
def get_host_info():
    return {
        bstack11ll11l_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᑌ"): platform.node(),
        bstack11ll11l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᑍ"): platform.system(),
        bstack11ll11l_opy_ (u"ࠦࡹࡿࡰࡦࠤᑎ"): platform.machine(),
        bstack11ll11l_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᑏ"): platform.version(),
        bstack11ll11l_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᑐ"): platform.architecture()[0]
    }
def bstack1l1lll111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1111l111l1_opy_():
    if bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᑑ")):
        return bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᑒ")
    return bstack11ll11l_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᑓ")
def bstack11111l111l_opy_(driver):
    info = {
        bstack11ll11l_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᑔ"): driver.capabilities,
        bstack11ll11l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᑕ"): driver.session_id,
        bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᑖ"): driver.capabilities.get(bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᑗ"), None),
        bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᑘ"): driver.capabilities.get(bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᑙ"), None),
        bstack11ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᑚ"): driver.capabilities.get(bstack11ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᑛ"), None),
    }
    if bstack1111l111l1_opy_() == bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᑜ"):
        if bstack11lllll1l1_opy_():
            info[bstack11ll11l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᑝ")] = bstack11ll11l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᑞ")
        elif driver.capabilities.get(bstack11ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑟ"), {}).get(bstack11ll11l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᑠ"), False):
            info[bstack11ll11l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᑡ")] = bstack11ll11l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᑢ")
        else:
            info[bstack11ll11l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᑣ")] = bstack11ll11l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᑤ")
    return info
def bstack11lllll1l1_opy_():
    if bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᑥ")):
        return True
    if bstack111111ll1_opy_(os.environ.get(bstack11ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᑦ"), None)):
        return True
    return False
def bstack1l1l1111ll_opy_(bstack111111l11l_opy_, url, data, config):
    headers = config.get(bstack11ll11l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᑧ"), None)
    proxies = bstack111lll11l_opy_(config, url)
    auth = config.get(bstack11ll11l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᑨ"), None)
    response = requests.request(
            bstack111111l11l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l11l1l1l_opy_(bstack1llll11lll_opy_, size):
    bstack1l1ll11ll1_opy_ = []
    while len(bstack1llll11lll_opy_) > size:
        bstack1llll11l1_opy_ = bstack1llll11lll_opy_[:size]
        bstack1l1ll11ll1_opy_.append(bstack1llll11l1_opy_)
        bstack1llll11lll_opy_ = bstack1llll11lll_opy_[size:]
    bstack1l1ll11ll1_opy_.append(bstack1llll11lll_opy_)
    return bstack1l1ll11ll1_opy_
def bstack11111ll1ll_opy_(message, bstack11111l1l1l_opy_=False):
    os.write(1, bytes(message, bstack11ll11l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᑩ")))
    os.write(1, bytes(bstack11ll11l_opy_ (u"ࠫࡡࡴࠧᑪ"), bstack11ll11l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᑫ")))
    if bstack11111l1l1l_opy_:
        with open(bstack11ll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬᑬ") + os.environ[bstack11ll11l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᑭ")] + bstack11ll11l_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭ᑮ"), bstack11ll11l_opy_ (u"ࠩࡤࠫᑯ")) as f:
            f.write(message + bstack11ll11l_opy_ (u"ࠪࡠࡳ࠭ᑰ"))
def bstack1111ll1l11_opy_():
    return os.environ[bstack11ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᑱ")].lower() == bstack11ll11l_opy_ (u"ࠬࡺࡲࡶࡧࠪᑲ")
def bstack111l1111_opy_(bstack1lllll1lll1_opy_):
    return bstack11ll11l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᑳ").format(bstack111l111lll_opy_, bstack1lllll1lll1_opy_)
def bstack1lll1l1ll_opy_():
    return bstack11l11lll11_opy_().replace(tzinfo=None).isoformat() + bstack11ll11l_opy_ (u"࡛ࠧࠩᑴ")
def bstack1111111111_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11ll11l_opy_ (u"ࠨ࡜ࠪᑵ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11ll11l_opy_ (u"ࠩ࡝ࠫᑶ")))).total_seconds() * 1000
def bstack11111l1lll_opy_(timestamp):
    return bstack1lllllll1ll_opy_(timestamp).isoformat() + bstack11ll11l_opy_ (u"ࠪ࡞ࠬᑷ")
def bstack11111ll1l1_opy_(bstack11111l11l1_opy_):
    date_format = bstack11ll11l_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩᑸ")
    bstack1111ll111l_opy_ = datetime.datetime.strptime(bstack11111l11l1_opy_, date_format)
    return bstack1111ll111l_opy_.isoformat() + bstack11ll11l_opy_ (u"ࠬࡠࠧᑹ")
def bstack1111ll1lll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11ll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᑺ")
    else:
        return bstack11ll11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᑻ")
def bstack111111ll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11ll11l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᑼ")
def bstack1111l11l11_opy_(val):
    return val.__str__().lower() == bstack11ll11l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᑽ")
def bstack11l11l11ll_opy_(bstack1111l1l1l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111l1l1l1_opy_ as e:
                print(bstack11ll11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᑾ").format(func.__name__, bstack1111l1l1l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1111ll11ll_opy_(bstack11111l11ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11111l11ll_opy_(cls, *args, **kwargs)
            except bstack1111l1l1l1_opy_ as e:
                print(bstack11ll11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᑿ").format(bstack11111l11ll_opy_.__name__, bstack1111l1l1l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1111ll11ll_opy_
    else:
        return decorator
def bstack1l1ll111_opy_(bstack11l11l111l_opy_):
    if bstack11ll11l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᒀ") in bstack11l11l111l_opy_ and bstack1111l11l11_opy_(bstack11l11l111l_opy_[bstack11ll11l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᒁ")]):
        return False
    if bstack11ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᒂ") in bstack11l11l111l_opy_ and bstack1111l11l11_opy_(bstack11l11l111l_opy_[bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᒃ")]):
        return False
    return True
def bstack1lll1l1l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1ll1ll111l_opy_(hub_url, CONFIG):
    if bstack1ll111l1l1_opy_() <= version.parse(bstack11ll11l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᒄ")):
        if hub_url != bstack11ll11l_opy_ (u"ࠪࠫᒅ"):
            return bstack11ll11l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᒆ") + hub_url + bstack11ll11l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᒇ")
        return bstack11lll1l111_opy_
    if hub_url != bstack11ll11l_opy_ (u"࠭ࠧᒈ"):
        return bstack11ll11l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᒉ") + hub_url + bstack11ll11l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤᒊ")
    return bstack1llll1l1ll_opy_
def bstack1111llll11_opy_():
    return isinstance(os.getenv(bstack11ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨᒋ")), str)
def bstack1l111ll1l_opy_(url):
    return urlparse(url).hostname
def bstack1llll1ll11_opy_(hostname):
    for bstack1l11111lll_opy_ in bstack1l1ll111l_opy_:
        regex = re.compile(bstack1l11111lll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111111l1ll_opy_(bstack11111l1l11_opy_, file_name, logger):
    bstack111l1111l_opy_ = os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"ࠪࢂࠬᒌ")), bstack11111l1l11_opy_)
    try:
        if not os.path.exists(bstack111l1111l_opy_):
            os.makedirs(bstack111l1111l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11ll11l_opy_ (u"ࠫࢃ࠭ᒍ")), bstack11111l1l11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11ll11l_opy_ (u"ࠬࡽࠧᒎ")):
                pass
            with open(file_path, bstack11ll11l_opy_ (u"ࠨࡷࠬࠤᒏ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1llll1l111_opy_.format(str(e)))
def bstack11111ll11l_opy_(file_name, key, value, logger):
    file_path = bstack111111l1ll_opy_(bstack11ll11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᒐ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack111ll1l1_opy_ = json.load(open(file_path, bstack11ll11l_opy_ (u"ࠨࡴࡥࠫᒑ")))
        else:
            bstack111ll1l1_opy_ = {}
        bstack111ll1l1_opy_[key] = value
        with open(file_path, bstack11ll11l_opy_ (u"ࠤࡺ࠯ࠧᒒ")) as outfile:
            json.dump(bstack111ll1l1_opy_, outfile)
def bstack1111lll1l_opy_(file_name, logger):
    file_path = bstack111111l1ll_opy_(bstack11ll11l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᒓ"), file_name, logger)
    bstack111ll1l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11ll11l_opy_ (u"ࠫࡷ࠭ᒔ")) as bstack1l1l1lll1_opy_:
            bstack111ll1l1_opy_ = json.load(bstack1l1l1lll1_opy_)
    return bstack111ll1l1_opy_
def bstack1l11l1lll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11ll11l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᒕ") + file_path + bstack11ll11l_opy_ (u"࠭ࠠࠨᒖ") + str(e))
def bstack1ll111l1l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11ll11l_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᒗ")
def bstack1l1l1lll1l_opy_(config):
    if bstack11ll11l_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᒘ") in config:
        del (config[bstack11ll11l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᒙ")])
        return False
    if bstack1ll111l1l1_opy_() < version.parse(bstack11ll11l_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᒚ")):
        return False
    if bstack1ll111l1l1_opy_() >= version.parse(bstack11ll11l_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᒛ")):
        return True
    if bstack11ll11l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᒜ") in config and config[bstack11ll11l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᒝ")] is False:
        return False
    else:
        return True
def bstack111l1l1ll_opy_(args_list, bstack1lllll1l1l1_opy_):
    index = -1
    for value in bstack1lllll1l1l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11ll11ll1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11ll11ll1l_opy_ = bstack11ll11ll1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11ll11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᒞ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11ll11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᒟ"), exception=exception)
    def bstack111lllllll_opy_(self):
        if self.result != bstack11ll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᒠ"):
            return None
        if isinstance(self.exception_type, str) and bstack11ll11l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᒡ") in self.exception_type:
            return bstack11ll11l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᒢ")
        return bstack11ll11l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᒣ")
    def bstack1111l1ll11_opy_(self):
        if self.result != bstack11ll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒤ"):
            return None
        if self.bstack11ll11ll1l_opy_:
            return self.bstack11ll11ll1l_opy_
        return bstack1111lllll1_opy_(self.exception)
def bstack1111lllll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1lllll1llll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l111111l1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l111111_opy_(config, logger):
    try:
        import playwright
        bstack1111l111ll_opy_ = playwright.__file__
        bstack1111lll111_opy_ = os.path.split(bstack1111l111ll_opy_)
        bstack111111l111_opy_ = bstack1111lll111_opy_[0] + bstack11ll11l_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᒥ")
        os.environ[bstack11ll11l_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᒦ")] = bstack11l11l1ll_opy_(config)
        with open(bstack111111l111_opy_, bstack11ll11l_opy_ (u"ࠩࡵࠫᒧ")) as f:
            bstack111111l11_opy_ = f.read()
            bstack1111llll1l_opy_ = bstack11ll11l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᒨ")
            bstack1lllll1ll1l_opy_ = bstack111111l11_opy_.find(bstack1111llll1l_opy_)
            if bstack1lllll1ll1l_opy_ == -1:
              process = subprocess.Popen(bstack11ll11l_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᒩ"), shell=True, cwd=bstack1111lll111_opy_[0])
              process.wait()
              bstack11111lll11_opy_ = bstack11ll11l_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬᒪ")
              bstack1llllll1ll1_opy_ = bstack11ll11l_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥᒫ")
              bstack11111111l1_opy_ = bstack111111l11_opy_.replace(bstack11111lll11_opy_, bstack1llllll1ll1_opy_)
              with open(bstack111111l111_opy_, bstack11ll11l_opy_ (u"ࠧࡸࠩᒬ")) as f:
                f.write(bstack11111111l1_opy_)
    except Exception as e:
        logger.error(bstack1l11l1l1ll_opy_.format(str(e)))
def bstack1ll1ll11ll_opy_():
  try:
    bstack1111l11ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11l_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᒭ"))
    bstack1111l1llll_opy_ = []
    if os.path.exists(bstack1111l11ll1_opy_):
      with open(bstack1111l11ll1_opy_) as f:
        bstack1111l1llll_opy_ = json.load(f)
      os.remove(bstack1111l11ll1_opy_)
    return bstack1111l1llll_opy_
  except:
    pass
  return []
def bstack11ll1lll1_opy_(bstack111ll111l_opy_):
  try:
    bstack1111l1llll_opy_ = []
    bstack1111l11ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᒮ"))
    if os.path.exists(bstack1111l11ll1_opy_):
      with open(bstack1111l11ll1_opy_) as f:
        bstack1111l1llll_opy_ = json.load(f)
    bstack1111l1llll_opy_.append(bstack111ll111l_opy_)
    with open(bstack1111l11ll1_opy_, bstack11ll11l_opy_ (u"ࠪࡻࠬᒯ")) as f:
        json.dump(bstack1111l1llll_opy_, f)
  except:
    pass
def bstack1ll111ll_opy_(logger, bstack1111l11lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack11ll11l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᒰ"), bstack11ll11l_opy_ (u"ࠬ࠭ᒱ"))
    if test_name == bstack11ll11l_opy_ (u"࠭ࠧᒲ"):
        test_name = threading.current_thread().__dict__.get(bstack11ll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ᒳ"), bstack11ll11l_opy_ (u"ࠨࠩᒴ"))
    bstack1llllll111l_opy_ = bstack11ll11l_opy_ (u"ࠩ࠯ࠤࠬᒵ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111l11lll_opy_:
        bstack11l1l1111_opy_ = os.environ.get(bstack11ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒶ"), bstack11ll11l_opy_ (u"ࠫ࠵࠭ᒷ"))
        bstack1lll111lll_opy_ = {bstack11ll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᒸ"): test_name, bstack11ll11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᒹ"): bstack1llllll111l_opy_, bstack11ll11l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᒺ"): bstack11l1l1111_opy_}
        bstack11111ll111_opy_ = []
        bstack1111ll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᒻ"))
        if os.path.exists(bstack1111ll1111_opy_):
            with open(bstack1111ll1111_opy_) as f:
                bstack11111ll111_opy_ = json.load(f)
        bstack11111ll111_opy_.append(bstack1lll111lll_opy_)
        with open(bstack1111ll1111_opy_, bstack11ll11l_opy_ (u"ࠩࡺࠫᒼ")) as f:
            json.dump(bstack11111ll111_opy_, f)
    else:
        bstack1lll111lll_opy_ = {bstack11ll11l_opy_ (u"ࠪࡲࡦࡳࡥࠨᒽ"): test_name, bstack11ll11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᒾ"): bstack1llllll111l_opy_, bstack11ll11l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᒿ"): str(multiprocessing.current_process().name)}
        if bstack11ll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪᓀ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1lll111lll_opy_)
  except Exception as e:
      logger.warn(bstack11ll11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᓁ").format(e))
def bstack11l111l1l_opy_(error_message, test_name, index, logger):
  try:
    bstack1111l11l1l_opy_ = []
    bstack1lll111lll_opy_ = {bstack11ll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᓂ"): test_name, bstack11ll11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᓃ"): error_message, bstack11ll11l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᓄ"): index}
    bstack1111l1111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᓅ"))
    if os.path.exists(bstack1111l1111l_opy_):
        with open(bstack1111l1111l_opy_) as f:
            bstack1111l11l1l_opy_ = json.load(f)
    bstack1111l11l1l_opy_.append(bstack1lll111lll_opy_)
    with open(bstack1111l1111l_opy_, bstack11ll11l_opy_ (u"ࠬࡽࠧᓆ")) as f:
        json.dump(bstack1111l11l1l_opy_, f)
  except Exception as e:
    logger.warn(bstack11ll11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᓇ").format(e))
def bstack11lll1ll_opy_(bstack1l1ll1l1_opy_, name, logger):
  try:
    bstack1lll111lll_opy_ = {bstack11ll11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᓈ"): name, bstack11ll11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᓉ"): bstack1l1ll1l1_opy_, bstack11ll11l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᓊ"): str(threading.current_thread()._name)}
    return bstack1lll111lll_opy_
  except Exception as e:
    logger.warn(bstack11ll11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᓋ").format(e))
  return
def bstack1111111lll_opy_():
    return platform.system() == bstack11ll11l_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬᓌ")
def bstack111l1l11_opy_(bstack1llllll1111_opy_, config, logger):
    bstack1llllll11ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1llllll1111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11ll11l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦᓍ").format(e))
    return bstack1llllll11ll_opy_
def bstack1111l1lll1_opy_(bstack11111l1ll1_opy_, bstack1111l1l111_opy_):
    bstack1lllll1ll11_opy_ = version.parse(bstack11111l1ll1_opy_)
    bstack1111ll1ll1_opy_ = version.parse(bstack1111l1l111_opy_)
    if bstack1lllll1ll11_opy_ > bstack1111ll1ll1_opy_:
        return 1
    elif bstack1lllll1ll11_opy_ < bstack1111ll1ll1_opy_:
        return -1
    else:
        return 0
def bstack11l11lll11_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1lllllll1ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111111l1l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1l111111_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack11ll11l_opy_ (u"࠭ࡧࡦࡶࠪᓎ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1111l1l11_opy_ = caps.get(bstack11ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᓏ"))
    bstack1llllllll1l_opy_ = True
    if bstack1111l11l11_opy_(caps.get(bstack11ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧᓐ"))) or bstack1111l11l11_opy_(caps.get(bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩᓑ"))):
        bstack1llllllll1l_opy_ = False
    if bstack1l1l1lll1l_opy_({bstack11ll11l_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥᓒ"): bstack1llllllll1l_opy_}):
        bstack1111l1l11_opy_ = bstack1111l1l11_opy_ or {}
        bstack1111l1l11_opy_[bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᓓ")] = bstack1111111l1l_opy_(framework)
        bstack1111l1l11_opy_[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᓔ")] = bstack1111ll1l11_opy_()
        if getattr(options, bstack11ll11l_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧᓕ"), None):
            options.set_capability(bstack11ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᓖ"), bstack1111l1l11_opy_)
        else:
            options[bstack11ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᓗ")] = bstack1111l1l11_opy_
    else:
        if getattr(options, bstack11ll11l_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᓘ"), None):
            options.set_capability(bstack11ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᓙ"), bstack1111111l1l_opy_(framework))
            options.set_capability(bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᓚ"), bstack1111ll1l11_opy_())
        else:
            options[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᓛ")] = bstack1111111l1l_opy_(framework)
            options[bstack11ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᓜ")] = bstack1111ll1l11_opy_()
    return options
def bstack111111111l_opy_(bstack1111l1ll1l_opy_, framework):
    if bstack1111l1ll1l_opy_ and len(bstack1111l1ll1l_opy_.split(bstack11ll11l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᓝ"))) > 1:
        ws_url = bstack1111l1ll1l_opy_.split(bstack11ll11l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᓞ"))[0]
        if bstack11ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᓟ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1lllllll1l1_opy_ = json.loads(urllib.parse.unquote(bstack1111l1ll1l_opy_.split(bstack11ll11l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᓠ"))[1]))
            bstack1lllllll1l1_opy_ = bstack1lllllll1l1_opy_ or {}
            bstack1lllllll1l1_opy_[bstack11ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᓡ")] = str(framework) + str(__version__)
            bstack1lllllll1l1_opy_[bstack11ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᓢ")] = bstack1111ll1l11_opy_()
            bstack1111l1ll1l_opy_ = bstack1111l1ll1l_opy_.split(bstack11ll11l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᓣ"))[0] + bstack11ll11l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᓤ") + urllib.parse.quote(json.dumps(bstack1lllllll1l1_opy_))
    return bstack1111l1ll1l_opy_
def bstack11lll11l1_opy_():
    global bstack111ll11l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack111ll11l_opy_ = BrowserType.connect
    return bstack111ll11l_opy_
def bstack1l1ll1l11l_opy_(framework_name):
    global bstack111ll1ll_opy_
    bstack111ll1ll_opy_ = framework_name
    return framework_name
def bstack1l1lll11ll_opy_(self, *args, **kwargs):
    global bstack111ll11l_opy_
    try:
        global bstack111ll1ll_opy_
        if bstack11ll11l_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᓥ") in kwargs:
            kwargs[bstack11ll11l_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᓦ")] = bstack111111111l_opy_(
                kwargs.get(bstack11ll11l_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᓧ"), None),
                bstack111ll1ll_opy_
            )
    except Exception as e:
        logger.error(bstack11ll11l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦᓨ").format(str(e)))
    return bstack111ll11l_opy_(self, *args, **kwargs)
def bstack11111l1111_opy_(bstack1lllllll111_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack111lll11l_opy_(bstack1lllllll111_opy_, bstack11ll11l_opy_ (u"ࠧࠨᓩ"))
        if proxies and proxies.get(bstack11ll11l_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᓪ")):
            parsed_url = urlparse(proxies.get(bstack11ll11l_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᓫ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11ll11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᓬ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11ll11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᓭ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11ll11l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᓮ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11ll11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᓯ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l1l1111l1_opy_(bstack1lllllll111_opy_):
    bstack1llllll1lll_opy_ = {
        bstack111l11l111_opy_[bstack1111lll1ll_opy_]: bstack1lllllll111_opy_[bstack1111lll1ll_opy_]
        for bstack1111lll1ll_opy_ in bstack1lllllll111_opy_
        if bstack1111lll1ll_opy_ in bstack111l11l111_opy_
    }
    bstack1llllll1lll_opy_[bstack11ll11l_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᓰ")] = bstack11111l1111_opy_(bstack1lllllll111_opy_, bstack1l1111l111_opy_.get_property(bstack11ll11l_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᓱ")))
    bstack1lllll1l1ll_opy_ = [element.lower() for element in bstack111l11l1ll_opy_]
    bstack11111llll1_opy_(bstack1llllll1lll_opy_, bstack1lllll1l1ll_opy_)
    return bstack1llllll1lll_opy_
def bstack11111llll1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11ll11l_opy_ (u"ࠢࠫࠬ࠭࠮ࠧᓲ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11111llll1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11111llll1_opy_(item, keys)