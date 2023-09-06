from PyQt6 import uic 
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import tenant

class Worker(QRunnable):

    def __init__(self, orgs, window, fromUser, toGroup, remove, fromGroup):
        super(Worker, self).__init__()
        self.orgs = orgs
        self.window = window
        self.fromUser = fromUser
        self.toGroup = toGroup
        self.remove = remove
        self.fromGroup = fromGroup

    @pyqtSlot()
    def run(self):
        self.orgs[self.window.clientBox.currentIndex()].group_op(self.fromUser, self.toGroup, self.remove, self.fromGroup)
         


class group_box(QWidget):

    def group_change(self, orgs, window,threadpool, fromUser, toGroup, fromGroup):
        
        worker = Worker(orgs, window, fromUser, toGroup, self.removeCheck.isChecked(), fromGroup)
        threadpool.start(worker)
    def update_lists(self, orgs, window, threadpool):
        self.groupBox.clear()
        for i in (orgs[window.clientBox.currentIndex()].get_usr_groups(self.userBox.currentText())):
            self.groupBox.addItem(i)

    def __init__(self, orgs, window, queue, UPNs):
        
        super().__init__()
        uic.loadUi("groups.ui", self)

        orgs[window.clientBox.currentIndex()].get_groups()
        
        for i in UPNs:
            self.userBox.addItem(i[0])
        for i in orgs[window.clientBox.currentIndex()].groups:
            self.allGroups.addItem(i[0])
        for i in (orgs[window.clientBox.currentIndex()].get_usr_groups(self.userBox.currentText())):
            self.groupBox.addItem(i)

        self.addGrp.clicked.connect(lambda: self.group_change(orgs,window,queue, self.userBox.currentIndex(), self.allGroups.currentIndex(), self.groupBox.currentText()))
        self.userBox.currentIndexChanged.connect(lambda: self.update_lists(orgs,window,queue))