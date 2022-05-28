#!/usr/bin/env python3
#fsk demod

import machine
import time
import timer

class fskdecoder:
  f1 = None
  f2 = None
  pin = None
  pinNum = None
  _lastRise = None
  _lastFall = None
  _lastChange = None
  samples = 0
  middle = 0
  short = None
  long = None
  output = 0
  timeout = 1.5
  cbHi = None
  cbLo = None
  cbTimeout = None
  lastLevel = 0
  
  def __init__(self, pinNum):
    self.pinNum = pinNum
    t = time.time()
    self._lastFall, self._lastRise = t, t
    self._lastChange = t
    # set irqs
    self.pin = machine.Pin(self.pinNum, machine.Pin.IN, machine.Pin.PULL_UP)
    self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.onChange)
    self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=self.onChange)

  def onRise(self):
    t = time.time()
    d = t-self._lastFall()
    self.middle += d
    self.samples += 1
    
  def onFall(self):
    t = time.time()
    d = t-self._lastRise()
    self.middle += d
    self.samples += 1
  
  def onChange(self, a=0):
    t = time.time()
    d = t-self._lastChange
    if d > self.timeout: 
      self._lastChange = t
      if self.cbTimeout: self.cbTimeout()
      return
    self.middle += d
    self.samples += 1
    m = self.middle / self.samples
    if d >m : 
      if 0==self.output and self.cbHi: self.cbHi()
      self.output = 1
    if d <m : 
       if self.output and  self.cbLo: self.cbLo()
       self.output = 0
     
    self._lastChange = t
    
    

def cb1(p=None):
  print('.')
def cbL():
  print("L")
def cbH():
  print("H")
def cbT():
  print(";")

if __name__ == "__main__":
  # test
  fd = fskdecoder(0)
  fd.cbLo, fd.cbHi = cbL, cbH
  t = timer.Timer(.01, cb1)
  tend = time.time()+130
  t.start()
  d=[]
  b=0
  by=0
  while tend > time.time():
    print(fd.output)
    time.sleep(1)
    if fd.output:
      by += 2**b
    b+=1
    if b==8:
      d.append(hex(by))
      b,by=0,0
      print(d)
  print("done.")
  del(fd)
