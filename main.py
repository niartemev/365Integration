import sys
import mainwindow
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui
import tenant

#Load List of tenants and related APIs from list.txt
def load_API(orgs):
        with open("list.txt") as f:
            for line in f:
                if line != []:
                    org_data = line.split("|")
                    if (len(org_data) < 3):
                        orgs.append(tenant.Tenant(org_data[0], 0))
                    else:
                        orgs.append(tenant.Tenant(org_data[0], org_data[1], org_data[2], org_data[3], org_data[4], org_data[5], org_data[6]))
                    
        return orgs


#initializes tenants and bar_list, then passes them to mainwindow
def main():
    orgs = []
    orgs = load_API(orgs)
    mainwindow.inito(orgs)



#initializer 
if __name__ == "__main__":
    main()
