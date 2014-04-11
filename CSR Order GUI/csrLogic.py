from PyQt5.QtWidgets import QWidget, QGridLayout, QToolButton, QDockWidget, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from queries import get_onSale

class CSRwidgets(QWidget):
    
    def createSaleButtons(self):
        btnLayout = QGridLayout()
        
        buttons = {}
        onSale = get_onSale()
        
        k = 0
        j = 0
        for i in range(len(onSale)):
            t = onSale[i]

            # keep a reference to the buttons
            buttons[(i)] = QToolButton(self)
            buttons[(i)].setIcon(QIcon("//wampserver/" + str(t[7])))
            buttons[(i)].setIconSize(QSize(120, 120))
            buttons[(i)].setAutoRaise(True)
            buttons[(i)].setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            buttons[(i)].setStyleSheet("background-color: rgb(255, 255, 255);")
            #buttons[(i)].setFont(QFont("Helvetica",10,QFont.Bold))
            buttons[(i)].setText(str(t[2]) + '\n' + str(t[1]))

            # add to the layout
            btnLayout.addWidget(buttons[(i)], j, k)   
            
            if k == 3:
                j += 1
                k = 0
            else:
                k += 1        
        
        return btnLayout        
    
    def createDockWindows(self):
        dock = QDockWidget("Stuff", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.customerList = QListWidget(dock)
        self.customerList.addItems((
            "stuff"))
        dock.setWidget(self.customerList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("More Stuff", self)
        self.paragraphsList = QListWidget(dock)
        self.paragraphsList.addItems((
            "more stuff"))
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())    
        
    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.quitAct)
        self.fileToolBar.addAction(self.printAct)        