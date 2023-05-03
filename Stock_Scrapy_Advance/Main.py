import os.path
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QColor, QBrush
from PyQt5.QtWidgets import QTableWidgetItem
from Stock_Scrapy import StockScrapy


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1109, 520)
        self.tW_StockInformation = QtWidgets.QTableWidget(Form)
        self.tW_StockInformation.setGeometry(QtCore.QRect(10, 50, 1091, 461))
        self.tW_StockInformation.setObjectName("tW_StockInformation")
        self.tW_StockInformation.setColumnCount(0)
        self.tW_StockInformation.setRowCount(0)
        self.btn_Scrapy = QtWidgets.QPushButton(Form)
        self.btn_Scrapy.setGeometry(QtCore.QRect(10, 10, 121, 31))
        self.btn_Scrapy.setObjectName("btn_Scrapy")
        #button典籍事件
        self.btn_Scrapy.clicked.connect(self.show_stock_information)

        self.txt_Url = QtWidgets.QTextEdit(Form)
        self.txt_Url.setGeometry(QtCore.QRect(190, 10, 721, 31))
        self.txt_Url.setObjectName("txt_Url")
        self.txt_Url.setText("https://tw.stock.yahoo.com/world-indices/")
        self.lbl_Url = QtWidgets.QLabel(Form)
        self.lbl_Url.setGeometry(QtCore.QRect(140, 20, 58, 15))
        self.lbl_Url.setObjectName("lbl_Url")
        self.btn_OutputCSV = QtWidgets.QPushButton(Form)
        self.btn_OutputCSV.setGeometry(QtCore.QRect(920, 10, 121, 28))
        self.btn_OutputCSV.setObjectName("btn_OutputCSV")
        #輸出文檔
        self.btn_OutputCSV.clicked.connect(self.Output_Stock_to_CSV)
        self.btn_Folder = QtWidgets.QPushButton(Form)
        self.btn_Folder.setGeometry(QtCore.QRect(1050, 10, 51, 28))
        self.btn_Folder.setText("")
        self.btn_Folder.setObjectName("btn_Folder")
        #self.btn_Folder.setWindowIcon(QtGui.QIcon("./images/folder.png"))
        self.btn_Folder.setStyleSheet("QPushButton{border-image: url(./images/folder.png)}")
        self.btn_Folder.clicked.connect(self.Open_Output_Folder)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        #以下為私有變數
        self.__Title =[]
        self.__Datas = []
        self.__OutputFolder_Path = "Output_Folder"

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_Scrapy.setText(_translate("Form", "取得股票資料"))
        self.lbl_Url.setText(_translate("Form", "網址:"))
        self.btn_OutputCSV.setText(_translate("Form", "輸出文檔"))

    #顯示股票資訊
    def show_stock_information(self):
        self.__Title,self.__Datas = StockScrapy(self.txt_Url.toPlainText()).scrapy_stock_information()
        self.tW_StockInformation.setColumnCount(len(self.__Title))
        self.tW_StockInformation.setRowCount(len(self.__Datas))
        self.tW_StockInformation.setHorizontalHeaderLabels(self.__Title)
        for i in range(len(self.__Datas)):
            for j in range(len(self.__Datas[i].values())):
                a = self.__Datas[i].values()
                b = list(a)
                newItem = ''
                if j== len(self.__Datas[i].values())-1:
                    if b[j] == '^':
                        newItem = QTableWidgetItem(QIcon("./images/increase.png"),'')
                    elif b[j] == 'v':
                        newItem = QTableWidgetItem(QIcon("./images/decrease.png"),'')
                else:
                    newItem = QTableWidgetItem(b[j])
                    if j==0:
                        newItem.setForeground(QBrush(QColor(0, 0, 255)))
                    elif j >=2 and j <= 4 :
                        if  b[len(self.__Datas[i].values())-1] == '^':
                            newItem.setForeground(QBrush(QColor(255,51,58)))
                        else:
                            newItem.setForeground(QBrush(QColor(0,171 ,94)))
                self.tW_StockInformation.setItem(i,j,newItem)

    #輸出股票文檔
    def Output_Stock_to_CSV(self):
        StockScrapy(self.txt_Url.toPlainText()).save_as_csv_report(self.__OutputFolder_Path,self.__Title,self.__Datas)

    #開啟輸出資料夾
    def Open_Output_Folder(self):
        if not os.path.exists(self.__OutputFolder_Path):
            os.mkdir(self.__OutputFolder_Path)
        os.startfile(self.__OutputFolder_Path)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    Form.setWindowTitle('Yahoo!股市')
    Form.setWindowIcon(QtGui.QIcon("./images/yahoo.png"))
    sys.exit(app.exec_())

