import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Thread1(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ThreadActive = None

    def run(self):
        self.ThreadActive = True
        video = cv2.VideoCapture(-1)
        if not video.isOpened():
            print("Can't open camera")
        while self.ThreadActive:
            ret, frame = video.read()
            # .read() checks frame read correctly or not and returns boolean
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = image.shape
                step = channel * width
                # create QImage from image
                qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
                qImg_scaled = qImg.scaled(560, 400, Qt.KeepAspectRatio)
                if not self.ThreadActive:
                    self.ImageUpdate.emit(self.readImage())
                elif self.ThreadActive:
                    self.ImageUpdate.emit(qImg_scaled)

    def stop(self):
        self.ThreadActive = False
        self.quit()

    def readImage(self):
        img = cv2.imread("icon.png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = img.shape
        step = channel * width
        # create QImage from img
        qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
        qImg_scaled = qImg.scaled(300, 200, Qt.KeepAspectRatio)
        return qImg_scaled


class Thread2 (QThread):
    date_signal = pyqtSignal(QDateTime)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ThreadActive = None

    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            datetime = QDateTime.currentDateTime()
            self.date_signal.emit(datetime)

    def stop(self):
        self.ThreadActive = False
        self.quit()
