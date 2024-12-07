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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llll111lll_opy_
bstack1l1111l111_opy_ = Config.bstack1lll1ll111_opy_()
def bstack1lll111111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll11111l1_opy_(bstack1ll1lllll1l_opy_, bstack1ll1lllll11_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1lllll1l_opy_):
        with open(bstack1ll1lllll1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll111111l_opy_(bstack1ll1lllll1l_opy_):
        pac = get_pac(url=bstack1ll1lllll1l_opy_)
    else:
        raise Exception(bstack11ll11l_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᘁ").format(bstack1ll1lllll1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11ll11l_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᘂ"), 80))
        bstack1ll1llllll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll1llllll1_opy_ = bstack11ll11l_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᘃ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1lllll11_opy_, bstack1ll1llllll1_opy_)
    return proxy_url
def bstack1ll1l1lll_opy_(config):
    return bstack11ll11l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᘄ") in config or bstack11ll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᘅ") in config
def bstack11l11l1ll_opy_(config):
    if not bstack1ll1l1lll_opy_(config):
        return
    if config.get(bstack11ll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᘆ")):
        return config.get(bstack11ll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᘇ"))
    if config.get(bstack11ll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᘈ")):
        return config.get(bstack11ll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᘉ"))
def bstack111lll11l_opy_(config, bstack1ll1lllll11_opy_):
    proxy = bstack11l11l1ll_opy_(config)
    proxies = {}
    if config.get(bstack11ll11l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᘊ")) or config.get(bstack11ll11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᘋ")):
        if proxy.endswith(bstack11ll11l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᘌ")):
            proxies = bstack1ll1l11lll_opy_(proxy, bstack1ll1lllll11_opy_)
        else:
            proxies = {
                bstack11ll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᘍ"): proxy
            }
    bstack1l1111l111_opy_.bstack1llll1lll1_opy_(bstack11ll11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᘎ"), proxies)
    return proxies
def bstack1ll1l11lll_opy_(bstack1ll1lllll1l_opy_, bstack1ll1lllll11_opy_):
    proxies = {}
    global bstack1ll1lllllll_opy_
    if bstack11ll11l_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᘏ") in globals():
        return bstack1ll1lllllll_opy_
    try:
        proxy = bstack1lll11111l1_opy_(bstack1ll1lllll1l_opy_, bstack1ll1lllll11_opy_)
        if bstack11ll11l_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᘐ") in proxy:
            proxies = {}
        elif bstack11ll11l_opy_ (u"ࠢࡉࡖࡗࡔࠧᘑ") in proxy or bstack11ll11l_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᘒ") in proxy or bstack11ll11l_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᘓ") in proxy:
            bstack1lll1111111_opy_ = proxy.split(bstack11ll11l_opy_ (u"ࠥࠤࠧᘔ"))
            if bstack11ll11l_opy_ (u"ࠦ࠿࠵࠯ࠣᘕ") in bstack11ll11l_opy_ (u"ࠧࠨᘖ").join(bstack1lll1111111_opy_[1:]):
                proxies = {
                    bstack11ll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᘗ"): bstack11ll11l_opy_ (u"ࠢࠣᘘ").join(bstack1lll1111111_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᘙ"): str(bstack1lll1111111_opy_[0]).lower() + bstack11ll11l_opy_ (u"ࠤ࠽࠳࠴ࠨᘚ") + bstack11ll11l_opy_ (u"ࠥࠦᘛ").join(bstack1lll1111111_opy_[1:])
                }
        elif bstack11ll11l_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᘜ") in proxy:
            bstack1lll1111111_opy_ = proxy.split(bstack11ll11l_opy_ (u"ࠧࠦࠢᘝ"))
            if bstack11ll11l_opy_ (u"ࠨ࠺࠰࠱ࠥᘞ") in bstack11ll11l_opy_ (u"ࠢࠣᘟ").join(bstack1lll1111111_opy_[1:]):
                proxies = {
                    bstack11ll11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᘠ"): bstack11ll11l_opy_ (u"ࠤࠥᘡ").join(bstack1lll1111111_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᘢ"): bstack11ll11l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᘣ") + bstack11ll11l_opy_ (u"ࠧࠨᘤ").join(bstack1lll1111111_opy_[1:])
                }
        else:
            proxies = {
                bstack11ll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᘥ"): proxy
            }
    except Exception as e:
        print(bstack11ll11l_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᘦ"), bstack1llll111lll_opy_.format(bstack1ll1lllll1l_opy_, str(e)))
    bstack1ll1lllllll_opy_ = proxies
    return proxies