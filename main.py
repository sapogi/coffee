import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from mainwindow import Ui_MainWindow
from addEditCoffeeForm import Ui_Form


class addEditCoffeeForm(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.cancel)

    def save(self):
        if self.lineEdit.text():

            id = int(self.lineEdit.text())
            sort = int(self.lineEdit_2.text())
            roast = int(self.lineEdit_3.text())
            form = self.lineEdit_4.text()
            taste = self.lineEdit_5.text()
            price = self.lineEdit_6.text()
            size = int(self.lineEdit_7.text())
            print(sort, roast, form, taste, price, size, id)
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()

            res = cur.execute("""UPDATE coffee
                                 SET (sort, roast, form, taste, price, size) = (?, ?, ?, ?, ?, ?)
                                 WHERE id = ?""", (sort, roast, form, taste, price, size, id)).fetchall()
            con.commit()
            self.close()
        else:
            sort = int(self.lineEdit_2.text())
            roast = int(self.lineEdit_3.text())
            form = self.lineEdit_4.text()
            taste = self.lineEdit_5.text()
            price = self.lineEdit_6.text()
            size = int(self.lineEdit_7.text())
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            res = cur.execute("""INSERT INTO coffee(sort, roast, form, taste, price, size) 
                                 VALUES(?, ?, ?, ?, ?, ?)""", (sort, roast, form, taste, price, size)).fetchall()
            con.commit()
            self.close()

    def cancel(self):
        self.close()


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.initUI)
        self.con = sqlite3.connect('data/coffee.sqlite')
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
            for value in row_data:
                item = QStandardItem(str(value))
                tableitem.append(item)
            model.insertRow(row_number, tableitem)

        self.view.setModel(model)
        self.setWindowTitle('кофе')

    def run(self):
        self.widget = addEditCoffeeForm(self)
        self.widget.show()
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
