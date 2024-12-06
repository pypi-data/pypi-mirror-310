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
class RobotHandler():
    def __init__(self, args, logger, bstack11l1111ll1_opy_, bstack11l1111l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1111ll1_opy_ = bstack11l1111ll1_opy_
        self.bstack11l1111l11_opy_ = bstack11l1111l11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l1ll1l11_opy_(bstack111llllll1_opy_):
        bstack111lllll11_opy_ = []
        if bstack111llllll1_opy_:
            tokens = str(os.path.basename(bstack111llllll1_opy_)).split(bstack1l1l1l_opy_ (u"ࠦࡤࠨཀྵ"))
            camelcase_name = bstack1l1l1l_opy_ (u"ࠧࠦࠢཪ").join(t.title() for t in tokens)
            suite_name, bstack111lllllll_opy_ = os.path.splitext(camelcase_name)
            bstack111lllll11_opy_.append(suite_name)
        return bstack111lllll11_opy_
    @staticmethod
    def bstack111lllll1l_opy_(typename):
        if bstack1l1l1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤཫ") in typename:
            return bstack1l1l1l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣཬ")
        return bstack1l1l1l_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ཭")