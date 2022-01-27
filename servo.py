"""pwm for servo. by lifesim.de"""
import machine

__version__ = "0.1.0"
__author__ = "lifesim.de"

servopin=2
maxDuty = 1023
minpwm = 25
maxpwm = 133
frequencyHz = 50


class ServoControl:
  pin = None
  pwmout = None
  gpio = None
  minpwm = 27
  maxpwm = 133
  maxdeg=180
  lastpos=0
  
  def __init__(self,pin=2):
    """
    init servo object
    pin = servo control output pin, default=2
    """
    self.pin=pin
    self.pwmout=machine.PWM(machine.Pin(self.pin))
    self.pwmout.freq(frequencyHz)
    self.pwmout.duty(0)
    self.gpio = machine.Pin(self.pin, machine.Pin.OUT)
    self.gpio.value(0)
    self._calcpwmperdeg()
    
  def _calcpwmperdeg(self, maxdeg=None):
    d = self.maxpwm - self.minpwm
    if maxdeg:
      self.maxdeg=maxdeg
    self.pwmperdeg = d/self.maxdeg
  
  def setpos(self, deg, stayon=True):
    """set servo 0..180 deg"""
    self.pwmout.duty(minpwm + int(deg*self.pwmperdeg))
    self.lastpos = deg
    
  def off(self):
    """set servo power off"""
    self.gpio.value(0)
    self.pwmout.duty(0)
    
  def setfreq(self,freq):
    self.pwmout.freq(freq)
    
  def getduty(self):
    return self.pwmout.duty()
  def getFreq(self):
    return self.pwmout.freq()
    
#eof
