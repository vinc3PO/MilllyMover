from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QVBoxLayout, QCheckBox,
                             QDialog, QProgressBar)
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import shutil
import os
import time


class MyMovingThread(QThread):
    fileProgress = pyqtSignal(int)
    done = pyqtSignal(int)

    def __init__(self, fileList, dst, parent=None):
        QThread.__init__(self, parent)
        self.fileList = fileList
        self.dst = dst

    def run(self):
        i = 0
        for path in self.fileList:
            pathDst = os.path.join(self.dst, os.path.basename(path))
            i += 1
            self.fileProgress.emit(i)
            while os.path.exists(pathDst):
                pathDst = os.path.splitext(pathDst)[0] + f"(1)" + os.path.splitext(pathDst)[1]
            shutil.copy2(path, pathDst)
            if i == len(self.fileList):
                time.sleep(2)
        self.done.emit(int)



class MyFileTransfer(QDialog):
    def __init__(self, total, parent=None):
        super(MyFileTransfer, self).__init__(parent)
        self.total = total
        self.setWindowTitle("Copy Files")
        vLayout = QVBoxLayout()
        self.moveLabel = QLabel("Copy ... to ...")
        vLayout.addWidget(self.moveLabel)
        self.pgBar = QProgressBar()
        self.pgBar.setMaximum(self.total)
        vLayout.addWidget(self.pgBar)
        self.setLayout(vLayout)
        self.setMinimumWidth(250)


    def updateDialog(self, iter):
        self.moveLabel.setText(f"Copy {iter} out of {self.total}")
        self.pgBar.setValue(iter)



class MyExtensionWidget(QWidget):
    def __init__(self, parent=None):
        super(MyExtensionWidget, self).__init__(parent)
        self.grid = QGridLayout()
        self.colCount = 4
        self.setLayout(self.grid)

    def fileGrid(self, extensions):
        self.clearGrid()
        i = 0
        for ext in extensions:
            myCheck = QCheckBox()
            myCheck.setText(str(ext))
            self.grid.addWidget(myCheck, int(i/4), i % 4)
            i +=1

    def clearGrid(self):
        for i in reversed(range(self.grid.count())):
            try:
                self.grid.itemAt(i).widget().setParent(None)
            except:
                print(sys.exc_info())
                pass
        self.repaint()

    def getExtension(self):
        extension = []
        for i in reversed(range(self.grid.count())):
            try:
                if self.grid.itemAt(i).widget().checkState() == 2:
                    extension.append(self.grid.itemAt(i).widget().text())
            except:
                print(sys.exc_info())
                pass
        return extension
