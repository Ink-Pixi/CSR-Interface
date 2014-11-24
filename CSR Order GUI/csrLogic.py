from PyQt5.QtWidgets import (QWidget, QGridLayout, QToolButton, QAction, QHBoxLayout, QFrame, QLabel, QVBoxLayout,
                             QListWidgetItem, QScrollArea, QTreeWidgetItemIterator, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QInputDialog, QApplication)
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence, QFont, QColor
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
        self.searchAct = QAction(QIcon('icon/search.png'), '&Search', self, shortcut=Qt.Key_Enter, statusTip="Find a design.",
                                 triggered=self.btnSearch_Click)
        self.homeAct = QAction(QIcon('icon/home-icon.png'), '&Home', self, shortcut="Ctrl+H", statusTip="Return to home screen.", 
                               triggered=self.btnHome_Click)
        self.undoAct = QAction(QIcon('icon/undo.png'), '&Undo', self, shortcut=QKeySequence.Undo, 
                               statusTip="This will undo actions added to order", triggered=self.btnUndo_Click)
      
    def loadDesignItem(self, sku_code):
        self.lblSkuName.setText(sku_code)
        des = mysql_db.designInfo(self, sku_code)
        
        #self.vBox = QVBoxLayout()
        self.winGrid = QGridLayout()
        
        if not des:
            lblOpps = QLabel("""We could put a .png or something here, something better than text, to let the CSR's know that 
                             they searched an empty string or that the design they were looking for does not exist or that 
                             they mistyped what they were looking for.""", self)
            self.grid.addWidget(lblOpps)
            CSRWidgets.changeCentralWidget(self, self.vBox)

        self.currentInfo = {}
        for i in des:
            CSRWidgets.item = QListWidgetItem()
            CSRWidgets.item.setText(str(i[7]))         
            self.currentInfo[i[7]] = (str(i[7]),str(i[8]),str(i[3]),str(i[9]),str(i[10]),str(i[11]),str(i[1]))
        smImage = self.currentInfo['T-Shirts'][3]

        hBox = QHBoxLayout()
        
        pix = QLabel()
        smImg = QPixmap("//wampserver/"+ smImage)
        myScaledPixmap = smImg.scaled(125,125, Qt.KeepAspectRatio)
        pix.setPixmap(myScaledPixmap)

        hBox.addWidget(pix)
       
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
        
        hBox.addStretch(1)
        
        hFrame = QFrame()
        hFrame.setLayout(hBox)
        hFrame.setMaximumHeight(200)
        hFrame.setStyleSheet("background-color: rgb(255, 255, 255);") 
        
        #Create table to hold and display details of order order as they are selected from the tree. 
        CSRWidgets.tblOrderDetails = QTableWidget(7, 0)
        CSRWidgets.tblOrderDetails.hide()
        #CSRWidgets.tblOrderDetails.setMaximumHeight(250)

        
        self.winGrid.addWidget(hFrame, 0, 0, 2, 2)
        #self.vBox.addWidget(hFrame)
        #self.vBox.addWidget(CSRWidgets.tblOrderDetails)
        self.winGrid.addWidget(CSRWidgets.tblOrderDetails, 2, 0, 1, 1)
        #self.winGrid.addWidget(CSRWidgets.totalBox, 2, 1, 1, 1)       
        #self.vBox.addStretch(1)

        CSRWidgets.changeCentralWidget(self, self.winGrid)
        
        CSRWidgets.updateOrderDetails(self)
        
        CSRWidgets.getCustomerName(self, sku_code)
        
    def totalBox(self):
        lblTest = QLabel("test")
        lblSomething = QLabel("something else")
        
        totBox = QVBoxLayout()
        totBox.addWidget(lblTest)
        totBox.addWidget(lblSomething)
        totBox.addStretch()
        
        tFrame = QFrame()
        tFrame.setLayout(totBox)
        tFrame.setMinimumWidth(350)
        
        return tFrame
               
    def undo(self):
        print("this will \"undo\" items added to the order.")
        self.searchBar.clear()
  
    def changeCentralWidget(self, widgetLayout):
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(widgetLayout)
        #self.mainWidget.setMinimumSize(900, 800)
        if str(widgetLayout.objectName()) == "designPage":
            self.mainWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.scrollWidget = QScrollArea()
        self.scrollWidget.setWidgetResizable(True)
        self.scrollWidget.setWidget(self.mainWidget)
        self.scrollWidget.setAlignment(Qt.AlignTop)
        
        self.setCentralWidget(self.scrollWidget)
        
    def loadGarmentInfo(self,sku_code,garment_type,garment_name,design_name):

        #print(garment_type)
        #Query the database to get all garments available for this particular SKU.      
        garm = mysql_db.garmentInfo(self, sku_code, garment_type)
        columnList = ["Design", "Size","Price", "Qty",""]
        
        #Set tree header/title stuff
        self.garmentTree.setHeaderLabels(columnList)
        self.garmentTree.setColumnCount(5)
        self.garmentTree.header().resizeSection(0, 280)
        self.garmentTree.header().resizeSection(1, 75)
        self.garmentTree.header().resizeSection(2, 45)
        self.garmentTree.header().resizeSection(3, 30)
        self.garmentTree.header().resizeSection(4, 10)
        
        #If there are no nodes in this tree yet, create the first one
        if self.garmentTree.topLevelItemCount() == 0:
            #print("NEW PARENT NODE")
            CSRWidgets.lblTotal = {}
            nm = QTreeWidgetItem(self.garmentTree)
            nm.setText(0, self.orderVars)
            nm.setBackground(0, QColor(180,180,180,127))
            nm.setBackground(1, QColor(180,180,180,127))
            nm.setBackground(2, QColor(180,180,180,127))
            nm.setBackground(3, QColor(180,180,180,127))
            nm.setBackground(4, QColor(180,180,180,127))
            nm.setFont(0, QFont("Helvetica",16,QFont.Bold))
            
            sku = QTreeWidgetItem(nm)
            sku.setText(0, sku_code)
            sku.setBackground(0, QColor(180,180,180,127))
            sku.setBackground(1, QColor(180,180,180,127))
            sku.setBackground(2, QColor(180,180,180,127))
            sku.setBackground(3, QColor(180,180,180,127))
            sku.setBackground(4, QColor(180,180,180,127))
            sku.setFont(0, QFont("Helvetica",12,QFont.Bold))
            
            #If the garment name does not exist we want to create a node for it. 
            garmName = QTreeWidgetItem(sku)
            garmName.setText(0, garment_name)
            garmName.setText(3, "")
            garmName.setFont(0,QFont("Helvetica",10,QFont.Bold))
            garmName.setFont(3,QFont("Helvetica",10,QFont.Bold))
            garmName.setBackground(0, QColor(230,230,230,127))
            garmName.setBackground(1, QColor(230,230,230,127))
            garmName.setBackground(2, QColor(230,230,230,127))
            garmName.setBackground(3, QColor(230,230,230,127))
            garmName.setBackground(4, QColor(230,230,230,127))
            
            removeName = QToolButton(self)
            removeName.setIcon(QIcon("Icon/close-widget.png"))
            removeName.setIconSize(QSize(14,14))
            removeName.setAutoRaise(True)
            removeName.clicked.connect(lambda: CSRWidgets.remove_widget(self))
            
            removeSku = QToolButton(self)
            removeSku.setIcon(QIcon("icon/close-widget.png"))
            removeSku.setIconSize(QSize(14, 14))
            removeSku.setAutoRaise(True)
            removeSku.clicked.connect(lambda: CSRWidgets.remove_widget(self))
            
            removeGarment = QToolButton(self)
            removeGarment.setIcon(QIcon("icon/close-widget.png"))
            removeGarment.setIconSize(QSize(14, 14))
            removeGarment.setAutoRaise(True)
            removeGarment.clicked.connect(lambda: CSRWidgets.remove_widget(self))

            CSRWidgets.lblTotal[str(sku_code + garment_name)] = QLabel()
            CSRWidgets.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
            CSRWidgets.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
            
            self.garmentTree.setItemWidget(nm, 4, removeName)
            self.garmentTree.setItemWidget(sku, 4, removeSku)
            self.garmentTree.setItemWidget(garmName, 4, removeGarment)              
            self.garmentTree.setItemWidget(garmName, 3, CSRWidgets.lblTotal[str(sku_code + garment_name)])
            CSRWidgets.le = {}
            #Create all the garment types for the first node
            for i in garm:
                kiddo = QTreeWidgetItem(garmName)
                kiddo.setText(0, i[1])
                kiddo.setText(2, str(i[3]))
                kiddo.setText(1, i[2])
                kiddo.setText(3,"")
                kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold) )
                kiddo.setText(4,"-")
                
                nm.setExpanded(True)
                sku.setExpanded(True)
                garmName.setExpanded(True)
                kiddo.setExpanded(True)
                #print(le.objectName())

                
                
        #If items already exist in the tree, do stuff depending on what sku/garment was clicked.
        else:          
            name_match = 0
            sku_match = 0       
            itSku = QTreeWidgetItemIterator(self.garmentTree) 

            #iterate through all tree items and see if anything matches the SKU we selected.           
            while itSku.value():
                if itSku.value().text(0) == self.orderVars:
                    name_match = 1
                    #print("NAME MATCHED!!!")
                #If the SKU we selected exists somewhere in the tree, set variable to indicate that.
                if itSku.value().text(0) == sku_code and itSku.value().parent().text(0) == self.orderVars:
                    sku_match = 1
                    #print("SKU MATCHED!!!")
                #Collapse all non-parent nodes so we can selectively open the nodes we are currently working on below.
                if itSku.value().parent() != None:   
                    itSku.value().setExpanded(False)
                itSku += 1

            if name_match == 1:
                #print("NAME MATCHED!!!!!!!!")
                #if the SKU we've selected already exists in the tree, check to see if the garment we've selected exists also   
                if sku_match == 1:
                    #print("SKU MATCHED!!!")
                    garm_match = 0
                    #print("already", sku_code)
                    #Create an iterator to iterate through all the elements in the tree.
                    itGarment = QTreeWidgetItemIterator(self.garmentTree)
                    #Open up iterator
                    while itGarment.value():
                        #If BOTH the SKU and garment already exist in the tree, just expand it while collapsing all other items.
                        if itGarment.value().text(0) == garment_name and itGarment.value().parent().text(0) == sku_code and itGarment.value().parent().parent().text(0) == self.orderVars:
                            #itGarment.value().parent().setExpanded(True)
                            #itGarment.value().setExpanded(True)
                            garm_match = 1
                            itGarment.value().parent().parent().setExpanded(True)
                            itGarment.value().parent().setExpanded(True)
                            itGarment.value().setExpanded(True)
                            
                        itGarment += 1
    
    
                    #If the selected garment does NOT exist in the tree for this SKU, create it.
                    if garm_match == 0:
                        #create tree iterator
                        itSizes = QTreeWidgetItemIterator(self.garmentTree)
                        while itSizes.value():
                            #When the iterator hits the correct SKU, create the new garment node that doesn't exist yet.                         
                            if itSizes.value().text(0) == sku_code and itSizes.value().parent().text(0) == self.orderVars:
                                #If the garment name does not exist we want to create a node for it. 
                                garmName = QTreeWidgetItem(itSizes.value())
                                garmName.setText(0, garment_name)
                                garmName.setText(3, "")
                                garmName.setFont(0,QFont("Helvetica",10,QFont.Bold))
                                garmName.setFont(3,QFont("Helvetica",10,QFont.Bold))
                                
                                
                                garmName.setBackground(0, QColor(230,230,230,127))
                                garmName.setBackground(1, QColor(230,230,230,127))
                                garmName.setBackground(2, QColor(230,230,230,127))
                                garmName.setBackground(3, QColor(230,230,230,127))
                                garmName.setBackground(4, QColor(230,230,230,127))
                                
                                removeGarment = QToolButton(self)
                                removeGarment.setIcon(QIcon("icon/close-widget.png"))
                                removeGarment.setIconSize(QSize(14, 14))
                                removeGarment.setAutoRaise(True)
                                removeGarment.clicked.connect(lambda: CSRWidgets.remove_widget(self))
                                CSRWidgets.lblTotal[str(sku_code + garment_name)] = QLabel(self.garmentTree)
                                CSRWidgets.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
                                CSRWidgets.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
                                
                                self.garmentTree.setItemWidget(garmName, 4, removeGarment)
                                self.garmentTree.setItemWidget(garmName, 3, CSRWidgets.lblTotal[str(sku_code + garment_name)])
                                #Create all the garment types for the node
                                #CSRWidgets.le = {}
                                for i in garm:
                                    kiddo = QTreeWidgetItem(garmName)
                                    kiddo.setText(0, i[1])
                                    kiddo.setText(2, str(i[3]))
                                    kiddo.setText(1, i[2])
                                    kiddo.setText(3,"")
                                    kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold) )
                                    kiddo.setText(4,"-")
                                    itSizes.value().setExpanded(True)
                                    garmName.setExpanded(True)
                                    kiddo.setExpanded(True)
                            itSizes += 1       
     
     
                                           
                    
                #If the SKU does NOT exist in the tree yet, but others already do, create this particular SKU.
                else:
                    #print("SAME NAME, DIFFERENT SKU!!!!! SKU = " + sku_code + " -- Name = " + self.orderVars)                       
                            
                    iterNewSku =  QTreeWidgetItemIterator(self.garmentTree) 
                    
                    while iterNewSku.value():
                        
                        if iterNewSku.value().childCount() > 0:
                            if iterNewSku.value().text(0) == self.orderVars:
                                                  
                                sku = QTreeWidgetItem(iterNewSku.value())     
                                sku.setText(0, sku_code)
                                sku.setBackground(0, QColor(180,180,180,127))
                                sku.setBackground(1, QColor(180,180,180,127))
                                sku.setBackground(2, QColor(180,180,180,127))
                                sku.setBackground(3, QColor(180,180,180,127))
                                sku.setBackground(4, QColor(180,180,180,127))
                                sku.setFont(0, QFont("Helvetica",12,QFont.Bold) )
                                removeSku = QToolButton(self)
                                removeSku.setIcon(QIcon("icon/close-widget.png"))
                                removeSku.setIconSize(QSize(14, 14))
                                removeSku.setAutoRaise(True)
                                removeSku.clicked.connect(lambda: CSRWidgets.remove_widget(self))
                                
                                
                                garmName = QTreeWidgetItem(sku)
                                garmName.setText(0, garment_name)
                                garmName.setText(3, "")
                                garmName.setFont(0,QFont("Helvetica",10,QFont.Bold))
                                garmName.setFont(3,QFont("Helvetica",10,QFont.Bold))
                                garmName.setBackground(0, QColor(230,230,230,127))
                                garmName.setBackground(1, QColor(230,230,230,127))
                                garmName.setBackground(2, QColor(230,230,230,127))
                                garmName.setBackground(3, QColor(230,230,230,127))
                                garmName.setBackground(4, QColor(230,230,230,127)) 
                                
                                removeGarment = QToolButton(self)
                                removeGarment.setIcon(QIcon("icon/close-widget.png"))
                                removeGarment.setIconSize(QSize(14, 14))
                                removeGarment.setAutoRaise(True)
                                removeGarment.clicked.connect(lambda: CSRWidgets.remove_widget(self))
                                
                                CSRWidgets.lblTotal[str(sku_code + garment_name)] = QLabel(self.garmentTree)
                                CSRWidgets.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
                                CSRWidgets.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
                                
                                self.garmentTree.setItemWidget(sku, 4, removeSku)
                                self.garmentTree.setItemWidget(garmName, 4, removeGarment)  
                                self.garmentTree.setItemWidget(garmName, 3, CSRWidgets.lblTotal[str(sku_code + garment_name)])
                                #CSRWidgets.le = {}
                                #Create all the garment types for the first node
                                for i in garm:
                                    kiddo = QTreeWidgetItem(garmName)
                                    kiddo.setText(0, i[1])
                                    kiddo.setText(2, str(i[3]))
                                    kiddo.setText(1, i[2])
                                    kiddo.setText(3,"")
                                    kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold))
                                    kiddo.setText(4,"-")
                                    #nm.setExpanded(True)
                                    sku.setExpanded(True)
                                    garmName.setExpanded(True)
                                    kiddo.setExpanded(True)
                            
                        iterNewSku += 1

                        
            else:
                #print("NEW NAME")

                CSRWidgets.lblTotal = {}
                nm = QTreeWidgetItem(self.garmentTree)
                nm.setText(0, self.orderVars)
                nm.setBackground(0, QColor(180,180,180,127))
                nm.setBackground(1, QColor(180,180,180,127))
                nm.setBackground(2, QColor(180,180,180,127))
                nm.setBackground(3, QColor(180,180,180,127))
                nm.setBackground(4, QColor(180,180,180,127))
                nm.setFont(0, QFont("Helvetica",16,QFont.Bold))
                
                sku = QTreeWidgetItem(nm)
                sku.setText(0, sku_code)
                sku.setBackground(0, QColor(180,180,180,127))
                sku.setBackground(1, QColor(180,180,180,127))
                sku.setBackground(2, QColor(180,180,180,127))
                sku.setBackground(3, QColor(180,180,180,127))
                sku.setBackground(4, QColor(180,180,180,127))
                sku.setFont(0, QFont("Helvetica",12,QFont.Bold))
                
                
                #If the garment name does not exist we want to create a node for it. 
                garmName = QTreeWidgetItem(sku)
                garmName.setText(0, garment_name)
                garmName.setText(3, "")
                garmName.setFont(0,QFont("Helvetica",10,QFont.Bold))
                garmName.setFont(3,QFont("Helvetica",10,QFont.Bold))
                garmName.setBackground(0, QColor(230,230,230,127))
                garmName.setBackground(1, QColor(230,230,230,127))
                garmName.setBackground(2, QColor(230,230,230,127))
                garmName.setBackground(3, QColor(230,230,230,127))
                garmName.setBackground(4, QColor(230,230,230,127))
                
                removeName = QToolButton(self)
                removeName.setIcon(QIcon("Icon/close-widget.png"))
                removeName.setIconSize(QSize(14,14))
                removeName.setAutoRaise(True)
                removeName.clicked.connect(lambda: CSRWidgets.remove_widget(self))                
                
                removeSku = QToolButton(self)
                removeSku.setIcon(QIcon("icon/close-widget.png"))
                removeSku.setIconSize(QSize(14, 14))
                removeSku.setAutoRaise(True)
                removeSku.clicked.connect(lambda: CSRWidgets.remove_widget(self))
                
                removeGarment = QToolButton(self)
                removeGarment.setIcon(QIcon("icon/close-widget.png"))
                removeGarment.setIconSize(QSize(14, 14))
                removeGarment.setAutoRaise(True)
                removeGarment.clicked.connect(lambda: CSRWidgets.remove_widget(self))
    
                CSRWidgets.lblTotal[str(sku_code + garment_name)] = QLabel()
                CSRWidgets.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
                CSRWidgets.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
                
                self.garmentTree.setItemWidget(nm, 4, removeName)
                self.garmentTree.setItemWidget(sku, 4, removeSku)
                self.garmentTree.setItemWidget(garmName, 4, removeGarment)              
                self.garmentTree.setItemWidget(garmName, 3, CSRWidgets.lblTotal[str(sku_code + garment_name)])
                CSRWidgets.le = {}
                #Create all the garment types for the first node
                for i in garm:
                    kiddo = QTreeWidgetItem(garmName)
                    kiddo.setText(0, i[1])
                    kiddo.setText(2, str(i[3]))
                    kiddo.setText(1, i[2])
                    kiddo.setText(3,"")
                    kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold) )
                    kiddo.setText(4,"-")
                    
                    nm.setExpanded(True)
                    sku.setExpanded(True)
                    garmName.setExpanded(True)
                    kiddo.setExpanded(True)
                    #print(le.objectName())
                
                
        self.treeDock.show()
        self.viewMenu.addAction(self.treeDock.toggleViewAction())        
        
        self.treeDock.setWidget(self.garmentTree)
        self.addDockWidget(Qt.RightDockWidgetArea, self.treeDock)
        
    def remove_widget(self):
        btn = self.sender()
        btn.setFocus()
        root = self.garmentTree.invisibleRootItem()
        
        rootParent = self.garmentTree.invisibleRootItem()
        print(rootParent.parent())
        
        for item in self.garmentTree.selectedItems():
            (item.parent() or root).removeChild(item)        
            
        CSRWidgets.updateOrderDetails(self)
        
    def sumQuantity(self, column):

        if self.text(column) and self.childCount() == 0 and self.parent() != None:
            #If this row has no Quantity yet, set it to zero.
            if self.text(3) == "":
                newNum = 0
            else:
                newNum = int(self.text(3))
            if self.parent().text(3) == "":
                newSum = 0
            else:
                newSum = int(self.parent().text(3))
                                               
            #If user clicks on the "-" sign in column 4, subtract 1
            if column == 4:
                if newNum > 0:
                    newNum = newNum - 1
                    if newSum > 0:                    
                        newSum = newSum - 1
                    
            #else if the user clicks anywhere BUT column 4, add number   
            else:
                newNum = newNum + 1                  
                newSum = newSum + 1

            #prepare the numbers for output    
            if newNum == 0:
                newNum = ""
            else:
                newNum = str(newNum)
                
            if newSum == 0:
                newSum = ""
            else:
                newSum = str(newSum)
            #Output    
            self.parent().setText(3,newSum)
            self.setText(3,newNum)
                      
    def updateOrderDetails(self):
        # If there is already a garment tree we want to clear out the old lists we do this to catch in an error
        # in case this function get's called before there is a tree build or grown, ha ha.
        if self.garmentTree:
            lstItems = []
            # Open a iterator to iterate through the tree (again) and build a list of lists of items in the tree to be added to the table.
            itOrders = QTreeWidgetItemIterator(self.garmentTree)
            while itOrders.value():
                if itOrders.value() != None:
                    # Below makes sure that there are values for both the price and the quantity.
                    if itOrders.value().text(3) != "" and itOrders.value().text(2) != "":
                        # This makes sure that we are at the correct level in the tree so we do try to add what shouldn't be added
                        if itOrders.value().parent().parent().parent() != None:
                            txtItems = []
                            txtItems = [itOrders.value().parent().parent().parent().text(0), itOrders.value().parent().parent().text(0), 
                                        itOrders.value().parent().text(0), itOrders.value().text(0), itOrders.value().text(1), 
                                        str(format(float(itOrders.value().text(2)) * float(itOrders.value().text(3)), '.2f')), 
                                        itOrders.value().text(3)]
                            lstItems.append(txtItems)
                itOrders += 1
            # A check to make sure the iterator picked up items from the list.
            if len(lstItems) > 0:
                # Build the table to hold the information from the tree.
                CSRWidgets.tblOrderDetails.setRowCount(len(lstItems))
                CSRWidgets.tblOrderDetails.setColumnCount(7)
                CSRWidgets.tblOrderDetails.setAlternatingRowColors(True)
                lstHeader = ["Name", "Design", "Category", "Type", "Size", "Price", "Qty" ]     
                CSRWidgets.tblOrderDetails.setHorizontalHeaderLabels(lstHeader)
                #CSRWidgets.tblOrderDetails.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                CSRWidgets.tblOrderDetails.setWordWrap(False)
                # Another check to make sure the list is there and has data, then we go through it and add data to the table.
                if lstItems:
                    for i, row in enumerate(lstItems):
                        for j, col in enumerate(row):
                            item = QTableWidgetItem(col)
                            item.setFlags(Qt.ItemIsEditable)
                            CSRWidgets.tblOrderDetails.setItem(i, j, item)      
                    
                    CSRWidgets.tblOrderDetails.resizeColumnsToContents()  
                      
                    #self.vBox.addWidget(CSRWidgets.tblOrderDetails)
                    CSRWidgets.tblOrderDetails.show() 
                    testBox = CSRWidgets.totalBox(self)
                    self.winGrid.addWidget(testBox, 2, 1, 1, 1)
                    #print("hit update orders")  
            else:
                CSRWidgets.tblOrderDetails.hide()        
   
    def getCustomerName(self, sku_code = None):
        #Grabs the last var2 that was used.
        if self.var2 == None and self.lblVar2 != None:
            self.var2 = self.lblVar2.text()
        #var2 = mysql_db.getSecondVar(self, sku_code)
        if not self.var1:
            var1 = mysql_db.getFirstVar(self, sku_code)
            inVar1, ok = QInputDialog.getText(self, "Enter "+var1, "Please Enter "+var1+":")
            if ok:
                self.lblVar1.setText(var1)
                self.lblTxtVar1.setText(inVar1)
                self.orderVars = inVar1
                var2 = mysql_db.getSecondVar(self, sku_code)
                if not var2:
                    self.var2 = None
                    self.lblVar2.hide()
                    self.lblTxtVar2.hide()
                    QApplication.instance().processEvents()               
                    self.orderVars = self.lblTxtVar1.text()                    
                else:
                    inVar2, ok = QInputDialog.getText(self, "Enter "+var2, "Please Enter " +var2+ ":")
                    if ok:
                        self.lblVar2.setText(var2)
                        self.lblTxtVar2.setText(inVar2)
                        self.var2 = inVar2
                        self.orderVars = self.orderVars + " :: " + inVar2
        elif self.var1 and not self.var2:
            var2 = mysql_db.getSecondVar(self, sku_code)
            if var2:
                inVar2, ok = QInputDialog.getText(self, "Enter "+var2, "Please Enter " +var2+ ":")
                if ok:
                    self.lblVar2.setText(var2)
                    self.lblTxtVar2.setText(inVar2)
                    self.var2 = inVar2
                    self.orderVars = self.orderVars + " :: " + inVar2
        elif self.var1 and self.var2:
            var1 = mysql_db.getFirstVar(self, sku_code)
            var2 = mysql_db.getSecondVar(self, sku_code)
            if not var2:
                self.var2 = None
                self.lblVar2.hide()
                self.lblTxtVar2.hide()
                QApplication.instance().processEvents()
                if self.lblVar1.text() == var1:               
                    self.orderVars = self.lblTxtVar1.text()
                else:
                    inVar1, ok = QInputDialog.getText(self, "Enter "+var1+":", "Please Enter "+var1+":")
                    if ok and inVar1:
                        self.lblVar1.setText(var1)
                        self.lblTxtVar1.setText(inVar1)
                        self.orderVars = inVar1
            else:
                if self.lblVar1.text() == var1:               
                    self.orderVars = self.lblTxtVar1.text()
                else:
                    inVar1, ok = QInputDialog.getText(self, "Enter "+var1+":", "Please Enter "+var1+":")
                    if ok and inVar1:
                        self.lblVar1.setText(var1)
                        self.lblTxtVar1.setText(inVar1)
                        self.orderVars = inVar1
                if self.lblVar2.text() == var2:
                    self.orderVars = self.orderVars + " :: " + self.lblTxtVar2.text()
                else:
                    inVar2, ok = QInputDialog.getText(self, "Enter "+var2+":", "Please Enter "+var2+":")
                    if ok and inVar2:
                        self.lblVar2.setText(var2)
                        self.lblTxtVar2.setText(inVar2)
                        self.orderVars = self.orderVars + " :: " + inVar2
                                        
                #self.var2 = self.lblTxtVar2.text()
                #self.var1 = self.lblTxtVar1.text()
                #self.orderVars = self.var1 + " :: " + self.var2
                
        
    def updateNameDesign(self):
        treeName = self.sender()
        CSRWidgets.getTreeVars(self, treeName)
        
        if str(treeName.objectName()) == 'garmentTree':
            #If top level (Name) node is selected.
            if treeName.currentItem().parent() == None:
                var = treeName.currentItem().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.lblTxtVar1.setText(var[0])
                    self.lblTxtVar2.setText(var[1])
                else: 
                    self.lblTxtVar1.setText(var)
                    self.lblVar2.hide()
                    self.lblTxtVar2.hide()
                skuCode = treeName.currentItem().child(0).text(0)
                self.orderVars = (treeName.currentItem().text(0))
            #Fourth tree node selected (sizes)
            elif treeName.currentItem().child(0) == None:
                var = treeName.currentItem().parent().parent().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.lblTxtVar1.setText(var[0]) 
                    self.lblTxtVar2.setText(var[1])
                else:
                    self.lblTxtVar1.setText(var)
                    self.lblVar2.hide()
                    self.lblTxtVar2.hide()                    
                skuCode = treeName.currentItem().parent().parent().text(0)
                self.orderVars = (treeName.currentItem().parent().parent().parent().text(0))               
            #Second tree node is selected (Sku)
            elif treeName.currentItem().child(0).child(0) != None and treeName.currentItem().parent() != None:
                var = treeName.currentItem().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.lblTxtVar1.setText(var[0])
                    self.lblTxtVar2.setText(var[1])
                else:
                    self.lblTxtVar1.setText(var)
                    self.lblVar2.hide()
                    self.lblTxtVar2.hide()                   
                skuCode = treeName.currentItem().text(0)
                self.orderVars = (treeName.currentItem().parent().text(0))
            #Third tree node selected (garment, T-Shirts)
            elif treeName.currentItem().child(0) != None and treeName.currentItem().parent().parent() != None:
                var = treeName.currentItem().parent().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.lblTxtVar1.setText(var[0])
                    self.lblTxtVar2.setText(var[1])
                else:
                    self.lblTxtVar1.setText(var)
                    self.lblVar2.hide()
                    self.lblTxtVar2.hide                    
                skuCode = treeName.currentItem().parent().text(0)    
                self.orderVars = (treeName.currentItem().parent().parent().text(0))
        self.lblSkuName.setText(skuCode)
        CSRWidgets.loadDesignItem(self, skuCode)         
        #CSRWidgets.updateOrderDetails(self)    
        
    def getTreeVars(self, garmTree):
        treeName = garmTree
        if str(treeName.objectName()) == 'garmentTree':
            #If top level (Name) node is selected.
            if treeName.currentItem().parent() == None:
                var = treeName.currentItem().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.var1 = var[0]
                    self.var2 = var[1]
                else: 
                    self.var1 = var
                    self.var2 = None
            #Fourth tree node selected (sizes)
            elif treeName.currentItem().child(0) == None:
                var = treeName.currentItem().parent().parent().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.var1 = var[0] 
                    self.var2 = var[1]
                else:
                    self.var1 = var
                    self.var2 = None
            #Second tree node is selected (Sku)
            elif treeName.currentItem().child(0).child(0) != None and treeName.currentItem().parent() != None:
                var = treeName.currentItem().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.var1 = var[0]
                    self.var2 = var[1]
                else:
                    self.var1 = var
                    self.var2 = None
            #Third tree node selected (garment, T-Shirts)
            elif treeName.currentItem().child(0) != None and treeName.currentItem().parent().parent() != None:
                var = treeName.currentItem().parent().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.var1 = var[0]
                    self.var2 = var[1]
                else:
                    self.var1 = var
                    self.var2 = None
    
        return self.var1, self.var2
    
    def changeCustName(self):
        sku_code = self.lblSkuName.text()
        self.var1 = mysql_db.getFirstVar(self, sku_code)
        self.var2 = mysql_db.getSecondVar(self, sku_code)
        
        inVar1, ok = QInputDialog.getText(self, "Enter "+self.var1, "Please enter "+self.var1+":")
        if ok and inVar1:
            self.orderVars = inVar1
            self.lblTxtVar1.setText(inVar1)
            self.lblVar1.setText(self.var1)
            
            if self.var2:
                inVar2, ok = QInputDialog.getText(self, "Enter "+self.var2, "Please enter "+self.var2+":")
                if ok and inVar2:
                    self.orderVars = self.orderVars +" :: "+ inVar2
                    self.lblTxtVar2.setText(inVar2)
                    self.lblVar2.setText(self.var2)