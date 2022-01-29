"""timer wrapper by lifesim.de"""

import machine

__version__ = "1.1.1"

class Timer:
  ti=None
  cb=None
  cb_userinfo = None
  callbackparamtype = "self"
  timer_id=None
  wait=0
  verbosity=1
  running = 0
  intervall = None
  
  def __init__(self, intervall_ms, callback=None, callbackparamtype="self", timer_id=-1):
    """params: intervall in ms, optional callback, optional type of callback params: "no","self","user" """
    self.timer_id=timer_id
    self.ti= machine.Timer(timer_id)
    if callback:
      self.cb = callback
      self.cbparamcount = callbackparamcount
      if self.cbparamcount > 2:
        raise Exception("max. 2 params allowed")
    self.setintervall(intervall_ms)
    
  def _cb(self,t=None):
    if self.cb and self.running:
      if self.callbackparamtype == "user":
        self.cb(self.cb_userinfo)
      elif self.callbackparamtype == "self":
        self.cb(self)
      elif self.callbackparamtype == "no":
        self.cb()
      else:
        if self.verbosity:
          print("unknown callbackparamtype:" +str(self.callbackparamtype))
      
  def __del__(self):
    self.ti.deinit()
    if self.verbosity:
      print("deinited.")
      
  def setintervall(self, ms):
    self.intervall = ms
    self.ti.init(period=ms, callback=self._cb)
    self.running = 1
    
  def setcallback(self, cb, callbackparamtype=None, userinfo=None):
    self.cb = cb
    if self.callbackparamtype:
      self.callbackparamtype = callbackparamtype
    self.cb_userinfo = userinfo
    
  def stop(self):
    self.running = 0
  def cont(self):
    self.running = 1
  def reset(self):
    self.setintervall(self.intervall)
    
  def info(self):
    return {"Intervall":self.intervall, "Callback":self.cb, "Callback parameter type":self.callbackparamtype, 
            "Userinfo":self.cb_userinfo, "Running":self.running, "verbosity":self.verbosity}
    
#eof
