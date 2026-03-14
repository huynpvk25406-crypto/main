import sys
import json
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from cart import cart
from giohangex import GioHang
class SanPham(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("sanpham.ui", self)
        # label hiển thị ảnh
        self.labels = [
            self.sp1, self.sp2, self.sp3, self.sp4,
            self.sp5, self.sp6, self.sp7, self.sp8
        ]
        # spinbox
        self.spinboxes = [
            self.spinBox, self.spinBox_2, self.spinBox_3, self.spinBox_4,
            self.spinBox_5, self.spinBox_6, self.spinBox_7, self.spinBox_8
        ]
        # nút thêm giỏ hàng
        self.buttons = [
            self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4,
            self.pushButton_5, self.pushButton_6, self.pushButton_7, self.pushButton_8
        ]
        for sp in self.spinboxes:
            sp.setMinimum(1)
        # load JSON
        with open("products.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.products = data["products"]
        self.show_products()
        # kết nối nút thêm giỏ
        for i, btn in enumerate(self.buttons):
            btn.clicked.connect(lambda checked, index=i: self.add_to_cart(index))
        # tìm kiếm
        self.timkiem.textChanged.connect(self.search_product)
        # mở giỏ hàng
        self.giohang.clicked.connect(self.open_cart)
    def show_products(self):
        for i, product in enumerate(self.products):
            pixmap = QPixmap(product["image"])
            self.labels[i].setPixmap(pixmap)
            self.labels[i].setScaledContents(True)
    def add_to_cart(self, index):
        product = self.products[index]
        sl = self.spinboxes[index].value()
        item = {
            "name": product["name"],
            "price": product["price"],
            "quantity": sl
        }
        cart.append(item)
        print(cart)
        QtWidgets.QMessageBox.information(self, "Thông báo", "Đã thêm vào giỏ hàng")
    def search_product(self):
        keyword = self.timkiem.text().lower()
        for i, product in enumerate(self.products):
            if keyword in product["name"].lower():
                self.labels[i].show()
                self.spinboxes[i].show()
                self.buttons[i].show()
            else:
                self.labels[i].hide()
                self.spinboxes[i].hide()
                self.buttons[i].hide()
    def open_cart(self):
        self.cart_window = GioHang()
        self.cart_window.load_cart()  # cập nhật dữ liệu mới
        self.cart_window.show()
app = QtWidgets.QApplication(sys.argv)
window = SanPham()
window.show()
sys.exit(app.exec())