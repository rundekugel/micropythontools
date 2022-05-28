#!/usr/bin/env python3
#fsk demod

import machine
import time


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
  timeout = .5
  cbHi = None
  cbLo = None
  lastLevel = 0
  
  def __init__(self, pinnum):
    self.pinnum = pinnum
    t = time.time()
    self._lastFall, self._lastRise = t, t
    self.__lastChange = t
    # set irqs
    self.pin = machine.Pin(self.pinNum, machine.Pin.IN, machine.Pin.PULL_UP)
    self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.onChange)
    self.pin.irq(trigger=Pin.IRQ_RISING, handler=self.onChange)

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
  
  def onChange(self):
    t = time.time()
    d = t-self._lastChange()
    if d > self.timeout: 
      self.__lastChange = t
      return
    self.middle += d
    self.samples += 1
    m = self.middle / self.samples
    if d >m : 
      if 0==self.output and self.cbHi: cbHi()
      self.output = 1
    if d <m : 
       if self.output and  self.cbLo: cbLo()
       self.output = 0
     
    self.__lastChange = t
    
    

if __name__ == "__main__":
  # test
  fd = fskdecoder(pin=0)
    


