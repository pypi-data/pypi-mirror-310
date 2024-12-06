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
from uuid import uuid4
from bstack_utils.helper import bstack1lll1ll1l_opy_, bstack1111l111l1_opy_
from bstack_utils.bstack1l1l111ll_opy_ import bstack1ll1llll111_opy_
class bstack11l1l11l11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11ll111l11_opy_=None, framework=None, tags=[], scope=[], bstack1ll1l11l1l1_opy_=None, bstack1ll1l11ll11_opy_=True, bstack1ll1l111lll_opy_=None, bstack11lll111ll_opy_=None, result=None, duration=None, bstack11l1ll1lll_opy_=None, meta={}):
        self.bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1l11ll11_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11ll111l11_opy_ = bstack11ll111l11_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1l11l1l1_opy_ = bstack1ll1l11l1l1_opy_
        self.bstack1ll1l111lll_opy_ = bstack1ll1l111lll_opy_
        self.bstack11lll111ll_opy_ = bstack11lll111ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack11l1l1111l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11ll1l1ll1_opy_(self, meta):
        self.meta = meta
    def bstack11ll1l1l1l_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll1l111ll1_opy_(self):
        bstack1ll1l1l1l11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᚐ"): bstack1ll1l1l1l11_opy_,
            bstack1l1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᚑ"): bstack1ll1l1l1l11_opy_,
            bstack1l1l1l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᚒ"): bstack1ll1l1l1l11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1l1l_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧᚓ") + key)
            setattr(self, key, val)
    def bstack1ll1l11ll1l_opy_(self):
        return {
            bstack1l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᚔ"): self.name,
            bstack1l1l1l_opy_ (u"࠭ࡢࡰࡦࡼࠫᚕ"): {
                bstack1l1l1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᚖ"): bstack1l1l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᚗ"),
                bstack1l1l1l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᚘ"): self.code
            },
            bstack1l1l1l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᚙ"): self.scope,
            bstack1l1l1l_opy_ (u"ࠫࡹࡧࡧࡴࠩᚚ"): self.tags,
            bstack1l1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ᚛"): self.framework,
            bstack1l1l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᚜"): self.bstack11ll111l11_opy_
        }
    def bstack1ll1l1l11ll_opy_(self):
        return {
         bstack1l1l1l_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ᚝"): self.meta
        }
    def bstack1ll1l1l1111_opy_(self):
        return {
            bstack1l1l1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ᚞"): {
                bstack1l1l1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭᚟"): self.bstack1ll1l11l1l1_opy_
            }
        }
    def bstack1ll1l11l111_opy_(self, bstack1ll1l1l1l1l_opy_, details):
        step = next(filter(lambda st: st[bstack1l1l1l_opy_ (u"ࠪ࡭ࡩ࠭ᚠ")] == bstack1ll1l1l1l1l_opy_, self.meta[bstack1l1l1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚡ")]), None)
        step.update(details)
    def bstack1lllll1l1l_opy_(self, bstack1ll1l1l1l1l_opy_):
        step = next(filter(lambda st: st[bstack1l1l1l_opy_ (u"ࠬ࡯ࡤࠨᚢ")] == bstack1ll1l1l1l1l_opy_, self.meta[bstack1l1l1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᚣ")]), None)
        step.update({
            bstack1l1l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚤ"): bstack1lll1ll1l_opy_()
        })
    def bstack11ll111l1l_opy_(self, bstack1ll1l1l1l1l_opy_, result, duration=None):
        bstack1ll1l111lll_opy_ = bstack1lll1ll1l_opy_()
        if bstack1ll1l1l1l1l_opy_ is not None and self.meta.get(bstack1l1l1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᚥ")):
            step = next(filter(lambda st: st[bstack1l1l1l_opy_ (u"ࠩ࡬ࡨࠬᚦ")] == bstack1ll1l1l1l1l_opy_, self.meta[bstack1l1l1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᚧ")]), None)
            step.update({
                bstack1l1l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᚨ"): bstack1ll1l111lll_opy_,
                bstack1l1l1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᚩ"): duration if duration else bstack1111l111l1_opy_(step[bstack1l1l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᚪ")], bstack1ll1l111lll_opy_),
                bstack1l1l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᚫ"): result.result,
                bstack1l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᚬ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1l11llll_opy_):
        if self.meta.get(bstack1l1l1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᚭ")):
            self.meta[bstack1l1l1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᚮ")].append(bstack1ll1l11llll_opy_)
        else:
            self.meta[bstack1l1l1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚯ")] = [ bstack1ll1l11llll_opy_ ]
    def bstack1ll1l1l1lll_opy_(self):
        return {
            bstack1l1l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᚰ"): self.bstack11l1l1111l_opy_(),
            **self.bstack1ll1l11ll1l_opy_(),
            **self.bstack1ll1l111ll1_opy_(),
            **self.bstack1ll1l1l11ll_opy_()
        }
    def bstack1ll1l1l11l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᚱ"): self.bstack1ll1l111lll_opy_,
            bstack1l1l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᚲ"): self.duration,
            bstack1l1l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᚳ"): self.result.result
        }
        if data[bstack1l1l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᚴ")] == bstack1l1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᚵ"):
            data[bstack1l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᚶ")] = self.result.bstack111lllll1l_opy_()
            data[bstack1l1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᚷ")] = [{bstack1l1l1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᚸ"): self.result.bstack111111ll11_opy_()}]
        return data
    def bstack1ll1l11lll1_opy_(self):
        return {
            bstack1l1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᚹ"): self.bstack11l1l1111l_opy_(),
            **self.bstack1ll1l11ll1l_opy_(),
            **self.bstack1ll1l111ll1_opy_(),
            **self.bstack1ll1l1l11l1_opy_(),
            **self.bstack1ll1l1l11ll_opy_()
        }
    def bstack11l11ll11l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1l1l_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩᚺ") in event:
            return self.bstack1ll1l1l1lll_opy_()
        elif bstack1l1l1l_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᚻ") in event:
            return self.bstack1ll1l11lll1_opy_()
    def bstack11l1l11lll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1l111lll_opy_ = time if time else bstack1lll1ll1l_opy_()
        self.duration = duration if duration else bstack1111l111l1_opy_(self.bstack11ll111l11_opy_, self.bstack1ll1l111lll_opy_)
        if result:
            self.result = result
class bstack11ll11lll1_opy_(bstack11l1l11l11_opy_):
    def __init__(self, hooks=[], bstack11ll1ll11l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11ll1ll11l_opy_ = bstack11ll1ll11l_opy_
        super().__init__(*args, **kwargs, bstack11lll111ll_opy_=bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࠨᚼ"))
    @classmethod
    def bstack1ll1l1l1ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1l1l_opy_ (u"ࠫ࡮ࡪࠧᚽ"): id(step),
                bstack1l1l1l_opy_ (u"ࠬࡺࡥࡹࡶࠪᚾ"): step.name,
                bstack1l1l1l_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᚿ"): step.keyword,
            })
        return bstack11ll11lll1_opy_(
            **kwargs,
            meta={
                bstack1l1l1l_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᛀ"): {
                    bstack1l1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᛁ"): feature.name,
                    bstack1l1l1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᛂ"): feature.filename,
                    bstack1l1l1l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᛃ"): feature.description
                },
                bstack1l1l1l_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ᛄ"): {
                    bstack1l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᛅ"): scenario.name
                },
                bstack1l1l1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᛆ"): steps,
                bstack1l1l1l_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᛇ"): bstack1ll1llll111_opy_(test)
            }
        )
    def bstack1ll1l1l111l_opy_(self):
        return {
            bstack1l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᛈ"): self.hooks
        }
    def bstack1ll1l11l1ll_opy_(self):
        if self.bstack11ll1ll11l_opy_:
            return {
                bstack1l1l1l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᛉ"): self.bstack11ll1ll11l_opy_
            }
        return {}
    def bstack1ll1l11lll1_opy_(self):
        return {
            **super().bstack1ll1l11lll1_opy_(),
            **self.bstack1ll1l1l111l_opy_()
        }
    def bstack1ll1l1l1lll_opy_(self):
        return {
            **super().bstack1ll1l1l1lll_opy_(),
            **self.bstack1ll1l11l1ll_opy_()
        }
    def bstack11l1l11lll_opy_(self):
        return bstack1l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᛊ")
class bstack11ll1111ll_opy_(bstack11l1l11l11_opy_):
    def __init__(self, hook_type, *args,bstack11ll1ll11l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1l11l11l_opy_ = None
        self.bstack11ll1ll11l_opy_ = bstack11ll1ll11l_opy_
        super().__init__(*args, **kwargs, bstack11lll111ll_opy_=bstack1l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᛋ"))
    def bstack11l11lll11_opy_(self):
        return self.hook_type
    def bstack1ll1l1ll111_opy_(self):
        return {
            bstack1l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᛌ"): self.hook_type
        }
    def bstack1ll1l11lll1_opy_(self):
        return {
            **super().bstack1ll1l11lll1_opy_(),
            **self.bstack1ll1l1ll111_opy_()
        }
    def bstack1ll1l1l1lll_opy_(self):
        return {
            **super().bstack1ll1l1l1lll_opy_(),
            bstack1l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫᛍ"): self.bstack1ll1l11l11l_opy_,
            **self.bstack1ll1l1ll111_opy_()
        }
    def bstack11l1l11lll_opy_(self):
        return bstack1l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᛎ")
    def bstack11ll111ll1_opy_(self, bstack1ll1l11l11l_opy_):
        self.bstack1ll1l11l11l_opy_ = bstack1ll1l11l11l_opy_