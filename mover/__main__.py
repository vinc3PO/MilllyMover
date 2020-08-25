from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,QLineEdit,
                             QPushButton, QFileDialog, QGroupBox, QHBoxLayout, QDialogButtonBox,)
from mover.qtclasses import MyExtensionWidget, MyMovingThread, MyFileTransfer
import sys
from mover import cli
import os

class Mover(QMainWindow):
    def __init__(self, parent=None):
        super(Mover, self).__init__(parent)

        ### Central Widget ###
        self.setWindowTitle("Milly's file Mover")
        centralWidget = QWidget(self)
        grid = QGridLayout(centralWidget)
        self.setCentralWidget(centralWidget)
        ### Top group box  ###
        grpBoxSRC = QGroupBox()
        grpBoxSRC.setTitle("Source")
        hLayout = QHBoxLayout()
        self.fromLine = QLineEdit()
        self.fromLine.setReadOnly(True)
        self.fromPB = QPushButton("Select Folder")
        hLayout.addWidget(self.fromLine)
        hLayout.addWidget(self.fromPB)
        grpBoxSRC.setLayout(hLayout)
        grid.addWidget(grpBoxSRC, 0, 0)
        ### Mid group box ###
        grpBoxEXT = QGroupBox()
        grpBoxEXT.setTitle("Extension")
        hLayout1 = QHBoxLayout()
        self.myWidget = MyExtensionWidget()
        hLayout1.addWidget(self.myWidget)
        grpBoxEXT.setLayout(hLayout1)
        grid.addWidget(grpBoxEXT, 1, 0)
        ### Lower group box ###
        grpBoxDST = QGroupBox()
        grpBoxDST.setTitle("Destination")
        hLayout2 = QHBoxLayout()
        self.toLine = QLineEdit()
        self.toLine.setReadOnly(True)
        self.toPB = QPushButton("Select Folder")
        self.toPB.setObjectName('To')
        hLayout2.addWidget(self.toLine)
        hLayout2.addWidget(self.toPB)
        grpBoxDST.setLayout(hLayout2)
        grid.addWidget(grpBoxDST, 2, 0)
        ### Buttons ###
        diagBox = QDialogButtonBox(self)
        diagBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        diagBox.accepted.connect(self.submit)
        diagBox.rejected.connect(self.close)
        self.okPB = QPushButton("OK")
        grid.addWidget(diagBox, 3, 0)
        self.grid = grid
        self.fromPB.clicked.connect(self.picker)
        self.toPB.clicked.connect(self.picker)
        self.setMinimumWidth(450)

    @property
    def dst(self):
        if self.toLine.text() != '':
            return self.toLine.text()

    @property
    def fileList(self):
        if not hasattr(self, "_fileList"):
            self._fileList = []
        return self._fileList

    def picker(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.Directory)
        fileDialog.setOption(QFileDialog.ShowDirsOnly)
        if fileDialog.exec_():
            fileNames = fileDialog.selectedFiles()
            if "To" in self.sender().objectName():
                self.toLine.setText(fileNames[0])
            else:
                self.fromLine.setText(fileNames[0])
                self._fileList, extension = cli.findFileinFolder(fileNames[0])
                self.myWidget.fileGrid(extension)

    def fileExtensionPicker(self):
        self.grid.addWidget()

    def submit(self):
        extension = self.myWidget.getExtension()
        cleanList = [path for path in self.fileList if os.path.splitext(path)[1] in extension]
        if self.dst and cleanList:
            fileTransfer = MyFileTransfer(len(cleanList), self)
            thread = MyMovingThread(cleanList, self.dst,  self)
            thread.fileProgress.connect(fileTransfer.updateDialog)
            thread.done.connect(fileTransfer.close)
            thread.start()
            fileTransfer.show()


def main():
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    ex = Mover()
    ex.show()
    app.exec_()

if __name__=='__main__':
    main()