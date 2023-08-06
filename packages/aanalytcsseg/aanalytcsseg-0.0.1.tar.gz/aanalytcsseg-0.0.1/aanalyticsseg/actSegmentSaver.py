from fileinput import filename
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import actGetSeg as ag
import sys
import os
import pymysql

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# form_class = uic.loadUiType("SegmentSaver\segment_saver.ui")[0]
form = resource_path("segment_saver.ui")
form_class = uic.loadUiType(form)[0]

class MyWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Segment ID Saver")
        self.segmentList_upload.clicked.connect(self.segment_list_open)
        self.current_segment_folder.clicked.connect(self.current_segment_open)
        self.segment_archive_folder.clicked.connect(self.segment_archive_open)
        self.complete.clicked.connect(self.function_execute)

    def segment_list_open(self):
        global segment_id_list
        # 파일 열면 tuple 형식으로 리턴
        segment_id_list = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.segmentList_show.setText(segment_id_list[0])

    def current_segment_open(self):
        global current_segment
        current_segment = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowser_currentSegment.setText(current_segment)

    def segment_archive_open(self):
        global segment_archive
        segment_archive = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowser_segmentArchive.setText(segment_archive)
        
    def function_execute(self):
        segmentName = ag.readCSV(segment_id_list[0])
        segment_id = ag.idToList(segmentName)

        for i in range(len(segment_id)):
            ag.getSegmentDefinition(segment_id[i], current_segment, segment_archive)
            print("'{segment}' is saved".format(segment = segmentName[i]))
            # self.textBrowse_log.append("'{segment}' is saved".format(segment = segmentName[i]))
        
        print('**All segment definitions have been saved***')
        # self.textBrowse_log.append('**All segment definitions have been saved***')
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()