from PyQt5.QtWidgets import (QWidget, QGridLayout, QToolButton, QAction, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QLabel, 
                             QListWidgetItem, QScrollArea, QGroupBox, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence, QFont
from PyQt5.QtCore import QSize, Qt
from queries import mysql_db


class CSRWidgets(QWidget):
    def __init__(self):
        super(CSRWidgets, self).__init__()    
    
    def createDesignButtons(self, qryId):
        btnLayout = QGridLayout()       
        buttons = {}
        if qryId == 'default':
            qryResult = mysql_db.saleButtons(self)
        else:
            qryResult = mysql_db.searchDesigns(self,qryId)
            

        k = 0
        j = 0
        for i in range(len(qryResult)):
            t = qryResult[i]

            # keep a reference to the buttons
            buttons[(i)] = QToolButton(self)
            buttons[(i)].setIcon(QIcon("//wampserver/" + str(t[2])))
            buttons[(i)].setIconSize(QSize(180, 180))
            buttons[(i)].setAutoRaise(True)
            buttons[(i)].setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            buttons[(i)].setStyleSheet("background-color: rgb(255, 255, 255);")
            buttons[(i)].setFont(QFont("Helvetica",12,QFont.Bold))
            buttons[(i)].setObjectName(str(t[1]))
            buttons[(i)].setText(str(t[1]) + '\n' + str(t[0]))
            buttons[(i)].clicked.connect(self.btnSale_Click)

            # add to the layout
            btnLayout.addWidget(buttons[(i)], j, k)   
            
            if k == 3:
                j += 1
                k = 0
            else:
                k += 1  
                
            btnLayout.setObjectName("designPage")    

        return btnLayout
 



  
    def createActions(self):

        self.quitAct = QAction(QIcon('icon/exit.png'), "&Quit", self, shortcut="Ctrl+Q", statusTip="Quit the application", 
                               triggered=self.close)

        self.aboutAct = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)  
        self.searchAct = QAction(QIcon('icon/search.png'), '&Search', self, shortcut=Qt.Key_Return, statusTip="Find a design.",
                                 triggered=self.btnSearch_Click)
        self.homeAct = QAction(QIcon('icon/home-icon.png'), '&Home', self, shortcut="Ctrl+H", statusTip="Return to home screen.", 
                               triggered=self.btnHome_Click)
        self.undoAct = QAction(QIcon('icon/undo.png'), '&Undo', self, shortcut=QKeySequence.Undo, 
                               statusTip="This will undo actions added to order", triggered=self.btnUndo_Click)
        self.enterAct = QAction(self, shortcut=Qt.Key_Enter, triggered=self.btnSearch_Click)
  
   
   
   
   
        
    def loadDesignItem(self, sku_code):
        self.availableItems.clear()
        self.orderItem.clear()
        des = mysql_db.designInfo(self, sku_code)
        
        self.vBox = QVBoxLayout()
        
        if not des:
            lblOpps = QLabel("We could put a .png or something here, something better than text, to let the CSR's know that " + \
                             "they searched an empty string or that the design they were looking for does not exist or that " + \
                             "they mistyped what they were looking for.", self)
            self.vBox.addWidget(lblOpps)
            CSRWidgets.changeCentralWidget(self, self.vBox)
        #print(des)        

        self.currentInfo = {}
        for i in des:
            CSRWidgets.item = QListWidgetItem()
            CSRWidgets.item.setText(str(i[7]))         
            self.currentInfo[i[7]] = (str(i[7]),str(i[8]),str(i[3]),str(i[9]),str(i[10]),str(i[11]))
            self.availableItems.addItem(CSRWidgets.item)
                
        smImage = self.currentInfo['T-Shirts'][3]
        hBox = QHBoxLayout()
        
        
        pix = QLabel()
        smImg = QPixmap("//wampserver/"+ smImage)
        myScaledPixmap = smImg.scaled(125,125, Qt.KeepAspectRatio)
        pix.setPixmap(myScaledPixmap)

        hBox.addWidget(pix)
        hFrame = QFrame()
        hFrame.setLayout(hBox)
        hFrame.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        print(self.currentInfo)
        
        
        
     
        
        icons = {}
        for i in des:
            icons[(i)] = QToolButton(self)
            icons[(i)].setIcon(QIcon("//wampserver/" + str(i[10])))
            icons[(i)].setIconSize(QSize(44, 44))
            icons[(i)].setAutoRaise(True)
            icons[(i)].setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            #icons[(i)].setStyleSheet("background-color: rgb(255, 255, 255);")
            icons[(i)].setFont(QFont("Helvetica",8))
            #icons[(i)].setObjectName(str(i[7]))
            icons[(i)].setText(str(i[7]) + '\n' + str(i[3]))
            icons[(i)].uniqueId = str(i[7])
            icons[(i)].clicked.connect(self.itemClicked_Click)
            hBox.addWidget(icons[(i)])
            print("//wampserver/" + str(i[10]))
        
        
        hBox.addStretch(1)
        self.vBox.addWidget(hFrame)
        self.vBox.addStretch(1)
        
        CSRWidgets.changeCentralWidget(self, self.vBox)
        
   
   
   
   
        

    def loadGarmentInfo(self,sku_code,garment_type,garment_name):      
        layout = {}
        self.grpBox = {}
        btnShow = {}
        btnHide = {}
        self.grpBox[garment_name] = QGroupBox(garment_name)
        
#         btnShow[garment_name] = QPushButton(garment_name)
#         btnShow[garment_name].setObjectName(garment_name)
#         btnShow[garment_name].clicked.connect(self.showOrder)
#         
#         btnHide[garment_name] = QPushButton(garment_name + " hide")
#         btnHide[garment_name].setObjectName(garment_name)
#         btnHide[garment_name].clicked.connect(self.hideOrder)
        
        self.orderItem.clear()
        garm = mysql_db.garmentInfo(self, sku_code, garment_type)
        layout[garment_type] = QVBoxLayout()
        #layout[garment_type].addWidget(btnShow[garment_name])
        
        
#         for g in garm:
#             CSRWidgets.item = QLabel()
#             CSRWidgets.item.setText(str(g[0])+ ' - '+str(g[1])+ ' - '+str(g[2]))
#             layout[garment_type].addWidget(CSRWidgets.item)
#             layout[garment_type].setAlignment(self, Qt.AlignTop)
#             print(layout[garment_type] )
            
        
        tree = QTreeWidget()
        tree.setHeaderLabels([garment_name])
        garm = mysql_db.garmentInfo(self, sku_code, garment_type)
        parent = QTreeWidgetItem(tree)
        parent.setText(0, garment_name)
        for i in garm:
            #l.append(QTreeWidgetItem(i[2]))
            kiddo = QTreeWidgetItem(parent)
            kiddo.setText(0, i[2])
        #tree.addTopLevelItems(l)
            
            #btnShow.clicked.connect(self.show)

        #self.grpBox[garment_name].setLayout(layout[garment_type])
        #self.vBox.addWidget(self.grpBox[garment_name])
        #self.vBox.addWidget(btnShow[garment_name])
        self.vBox.addWidget(tree)
        #self.vBox.addWidget(btnHide[garment_name])
        self.vBox.setAlignment(self, Qt.AlignTop)

    def undo(self):
        print("this will \"undo\" items added to the order.")
        self.searchBar.clear()
  
  
  
  
  
        
    def changeCentralWidget(self, widgetLayout):
       
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(widgetLayout)
        self.mainWidget.setMinimumSize(1100, 800)
        if str(widgetLayout.objectName()) == "designPage":
            self.mainWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.scrollWidget = QScrollArea()
        self.scrollWidget.setWidgetResizable(True)
        self.scrollWidget.setWidget(self.mainWidget)
        
        self.setCentralWidget(self.scrollWidget)