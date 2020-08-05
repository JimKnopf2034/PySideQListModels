import sys
import os
from os.path import join, dirname, abspath
from PySide2.QtCore import QStringListModel, QObject, Slot
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine


class Bridge(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self.model = QStringListModel(['a','b'])
    
    @Slot(result=bool)
    def add_one(self):
        print("Add Element to List")
        current_index = self.model.createIndex(self.model.rowCount(),0)
        self.model.insertRow(0, current_index)
        current_index = self.model.createIndex(0,0)
        self.model.setData(current_index, "FooBar")
        return True


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    bridge = Bridge()

    context = engine.rootContext()
    context.setContextProperty("bridge", bridge)
    context.setContextProperty("stringModel", bridge.model)
    qmlFile = join(dirname(__file__), 'main.qml')
    engine.load(abspath(qmlFile))

    # stop if qml does not do the job
    if not engine.rootObjects():
        sys.exit(-1)

    app.exec_()
