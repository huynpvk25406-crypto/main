from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem, QTableWidgetItem, QFileDialog
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QDialog,QLabel,QVBoxLayout
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
from tintuc import Ui_TinTuc
from hiensanphamchitiet import Ui_HienSanPhamChiTiet
import json
import random
from datetime import datetime
from pathlib import Path

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
        self.logo.setPixmap(QPixmap("image/logo.png"))
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
            with open("data/user.json", "r") as f:
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
            with open("data/user.json", "r") as f:
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
        with open("data/user.json", "w") as f:
            json.dump(users, f)
        QMessageBox.information(self, "Chúc mừng, ", "Bạn đã đăng ký thành công")













class TrangChu(MoGiaoDien,Ui_TrangChu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda:self.mogiaodien(DangNhap))
        self.sanpham.clicked.connect(lambda:self.mogiaodien(SanPham))
        self.trangchu.clicked.connect(lambda:self.mogiaodien(TrangChu))
        self.giohang.clicked.connect(lambda:self.mogiaodien(GioHang))
        self.tintuc.clicked.connect(lambda:self.mogiaodien(TinTuc))
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
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda:self.mogiaodien(DangNhap))
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
            with open("data/products.json", "r") as f:
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
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda:self.mogiaodien(DangNhap))
        self.sanpham.clicked.connect(lambda:self.mogiaodien(SanPham))
        self.trangchu.clicked.connect(lambda:self.mogiaodien(TrangChu))
        self.giohang.clicked.connect(lambda:self.mogiaodien(GioHang))
        self.tintuc.clicked.connect(lambda:self.mogiaodien(TinTuc))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))
        self.tenspchitiet.setText(sp["name"])
        self.giaspchitiet.setText(sp["price"])
        self.motaspchitiet.setText(sp["desc"])
        self.anhspchitiet.setPixmap(QPixmap(sp["img"]))
        self.sp = sp
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
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda:self.mogiaodien(DangNhap))
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
            price = int(item["price"].replace(".", "").replace(" VND", ""))
            qty = item["qty"]
            thanhtien = price * qty
            tong += thanhtien
            self.thongtingiohang.setItem(row, 0, QTableWidgetItem(name))
            self.thongtingiohang.setItem(row, 1, QTableWidgetItem(str(price)))
            self.thongtingiohang.setItem(row, 2, QTableWidgetItem(str(qty)))
            self.thongtingiohang.setItem(row, 3, QTableWidgetItem(str(thanhtien)))
        self.tongtien.setText(str(tong))
        if len(cart) == 0:
            self.thanhtoan.setEnabled(False)
        else:
            self.thanhtoan.setEnabled(True)
    def xoa_sanpham(self):
        row = self.thongtingiohang.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Thông báo", "Hãy chọn sản phẩm cần xóa")
            return
        if row >= len(cart):
            return
        cart.pop(row)
        self.load_cart()

class TinTuc(MoGiaoDien, Ui_TinTuc):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda: self.mogiaodien(DangNhap))
        self.sanpham.clicked.connect(lambda: self.mogiaodien(SanPham))
        self.trangchu.clicked.connect(lambda: self.mogiaodien(TrangChu))
        self.giohang.clicked.connect(lambda: self.mogiaodien(GioHang))
        self.tintuc.clicked.connect(lambda:self.mogiaodien(TinTuc))

class QRWindow(QDialog):
    def __init__(self,path):
        super().__init__()
        self.setWindowTitle("Quét QR để thanh toán")
        self.setFixedSize(300,350)
        layout=QVBoxLayout()
        label=QLabel()
        pix=QPixmap(path)
        label.setPixmap(pix)
        label.setScaledContents(True)
        layout.addWidget(label)
        self.setLayout(layout)
class ThanhToan(MoGiaoDien,Ui_ThanhToan):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda:self.mogiaodien(DangNhap))
        self.sanpham.clicked.connect(lambda:self.mogiaodien(SanPham))
        self.trangchu.clicked.connect(lambda:self.mogiaodien(TrangChu))
        self.giohang.clicked.connect(lambda:self.mogiaodien(GioHang))
        self.tintuc.clicked.connect(lambda:self.mogiaodien(TinTuc))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))
        self.thongtin={}
        self.pttt=""
        self.cod.toggled.connect(self.chon_thanhtoan)
        self.zalopay.toggled.connect(self.chon_thanhtoan)
        self.momo.toggled.connect(self.chon_thanhtoan)
        self.vnpay.toggled.connect(self.chon_thanhtoan)
        self.dathang.clicked.connect(self.dat_hang)
    def lay_thong_tin(self):
        self.thongtin={"ten":self.hoten.text(),"sdt":self.sdt.text(),"email":self.email.text(),"diachi":self.diachi.text(),"ghichu":self.ghichu.text()}
    def chon_thanhtoan(self):
        if self.cod.isChecked():
            self.pttt="COD"
            self.phuongthuc.setText("Thanh toán khi nhận hàng")
        elif self.zalopay.isChecked():
            self.pttt="ZaloPay"
            self.phuongthuc.setText("Thanh toán ZaloPay")
        elif self.momo.isChecked():
            self.pttt="MoMo"
            self.phuongthuc.setText("Thanh toán MoMo")
        elif self.vnpay.isChecked():
            self.pttt="VNPay"
            self.phuongthuc.setText("Thanh toán VNPay")
    def mo_qr(self,path):
        self.qr_window=QRWindow(path)
        self.qr_window.exec()
    def dat_hang(self):
        self.lay_thong_tin()
        if self.thongtin["ten"]=="" or self.thongtin["sdt"]=="":
            QMessageBox.warning(self,"Lỗi","Vui lòng nhập thông tin")
            return
        if self.pttt=="":
            QMessageBox.warning(self,"Lỗi","Hãy chọn phương thức thanh toán")
            return
        if self.pttt=="COD":
            if self.hoadon.isChecked():
                text=f"Tên: {self.thongtin['ten']}\nSĐT: {self.thongtin['sdt']}\nEmail: {self.thongtin['email']}\nĐịa chỉ: {self.thongtin['diachi']}\nPhương thức: COD"
                QMessageBox.information(self,"Hóa đơn",text)
            else:
                QMessageBox.information(self,"Thông báo","Đặt hàng thành công")
        else:
            if self.pttt=="MoMo":
                path="image/momo.jpg"
            elif self.pttt=="ZaloPay":
                path="image/zalopay.jpg"
            elif self.pttt=="VNPay":
                path="image/vnpay.jpg"
            if self.hoadon.isChecked():
                text=f"Tên: {self.thongtin['ten']}\nSĐT: {self.thongtin['sdt']}\nEmail: {self.thongtin['email']}\nĐịa chỉ: {self.thongtin['diachi']}\nPhương thức: {self.pttt}\nQuét QR để thanh toán"
                QMessageBox.information(self,"Hóa đơn",text)
            self.mo_qr(path)













class QuanLy(MoGiaoDien,Ui_QuanLy):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda:self.mogiaodien(DangNhap))
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
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda:self.mogiaodien(DangNhap))
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
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return
        try:
            with open("data/products.json", "r") as f:
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
        with open("data/products.json", "w") as f:
            json.dump(products, f)
        QMessageBox.information(self,"Chúc mừng, ","Ban đã thêm sản phẩm thành công")
        self.themidsp.clear()
        self.themtensp.clear()
        self.themgiasp.clear()
        self.themlinkanhsp.clear()
        self.themmotasp.clear()

class QuanLyHangTonKho(MoGiaoDien,Ui_QuanLyHangTonKho):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda:self.mogiaodien(DangNhap))
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
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda:self.mogiaodien(DangNhap))
        self.trangchu2.clicked.connect(lambda:self.mogiaodien(QuanLy))
        self.quanlysanpham.clicked.connect(lambda:self.mogiaodien(QuanLySanPham))
        self.hangtonkho.clicked.connect(lambda:self.mogiaodien(QuanLyHangTonKho))
        self.quanlynhanvien.clicked.connect(lambda:self.mogiaodien(QuanLyNhanVien))
        self.quanlythunhap.clicked.connect(lambda:self.mogiaodien(QuanLyThuNhap))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))
        self.pushButtonSave.clicked.connect(self.luu_nhanvien)
        self.pushButtonDel.clicked.connect(self.xoa_nhanvien)
        self.lineEditSearch.textChanged.connect(self.timkiem)
        self.pushButtonSave.setText("💾 Lưu")
        self.pushButtonDel.setText("🗑 Xóa")
        self.load_nhanvien()
    def load_nhanvien(self):
        try:
            with open("data/nhanvien.json","r",encoding="utf-8") as f:
                self.ds_nhanvien = json.load(f)
        except:
            self.ds_nhanvien = []
        self.capnhat_danhsach()
    def save_json(self):
        with open("data/nhanvien.json","w",encoding="utf-8") as f:
            json.dump(self.ds_nhanvien,f,ensure_ascii=False,indent=4)
    def luu_nhanvien(self):
        ma = self.lineEditMaNV.text()
        ten = self.lineEditName.text()
        luong = self.lineEditLuong.text()
        dt = self.lineEditDT.text()
        email = self.lineEditEmail.text()
        chucvu = self.ComboChucVu.currentText()
        if self.radMan.isChecked():
            gioitinh = "Nam"
        else:
            gioitinh = "Nữ"
        nv = {
            "ma": ma,
            "ten": ten,
            "gioitinh": gioitinh,
            "chucvu": chucvu,
            "luong": luong,
            "dt": dt,
            "email": email
        }
        self.ds_nhanvien.append(nv)
        self.save_json()
        self.capnhat_danhsach()
        self.lineEditMaNV.clear()
        self.lineEditName.clear()
        self.lineEditLuong.clear()
        self.lineEditDT.clear()
        self.lineEditEmail.clear()
    def capnhat_danhsach(self):
        self.danhsachnv.clear()
        for nv in self.ds_nhanvien:
            text = f'{nv["ma"]} | {nv["ten"]} | {nv["gioitinh"]} | {nv["chucvu"]} | {nv["luong"]} | {nv["dt"]} | {nv["email"]}'
            self.danhsachnv.addItem(text)
    def xoa_nhanvien(self):
        row = self.danhsachnv.currentRow()
        if row >= 0:
            self.ds_nhanvien.pop(row)
            self.save_json()
            self.capnhat_danhsach()
    def timkiem(self):
        tukhoa = self.lineEditSearch.text().lower()
        self.danhsachnv.clear()
        for nv in self.ds_nhanvien:
            text = f'{nv["ma"]} | {nv["ten"]} | {nv["gioitinh"]} | {nv["chucvu"]} | {nv["luong"]} | {nv["dt"]} | {nv["email"]}'
            if tukhoa in text.lower():
                self.danhsachnv.addItem(text)

class QuanLyThuNhap(MoGiaoDien, Ui_QuanLyThuNhap):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap("image/logo.png"))
        self.dangxuat.clicked.connect(lambda:self.mogiaodien(DangNhap))
        self.trangchu2.clicked.connect(lambda:self.mogiaodien(QuanLy))
        self.quanlysanpham.clicked.connect(lambda:self.mogiaodien(QuanLySanPham))
        self.hangtonkho.clicked.connect(lambda:self.mogiaodien(QuanLyHangTonKho))
        self.quanlynhanvien.clicked.connect(lambda:self.mogiaodien(QuanLyNhanVien))
        self.quanlythunhap.clicked.connect(lambda:self.mogiaodien(QuanLyThuNhap))
        self.cuoi.setPixmap(QPixmap("image/cuoi.png"))