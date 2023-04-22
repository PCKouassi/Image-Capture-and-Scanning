 import sys
import RPi.GPIO as GPIO
import time
import encodings
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from gui_v2 import Ui_MainWindow
from PyQt5.QtCore import QTimer

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#STEP(PUL) PINS
# stepper A
GPIO.setup(17,GPIO.OUT)
GPIO.output(17, False)
# stepper B
GPIO.setup(5,GPIO.OUT)
GPIO.output(5, False)

#DIR PINS
# stepper A
GPIO.setup(18,GPIO.OUT)
GPIO.output(18, False)
# stepper B
GPIO.setup(6,GPIO.OUT)
GPIO.output(6, False)

#ENABLE PINS
# stepper A
GPIO.setup(27,GPIO.OUT)
GPIO.output(27, True)
# stepper B
GPIO.setup(19,GPIO.OUT)
GPIO.output(19, True)

x_delay = 0.002  

    
class gui(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.button_B.clicked.connect(self.moveB)
        self.button_A.clicked.connect(self.moveA)
        self.timer= QTimer()

    
    def moveB(self): #as long as button B is kept pressed, this motor should keep running
        GPIO.output(19, True) #EN
        GPIO.output(6, True)  #DIR
        GPIO.output(5, False)
        time.sleep(0.00001)
        GPIO.output(5, True)
          
    def moveA(self): #by one press of button A, this motor runs continuously

        GPIO.output(27, True) #EN
        GPIO.output(18, False) #DIR
        def f():
            GPIO.output(17, False)
            time.sleep(0.002)
            GPIO.output(17, True)
        self.timer.timeout.connect(f)
        self.timer.start(2) #2msec


#    def stop(self):
#        GPIO.output(27, False)
#        self.timer.stop()

               
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    program = gui(dialog)
    dialog.show()
    sys.exit(app.exec_())
     