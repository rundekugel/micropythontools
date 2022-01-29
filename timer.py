"""timer wrapper by lifesim.de"""

import machine

__version__ = "1.0.1"

class Timer:
  ti=None
  cb=None
  tid=None
  wait=0
  verbosity=1
  running = 0
  intervall = None
  
  def __init__(self, intervall_ms, callback=None, tid=-1):
    self.tid=tid
    self.ti= machine.Timer(tid)
    if callback:
      self.cb = callback
    self.setintervall(intervall_ms)
    
  def _cb(self,t=None):
    if self.cb and self.running:
      self.cb(t)
      
  def __del__(self):
    self.ti.deinit()
    if self.verbosity:
      print("deinited.")
      
  def setintervall(self, ms):
    self.intervall = ms
    self.ti.init(period=ms, callback=self._cb)
    self.running = 1
    
  def setcallback(self, cb):
    self._cb = cb
    
  def stop(self):
    self.running = 0
  def cont(self):
    self.running = 1
  def reset(self):
    self.setintervall(self.intervall)
    
#eof
