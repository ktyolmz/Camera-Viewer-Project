import sys
from PyQt5 import QtWidgets, uic
from camera import *


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main_window_ui.ui', self)

        self.startButton.clicked.connect(self.startButtonClicked)
        self.stopButton.clicked.connect(self.stopButtonClicked)

        self.Thread1 = Thread1()
        self.label.setPixmap(QPixmap.fromImage(self.Thread1.readImage()))

        self.Thread2 = Thread2()
        self.Thread2.date_signal.connect(self.dateTimeUpdateSlot)
        self.Thread2.start()

    def dateTimeUpdateSlot(self, dateTime):
        self.dateTime_label.setText(dateTime.toString())

    def ImageUpdateSlot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def startButtonClicked(self):
        print("Pressed Start")
        self.Thread1.start()
        self.Thread1.ImageUpdate.connect(self.ImageUpdateSlot)

    def stopButtonClicked(self):
        print("Pressed Stop")
        self.Thread1.stop()
        print(self.Thread1.isRunning())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()
    window.Thread2.stop()
