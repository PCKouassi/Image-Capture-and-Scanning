import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

inp = input("Choose Stepper: ")
control_pins_x = [22,27,17,4]
control_pins_y = [6,13,19,26]
control_pins_z = [21,20,16,12]

if inp == 'x':
  control_pins = control_pins_x
elif inp == 'y':
  control_pins = control_pins_y
elif inp == 'z':
  control_pins = control_pins_z

else:
  control_pins = control_pins_z

for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
  print(pin)

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

for i in range(512*3):
  for halfstep in range(8):
    for pin in range(4):
      GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
    time.sleep(0.001)
GPIO.cleanup()
