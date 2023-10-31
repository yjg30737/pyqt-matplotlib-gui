import os, sys

from PyQt5.QtGui import QFont

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QComboBox, QVBoxLayout, QWidget, QApplication, QScrollArea
from PyQt5.QtCore import Qt, QCoreApplication
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

        self.__figure1 = plt.figure(figsize=(8, 8))
        self.__figure2 = plt.figure(figsize=(8, 8))

        self.__axis1 = self.__figure1.add_subplot(111)

        canvas1 = FigureCanvas(self.__figure1)
        canvas2 = FigureCanvas(self.__figure2)

        lay = QVBoxLayout()
        lay.addWidget(canvas1)
        lay.addWidget(canvas2)
        graphScrollWidget = QWidget()
        graphScrollWidget.setLayout(lay)

        graphScrollArea = QScrollArea()
        graphScrollArea.setWidget(graphScrollWidget)

        lay = QVBoxLayout()
        lay.addWidget(columnCmbBox)
        lay.addWidget(graphScrollArea)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

        self.__setHist(self.__df.columns[0])
        self.__setSeaborn()

    def updatePlot(self):
        selected_column = self.sender().currentText()
        self.__setHist(selected_column)

    def __setSeaborn(self):
        colormap = plt.cm.gist_heat
        plt.title('Heatmap')
        sns.heatmap(self.__df.corr(), linewidths=0.1, vmax=0.5, cmap=colormap, linecolor='white', annot=True)
        self.__figure2.canvas.draw()
        
    def __setHist(self, column_name):
        self.__axis1.clear()

        context = f'Correlation between diabetes and {column_name}'

        self.__axis1.set_title(context)
        self.__axis1.hist(
            x=[self.__df[self.__df.diabetes == 0][column_name], self.__df[self.__df.diabetes == 1][column_name]],
            bins=30, histtype='barstacked', label=['normal', 'diabetes'])

        self.__axis1.legend()
        self.__figure1.canvas.draw()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
