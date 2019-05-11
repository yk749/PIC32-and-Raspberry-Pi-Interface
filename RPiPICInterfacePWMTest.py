import sys
import PIC32Interface
import time

PIC32Interface.SetPWMPeriod(22, 3)
#time.sleep(0.1)
PIC32Interface.EnablePWM1(0,1)
PIC32Interface.EnablePWM2(0,1)

PIC32Interface.SetDACA(2000)
PIC32Interface.SetDACB(2000)
