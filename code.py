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

class ThanhToan(MoGiaoDien,Ui_ThanhToan):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.jpg"))
        self.sanpham.clicked.connect(lambda:self.mogiaodien(SanPham))
        self.trangchu.clicked.connect(lambda:self.mogiaodien(TrangChu))
        self.giohang.clicked.connect(lambda:self.mogiaodien(GioHang))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))










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