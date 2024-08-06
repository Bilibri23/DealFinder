import os.path

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PIL import Image
import sys
import sqlite3

import addcustomer
import adddeal
import sellings

# creating global connections to the database
# the 3rd table in the database is used to link the other two tables
# where from the product and customer id are foreign keeys in there.
con=sqlite3.connect("dealsfinder.db")
cur=con.cursor()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deals finder")
        self.setWindowIcon(QIcon("Icons/icon.ico"))
        self.setGeometry(450, 150, 1350, 750)

        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.displayProducts()
        self.displaycustomers()
       # self.getstatistics()

    def toolBar(self):
        self.tb=self.addToolBar("tool bar")
        ###toolbar buttons##
        ###add product##

        self.addProduct=QAction(QIcon('Icons/add.png'), "Add Product", self)
        self.tb.addAction(self.addProduct)
        # when you click on the add product tool abr you want an action to be triggered
        # creating add product window
        self.addProduct.triggered.connect(self.funcAddProduct)
        self.tb.addSeparator()

        #################add customer ###############
        self.customer=QAction(QIcon('Icons/users.png'), "Add customer", self)
        self.tb.addAction(self.customer)
        self.customer.triggered.connect(self.funcaddcustomer)
        self.tb.addSeparator()
        ########sell product ##########
        self.sellproduct=QAction(QIcon('Icons/sell.png'), "sell product", self)
        self.tb.addAction(self.sellproduct)
        self.sellproduct.triggered.connect(self.funcsellproduct)
        self.tb.addSeparator()

    def tabWidget(self):
        # remember that tabs are like main window, so for each tab we create its layouts
        self.tabs=QTabWidget()
        self.tabs.blockSignals(True)
        #self.tabs.currentWidget.connect(self.tabchanged)
        self.setCentralWidget(self.tabs)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()

        self.tabs.addTab(self.tab1, "deal products")
        self.tabs.addTab(self.tab2, "deal customers")
        self.tabs.addTab(self.tab3, "deal statistics")

    def widgets(self):
        #### tab1 widgets ###
        ####addproduct widget###
        ####Mainleft layout widget ####
        self.productTable=QTableWidget()
        self.productTable.setColumnCount(6)
        self.productTable.setColumnHidden(0, True)
        self.productTable.setHorizontalHeaderItem(0, QTableWidgetItem("product id"))
        self.productTable.setHorizontalHeaderItem(1, QTableWidgetItem("product name"))
        self.productTable.setHorizontalHeaderItem(2, QTableWidgetItem("product manufacturer"))
        self.productTable.setHorizontalHeaderItem(3, QTableWidgetItem("product price"))
        self.productTable.setHorizontalHeaderItem(4, QTableWidgetItem("product quota"))
        self.productTable.setHorizontalHeaderItem(5, QTableWidgetItem("product Availability"))
        self.productTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.productTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.productTable.doubleClicked.connect(self.selectedproduct)

        ##########right top wwidget########3

        self.searchtext=QLabel("search")
        self.searchentry=QLineEdit()
        self.searchentry.setPlaceholderText("Search for products")
        self.searchbutton=QPushButton("search")
        self.searchbutton.clicked.connect(self.searchproduct)
        #####33right middle layout widget #####3
        self.allproducts=QRadioButton("All products")
        self.availableproducts=QRadioButton("available products")
        self.notavailableproducts=QRadioButton("not available")
        self.listbutton=QPushButton("list")
        self.listbutton.clicked.connect(self.listProducts)
        ################Tab2 widgets##########
        self.customerstablewidgets=QTableWidget()
        self.customerstablewidgets.setColumnCount(4)
        self.customerstablewidgets.setHorizontalHeaderItem(0, QTableWidgetItem("customer ID"))
        self.customerstablewidgets.setHorizontalHeaderItem(1, QTableWidgetItem("customer Name"))
        self.customerstablewidgets.setHorizontalHeaderItem(2, QTableWidgetItem("customer surname"))
        self.customerstablewidgets.setHorizontalHeaderItem(3, QTableWidgetItem("phone_number"))
        self.customerstablewidgets.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.customerstablewidgets.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.customerstablewidgets.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.customerstablewidgets.doubleClicked.connect(self.selectedcustomer)
        self.customersearchtext=QLabel("search customers")

        self.entrycustomersearch=QLineEdit()
        self.customersearchbutton=QPushButton("search")
        self.customersearchbutton.clicked.connect(self.searchcustomer)

        #########tab 3 widgets####
        self.totalproductlabel = QLabel()
        self.totalcustomerlabel = QLabel()
        self.soldproductslabel = QLabel()
        self.totalamountlabel = QLabel()

    def layouts(self):
        #########tab1 layout############

        self.mainlayout=QHBoxLayout()
        self.mainleftlayout=QVBoxLayout()
        self.mainrightlayout=QVBoxLayout()
        self.righttoplayout=QVBoxLayout()
        self.rightmiddlelayout=QHBoxLayout()
        # to  use settle sheet we use grp box ##
        self.topgroupbox=QGroupBox("search box")
        self.middlegroupbox=QGroupBox("list box")
        # adding the tab1 widget (table widget) to a layout

        ##### left main  layout widget #####

        self.mainleftlayout.addWidget(self.productTable)
        ########right toplayout widget#####
        self.righttoplayout.addWidget(self.searchtext)
        self.righttoplayout.addWidget(self.searchentry)
        self.righttoplayout.addWidget(self.searchbutton)
        self.topgroupbox.setLayout(self.righttoplayout)
        self.rightmiddlelayout.addWidget(self.allproducts)
        self.rightmiddlelayout.addWidget(self.availableproducts)
        self.rightmiddlelayout.addWidget(self.notavailableproducts)
        self.rightmiddlelayout.addWidget(self.listbutton)
        self.middlegroupbox.setLayout(self.rightmiddlelayout)
        self.mainlayout.addLayout(self.mainleftlayout)
        # making it visible, group box is a widget
        self.mainrightlayout.addWidget(self.topgroupbox)
        self.mainrightlayout.addWidget(self.middlegroupbox)
        self.mainlayout.addLayout(self.mainrightlayout)
        self.mainlayout.addLayout(self.mainleftlayout)
        self.tab1.setLayout(self.mainlayout)

        ########### tab2 layouts ##############
        self.customermainlayout=QHBoxLayout()
        self.customerleftlayout=QHBoxLayout()
        self.customerrightlayout=QHBoxLayout()
        self.customerrightgroupbox=QGroupBox("search for customers")

        self.customerrightgroupbox.setContentsMargins(0, 30, 0, 500)

        self.customerrightlayout.addWidget(self.customersearchtext)
        self.customerrightlayout.addWidget(self.entrycustomersearch)
        self.customerrightlayout.addWidget(self.customersearchbutton)
        self.customerrightgroupbox.setLayout(self.customerrightlayout)

        ###  from line above customergroupbox becomes parent and customerright layout becomes child

        self.customerleftlayout.addWidget(self.customerstablewidgets)

        self.customermainlayout.addLayout(self.customerleftlayout, 70)
        self.customermainlayout.addWidget(self.customerrightgroupbox, 30)  # group box is a widget
        self.tab2.setLayout(self.customermainlayout)

        ################tab3 widget###########
        self.statisticsmainlayout = QVBoxLayout()
        self.statisticslayout = QFormLayout()
        self.staristicsgroupbox = QGroupBox("Statistics")
        self.statisticslayout.addRow(QLabel("Total products"), self.totalproductlabel)
        self.statisticslayout.addRow(QLabel("Total customers"), self.totalcustomerlabel)
        self.statisticslayout.addRow(QLabel("sold products"), self.soldproductslabel)
        self.statisticslayout.addRow(QLabel("Total amount"), self.totalamountlabel)
        self.staristicsgroupbox.setLayout(self.statisticslayout)
        self.staristicsgroupbox.setFont(QFont("Arial", 20))
        self.statisticsmainlayout.addWidget(self.staristicsgroupbox)
        self.tab3.setLayout(self.statisticsmainlayout)

        self.tabs.blockSignals(False)


    def funcAddProduct(self):
        self.newProduct=adddeal.AddDeal()  # where adddeal is python file, and addDead() is class name

    def funcaddcustomer(self):
        self.newcustomer=addcustomer.AddCustomer()

    def displayProducts(self):
        self.productTable.setFont(QFont("Times", 12))
        for i in reversed(range(self.productTable.rowCount())):
            self.productTable.removeRow(i)

        query=cur.execute(
            "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_availability FROM products ")

        for row_data in query:
            row_number=self.productTable.rowCount()
            self.productTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # making the table_widget content to be uneditable
        self.productTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def displaycustomers(self):
        self.customerstablewidgets.setFont(QFont("Times", 12))
        for i in reversed(range(self.customerstablewidgets.rowCount())):
            self.customerstablewidgets.removeRow(i)

        query=cur.execute("SELECT * FROM customers")

        for row_data in query:
            row_number=self.customerstablewidgets.rowCount()
            self.customerstablewidgets.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.customerstablewidgets.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # making the table_widget content to be uneditable
        self.customerstablewidgets.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def selectedproduct(self):
        global productId  # can be used in another class
        # getting info about the selected product
        listproduct=[]
        for i in range(0, 6):
            listproduct.append(self.productTable.item(self.productTable.currentRow(), i).text())
        productId=listproduct[0]
        self.display=DisplayProduct()  # creating a new instance of the display product class
        self.display.show()

    def selectedcustomer(self):
        global customerId
        listcustomer=[]
        for i in range(0, 4):
            listcustomer.append(self.customerstablewidgets.item(self.customerstablewidgets.currentRow(), i).text())
        customerId=listcustomer[0]
        self.displaycustomer=DisplayCustomer()
        self.displaycustomer.show()

    def searchproduct(self):
        value = self.searchentry.text()  # taking the  text from your search entry
        if value == "":
            QMessageBox.information(self,"warning","query cant be empty bro!!", QMessageBox.StandardButton.Ok)
        else:
            self.searchentry.setText("")

            query ="SELECT product_id, product_name, product_manufacturer, product_quota, product_availability FROM products WHERE product_name LIKE ? or product_manufacturer LIKE ?"
            result = cur.execute(query,('%'+ value + '%', '%' + value + '%')).fetchall()
            # in sql the % symbol is symbol character used with the LIKE operator to represent any sequence of characters in string
            # we are searching based on the products name or product manufacturer.
            # % sign helps to define the fields we defined in the query, start and end of product name and manufacturer respectively
            # the query retrieves records  from products table where the product name contains the word specified in value
            print(result)
            if result == []:
                QMessageBox.information(self, "info", "not found", QMessageBox.StandardButton.Ok)
            else:
                for i in reversed(range(self.productTable.rowCount())):
                    self.productTable.removeRow(i)


                for row_data in result:
                    row_number = self.productTable.rowCount()
                    self.productTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def searchcustomer(self):
        value = self.entrycustomersearch.text()
        if value =="":
            QMessageBox.information(self, "warning", "search query cant be empty",QMessageBox.StandardButton.Ok)
        else:
            self.entrycustomersearch.setText("")
            query ="SELECT * FROM  customers WHERE customer_name LIKE ? or customer_surname LIKE ?  or customer_phonenumber LIKE ?"
            result = cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()
            if result == []:
                QMessageBox.information(self, "warning", "not found ",QMessageBox.StandardButton.Ok)
            else:
                for i in   reversed(range(self.customerstablewidgets.rowCount())):
                    self.customerstablewidgets.removeRow(i)

                for row_data in result:
                    row_number = self.customerstablewidgets.rowCount()
                    self.customerstablewidgets.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.customerstablewidgets.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def listProducts(self):
        if self.allproducts.isChecked() == True:
            self.displayProducts()
        elif self.availableproducts.isChecked() == True:
            query ="SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_availability FROM products WHERE product_availability = 'Available' "
            products = cur.execute(query).fetchall()
            print(products)

            for i in  reversed(range(self.productTable.rowCount())):
                self.productTable.removeRow(i)

            for row_data in products:
                row_number = self. productTable.rowCount()
                self.productTable.insertRow(row_number)
                for column_number, data in  enumerate(row_data):
                    self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        elif self.notavailableproducts.isChecked()== True:
            query="SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_availability FROM products WHERE product_availability = 'unavailable' "
            products=cur.execute(query).fetchall()
            print(products)

            for i in reversed(range(self.productTable.rowCount())):
                self.productTable.removeRow(i)

            for row_data in products:
                row_number=self.productTable.rowCount()
                self.productTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def funcsellproduct(self):
        self.sell = sellings.sellProducts()

    # def getstatistics(self):
    #     countproducts = cur.execute("SELECT count(product_id) FROM products").fetchall()
    #     countcustomers = cur.execute("SELECT count(customer_id) FROM  customers").fetchall()
    #     soldproducts = cur.execute("SELECT SUM(selling_quantity) FROM sellings").fetchall()

    #     totalamount = cur.execute("SELECT SUM(selling_amount FROM sellings)").fetchall()
    #     totalamount = totalamount[0][0]
    #     soldproducts = soldproducts[0][0]
    #     countcustomers = countcustomers[0][0]
    #     countproducts = countproducts[0][0]

    #     self.totalproductlabel.setText(str(countproducts))
    #     self.totalcustomerlabel.setText(str(countcustomers))
    #     self.soldproductslabel.setText(str(soldproducts))
    #     self.totalamountlabel.setText(str(totalamount) + "$")

    #def tabchanged(self):
        #self.getstatistics()
        #self.displayProducts()
        #self.displaycustomers()

class DisplayCustomer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("customer details")
        self.setWindowIcon(QIcon("Icons/icon.ico"))
        self.setGeometry(450, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.customerdetails()
        self.widgets()
        self.layouts()

    def customerdetails(self):
        global customerId
        query=("SELECT * FROM customers WHERE  customer_id = ?")
        customer=cur.execute(query, (customerId,)).fetchone()
        self.customerName=customer[1]
        self.customersurName=customer[2]
        self.customerphone=customer[3]

    def widgets(self):
        #####widgets of top layouts#####
        self.customerimage=QLabel()
        self.image=QPixmap('icons/members.png')
        self.customerimage.setPixmap(self.image)
        self.customerimage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titletext=QLabel("Display member")
        self.titletext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #####widgets of bottom layouts#######

        self.nameEntry=QLineEdit()
        self.nameEntry.setText(self.customerName)
        self.surnameEntry=QLineEdit()
        self.surnameEntry.setText(self.customersurName)
        self.phoneEntry=QLineEdit()
        self.phoneEntry.setText(self.customerphone)
        self.updatebtn=QPushButton("Update")
        self.updatebtn.clicked.connect(self.updatecustomer)
        self.deletebtn=QPushButton("Delete")
        self.deletebtn.clicked.connect(self.deletecustomer)


    def layouts(self):
        self.mainlayout=QVBoxLayout()
        self.toplayout=QVBoxLayout()
        self.bottomlayout=QFormLayout()
        self.topframe=QFrame()
        self.bottomframe=QFrame()
        self.toplayout.addWidget(self.titletext)
        self.toplayout.addWidget(self.customerimage)
        self.topframe.setLayout(self.toplayout)
        self.bottomlayout.addRow(QLabel("Name"), self.nameEntry)
        self.bottomlayout.addRow(QLabel("Surname"), self.surnameEntry)
        self.bottomlayout.addRow(QLabel("Phone"), self.phoneEntry)
        self.bottomlayout.addRow(QLabel(""), self.updatebtn)
        self.bottomlayout.addRow(QLabel(""), self.deletebtn)
        self.bottomframe.setLayout(self.bottomlayout)
        self.mainlayout.addWidget(self.topframe)
        self.mainlayout.addWidget(self.bottomframe)

        self.setLayout(self.mainlayout)

    def deletecustomer(self):
        global customerId

        mbox=QMessageBox.question(self, "warning", "are u sure to delete this customer?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if (mbox == QMessageBox.StandardButton.Yes):
            try:
                cur.execute("DELETE FROM customers WHERE customer_id = ?", (customerId,))
                con.commit()
                QMessageBox.information(self, "info", "customer deleted", QMessageBox.StandardButton.Ok)
                self.close()
            except:
                QMessageBox.information(self, "info", "customer  not deleted", QMessageBox.StandardButton.Ok)

    def updatecustomer(self):
        global customerId
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()

        if(name and surname and phone)!= "":
            try:
                query = "UPDATE customers set customer_name = ?, customer_surname = ?, customer_phonenumber =? WHERE customer_id =?"
                cur.execute(query, (name, surname, phone, customerId))
                con.commit()
                QMessageBox.information(self, "info", "customer updated", QMessageBox.StandardButton.Ok)

            except:
                QMessageBox.information(self, "info", "customer not updated", QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "info", "fields cant be empty", QMessageBox.StandardButton.Ok)




class DisplayProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("product details")
        self.setWindowIcon(QIcon("Icons/icon.ico"))
        self.setGeometry(450, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.productdetails()
        self.widgets()
        self.layouts()

    def productdetails(self):
        global productId
        query=("SELECT * FROM  products WHERE product_id = ?")
        product=cur.execute(query, (productId,)).fetchone()  # single item tuple =(1,)
        self.productname=product[1]
        self.productmanufacturer=product[2]
        self.productprice=product[3]
        self.productquota=product[4]
        self.productimg=product[5]
        self.productstatus=product[6]

    def widgets(self):
        #####top widgwts##
        self.product_img=QLabel()
        self.img=QPixmap('img/{}'.format(self.productimg))
        self.product_img.setPixmap(self.img)
        self.product_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titletext=QLabel("Update product")
        self.product_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titletext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ######### bottom layouts widget########
        self.nameEntry=QLineEdit()
        self.nameEntry.setText(self.productname)
        self.manufacturerEntry=QLineEdit()
        self.manufacturerEntry.setText(self.productmanufacturer)
        self.priceEntry=QLineEdit()
        self.priceEntry.setText(str(self.productprice))
        self.quotaEntry=QLineEdit()
        self.quotaEntry.setText(str(self.productquota))
        self.availabiltycombo=QComboBox()
        self.availabiltycombo.addItems(["Available", "unavailable"])
        self.uploadbtn=QPushButton("upload")
        self.uploadbtn.clicked.connect(self.uploadimg)
        self.deletebtn=QPushButton("Delete")
        self.deletebtn.clicked.connect(self.deleteproduct)
        self.updatebtn=QPushButton("Update")
        self.updatebtn.clicked.connect(self.updateproduct)

    def layouts(self):
        self.mainlayout=QVBoxLayout()
        self.toplayout=QVBoxLayout()
        self.bottomlayout=QFormLayout()
        self.topframe=QFrame()
        self.bottomframe=QFrame()
        ########add widgets ########
        self.toplayout.addWidget(self.titletext)
        self.toplayout.addWidget(self.product_img)
        self.topframe.setLayout(self.toplayout)
        self.bottomlayout.addRow(QLabel("Name:"), self.nameEntry)
        self.bottomlayout.addRow(QLabel("Manufacturer:"), self.manufacturerEntry)
        self.bottomlayout.addRow(QLabel("Price:"), self.priceEntry)
        self.bottomlayout.addRow(QLabel("Quota:"), self.quotaEntry)
        self.bottomlayout.addRow(QLabel("Status:"), self.availabiltycombo)
        self.bottomlayout.addRow(QLabel("Image:"), self.uploadbtn)
        self.bottomlayout.addRow(QLabel("Delete:"), self.deletebtn)
        self.bottomlayout.addRow(QLabel("update:"), self.updatebtn)
        self.bottomframe.setLayout(self.bottomlayout)
        self.mainlayout.addWidget(self.topframe)
        self.mainlayout.addWidget(self.bottomframe)

        self.setLayout(self.mainlayout)

    def uploadimg(self):
        size=(256, 256)
        self.filename, ok=QFileDialog.getOpenFileName(self, "upload image", '', 'Image files(*.jpg *.png)')
        if ok:
            self.productimg=os.path.basename(self.filename)
            img=Image.open(self.filename)

            img=img.resize(size)
            img.save("img/{0}".format(self.productimg))

    def updateproduct(self):
        global productId
        name=self.nameEntry.text()
        manufacturer=self.manufacturerEntry.text()
        priced=(self.priceEntry.text())
        price_without_dollar=priced.replace('$', '')
        price=int(price_without_dollar)
        quota=int(self.quotaEntry.text())  # prices in database are integers
        status=self.availabiltycombo.currentText()
        defaultimg=self.productimg

        if (name and manufacturer and price and quota) != "":

            try:
                query="UPDATE products set product_name =?, product_manufacturer = ?, product_price =?, product_quota =?, product_img =?, product_availability =? WHERE  product_id =?"
                cur.execute(query, (name, manufacturer, price, quota, defaultimg, status, productId))
                con.commit()
                QMessageBox.information(self, "info", "product updated!", QMessageBox.StandardButton.Yes)
            except:
                QMessageBox.information(self, " product not updated", "INFO", QMessageBox.StandardButton.No)
        else:
            QMessageBox.information(self, " fields cant be empty", "INFO", QMessageBox.StandardButton.OK)

    def deleteproduct(self):
        global productId

        mbox=QMessageBox.question(self, "warning", "are u sure to delete this product",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if (mbox == QMessageBox.StandardButton.Yes):
            try:
                cur.execute("DELETE FROM products WHERE product_id = ?", (productId,))
                con.commit()
                QMessageBox.information(self, "info", "product deleted", QMessageBox.StandardButton.Ok)
                self.close()
            except:
                QMessageBox.information(self, "info", "product  not deleted", QMessageBox.StandardButton.Ok)


def main():
    app=QApplication([])
    window=Main()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
