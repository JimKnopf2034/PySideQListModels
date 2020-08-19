import sys
import os
from os.path import join, dirname, abspath
from PySide2.QtCore import QStringListModel, QObject, Slot, QAbstractListModel, Qt
from PySide2.QtCore import QModelIndex
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine


class Bridge(QObject):
    """
    Bridge
    ======

    The bridge is the QObject that manages communication between python code and QML
    frontend.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.model = MyListModel(['a','b'])
    
    @Slot(result=bool)
    def add_one(self):
        current_index = self.model.createIndex(self.model.rowCount(),0)
        self.model.insertRow(0, current_index)
        current_index = self.model.createIndex(0,0)
        self.model.setData(current_index, "FooBar")
        return True


class MyListModel(QAbstractListModel):
    """
    A abstract list model that implements the minimum amount of functions
    neccessary to use the model with a QML QtQuick ComboBox.
    """
    def __init__(self, data, parent=None):
        super().__init__()
        self.parent = parent
        self.lst = ['a','c']
    
    def rowCount(self, idx: QModelIndex=None) -> int:
        return len(self.lst)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole:
            return self.lst[index.row()]
        
        if role == Qt.UserRole:
            return 99
        return

    def insertRow(self, row: int, index: QModelIndex=QModelIndex()) -> bool:
        if row < 0 or row > len(self.lst):
            return False

        self.beginInsertRows(QModelIndex(), row, row+1-1)
        self.lst.insert(row, "Lorem Ipsum")
        self.endInsertRows()
        return True

    def setData(self, index: QModelIndex, value: str, role: int=Qt.DisplayRole) -> bool:
        if index.row() >=0 and index.row() < len(self.lst):
            if not role == Qt.DisplayRole or role == Qt.EditRole:
                return False
            self.lst[index.row()] = value
            self.dataChanged.emit(index, index, [Qt.EditRole | Qt.DisplayRole])
            return True
        return False

    def setNewList(self, lst: list=[]):
        self.beginResetModel()
        self.lst = lst
        self.endResetModel()
        return

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
