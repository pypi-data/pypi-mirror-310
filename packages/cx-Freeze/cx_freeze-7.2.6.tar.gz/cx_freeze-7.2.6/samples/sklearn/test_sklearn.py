"""A simple script to demonstrate PyQt5."""

from __future__ import annotations

import sys
import sklearn
from sklearn import neural_network
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(100,70)
        button.clicked.connect(self.on_click)
        self.show()
    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        from sklearn import datasets
        from sklearn.svm import SVC
        iris = datasets.load_iris()
        clf = sklearn.neural_network.MLPClassifier()
        clf.fit(iris.data, iris.target)
        list(clf.predict(iris.data[:3]))
        clf.fit(iris.data, iris.target_names[iris.target])
        print(list(clf.predict(iris.data[:3])))
        scores = sklearn.model_selection.cross_val_score(clf, iris.data, iris.target_names[iris.target], cv=50, n_jobs=-1)
        print("Scores:")
        print(scores)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    