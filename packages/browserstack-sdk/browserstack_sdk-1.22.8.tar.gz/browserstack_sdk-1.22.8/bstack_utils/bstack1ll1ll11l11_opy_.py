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
import threading
bstack1ll1ll1111l_opy_ = 1000
bstack1ll1ll1l11l_opy_ = 5
bstack1ll1ll11lll_opy_ = 30
bstack1ll1ll1l111_opy_ = 2
class bstack1ll1ll11l1l_opy_:
    def __init__(self, handler, bstack1ll1ll1ll11_opy_=bstack1ll1ll1111l_opy_, bstack1ll1ll1l1ll_opy_=bstack1ll1ll1l11l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll1ll1ll11_opy_ = bstack1ll1ll1ll11_opy_
        self.bstack1ll1ll1l1ll_opy_ = bstack1ll1ll1l1ll_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1ll1ll111l1_opy_()
    def bstack1ll1ll111l1_opy_(self):
        self.timer = threading.Timer(self.bstack1ll1ll1l1ll_opy_, self.bstack1ll1ll111ll_opy_)
        self.timer.start()
    def bstack1ll1ll1l1l1_opy_(self):
        self.timer.cancel()
    def bstack1ll1ll11ll1_opy_(self):
        self.bstack1ll1ll1l1l1_opy_()
        self.bstack1ll1ll111l1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll1ll1ll11_opy_:
                t = threading.Thread(target=self.bstack1ll1ll111ll_opy_)
                t.start()
                self.bstack1ll1ll11ll1_opy_()
    def bstack1ll1ll111ll_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1ll1ll1ll11_opy_]
        del self.queue[:self.bstack1ll1ll1ll11_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1ll1ll1l1l1_opy_()
        while len(self.queue) > 0:
            self.bstack1ll1ll111ll_opy_()