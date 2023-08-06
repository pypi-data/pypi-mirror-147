from fileinput import filename
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import actLibrarySeg as al
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# form_class = uic.loadUiType("SegmentLibrary\segment_library.ui")[0]
form = resource_path("segment_library.ui")
form_class = uic.loadUiType(form)[0]
 

class MyWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Segment Library")
        self.textLine_owner_enter.clicked.connect(self.getOwnerId)
        self.segmentArchive.clicked.connect(self.segment_archive_open)
        self.complete.clicked.connect(self.function_execute)

    def getOwnerId(self):
        global owner_id
        owner_id = self.textLine_owner.text()
        self.textLine_owner_out.setText(owner_id)

    def segment_archive_open(self):
        global old_segment
        old_segment = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.textBrowser_segList.setText(old_segment[0])

    def function_execute(self):
        # self.textBrowser_log.append('Program Start')
        seg = al.createSegment(al.pullFromLib(owner_id, old_segment[0]))
        print(seg)
        print('***Segment have been created successfully***')
        # self.textBrowser_log.append('Updated : ' + seg['name'])
        # self.textBrowser_log.append('***Segment have been created successfully***')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()