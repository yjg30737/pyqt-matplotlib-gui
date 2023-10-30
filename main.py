import os, sys

from PyQt5.QtGui import QFont

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QComboBox, QVBoxLayout, QWidget, QApplication
from PyQt5.QtCore import Qt, QCoreApplication
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('PyQt Matplotlib Window Example')

        self.__df = pd.read_csv('pima-indians-diabetes3.csv')

        columnCmbBox = QComboBox()
        columnCmbBox.addItems(self.__df.columns)
        columnCmbBox.currentIndexChanged.connect(self.updatePlot)

        self.__figure = plt.figure(figsize=(8, 8))
        self.__axis = self.__figure.add_subplot(111)

        canvas = FigureCanvas(self.__figure)

        lay = QVBoxLayout()
        lay.addWidget(columnCmbBox)
        lay.addWidget(canvas)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

        # 처음 그림을 그릴 때 기본적으로 첫 번째 컬럼을 사용
        self.__setHist(self.__df.columns[0])

    def updatePlot(self):
        selected_column = self.sender().currentText()
        self.__setHist(selected_column)

    def __setHist(self, column_name):
        # 이전 그림 지우기
        self.__axis.clear()

        # 선택된 컬럼을 기반으로 히스토그램 그리기
        self.__axis.hist(
            x=[self.__df[self.__df.diabetes == 0][column_name], self.__df[self.__df.diabetes == 1][column_name]],
            bins=30, histtype='barstacked', label=['normal', 'diabetes'])

        self.__axis.legend()
        self.__figure.canvas.draw()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
