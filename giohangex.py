import sys
from PyQt6 import QtWidgets, uic
from cart import cart


class GioHang(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi("giohang.ui", self)

        # kết nối nút xóa
        self.btnXoa.clicked.connect(self.delete_item)

        self.load_cart()

    def load_cart(self):

        self.tableGiohang.setRowCount(len(cart))

        tong_tien = 0

        for row, item in enumerate(cart):

            name = QtWidgets.QTableWidgetItem(item["name"])
            price = QtWidgets.QTableWidgetItem(str(item["price"]))
            quantity = QtWidgets.QTableWidgetItem(str(item["quantity"]))

            total = item["price"] * item["quantity"]
            total_item = QtWidgets.QTableWidgetItem(str(total))

            tong_tien += total

            self.tableGiohang.setItem(row, 0, name)
            self.tableGiohang.setItem(row, 1, price)
            self.tableGiohang.setItem(row, 2, quantity)
            self.tableGiohang.setItem(row, 3, total_item)

        # hiển thị tổng tiền
        self.lineEdit.setText(str(tong_tien))

    def delete_item(self):

        row = self.tableGiohang.currentRow()

        if row >= 0:
            cart.pop(row)
            self.load_cart()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = GioHang()
    window.show()

    sys.exit(app.exec())