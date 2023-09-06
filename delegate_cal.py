from PyQt6 import uic 
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import tenant
import reset_pw

class Worker(QRunnable):

    def __init__(self, orgs, window,fromUser, toUser, remove, cal_name, cal_id, editor, reviewer, owner):
        super(Worker, self).__init__()
        self.orgs = orgs
        self.window = window
        self.fromUser = fromUser
        self.toUser = toUser
        self.remove = remove
        self.cal_name = cal_name
        self.cal_id = cal_id
        self.cal_list = []
        self.editor = editor
        self.reviewer = reviewer
        self.owner = owner

    @pyqtSlot()
    def run(self):
        self.orgs[self.window.clientBox.currentIndex()].delegate_cal(self.fromUser, self.toUser, self.remove, self.cal_name, self.cal_id, self.editor, self.reviewer, self.owner)
         


class delegate_cal(QWidget):

    def delegate(self, orgs, window,threadpool):
        
        if self.fromUserbox.currentText() == self.toUserbox.currentText():
            print("Cannot delegate to self")
            return 0
        if self.editor.isChecked() and self.reviewer.isChecked() or self.owner.isChecked and self.reviewer.isChecked() or self.editor.isChecked() and self.owner.isChecked():
            print("Please only select one permission")
            return 0


        worker = Worker(orgs, window, self.fromUserbox.currentText(), self.toUserbox.currentText(), self.remove.isChecked(), self.calBox.currentText(), self.cal_list[self.calBox.currentIndex()].split("|")[1], self.editor.isChecked(), self.reviewer.isChecked(), self.owner.isChecked() )
        threadpool.start(worker)

    def update_list(self, orgs, window, threadpool):
        self.calBox.clear()
        self.cal_list = orgs[window.clientBox.currentIndex()].get_cals(self.fromUserbox.currentText())

        for i in self.cal_list:
            item = i.split("|")
            self.calBox.addItem(item[0])

    def __init__(self, orgs, window, queue, UPNs):
        super().__init__()
        uic.loadUi("deleg_cal.ui", self)
        for i in UPNs:
            self.fromUserbox.addItem(i[0])
            self.toUserbox.addItem(i[0])
            
        user = self.fromUserbox.currentText()
        
        

        self.update_list(orgs,window,queue)
        self.submitBtn2.clicked.connect(lambda: self.delegate(orgs,window,queue))
        self.fromUserbox.currentIndexChanged.connect(lambda: self.update_list(orgs,window,queue))