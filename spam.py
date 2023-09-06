from PyQt6 import uic 
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import tenant

class Worker(QRunnable):

    def __init__(self, orgs, window, client, target, api):
        super(Worker, self).__init__()
        self.orgs = orgs
        self.window = window
        self.client = client
        self.target = target
        self.api = api

    @pyqtSlot()
    def run(self):
        self.orgs[self.window.clientBox.currentIndex()].spam_ops(self.client,self.target, self.api)
         


class spam_ops(QWidget):

    def start_worker(self, orgs, window,threadpool):
        
        worker = Worker(orgs, window, self.clientBox.currentText(), self.target_email.text(), self.bar_list[self.clientBox.currentIndex()][1])
        threadpool.start(worker)

    def keyPressEvent(self, event):
        if(event.key() == 16777220):
            c = 0
            for i in self.bar_list:
                c += 1
                if self.searchBox.text().lower() in i[0].lower():
                    self.clientBox.setCurrentIndex(c-1)
                    break

    def __init__(self, window, orgs, threadpool, bar_list):
        
        self.bar_list = bar_list
        super().__init__()
        uic.loadUi("spam_block.ui", self)

        for i in orgs:
            self.clientBox.addItem(i.name)
 
       
       
        self.spamSubmit.clicked.connect(lambda: self.start_worker(orgs,window,threadpool))