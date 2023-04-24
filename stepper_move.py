import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


control_pins_x = [22,27,17,4]
control_pins_y = [6,13,19,26]
control_pins_z = [21,20,16,12]

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

def move_a_motor(motor):
    if abs(motor) == 1:
       control_pins = control_pins_x
       if motor < 0:
          halfstep_seq = list(reversed(halfstep_seq))

    if abs(motor) == 2:
       control_pins = control_pins_y
       if motor < 0:
          halfstep_seq = list(reversed(halfstep_seq))

    if abs(motor) == 3:
       control_pins = control_pins_z
       if motor < 0:
          halfstep_seq = list(reversed(halfstep_seq))
    

    for pin in control_pins:
       GPIO.setup(pin, GPIO.OUT)
       GPIO.output(pin, 0)
       print(pin)
    
    on_off = True
    
    while on_off:
       for halfstep in range(8):
          for pin in range(4):
             GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
    on_off = False

time.sleep(0.001)
GPIO.cleanup()
