from PyQt5.QtCore import QFile, Qt, QTextStream
from PyQt5.QtGui import (QIcon, QKeySequence)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QDockWidget,
        QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit, QFrame)

from csrLogic import CSRwidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        frmDesign = QFrame()
        frmDesign.setStyleSheet("background-color: rgb(255, 255, 255);")
        frmDesign.setLayout(CSRwidgets.createSaleButtons(self))
           
        self.textEdit = QTextEdit()
        self.setCentralWidget(frmDesign)
        
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()

        self.setWindowTitle("CSR proving ground")

            
    def print_(self):
        document = self.textEdit.document()
        printer = QPrinter()

        dlg = QPrintDialog(printer, self)
        if dlg.exec_() != QDialog.Accepted:
            return

        document.print_(printer)

        self.statusBar().showMessage("Ready", 2000)

    def save(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "HTML (*.html *.htm)")
        if not filename:
            return

        file = QFile(filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Dock Widgets",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out << self.textEdit.toHtml()
        QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Saved '%s'" % filename, 2000)



    def about(self):
        QMessageBox.about(self, "About Dock Widgets",
                "The <b>Dock Widgets</b> example demonstrates how to use "
                "Qt's dock widgets. You can enter your own text, click a "
                "customer to add a customer name and address, and click "
                "standard paragraphs to add them.")

    def createActions(self):

        self.saveAct = QAction(QIcon(':/images/save.png'), "&Save...", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the current form letter", triggered=self.save)

        self.printAct = QAction(QIcon(':/images/print.png'), "&Print...", self,
                shortcut=QKeySequence.Print,
                statusTip="Print the current form letter",
                triggered=self.print_)

        self.undoAct = QAction(QIcon(':/images/undo.png'), "&Undo", self,
                shortcut=QKeySequence.Undo,
                statusTip="Undo the last editing action")

        self.quitAct = QAction(QIcon('icon/exit.png'), "&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.quitAct)
        self.fileToolBar.addAction(self.printAct)

        self.editToolBar = self.addToolBar("Edit")

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        dock = QDockWidget("Customers", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.customerList = QListWidget(dock)
        self.customerList.addItems((
            "stuff"))
        dock.setWidget(self.customerList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Paragraphs", self)
        self.paragraphsList = QListWidget(dock)
        self.paragraphsList.addItems((
            "more stuff"))
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
