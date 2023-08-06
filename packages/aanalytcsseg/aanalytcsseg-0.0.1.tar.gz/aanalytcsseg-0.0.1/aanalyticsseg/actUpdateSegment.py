from fileinput import filename
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import actUpdateSeg as au
import sys
import os
import pymysql

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path("segment_update_main.ui")
form_class = uic.loadUiType(form)[0]


class MyWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Segment Update")
        self.pushButton_component.clicked.connect(self.component_segment)
        self.pushButton_current.clicked.connect(self.current_segment_open)
        self.pushButton_archive.clicked.connect(self.segment_archive_open)
        self.pushButton_complete.clicked.connect(self.function_execute)

    def component_segment(self):
        global component_seg
        component_seg = self.lineEdit_component.text()
        self.lineEdit_component_out.setText(component_seg)

    def current_segment_open(self):
        global current_segment
        current_segment = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textEdit_current.setText(current_segment)

    def segment_archive_open(self):
        global segment_archive
        segment_archive = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textEdit_archive.setText(segment_archive)
        
    def function_execute(self):
        # self.textBrowser_log.append('Program Start\n')
        result = au.segmentUpdate(component_seg, current_segment, segment_archive)
        seg_list = result[0]
        checker_list = result[1]
        
        for i in range(len(seg_list)):
            seg_loc = current_segment + "\\" + seg_list[i] + '.json'
            if checker_list[i] == True:
                print('Updated Successfully')
                # self.textBrowser_log.append('Updated Successfully')
            else:
                print('Nothing has been detected to change')
                # self.textBrowser_log.append('Nothing has been detected to change')
            update_log = au.updateSegment(seg_list[i], au.readJson(seg_loc))
            print(update_log)
            # self.textBrowser_log.append('Updated : {0}\n'.format(update_log['name']))
        
        print('**All segment definitions have been saved***')
        # self.textBrowser_log.append('**All segment definitions have been saved***')        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()