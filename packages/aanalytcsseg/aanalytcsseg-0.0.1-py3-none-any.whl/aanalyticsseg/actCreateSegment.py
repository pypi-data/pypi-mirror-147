from fileinput import filename
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import actCreateSeg as ac
import sys
import os
import pymysql


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path("segment_create_main.ui")
form_class = uic.loadUiType(form)[0]
# form_class = uic.loadUiType("..\SegmentCreate\segment_create_main.ui")[0]

class MyWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("User Flow Segment Creator")
        self.textLine_owner_enter.clicked.connect(self.getOwnerId)
        self.segmentList.clicked.connect(self.segment_list_open)
        self.segmentSequence.clicked.connect(self.segment_sequence_open)
        self.segmentPrefix_enter.clicked.connect(self.getSegmentPrefix)
        self.pushButton_currentSeg.clicked.connect(self.current_segment_open)
        self.pushButton_segArc.clicked.connect(self.segment_archive_open)
        self.complete.clicked.connect(self.function_execute)

    def getOwnerId(self):
        global owner_id
        owner_id = self.textLine_owner.text()
        self.textLine_owner_out.setText(owner_id)

    def segment_list_open(self):
        global segment_list
        segment_list = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.textBrowser_segList.setText(segment_list[0])

    def segment_sequence_open(self):
        global segment_sequence
        segment_sequence = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.textBrowser_segSeq.setText(segment_sequence[0])

    def getSegmentPrefix(self):
        global segment_prefix
        segment_prefix = self.segmentPrefix.text()
        self.segmentPrefix_out.setText(segment_prefix)

    def current_segment_open(self):
        global current_segment
        current_segment = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowser_currentSeg.setText(current_segment)

    def segment_archive_open(self):
        global segment_archive
        segment_archive = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowser_segArc.setText(segment_archive)
        
    def function_execute(self):
        ac.getSegment(segment_list[0], segment_archive, current_segment, segment_sequence[0], segment_prefix, int(owner_id))
        print("***All User Flow Segments has been created***")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()