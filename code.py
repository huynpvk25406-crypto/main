from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem
from PyQt6.QtGui import QPixmap, QIcon
from dangnhap import Ui_DangNhap
from quanly import Ui_QuanLy
from sanpham import Ui_SanPham
from trangchu import Ui_TrangChu
from giohang import Ui_GioHang
from thanhtoan import Ui_ThanhToan
from quanlysanpham import Ui_QuanLySanPham
from quanlyhangtonkho import Ui_QuanLyHangTonKho
from quanlynhanvien import Ui_QuanLyNhanVien
from quanlythunhap import Ui_QuanLyThuNhap
from hiensanphamchitiet import Ui_HienSanPhamChiTiet
from account_manager import AccountManager
import json
from PyQt6.QtWidgets import QTableWidgetItem
cart=[]
import random
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import QFileDialog
class MoGiaoDien(QMainWindow):
    def mogiaodien(self,window_class):
        self.window=window_class()
        self.window.show()
        self.close()

class DangNhap(MoGiaoDien,Ui_DangNhap):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.mostaff.clicked.connect(lambda:self.mogiaodien(QuanLy))
        self.xacnhan2.clicked.connect(lambda:self.mogiaodien(TrangChu))
        self.staff_accounts = {
            "admin1": "123",
            "admin2": "123"
        }
        self.xacnhan2.clicked.connect(self.login)
        self.xacnhan1.clicked.connect(self.register)

    def login(self):
        username = self.dnten.text()
        password = self.dnmk.text()
        if username in self.staff_accounts and self.staff_accounts[username] == password:
            self.mogiaodien(QuanLy)
            return
        try:
            with open("user.json", "r") as f:
                users = json.load(f)
        except:
            users = []
        for u in users:
            if u["username"] == username and u["password"] == password:
                self.mogiaodien(TrangChu)
                return
        QMessageBox.warning(self, "Lỗi", "Sai tài khoản hoặc mật khẩu")

    def register(self):
        username = self.dkten.text()
        password = self.dkmk.text()
        repass = self.dknlmk.text()
        if password != repass:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu nhập lại không đúng")
            return
        try:
            with open("user.json", "r") as f:
                users = json.load(f)
        except:
            users = []
        for u in users:
            if u["username"] == username:
                QMessageBox.warning(self, "Lỗi", "Tài khoản đã tồn tại")
                return
        users.append({
            "username": username,
            "password": password
        })
        with open("user.json", "w") as f:
            json.dump(users, f)
        QMessageBox.information(self, "OK", "Đăng ký thành công")

class TrangChu(MoGiaoDien,Ui_TrangChu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.sanpham.clicked.connect(lambda:self.mogiaodien(SanPham))
        self.trangchu.clicked.connect(lambda:self.mogiaodien(TrangChu))
        self.giohang.clicked.connect(lambda:self.mogiaodien(GioHang))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))
        self.images=["image/anh1.jpg","image/anh2.jpg","image/anh3.jpg","image/anh4.jpg"]
        self.index=0
        self.anh.setPixmap(QPixmap(self.images[self.index]))
        self.timer=QTimer()
        self.timer.timeout.connect(self.next_image)
        self.timer.start(3000)
    def next_image(self):
        self.index=(self.index+1)%len(self.images)
        self.anh.setPixmap(QPixmap(self.images[self.index]))

class SanPham(MoGiaoDien,Ui_SanPham):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.sanpham.clicked.connect(lambda:self.mogiaodien(SanPham))
        self.trangchu.clicked.connect(lambda:self.mogiaodien(TrangChu))
        self.giohang.clicked.connect(lambda:self.mogiaodien(GioHang))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))

        self.hiensanpham()
        self.bangsanpham.itemClicked.connect(self.xem_chitiet)
        self.bangsanpham.setIconSize(QSize(120, 120))
        self.bangsanpham.setGridSize(QSize(170, 260))

    def hiensanpham(self):
        try:
            with open("products.json", "r") as f:
                products = json.load(f)
        except:
            products = []
        for p in products:
            item = QListWidgetItem()
            item.setText(p["name"])
            item.setIcon(QIcon(p["img"]))
            item.setData(Qt.ItemDataRole.UserRole, p)
            self.bangsanpham.addItem(item)

    def xem_chitiet(self, item):
        sp = item.data(Qt.ItemDataRole.UserRole)
        self.window = HienSanPhamChiTiet(sp)
        self.window.show()
        self.close()

class HienSanPhamChiTiet(MoGiaoDien, Ui_HienSanPhamChiTiet):
    def __init__(self, sp):
        super().__init__()
        self.setupUi(self)

        self.sp = sp

        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.sanpham.clicked.connect(lambda:self.mogiaodien(SanPham))
        self.trangchu.clicked.connect(lambda:self.mogiaodien(TrangChu))
        self.giohang.clicked.connect(lambda:self.mogiaodien(GioHang))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))

        self.tenspchitiet.setText(sp["name"])
        self.giaspchitiet.setText(sp["price"])
        self.motaspchitiet.setText(sp["desc"])
        self.anhspchitiet.setPixmap(QPixmap(sp["img"]))

        # nút thêm giỏ
        self.xacnhanthem.clicked.connect(self.them_vao_gio)

    def them_vao_gio(self):
        soluong = self.soluong.value()

        item = {
            "name": self.sp["name"],
            "price": self.sp["price"],
            "qty": soluong
        }

        cart.append(item)

        QMessageBox.information(self, "Thông báo", "Đã thêm vào giỏ hàng")

class GioHang(MoGiaoDien,Ui_GioHang):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.sanpham.clicked.connect(lambda:self.mogiaodien(SanPham))
        self.trangchu.clicked.connect(lambda:self.mogiaodien(TrangChu))
        self.giohang.clicked.connect(lambda:self.mogiaodien(GioHang))
        self.thanhtoan.clicked.connect(lambda:self.mogiaodien(ThanhToan))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))
        self.load_cart()
        self.xoa.clicked.connect(self.xoa_sanpham)
    def load_cart(self):
        self.thongtingiohang.setRowCount(len(cart))

        tong = 0

        for row, item in enumerate(cart):
            name = item["name"]
            price = int(item["price"].replace(".","").replace(" VND",""))
            qty = item["qty"]
            thanhtien = price * qty
            tong += thanhtien
            self.thongtingiohang.setItem(row,0,QTableWidgetItem(name))
            self.thongtingiohang.setItem(row,1,QTableWidgetItem(str(price)))
            self.thongtingiohang.setItem(row,2,QTableWidgetItem(str(qty)))
            self.thongtingiohang.setItem(row,3,QTableWidgetItem(str(thanhtien)))

        self.tongtien.setText(str(tong))

    def xoa_sanpham(self):
        row = self.thongtingiohang.currentRow()

        # kiểm tra có chọn dòng chưa
        if row == -1:
            QMessageBox.warning(self, "Thông báo", "Hãy chọn sản phẩm cần xóa")
            return

        # kiểm tra index có hợp lệ không
        if row >= len(cart):
            return

        cart.pop(row)

        self.load_cart()

class ThanhToan(MoGiaoDien, Ui_ThanhToan):
    QR = {"ZaloPay": "zalopay_qr.png", "MoMo": "momo_qr.png", "VNPay": "vnpay_qr.png"}
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tong = 0
        self.pttt = 0
        self.lichsu = []
        self._setup()
        self._load()

    def _setup(self):
        for n, w in [("logo.jpg", self.logo), ("cuoi.png", self.cuoi)]:
            if (p := Path("image") / n).exists():
                w.setPixmap(QPixmap(str(p)))
                w.setScaledContents(True)
        self.textEdit.hide()
        self.btnTimeline.hide()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Mã", "TG", "PTTT", "Tổng", "TT"])
        self.trangchu.clicked.connect(lambda: self.mogiaodien(TrangChu))
        self.sanpham.clicked.connect(lambda: self.mogiaodien(SanPham))
        self.giohang.clicked.connect(lambda: self.mogiaodien(GioHang))

        for btn, m in [(self.radioButton, "COD"),
                       (self.radioButton_2, "ZaloPay"),
                       (self.radioButton_3, "MoMo"),
                       (self.radioButton_4, "VNPay")]:
            btn.clicked.connect(lambda _, m=m: self.chon_pt(m))

        self.pushButton.clicked.connect(self.dat_hang)
        self.downloadButton.clicked.connect(self.xuat_hd)

    def _load(self):
        global cart
        self.tong = 0
        if not cart:
            self.itemsText.setText("GIỎ HÀNG TRỐNG")
            self.hientien.setText("0 VNĐ")
            return

        lines = []
        for i in cart:
            tt = int(i.get("price", "0").replace(".", "").replace(" VND", "0")) * i.get("qty", 0)
            self.tong += tt
            lines.append(f"• {i.get('name', '?')} x{i.get('qty', 0)}: {tt:,}đ")

        self.itemsText.setText("SẢN PHẨM:\n" + "\n".join(lines))
        self.hientien.setText(f"{self.tong:,} VNĐ")

    def chon_pt(self, m):
        self.pttt = m
        self.hienphuongthuc.setText(m)
        if m in self.QR and (p := Path("image") / self.QR[m]).exists():
            self.qrLabel.setPixmap(QPixmap(str(p)))
            self.qrLabel.setScaledContents(True)
        else:
            self.qrLabel.setText("Thanh toán khi nhận hàng")
            self.qrLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def dat_hang(self):
        global cart
        if not cart or not self.pttt:
            QMessageBox.warning(self, "Lỗi", "Giỏ trống hoặc chưa chọn PTTT!")
            return

        now = datetime.now()
        o = {
            "id": f"ORD{random.randint(100000, 999999)}",
            "time": now.strftime("%Y-%m-%d %H:%M"),
            "pt": self.pttt,
            "tong": self.tong,
            "tt": "Đang xử lý"
        }

        self.lichsu.insert(0, o)
        cart.clear()
        self.tableWidget.insertRow(0)

        for c, v in enumerate([o["id"], o["time"], o["pt"], f"{o['tong']:,}đ", o["tt"]]):
            self.tableWidget.setItem(0, c, QTableWidgetItem(v))

        QMessageBox.information(self, "OK", f"Đặt hàng thành công!\nMã: {o['id']}\nTổng: {self.tong:,}đ")
        self._load()

    def xuat_hd(self):
        if (r := self.tableWidget.currentRow()) < 0:
            QMessageBox.warning(self, "Lỗi", "Chọn đơn hàng cần xuất!")
            return

        d = self.lichsu[r]
        f, _ = QFileDialog.getSaveFileName(self, "Lưu hóa đơn", f"hoadon_{d['id']}.txt", "Text Files (*.txt)")

        if f:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(f"HÓA ĐƠN\nMã: {d['id']}\nTG: {d['time']}\nPTTT: {d['pt']}\nTổng: {d['tong']:,}đ")
            QMessageBox.information(self, "OK", "Đã lưu hóa đơn!")

class QuanLy(MoGiaoDien,Ui_QuanLy):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.trangchu2.clicked.connect(lambda:self.mogiaodien(QuanLy))
        self.quanlysanpham.clicked.connect(lambda:self.mogiaodien(QuanLySanPham))
        self.hangtonkho.clicked.connect(lambda:self.mogiaodien(QuanLyHangTonKho))
        self.quanlynhanvien.clicked.connect(lambda:self.mogiaodien(QuanLyNhanVien))
        self.quanlythunhap.clicked.connect(lambda:self.mogiaodien(QuanLyThuNhap))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))
        self.images=["image/anh1.jpg","image/anh2.jpg","image/anh3.jpg","image/anh4.jpg"]
        self.index=0
        self.anh.setPixmap(QPixmap(self.images[self.index]))
        self.timer=QTimer()
        self.timer.timeout.connect(self.next_image)
        self.timer.start(3000)
    def next_image(self):
        self.index=(self.index+1)%len(self.images)
        self.anh.setPixmap(QPixmap(self.images[self.index]))

class QuanLySanPham(MoGiaoDien,Ui_QuanLySanPham):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.trangchu2.clicked.connect(lambda:self.mogiaodien(QuanLy))
        self.quanlysanpham.clicked.connect(lambda:self.mogiaodien(QuanLySanPham))
        self.hangtonkho.clicked.connect(lambda:self.mogiaodien(QuanLyHangTonKho))
        self.quanlynhanvien.clicked.connect(lambda:self.mogiaodien(QuanLyNhanVien))
        self.quanlythunhap.clicked.connect(lambda:self.mogiaodien(QuanLyThuNhap))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))

        self.xacnhanthem.clicked.connect(self.them_sp)

    def them_sp(self):
        idsp = self.themidsp.text()
        name = self.themtensp.text()
        price = self.themgiasp.text()
        img = self.themlinkanhsp.text()
        desc = self.themmotasp.text()
        if name == "" or price == "" or img == "":
            QMessageBox.warning(self, "Lỗi", "Nhập đầy đủ thông tin")
            return
        try:
            with open("products.json", "r") as f:
                products = json.load(f)
        except:
            products = []
        products.append({
            "id": idsp,
            "name": name,
            "price": price,
            "img": img,
            "desc": desc
        })
        with open("products.json", "w") as f:
            json.dump(products, f)
        QMessageBox.information(self,"OK","Thêm sản phẩm thành công")
        self.themidsp.clear()
        self.themtensp.clear()
        self.themgiasp.clear()
        self.themlinkanhsp.clear()
        self.themmotasp.clear()

class QuanLyHangTonKho(MoGiaoDien,Ui_QuanLyHangTonKho):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.trangchu2.clicked.connect(lambda:self.mogiaodien(QuanLy))
        self.quanlysanpham.clicked.connect(lambda:self.mogiaodien(QuanLySanPham))
        self.hangtonkho.clicked.connect(lambda:self.mogiaodien(QuanLyHangTonKho))
        self.quanlynhanvien.clicked.connect(lambda:self.mogiaodien(QuanLyNhanVien))
        self.quanlythunhap.clicked.connect(lambda:self.mogiaodien(QuanLyThuNhap))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))

class QuanLyNhanVien(MoGiaoDien, Ui_QuanLyNhanVien):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.trangchu2.clicked.connect(lambda:self.mogiaodien(QuanLy))
        self.quanlysanpham.clicked.connect(lambda:self.mogiaodien(QuanLySanPham))
        self.hangtonkho.clicked.connect(lambda:self.mogiaodien(QuanLyHangTonKho))
        self.quanlynhanvien.clicked.connect(lambda:self.mogiaodien(QuanLyNhanVien))
        self.quanlythunhap.clicked.connect(lambda:self.mogiaodien(QuanLyThuNhap))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))

class QuanLyThuNhap(MoGiaoDien, Ui_QuanLyThuNhap):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.trangchu2.clicked.connect(lambda:self.mogiaodien(QuanLy))
        self.quanlysanpham.clicked.connect(lambda:self.mogiaodien(QuanLySanPham))
        self.hangtonkho.clicked.connect(lambda:self.mogiaodien(QuanLyHangTonKho))
        self.quanlynhanvien.clicked.connect(lambda:self.mogiaodien(QuanLyNhanVien))
        self.quanlythunhap.clicked.connect(lambda:self.mogiaodien(QuanLyThuNhap))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))
