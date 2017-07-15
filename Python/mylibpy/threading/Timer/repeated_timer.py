# -*- utf-8 -*-
import threading
from threading import Timer

class RepeatedTimer(Timer):
  def __init__(self, interval, function, args=[], kwargs={}):
    """コンストラクタ"""
    Timer.__init__(self, interval, self.run, args, kwargs)
    self.thread = None
    self.function = function

  def start(self):
    """タイマー処理開始"""
    self.thread = Timer(self.interval, self.start)
    self.thread.start()
    self.function(*self.args, **self.kwargs)

  def cancel(self):

    """中止処理"""
    if self.thread is not None:
      self.thread.cancel()
      self.thread.join()
      del self.thread

if __name__ == '__main__':
    pass

