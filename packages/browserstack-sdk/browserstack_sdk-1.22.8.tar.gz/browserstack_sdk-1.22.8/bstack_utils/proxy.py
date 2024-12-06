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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llll11l11l_opy_
bstack1l1111lll1_opy_ = Config.bstack111ll1l11_opy_()
def bstack1lll111111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1ll1llll1ll_opy_(bstack1ll1lllll11_opy_, bstack1ll1lllll1l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1lllll11_opy_):
        with open(bstack1ll1lllll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll111111l_opy_(bstack1ll1lllll11_opy_):
        pac = get_pac(url=bstack1ll1lllll11_opy_)
    else:
        raise Exception(bstack1l1l1l_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᘁ").format(bstack1ll1lllll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1l1l_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᘂ"), 80))
        bstack1lll1111111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll1111111_opy_ = bstack1l1l1l_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᘃ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1lllll1l_opy_, bstack1lll1111111_opy_)
    return proxy_url
def bstack11l111l1_opy_(config):
    return bstack1l1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᘄ") in config or bstack1l1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᘅ") in config
def bstack1111l111_opy_(config):
    if not bstack11l111l1_opy_(config):
        return
    if config.get(bstack1l1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᘆ")):
        return config.get(bstack1l1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᘇ"))
    if config.get(bstack1l1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᘈ")):
        return config.get(bstack1l1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᘉ"))
def bstack11ll1l111_opy_(config, bstack1ll1lllll1l_opy_):
    proxy = bstack1111l111_opy_(config)
    proxies = {}
    if config.get(bstack1l1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᘊ")) or config.get(bstack1l1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᘋ")):
        if proxy.endswith(bstack1l1l1l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᘌ")):
            proxies = bstack1ll1lll1ll_opy_(proxy, bstack1ll1lllll1l_opy_)
        else:
            proxies = {
                bstack1l1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᘍ"): proxy
            }
    bstack1l1111lll1_opy_.bstack1l1111l1l_opy_(bstack1l1l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᘎ"), proxies)
    return proxies
def bstack1ll1lll1ll_opy_(bstack1ll1lllll11_opy_, bstack1ll1lllll1l_opy_):
    proxies = {}
    global bstack1ll1lllllll_opy_
    if bstack1l1l1l_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᘏ") in globals():
        return bstack1ll1lllllll_opy_
    try:
        proxy = bstack1ll1llll1ll_opy_(bstack1ll1lllll11_opy_, bstack1ll1lllll1l_opy_)
        if bstack1l1l1l_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᘐ") in proxy:
            proxies = {}
        elif bstack1l1l1l_opy_ (u"ࠢࡉࡖࡗࡔࠧᘑ") in proxy or bstack1l1l1l_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᘒ") in proxy or bstack1l1l1l_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᘓ") in proxy:
            bstack1ll1llllll1_opy_ = proxy.split(bstack1l1l1l_opy_ (u"ࠥࠤࠧᘔ"))
            if bstack1l1l1l_opy_ (u"ࠦ࠿࠵࠯ࠣᘕ") in bstack1l1l1l_opy_ (u"ࠧࠨᘖ").join(bstack1ll1llllll1_opy_[1:]):
                proxies = {
                    bstack1l1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᘗ"): bstack1l1l1l_opy_ (u"ࠢࠣᘘ").join(bstack1ll1llllll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᘙ"): str(bstack1ll1llllll1_opy_[0]).lower() + bstack1l1l1l_opy_ (u"ࠤ࠽࠳࠴ࠨᘚ") + bstack1l1l1l_opy_ (u"ࠥࠦᘛ").join(bstack1ll1llllll1_opy_[1:])
                }
        elif bstack1l1l1l_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᘜ") in proxy:
            bstack1ll1llllll1_opy_ = proxy.split(bstack1l1l1l_opy_ (u"ࠧࠦࠢᘝ"))
            if bstack1l1l1l_opy_ (u"ࠨ࠺࠰࠱ࠥᘞ") in bstack1l1l1l_opy_ (u"ࠢࠣᘟ").join(bstack1ll1llllll1_opy_[1:]):
                proxies = {
                    bstack1l1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᘠ"): bstack1l1l1l_opy_ (u"ࠤࠥᘡ").join(bstack1ll1llllll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᘢ"): bstack1l1l1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᘣ") + bstack1l1l1l_opy_ (u"ࠧࠨᘤ").join(bstack1ll1llllll1_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᘥ"): proxy
            }
    except Exception as e:
        print(bstack1l1l1l_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᘦ"), bstack1llll11l11l_opy_.format(bstack1ll1lllll11_opy_, str(e)))
    bstack1ll1lllllll_opy_ = proxies
    return proxies