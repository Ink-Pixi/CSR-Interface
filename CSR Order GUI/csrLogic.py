from PyQt5.QtWidgets import QWidget, QGridLayout, QToolButton, QAction, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from queries import getQueries


class CSRWidgets(QWidget):
    
    def createSaleButtons(self):
        btnLayout = QGridLayout()
        
        buttons = {}

        onSale = getQueries.get_onSale(self)

        
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
            buttons[(i)].setObjectName(str(t[2]))
            buttons[(i)].setText(str(t[2]) + '\n' + str(t[1]))
            buttons[(i)].clicked.connect(self.btnSaleClick)

            # add to the layout
            btnLayout.addWidget(buttons[(i)], j, k)   
            
            if k == 3:
                j += 1
                k = 0
            else:
                k += 1        
        
        return btnLayout        
    
    def createActions(self):

        self.quitAct = QAction(QIcon('icon/exit.png'), "&Quit", self, shortcut="Ctrl+Q", statusTip="Quit the application", 
                               triggered=self.close)

        self.aboutAct = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)  
        self.searchAct = QAction(QIcon('icon/search.png'), '&Search', self, shortcut=Qt.Key_Return, statusTip="Find a design.",
                                 triggered=self.btnSearch_Click)
        
    def loadDesignItem(self, sku_code):
        des = getQueries.get_Design(self, sku_code)
        print(des)
        
    def onShow(self):
        if not self.mainFrame:
            self.createButtons()
            self.setCentralWidget(self.mainFrame)
            
    def onHide(self):
        if self.mainFrame:
            self.mainFrame.deleteLater()
            self.mainFrame = None
            
            hBox = QHBoxLayout()
            btnTest = QPushButton("Test")
            btnTest.clicked.connect(self.btnShow_Click)
            hBox.addWidget(btnTest)
            
            self.frmTest = QFrame()
            self.frmTest.setLayout(hBox)
            self.setCentralWidget(self.frmTest)
            
    def designSearch(self):
        test = self.searchBar.text()
        print(test)
