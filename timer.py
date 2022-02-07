"""timer wrapper by lifesim.de"""
"""intervall is now in seconds"""

import machine

__version__ = "2.0.0"

class Timer:
  ti=None
  cb=None
  cb_userinfo = None
  callbackparamtype = "self"
  timer_id=None
  wait=0
  verbosity=0
  running = 0
  intervall = None
  periodic = 1
  
  def __init__(self, intervall_s, callback=None, callbackparamtype="no", timer_id=-1):
    """params: intervall in s, optional callback, optional type of callback params: "no","self","user" """
    self.timer_id=timer_id
    self.ti= machine.Timer(timer_id)
    if callback:
      self.cb = callback
      self.callbackparamtype = callbackparamtype
      # self.cbparamcount = callbackparamcount
      # if self.cbparamcount > 2:
        # raise Exception("max. 2 params allowed")
    self.setintervall(intervall_s)
    
  def _cb(self,*args):
    #print(args)
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
    self.running = 0
    self.ti.deinit()
    if self.verbosity:
      print("deinited.")
      
  def setintervall(self, s):
    self.intervall = s
    self.ti.init(period=int(self.intervall*1000), callback=self._cb, mode=self.periodic)
    self.running = 1
    
  def setcallback(self, cb, callbackparamtype=None, userinfo=None):
    self.cb = cb
    if self.callbackparamtype:
      self.callbackparamtype = callbackparamtype
    self.cb_userinfo = userinfo
    
  def is_alive(self):
    return self.running
    
  def stop(self):
    self.running = 0
  def cancel(self):
    self.__del__()
  def cont(self):
    self.running = 1
  def start(self):
    self.reset()
  def reset(self):
    self.setintervall(self.intervall)
    
  def info(self):
    return {"Intervall":self.intervall, "Callback":self.cb, "Callback parameter type":self.callbackparamtype, 
            "Userinfo":self.cb_userinfo, "Running":self.running, "verbosity":self.verbosity}
    
#eof
