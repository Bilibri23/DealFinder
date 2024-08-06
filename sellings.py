from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import sqlite3

con=sqlite3.connect("dealsfinder.db")
cur=con.cursor()
default_img="store.png"


class sellProducts(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sell product")
        self.setWindowIcon(QIcon("Icons/icon.ico"))
        self.setGeometry(450, 150, 350, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ######### top widgets ###########
        self.sellproductimg=QLabel()
        self.img=QPixmap("Icons/shop.png")
        self.sellproductimg.setPixmap(self.img)
        self.sellproductimg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titletext=QLabel("sell product")
        self.titletext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ####### bottom widgets##########
        self.productcombo=QComboBox()
        self.productcombo.currentIndexChanged.connect(self.changecombovalue)
        self.customercombo=QComboBox()
        self.quantitycombo=QComboBox()
        self.submitbtn=QPushButton("Submit")
        self.submitbtn.clicked.connect(self.sellproduct)

        query1="SELECT * FROM  products WHERE  product_availability = ?"
        products=cur.execute(query1, ('Available',)).fetchall()
        query2="SELECT customer_id, customer_name FROM customers"
        customers=cur.execute(query2).fetchall()

        quantity=products[0][4]

        for product in products:
            self.productcombo.addItem(product[1], product[0])

        for customer in customers:
            self.customercombo.addItem(customer[1], customer[0])

        for i in range(1, quantity + 1):
            self.quantitycombo.addItem(str(i))

    def layouts(self):
        self.mainlayout=QVBoxLayout()
        self.toplayout=QVBoxLayout()
        self.bottomlayout=QFormLayout()
        self.topframe=QFrame()
        self.bottomframe=QFrame()
        #####adding widget to layout#########
        self.toplayout.addWidget(self.titletext)
        self.toplayout.addWidget(self.sellproductimg)
        self.topframe.setLayout(self.toplayout)

        self.bottomlayout.addRow(QLabel("Product"), self.productcombo)
        self.bottomlayout.addRow(QLabel("customer"), self.customercombo)
        self.bottomlayout.addRow(QLabel("quantity"), self.quantitycombo)
        self.bottomlayout.addRow(QLabel(""), self.submitbtn)

        self.bottomframe.setLayout(self.bottomlayout)

        self.mainlayout.addWidget(self.topframe)
        self.mainlayout.addWidget(self.bottomframe)

        self.setLayout(self.mainlayout)

    def changecombovalue(self):
        self.quantitycombo.clear()
        product_id=self.productcombo.currentData()
        # print(product_id)
        query="SELECT product_quota FROM products WHERE product_id = ?"
        quota=cur.execute(query, (product_id,)).fetchone()
        # print(quota)
        for i in range(1, quota[0] + 1):
            self.quantitycombo.addItem(str(i))

    def sellproduct(self):
        global productname,productId,customername,customerId,quantity
        productname=self.productcombo.currentText()
        productId=self.productcombo.currentData()
        customername=self.customercombo.currentText()
        customerId=self.customercombo.currentData()
        quantity=int(self.quantitycombo.currentText())

        self.confirm=ConfirmWindow()  # instance of class we are creating a new window
        self.confirm.show()
        self.close()


class ConfirmWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sell product")
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
        self.sellproductimg=QLabel()
        self.img=QPixmap("Icons/shop.png")
        self.sellproductimg.setPixmap(self.img)
        ##aligining the customer img and text to center
        self.sellproductimg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titletext=QLabel("sell product")
        self.titletext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ######### widgets of bottom layouts ########
        global productname, productId, customername, customerId, quantity
        pricequery = "SELECT product_price FROM products WHERE product_id = ?"
        price = cur.execute(pricequery, (productId,)).fetchone()
        print(price)
        self.amount = quantity * price[0]
        self.productname=QLabel()
        self.productname.setText(productname)
        self.customername=QLabel()
        self.customername.setText(customername)
        self.amountlabel=QLabel()
        self.amountlabel.setText(str(price[0]) + "x" + str(quantity) + "=" + str(self.amount))
        self.confirmbtn=QPushButton("Confirm")
        self.confirmbtn.clicked.connect(self.confirmfunc)

    def layouts(self):
        self.mainlayout=QVBoxLayout()
        self.toplayout=QVBoxLayout()
        self.bottomlayout=QFormLayout()
        self.topframe=QFrame()
        self.bottomframe=QFrame()

        self.toplayout.addWidget(self.titletext)
        self.toplayout.addWidget(self.sellproductimg)
        self.topframe.setLayout(self.toplayout)

        self.bottomlayout.addRow(QLabel("Product name"), self.productname)
        self.bottomlayout.addRow(QLabel("Customer name"), self.customername)
        self.bottomlayout.addRow(QLabel("Amount"), self.amountlabel)
        self.bottomlayout.addRow(QLabel(""), self.confirmbtn)

        self.bottomframe.setLayout(self.bottomlayout)

        self.mainlayout.addWidget(self.topframe)
        self.mainlayout.addWidget(self.bottomframe)

        self.setLayout(self.mainlayout)

    def confirmfunc(self):
        try:
            sellquery ="INSERT INTO 'sellings' (selling_product_id, selling_member_id, selling_quantity, selling_amount) VALUES (?,?,?,?)"
            cur.execute(sellquery, (productId, customerId, quantity, self.amount))
            quotaquery = "SELECT product_quota FROM products WHERE product_id =?"
            self.quota = cur.execute(quotaquery, (productId, )).fetchone()
            print(self.quota)
            con.commit()

            if quantity ==self.quota[0]: # checking if you sold it  out that already
                updatequotaquery ="UPDATE products set product_quota =?, product_availability =?, WHERE product_id = ?"
                cur.execute(updatequotaquery, (0, 'unavailable', productId))
                con.commit()
            else:
                newQuota = (self.quota[0] - quantity)
                updatequotaquery ="UPDATE products set product_quota =? WHERE product_id = ?"
                cur.execute(updatequotaquery, (newQuota, productId))
                con.commit()

            QMessageBox.information(self, "info", "success", QMessageBox.StandardButton.Ok)

        except:
            QMessageBox.information(self, "info", "something went wrong", QMessageBox.StandardButton.Ok)
