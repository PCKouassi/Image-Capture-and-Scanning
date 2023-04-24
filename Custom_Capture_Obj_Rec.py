import os
import sys
import time
#import stepper_move


import cv2
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)


class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.trained_file = None
        self.status = True
        self.cap = True
        self.scan_number = 0 


    def set_file(self, fname):
        # The data comes with the 'opencv-python' module
        self.trained_file = os.path.join(cv2.data.haarcascades, fname)

    def capture(self):
        dirname = "/Users/peter/Desktop/captures"
        print("Taking a picture")
        ft, image = self.cap.read()
        image_name = "TB_SSM_Scan_{}.jpg".format(self.scan_number)
        cv2.imwrite(os.path.join(dirname, image_name), image)
        print("Saved image to dirname")
        self.scan_number += 1

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.status:
            cascade = cv2.CascadeClassifier(self.trained_file)
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Reading frame in gray scale to process the pattern
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            detections = cascade.detectMultiScale(gray_frame, scaleFactor=1.1,
                                                  minNeighbors=5, minSize=(30, 30))

            # Drawing green rectangle around the pattern
            for (x, y, w, h) in detections:
                pos_ori = (x, y)
                pos_end = (x + w, y + h)
                color = (0, 255, 0)
                cv2.rectangle(frame, pos_ori, pos_end, color, 2)

            # Reading the image in RGB to display it
            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Creating and scaling QImage
            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
            scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)

            # Emit signal
            self.updateFrame.emit(scaled_img)
        sys.exit(-1)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Title and dimensions
        self.setWindowTitle("POCAS Mobile Microscope")
        self.setGeometry(0, 0, 800, 480)

        # Main menu bar
        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("File")
        exit = QAction("Exit", self, triggered=QApplication.quit)
        self.menu_file.addAction(exit)

        self.menu_about = self.menu.addMenu("&About")
        about = QAction("About Qt", self, shortcut=QKeySequence(QKeySequence.HelpContents),
                        triggered=QApplication.aboutQt)
        self.menu_about.addAction(about)

        # Create a label for the display camera
        self.label = QLabel(self)
        self.label.setFixedSize(640, 480)

        # Thread in charge of updating the image
        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        # Model group
        self.group_model = QGroupBox("Trained model")
        self.group_model.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        model_layout = QHBoxLayout()

        self.combobox = QComboBox()
        for xml_file in os.listdir(cv2.data.haarcascades):
            if xml_file.endswith(".xml"):
                self.combobox.addItem(xml_file)

        model_layout.addWidget(QLabel("File:"), 10)
        model_layout.addWidget(self.combobox, 90)
        self.group_model.setLayout(model_layout)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.button1 = QPushButton("Start")
        self.button2 = QPushButton("Stop/Close")
        self.button3 = QPushButton("Capture")
        self.button1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.button3)
        buttons_layout.addWidget(self.button2)
        buttons_layout.addWidget(self.button1)

        self.button4 = QPushButton("Right")
        self.button5 = QPushButton("Left")
        self.button6 = QPushButton("Up")
        self.button7 = QPushButton("Down")
        self.button8 = QPushButton("+ Z")
        self.button9 = QPushButton("- Z")
        self.button4.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button5.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button6.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button7.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button8.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button9.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.button4)
        buttons_layout.addWidget(self.button5)
        buttons_layout.addWidget(self.button6)
        buttons_layout.addWidget(self.button7)
        buttons_layout.addWidget(self.button8)
        buttons_layout.addWidget(self.button9)


        right_layout = QHBoxLayout()
        right_layout.addWidget(self.group_model, 1)
        right_layout.addLayout(buttons_layout, 1)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(right_layout)

        # Central widget
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connections
        self.button1.clicked.connect(self.start)
        self.button2.clicked.connect(self.kill_thread)
        self.button3.clicked.connect(self.capture_button)
        self.button4.clicked.connect(self.stepper_right)
        self.button5.clicked.connect(self.stepper_left)
        self.button6.clicked.connect(self.stepper_up)
        self.button7.clicked.connect(self.stepper_down)
        self.button8.clicked.connect(self.stepper_zplus)
        self.button9.clicked.connect(self.stepper_zminus)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
        self.button5.setEnabled(False)
        self.button6.setEnabled(False)
        self.button7.setEnabled(False)
        self.button8.setEnabled(False)
        self.button9.setEnabled(False)
        self.combobox.currentTextChanged.connect(self.set_model)

    @Slot()
    def set_model(self, text):
        self.th.set_file(text)

    @Slot()
    def kill_thread(self):
        print("Finishing...")
        self.button3.setEnabled(False)
        self.button2.setEnabled(False)
        self.button1.setEnabled(True)
        self.th.cap.release()
        cv2.destroyAllWindows()
        self.status = False
        self.th.terminate()
        # Give time for the thread to finish
        time.sleep(1)

    @Slot()
    def start(self):
        print("Starting...")
        self.button3.setEnabled(True)
        self.button2.setEnabled(True)
        self.button4.setEnabled(True)
        self.button5.setEnabled(True)
        self.button6.setEnabled(True)
        self.button7.setEnabled(True)
        self.button8.setEnabled(True)
        self.button9.setEnabled(True)
        self.button1.setEnabled(False)
        self.th.set_file(self.combobox.currentText())
        self.th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
    
    @Slot()
    def capture_button(self):
        self.th.capture()

    
    @Slot()
    def stepper_left(self):
        stepper_move.move_a_motor(1)
        
    @Slot()
    def stepper_right(self):
        stepper_move.move_a_motor(-1)

    @Slot()
    def stepper_up(self):
        stepper_move.move_a_motor(2)
    
    @Slot()
    def stepper_down(self):
        stepper_move.move_a_motor(-2)
    

    @Slot()
    def stepper_zplus(self):
        stepper_move.move_a_motor(3)

    @Slot()
    def stepper_zminus(self):
        stepper_move.move_a_motor(-3)
    


if __name__ == "__main__":
    app = QApplication()
    w = Window()
    w.show()
    sys.exit(app.exec())