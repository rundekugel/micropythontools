#!/usr/bin/env python3
#fsk demod

import machine
import time
import timer

class globs:
  verbosity=3

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
  short, long = 0,0
  shortD,longD=0,0
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
    self.d=d
    if d > self.timeout: 
      self._lastChange = t
      if self.cbTimeout: self.cbTimeout()
      self.output = '-'
      return
    self.middle += d
    self.samples += 1
    m = self.middle / self.samples
    if d >m :
      self.long += 1; self.longD += d
      if 0==self.output and self.cbHi: self.cbHi()
      self.output = 1
    if d <m :
      self.short += 1;
      self.shortD += d
      if self.output and  self.cbLo: self.cbLo()
      self.output = 0
     
    self._lastChange = t
  def proc(self):
    d = time.time() - self._lastChange
    self.d = d
    if d > self.timeout:
      self.output = '-'
      return

  def __str__(self):
    r = {} ; wl =("output","d","middle","short","long","samples")
    d=self.__dict__
    for i in d:
      if i in wl: r[i]=d[i]
    return str(r)

# Testing:

def cb1(p=None):
  if globs.verbosity >1: print('.')
def cbL():
  if globs.verbosity >3: print("L")
def cbH():
  if globs.verbosity >3: print("H")
def cbT():
  if globs.verbosity > 1: print(";")

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
    fd.proc()
    print(fd.output, end="")
    time.sleep(1)  # todo: sync with fd
    if fd.output =='-':
      if b>0: b=0; print()
      continue
    if fd.output:
      by += 2**b
    b+=1
    if b>7:
      d.append(hex(by))
      b,by=0,0
      print(d,fd)
  print("done.")
  del(fd)
