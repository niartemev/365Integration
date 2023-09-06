from PyQt6 import uic 
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import tenant
import reset_pw
import delegate_em
import delegate_cal
import group
import change_info
import spam

#Main Menu Control
class MainWindow(QMainWindow):
      
    def action_selector_sec(self, value):
        match value:
            case 0:
                self.window = spam.spam_ops(self, self.orgs, self.threadpool, self.bar_list)
                self.window.show()
                print("block spam")
            case 1:
                print("change mfa")
            case 2:
                print("block sign in")
    
    def action_selector(self, value):
        match value:
            case 0:
                print("Reset Password")
                self.window = reset_pw.reset_pw(self.userBox.currentText(), self.orgs, self)
                self.window.show()
            case 1:
                self.window = delegate_em.delegate_em(self.orgs, self, self.threadpool, self.UPNs)
                self.window.show()
                print("Delegate Email")
            case 2:
                self.window = delegate_cal.delegate_cal(self.orgs, self, self.threadpool, self.UPNs)
                self.window.show()
                print("Delegate Calendar")
            case 3:
                self.window = change_info.change_info(self.orgs, self, self.threadpool, self.UPNs, self.userBox.currentText())
                self.window.show()
                print("Edit Info")
            case 4:
                self.window = group.group_box(self.orgs, self, self.threadpool, self.UPNs)
                self.window.show()
                print("Group Membership")


    #updates the client box with the list of clients
    def update_cBox(self, organizations):

        c = 0
        for i in organizations:
            if(organizations[c].api != 0):
                self.clientBox.addItem(organizations[c].name)
                c += 1
            if(organizations[c].api == 0):
                return 0

    #updates the user box with the list of users
    def update_uBox(self, value):
        
        
        self.userBox.clear()

        #print(self.orgs[value].name)
        self.orgs[value].get_token()
        self.UPNs = self.orgs[value].get_user_list()

        c = 0
        for i in self.orgs[value].UPNs:
            self.userBox.addItem(self.orgs[value].UPNs[c][0])
            c += 1

    #initializes nothing for now
    def main(self):
        orgs = []
        bar_list = []

        self.update_uBox(0)
    

    #initializes the window
    def __init__(self,orgs, bar_list):

        self.threadpool = QThreadPool()
        print("we re her1e")
        super().__init__()
        self.orgs = orgs
        self.bar_list = bar_list
        self.UPNs = []
        uic.loadUi("interface2.ui", self)
        self.setWindowTitle("Helpdesk Hero")

        self.statusWindow.ensureCursorVisible()
        self.update_cBox(orgs)
        self.clientBox.currentIndexChanged.connect(self.update_uBox)
        self.action_1.activated.connect(self.action_selector)
        self.secure_box.activated.connect(self.action_selector_sec)
        self.main()
        


#initializes the objects and calls to init the window
def inito(orgs, bar_list):
    app = QApplication([])
    window = MainWindow(orgs, bar_list)
    window.show()
    app.exec()
    
