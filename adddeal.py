import os

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import sqlite3
from PIL import Image

# main.py is the parent python file while add deal.py is thr child python file


con=sqlite3.connect("dealsfinder.db")
cur=con.cursor()

defaultimg="store.png"


class AddDeal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add deal")
        self.setWindowIcon(QIcon("Icons/icon.ico"))
        self.setGeometry(450, 150, 350, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##########widgets of top layout####3
        self.addproductImg=QLabel()
        self.img=QPixmap('Icons/addproduct.png')
        self.addproductImg.setPixmap(self.img)
        self.titletext=QLabel("Add product")
        ######## widgets of bottom layout#######
        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Enter the name of product ")
        self.manufacturerEntry=QLineEdit()
        self.manufacturerEntry.setPlaceholderText("Enter nameof manufacturer")
        self.priceEntry=QLineEdit()
        self.priceEntry.setPlaceholderText("Enter price of product")
        self.quotaEntry=QLineEdit()
        self.quotaEntry.setPlaceholderText("Enter the product quota")

        self.uploadbtn=QPushButton("Upload")
        self.uploadbtn.clicked.connect(self.uploadimg)
        self.submitbtn=QPushButton("submit")
        self.submitbtn.clicked.connect(self.addproduct)

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QHBoxLayout()
        self.bottomLayout=QFormLayout()
        # creating two frames , frames are widgets
        self.topframe=QFrame()
        self.bottomFrame=QFrame()
        ###########add widget #####
        ####widgets of toplayouts######
        self.topLayout.addWidget(self.addproductImg)
        self.topLayout.addWidget(self.titletext)
        self.topframe.setLayout(self.topLayout)
        ###########widgets of form layout########
        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer: "), self.manufacturerEntry)
        self.bottomLayout.addRow(QLabel("Price: "), self.priceEntry)
        self.bottomLayout.addRow(QLabel("Quota: "), self.quotaEntry)
        self.bottomLayout.addRow(QLabel("upload: "), self.uploadbtn)
        self.bottomLayout.addRow(QLabel("submit: "), self.submitbtn)

        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topframe)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def uploadimg(self):
        global defaultimg
        size=(256, 256)
        self.filename, ok=QFileDialog.getOpenFileName(self, "Upload Image", "", "Image File(*.jpg *.jpg)")
        if ok:
            print(self.filename)
            defaultimg=os.path.basename(self.filename)
            print(defaultimg)
            img=Image.open(self.filename)
            img=img.resize(size)
            img.save("img/{0}".format(defaultimg))

    def addproduct(self):
        global defaultimg
        name=self.nameEntry.text()
        manufacturer=self.manufacturerEntry.text()
        price=self.priceEntry.text()
        quota=self.quotaEntry.text()

        if (name and manufacturer and price and quota) != "":  # checking if all the fields are filled
            try:
                query=("INSERT INTO 'products' (product_name, product_manufacturer, product_price, product_quota, "
                       "product_img) VALUES(?,?,?,?,?)")
                cur.execute(query, (name, manufacturer, price, quota, defaultimg))
                con.commit()  # save the changes in database

                QMessageBox.information(self, "information", " product added!", QMessageBox.StandardButton.Yes,
                                        QMessageBox.StandardButton.No)
            except:
                QMessageBox.information(self, "information", " product not added!", QMessageBox.StandardButton.Yes,
                                        QMessageBox.StandardButton.No)

        else:
            QMessageBox.information(self, "information", " fields can't be empty", QMessageBox.StandardButton.Yes,
                                    QMessageBox.StandardButton.No)
