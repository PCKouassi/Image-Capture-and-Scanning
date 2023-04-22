import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time

def set_pinouts():
    #Define GPIO pins
    GPIO.setmode(GPIO.BOARD)

    #Set GPIO pins for X Y Motors
    pinx = [26,19,13,6]
    piny = [1,7,8,25]

    #x
    for pin in pinx:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    #Y
    for pin in piny:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    return pinx, piny

def set_step_size():
    #Define step size
    halfstep_seq = [
      [1,0,0,0],
      [1,1,0,0],
      [0,1,0,0],
      [0,1,1,0],
      [0,0,1,0],
      [0,0,1,1],
      [0,0,0,1],
      [1,0,0,1]
    ]
    #Define number of steps to cross field of view
    numStepsx = 62
    numStepsy = 64

    return numStepsx, numStepsy, halfstep_seq

def translate_axis(axis): 
    pinx, piny = set_pinouts()
    numStepsx, numStepsy, halfstep_seq = set_step_size()
    #Translate stage through grid pattern
    if axis == 0:
        for i in range(numStepsx*512):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(pinx[pin],halfstep_seq[halfstep][pin])
                time.sleep(0.001)
    if axis == 1:
        for j in range(numStepsy*512):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(piny[pin],halfstep_seq[halfstep][pin])
                time.sleep(0.001)
            
