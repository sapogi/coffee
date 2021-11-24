import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QWidget, QTableView, QApplication, QMainWindow


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        res = self.cur.execute("""SELECT coffee.id, sorts.name, roast.title, coffee.form, coffee.taste, coffee.price, size.size  FROM coffee
                                  LEFT JOIN sorts ON sorts.id = coffee.sort
                                  LEFT JOIN roast ON roast.id = coffee.roast
                                  LEFT JOIN size ON size.id = coffee.size""").fetchall()
        headers = ['id', 'Сорт', 'Обжарка', 'вид', 'вкус', 'цена', 'объем']
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        r = 1
        for row_number, row_data in enumerate(res):
            tableitem = []
            model.insertRow(row_number)
            for value in row_data:
                item = QStandardItem(str(value))
                tableitem.append(item)
            model.insertRow(row_number, tableitem)

        self.view.setModel(model)
        self.setWindowTitle('кофе')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
