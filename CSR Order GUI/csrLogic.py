from PyQt5.QtWidgets import (QWidget, QGridLayout, QToolButton, QAction, QLineEdit, QHBoxLayout, QVBoxLayout, QFrame, QLabel, 
                             QListWidgetItem, QScrollArea, QTreeWidgetItemIterator, QTreeWidgetItem, QMessageBox)
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
        #self.orderItem.clear()
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
            #print("//wampserver/" + str(i[10]))
        
        
        hBox.addStretch(1)
        hBox.setAlignment(self, Qt.AlignTop)
        self.vBox.addWidget(hFrame)
        self.vBox.addStretch(1)
        
        CSRWidgets.changeCentralWidget(self, self.vBox)
        
   
   
   
   
        

    def loadGarmentInfo(self,sku_code,garment_type,garment_name):
        
              
        garm = mysql_db.garmentInfo(self, sku_code, garment_type)
        columnList = ["Garment", "Quantity"]
        
        #self.garmentTree.header().close()
        self.garmentTree.setHeaderLabels(columnList)
        self.garmentTree.header().resizeSection(0, 275)
        self.garmentTree.setColumnCount(2)
        #self.garmentTree.setMinimumHeight(700)
        
        itSku = QTreeWidgetItemIterator(self.garmentTree)
 
 


        if self.garmentTree.topLevelItemCount() == 0:
            print("NEW PARENT NODE")
            sku = QTreeWidgetItem(self.garmentTree)
            sku.setText(0, sku_code)
            #If the garment name does not exist we want to create a node for it. 
            garmName = QTreeWidgetItem(sku)
            garmName.setText(0, garment_name)
            print(sku.text(0))           
            #Create all the garment types for the node
            for i in garm:
                kiddo = QTreeWidgetItem(garmName)
                kiddo.setText(0, i[1] + " " + i[2])
                le = QLineEdit(self.garmentTree)
                le.setMaximumWidth(30)
                self.garmentTree.setItemWidget(kiddo, 1, le)
                sku.setExpanded(True)
                garmName.setExpanded(True)
                kiddo.setExpanded(True)
        else:       
            while itSku.value():
                print(itSku.value().text(0))
                if itSku.value().text(0) == sku_code:
                    sku_match = 1
                
            if sku_match == 1:
                print("already", sku_code)
                '''
                #Create an iterator to iterate through all the elements in the tree.
                itGarment = QTreeWidgetItemIterator(self.garmentTree)
                #Create a list to hold all the elements in the tree for later reference.
                ls = []
                #Open up iterator
                while itGarment.value():
                    #print(itGarment.value().text(0))
                    #print(sku_code)
                    # if the node has a parent add it to the list
                    if itGarment.value().parent() != None:
                        ls.append(itGarment.value().text(0) + itGarment.value().parent().text(0))
                    #if the node does not equal the garment name passed in the we want to collapse it.
                    if itGarment.value().text(0) != garment_name:
                        itGarment.value().setExpanded(False)
                    itGarment += 1
                #If the garment name is in the list created above we want to tell the user the item in already there and do nothing
                #else, although it keeps collapsing the entire thing.
                if garment_name + sku_code in ls:
                    print("already", garment_name)
                else:
                    #If the garment name does not exist we want to create a node for it. 
                    garmName = QTreeWidgetItem(sku)
                    garmName.setText(0, garment_name)
                    print(sku.text(0))           
                    #Create all the garment types for the node
                    for i in garm:
                        kiddo = QTreeWidgetItem(garmName)
                        kiddo.setText(0, i[1] + " " + i[2])
                        le = QLineEdit(self.garmentTree)
                        le.setMaximumWidth(30)
                        self.garmentTree.setItemWidget(kiddo, 1, le)
                        sku.setExpanded(True)
                        garmName.setExpanded(True)
                        kiddo.setExpanded(True)  
                '''
            else:
                print("New Sku Parent")


                       

            
        

                  
        self.treeDock.show()
        self.viewMenu.addAction(self.treeDock.toggleViewAction())        
        self.vBox.addWidget(self.garmentTree)
        
        self.treeDock.setWidget(self.garmentTree)
        self.addDockWidget(Qt.RightDockWidgetArea, self.treeDock)
        
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
        self.scrollWidget.setAlignment(Qt.AlignTop)
        
        self.setCentralWidget(self.scrollWidget)