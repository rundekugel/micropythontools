"""pins for wemos nodemcu v3"""

__version__ = "1.0.0"

import machine

pinLed = 2
pinBtn = 0

def getBtn():
  p0=machine.Pin(pinBtn,machine.Pin.IN)
  return p0.value()
  
def pwmLed():
  pw2=machine.PWM(machine.Pin(pinLed))
  return pw2
     
def ledOnOff(onOff):
  p2=machine.Pin(pinLed, machine.Pin.OUT)
  if onOff:
    p2.value(0)
  else:
    p2.value(1)
  
  
# eof
