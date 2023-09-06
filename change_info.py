from PyQt6 import uic 
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import tenant
import reset_pw


class Worker(QRunnable):

    def __init__(self, orgs,window, user, firstN, lastN, displN, emAddy):# window, user, new_name, new_phone, new_title):
        super(Worker, self).__init__()
        self.orgs = orgs
        self.window = window
        self.user = user
        self.firstN = firstN
        self.lastN = lastN
        self.displN = displN
        self.emAddy = emAddy
        

        

    @pyqtSlot()
    def run(self):
        self.orgs[self.window.clientBox.currentIndex()].change_info(self.user, self.firstN, self.lastN, self.displN, self.emAddy)
         


class change_info(QWidget):

    def change_info(self,orgs,window,threadpool, user):
        worker = Worker(orgs,window,user, self.firstName.text(), self.lastName.text(), self.displayName.text(), self.emailAddy.text())
        threadpool.start(worker)

    def __init__(self, orgs, window, queue, UPNs, user):
        super().__init__()
        uic.loadUi("change_info.ui", self)
        
        self.submitInfo.clicked.connect(lambda: self.change_info(orgs,window,queue,user))
            
        
        
