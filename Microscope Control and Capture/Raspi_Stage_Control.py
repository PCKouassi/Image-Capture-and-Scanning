import RPi.GPIO as GPIO
from RpiMotorlib import RpiMotorlib
import time

def set_pinouts():
    #Define GPIO pins
    GPIO.setmode(GPIO.BOARD)

    #Set GPIO pins for X Y Motors
    pinx = [2,3,14,15]
    piny = [17,27,18,23]

    #x
    for pinx in control_pins:
        GPIO.setup(pinx, GPIO.OUT)
        GPIO.output(pinx, 0)
    #Y
    for piny in control_pins:
        GPIO.setup(piny, GPIO.OUT)
        GPIO.output(piny, 0)

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
    numStepsx = 2
    numStepsy = 4

def translate_axis(axis): 
    set_pinouts()
    set_step_size()
    #Translate stage through grid pattern
    if axis == 0:
        for i in range(numStepsx*512):
            for halfstep in range(8):
                for pin in range(4):
                    GPIIO.output(pinx[pin],halfstep_seq[halfstep][pin])
                time.sleep(0.001)
    if axis == 1:
        for j in range(numStepsy*512):
            for halfstep in range(8):
                for pin in range(4):
                    GPIIO.output(pinx[pin],halfstep_seq[halfstep][pin])
                time.sleep(0.001)
            