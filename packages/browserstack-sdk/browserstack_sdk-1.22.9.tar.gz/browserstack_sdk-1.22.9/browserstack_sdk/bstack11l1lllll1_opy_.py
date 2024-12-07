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
class RobotHandler():
    def __init__(self, args, logger, bstack11l11l111l_opy_, bstack11l111ll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l11l111l_opy_ = bstack11l11l111l_opy_
        self.bstack11l111ll1l_opy_ = bstack11l111ll1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l1l1l111_opy_(bstack111lllll1l_opy_):
        bstack111llllll1_opy_ = []
        if bstack111lllll1l_opy_:
            tokens = str(os.path.basename(bstack111lllll1l_opy_)).split(bstack11ll11l_opy_ (u"ࠦࡤࠨཀྵ"))
            camelcase_name = bstack11ll11l_opy_ (u"ࠧࠦࠢཪ").join(t.title() for t in tokens)
            suite_name, bstack11l1111111_opy_ = os.path.splitext(camelcase_name)
            bstack111llllll1_opy_.append(suite_name)
        return bstack111llllll1_opy_
    @staticmethod
    def bstack111lllllll_opy_(typename):
        if bstack11ll11l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤཫ") in typename:
            return bstack11ll11l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣཬ")
        return bstack11ll11l_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ཭")