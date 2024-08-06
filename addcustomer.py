from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import sqlite3

con=sqlite3.connect("dealsfinder.db")
cur=con.cursor()


class AddCustomer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add customer")
        self.setWindowIcon(QIcon("Icons/icon.ico"))
        self.setGeometry(450, 150, 350, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()


    def widgets(self):
        #############widgets of top layout####
        self.addcustomerImg = QLabel()
        self.img = QPixmap("Icons/addmember.png")
        self.addcustomerImg.setPixmap(self.img)
        ##aligining the customer img and text to center
        self.addcustomerImg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titletext = QLabel("Add customer")
        self.titletext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ######### widgets of bottom layouts ########
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter name of customer")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setPlaceholderText("Enter surname of customer")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter phone number ")
        self.submitbtn = QPushButton("Submit")
        self.submitbtn.clicked.connect(self.addcustomer)

    def layouts(self):
        self.mainlayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        ##### add widgets #######
        self.topLayout.addWidget(self.titletext)
        self.topLayout.addWidget(self.addcustomerImg)
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("surname: "), self.surnameEntry)
        self.bottomLayout.addRow(QLabel("phone: "), self.phoneEntry)
        self.bottomLayout.addRow(QLabel(""), self.submitbtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainlayout.addWidget(self.topFrame)
        self.mainlayout.addWidget(self.bottomFrame)

        # below code is important it helps the mainlayout(which contains all layouts and widgets) to be displayed on window
        self.setLayout(self.mainlayout)


    def addcustomer(self):
    #getting values from customer entries
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()

        if(name and surname and phone)!="":
            try:
                query = "INSERT INTO 'customers' (customer_name, customer_surname, customer_phonenumber) VALUES(?,?,?)"
                cur.execute(query,(name, surname, phone))
                con.commit()
                QMessageBox.information(self, "added customer"," INFO", QMessageBox.StandardButton.Yes)
                #setting it back to empty
                self.nameEntry.setText("")
                self.surnameEntry.setText("")
                self.phoneEntry.setText("")

            except:
                QMessageBox.information(self, " not added customer", "INFO", QMessageBox.StandardButton.No)

        else:
            QMessageBox.information(self, " fields cannot be empty", "INFO", QMessageBox.StandardButton.Yes)