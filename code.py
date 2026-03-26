from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem, QTableWidgetItem, QFileDialog
from PyQt6.QtGui import QPixmap, QIcon, QColor
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
        self.tenspchitiet.setText(sp["name"])
        self.giaspchitiet.setText(sp["price"])
        self.motaspchitiet.setText(sp["desc"])
        self.anhspchitiet.setPixmap(QPixmap(sp["img"]))
        self.sp = sp
        self.so_luong_ton = self.lay_so_luong()
        if self.so_luong_ton > 0:
            self.soluong.setMinimum(1)
            self.soluong.setMaximum(self.so_luong_ton)
            self.soluong.setValue(1)
        else:
            self.soluong.setMinimum(0)
            self.soluong.setMaximum(0)
            self.soluong.setValue(0)
            self.xacnhanthem.setEnabled(False)
        self.xacnhanthem.clicked.connect(self.them_vao_gio)
    def lay_so_luong(self):
        try:
            return int(self.sp.get("soluong", 0))
        except:
            text = str(self.sp.get("soluong", "")).strip()
            so = "".join(char for char in text if char.isdigit())
            if so == "":
                return 0
            return int(so)
    def them_vao_gio(self):
        if self.so_luong_ton <= 0:
            QMessageBox.warning(self, "Thông báo", "Sản phẩm hiện đang hết hàng")
            return
        soluong = self.soluong.value()
        item = {
            "id": self.sp.get("id", ""),
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
        self.thongtin={}
        self.pttt=""
        self.cod.toggled.connect(self.chon_thanhtoan)
        self.zalopay.toggled.connect(self.chon_thanhtoan)
        self.momo.toggled.connect(self.chon_thanhtoan)
        self.vnpay.toggled.connect(self.chon_thanhtoan)
        self.dathang.clicked.connect(self.dat_hang)
    def lay_thong_tin(self):
        self.thongtin={"ten":self.hoten.text(),"sdt":self.sdt.text(),"email":self.email.text(),"diachi":self.diachi.text(),"ghichu":self.ghichu.text()}
    def doc_products(self):
        try:
            with open("data/products.json", "r") as f:
                return json.load(f)
        except:
            return []
    def ghi_products(self, products):
        with open("data/products.json", "w") as f:
            json.dump(products, f)
    def lay_so_luong(self, sanpham):
        try:
            return int(sanpham.get("soluong", 0))
        except:
            text = str(sanpham.get("soluong", "")).strip()
            so = "".join(char for char in text if char.isdigit())
            if so == "":
                return 0
            return int(so)
    def tim_sp(self, products, item):
        masp = str(item.get("id", "")).strip()
        if masp != "":
            for sp in products:
                if str(sp.get("id", "")).strip() == masp:
                    return sp
        ten = str(item.get("name", "")).strip()
        for sp in products:
            if str(sp.get("name", "")).strip() == ten:
                return sp
        return None
    def tong_mua(self):
        ds = {}
        for item in cart:
            masp = str(item.get("id", "")).strip()
            if masp == "":
                masp = "TEN::" + str(item.get("name", "")).strip()
            qty = int(item.get("qty", 0))
            ds[masp] = ds.get(masp, 0) + qty
        return ds
    def cap_nhat_kho(self):
        if len(cart) == 0:
            QMessageBox.warning(self, "Thông báo", "Giỏ hàng hiện đang trống")
            return False
        products = self.doc_products()
        tong = self.tong_mua()
        for masp, qty in tong.items():
            if str(masp).startswith("TEN::"):
                item = {"name": str(masp)[5:], "qty": qty}
            else:
                item = {"id": masp, "qty": qty}
            sp = self.tim_sp(products, item)
            if sp is None:
                QMessageBox.warning(self, "Thông báo", "Không tìm thấy sản phẩm để cập nhật tồn kho")
                return False
            ton = self.lay_so_luong(sp)
            if qty > ton:
                QMessageBox.warning(self, "Thông báo", f"Sản phẩm {sp.get('name', '')} không đủ số lượng trong kho")
                return False
        for masp, qty in tong.items():
            if str(masp).startswith("TEN::"):
                item = {"name": str(masp)[5:], "qty": qty}
            else:
                item = {"id": masp, "qty": qty}
            sp = self.tim_sp(products, item)
            if sp is not None:
                sp["soluong"] = self.lay_so_luong(sp) - qty
        self.ghi_products(products)
        cart.clear()
        return True
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
        if self.cap_nhat_kho() == False:
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
        self.xacnhanthem.clicked.connect(self.them_sp)
        self.xacnhancapnhat.clicked.connect(self.capnhat_sp)
        self.xacnhanxoa.clicked.connect(self.xoa_sp)
    def doc_products(self):
        try:
            with open("data/products.json", "r") as f:
                return json.load(f)
        except:
            return []
    def ghi_products(self, products):
        with open("data/products.json", "w") as f:
            json.dump(products, f)
    def them_sp(self):
        idsp = self.themidsp.text().strip()
        name = self.themtensp.text()
        price = self.themgiasp.text()
        img = self.themlinkanhsp.text()
        desc = self.themmotasp.text()
        soluong_text = self.themsoluongsp.text().strip()
        if name == "" or price == "" or img == "" or soluong_text == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return
        try:
            soluong = int(soluong_text)
            if soluong < 0:
                raise ValueError
        except:
            QMessageBox.warning(self, "Loi", "So luong phai la so nguyen khong am")
            return
        products = self.doc_products()
        for p in products:
            if str(p.get("id", "")).strip() == idsp:
                QMessageBox.warning(self, "Lỗi", "ID sản phẩm đã tồn tại")
                return
        products.append({
            "id": idsp,
            "name": name,
            "price": price,
            "img": img,
            "desc": desc,
            "soluong": soluong
        })
        self.ghi_products(products)
        QMessageBox.information(self,"Chúc mừng, ","Ban đã thêm sản phẩm thành công")
        self.themidsp.clear()
        self.themtensp.clear()
        self.themgiasp.clear()
        self.themlinkanhsp.clear()
        self.themmotasp.clear()
        self.themsoluongsp.clear()
    def capnhat_sp(self):
        idsp = self.capnhatidsp.text().strip()
        name = self.capnhattensp.text().strip()
        img = self.capnhatlinkanhsp.text().strip()
        price = self.capnhatgiasp.text().strip()
        desc = self.capnhatmotasp.text().strip()
        soluong_text = self.capnhatsoluongsp.text().strip()
        if idsp == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID sản phẩm cần cập nhật")
            return
        if name == "" and img == "" and price == "" and desc == "" and soluong_text == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ít nhất một thông tin để cập nhật")
            return
        soluong = None
        if soluong_text != "":
            try:
                soluong = int(soluong_text)
                if soluong < 0:
                    raise ValueError
            except:
                QMessageBox.warning(self, "Loi", "So luong phai la so nguyen khong am")
                return
        products = self.doc_products()
        for p in products:
            if str(p.get("id", "")) == idsp:
                if name != "":
                    p["name"] = name
                if img != "":
                    p["img"] = img
                if price != "":
                    p["price"] = price
                if desc != "":
                    p["desc"] = desc
                if soluong is not None:
                    p["soluong"] = soluong
                self.ghi_products(products)
                QMessageBox.information(self, "Thông báo", "Cập nhật sản phẩm thành công")
                self.capnhatidsp.clear()
                self.capnhattensp.clear()
                self.capnhatlinkanhsp.clear()
                self.capnhatgiasp.clear()
                self.capnhatmotasp.clear()
                self.capnhatsoluongsp.clear()
                return
        QMessageBox.warning(self, "Lỗi", "Không tìm thấy sản phẩm cần cập nhật")
    def xoa_sp(self):
        idsp = self.xoasp.text().strip()
        if idsp == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID sản phẩm cần xóa")
            return
        products = self.doc_products()
        products_moi = [p for p in products if str(p.get("id", "")) != idsp]
        if len(products_moi) == len(products):
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy sản phẩm cần xóa")
            return
        self.ghi_products(products_moi)
        QMessageBox.information(self, "Thông báo", "Xóa sản phẩm thành công")
        self.xoasp.clear()

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
        self.tableWidget.verticalHeader().setVisible(False)
        self.tai_ton_kho()
    def doc_products(self):
        try:
            with open("data/products.json", "r") as f:
                return json.load(f)
        except:
            return []
    def lay_so_luong(self, sanpham):
        try:
            return int(sanpham.get("soluong", 0))
        except:
            text = str(sanpham.get("soluong", "")).strip()
            so = "".join(char for char in text if char.isdigit())
            if so == "":
                return 0
            return int(so)
    def lay_tinh_trang(self, soluong):
        if soluong < 10:
            return "Cần nhập hàng", QColor("#fecaca"), QColor("#991b1b")
        if soluong <= 24:
            return "Sắp hết hàng", QColor("#fef3c7"), QColor("#92400e")
        return "Còn hàng", QColor("#dcfce7"), QColor("#166534")
    def tao_item(self, text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item
    def tai_ton_kho(self):
        products = self.doc_products()
        self.tableWidget.setRowCount(len(products))
        for row, sanpham in enumerate(products):
            soluong = self.lay_so_luong(sanpham)
            tinhtrang, mau_nen, mau_chu = self.lay_tinh_trang(soluong)
            item_stt = self.tao_item(row + 1)
            item_id = self.tao_item(sanpham.get("id", ""))
            item_name = self.tao_item(sanpham.get("name", ""))
            item_soluong = self.tao_item(soluong)
            item_tinhtrang = self.tao_item(tinhtrang)
            item_tinhtrang.setBackground(mau_nen)
            item_tinhtrang.setForeground(mau_chu)
            self.tableWidget.setItem(row, 0, item_stt)
            self.tableWidget.setItem(row, 1, item_id)
            self.tableWidget.setItem(row, 2, item_name)
            self.tableWidget.setItem(row, 3, item_soluong)
            self.tableWidget.setItem(row, 4, item_tinhtrang)

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
    records = []
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

        self.fileDT = "data/doanhthu.json"
        self.ds_giaodich = self.docFile()
        QuanLyThuNhap.records = self.ds_giaodich
        self.cot_bieu_do = [
            self.T1, self.T2, self.T3, self.T4, self.T5, self.T6,
            self.T7, self.T8, self.T9, self.T10, self.T11, self.T12
        ]
        self.thong_so_cot_goc = []
        for cot in self.cot_bieu_do:
            hinh = cot.geometry()
            self.thong_so_cot_goc.append((hinh.x(), hinh.y(), hinh.width(), hinh.height()))
        self.chieu_cao_cot_nho_nhat = 6
        self.chieu_cao_cot_lon_nhat = max(thong_so[3] for thong_so in self.thong_so_cot_goc)

        self.khoiTaoLoai()
        self.khoaTong()
        self.chonMacDinh()
        self.ganSuKien()

        self.lamMoi()
    def docFile(self):
        try:
            with open(self.fileDT, "r", encoding="utf-8") as f:
                noi_dung = f.read().strip()
                if noi_dung == "":
                    with open(self.fileDT, "w", encoding="utf-8") as fw:
                        json.dump([], fw, ensure_ascii=False, indent=4)
                    return []
                return json.loads(noi_dung)
        except:
            with open(self.fileDT, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
            return []
    def luuFile(self):
        with open(self.fileDT, "w", encoding="utf-8") as f:
            json.dump(self.ds_giaodich, f, ensure_ascii=False, indent=4)
    def khoiTaoLoai(self):
        if self.loaigiaodich.count() == 0:
            self.loaigiaodich.addItems(["Doanh thu", "Chi tieu"])
    def khoaTong(self):
        self.tongthu.setReadOnly(True)
        self.tongchi.setReadOnly(True)
        self.loinhuan.setReadOnly(True)
    def chonMacDinh(self):
        ngay = self.dategiaodich.date()
        self.chonthang.setCurrentIndex(max(0, ngay.month() - 1))
        for i in range(self.chonnam.count()):
            if str(ngay.year()) in self.chonnam.itemText(i):
                self.chonnam.setCurrentIndex(i)
                break
    def ganSuKien(self):
        self.themdoanhthu.clicked.connect(self.them_giaodich)
        self.xoadoanhthu.clicked.connect(self.xoa_giaodich)
        self.chonthang.currentIndexChanged.connect(self.lamMoi)
        self.chonnam.currentIndexChanged.connect(self.lamMoi)
    def tachTien(self, text):
        chu_so = "".join(ky_tu for ky_tu in text if ky_tu.isdigit())
        if chu_so == "":
            return 0
        return int(chu_so)
    def formatTien(self, value):
        return f"{value:,}".replace(",", ".")
    def laDoanhThu(self, loai):
        loai = loai.strip().lower()
        return "thu" in loai and "chi" not in loai
    def layNam(self):
        chu_so = "".join(ky_tu for ky_tu in self.chonnam.currentText() if ky_tu.isdigit())
        if chu_so == "":
            return self.dategiaodich.date().year()
        return int(chu_so)
    def layThang(self):
        return self.chonthang.currentIndex() + 1
    def taoText(self, gd):
        tien = self.formatTien(gd["so_tien"])
        return f'{gd["ngay"]} | {gd["loai"]} | {tien} | {gd["noi_dung"]}'
    def taiBang(self):
        self.bangghinhan.clear()
        for gd in self.ds_giaodich:
            item = QListWidgetItem(self.taoText(gd))
            item.setData(Qt.ItemDataRole.UserRole, gd["id"])
            self.bangghinhan.addItem(item)
    def tinhTong(self):
        nam = self.layNam()
        thang = self.layThang()
        tong_thu = 0
        tong_chi = 0
        for gd in self.ds_giaodich:
            if gd["year"] != nam or gd["month"] != thang:
                continue
            if self.laDoanhThu(gd["loai"]):
                tong_thu += gd["so_tien"]
            else:
                tong_chi += gd["so_tien"]
        return tong_thu, tong_chi
    def hienTong(self):
        tong_thu, tong_chi = self.tinhTong()
        loi_nhuan = tong_thu - tong_chi
        self.tongthu.setText(self.formatTien(tong_thu))
        self.tongchi.setText(self.formatTien(tong_chi))
        self.loinhuan.setText(self.formatTien(loi_nhuan))
    def doanhThuNam(self):
        nam = self.layNam()
        ds_thang = [0] * 12
        for gd in self.ds_giaodich:
            if gd["year"] == nam and self.laDoanhThu(gd["loai"]):
                ds_thang[gd["month"] - 1] += gd["so_tien"]
        return ds_thang
    def hienBieuDo(self):
        ds_thang = self.doanhThuNam()
        lon_nhat = max(ds_thang) if any(ds_thang) else 0
        for i, cot in enumerate(self.cot_bieu_do):
            x, y, w, h = self.thong_so_cot_goc[i]
            day = y + h
            gia_tri = ds_thang[i]
            if lon_nhat == 0 or gia_tri == 0:
                chieu_cao = self.chieu_cao_cot_nho_nhat
            else:
                ty_le = gia_tri / lon_nhat
                chieu_cao = max(self.chieu_cao_cot_nho_nhat, int(self.chieu_cao_cot_lon_nhat * ty_le))
            y_moi = day - chieu_cao
            cot.setGeometry(x, y_moi, w, chieu_cao)
            cot.setToolTip(f"Thang {i + 1}: {self.formatTien(gia_tri)}")
    def lamMoi(self):
        self.taiBang()
        self.hienTong()
        self.hienBieuDo()
    def them_giaodich(self):
        loai_giao_dich = self.loaigiaodich.currentText().strip()
        ngay_giao_dich = self.dategiaodich.date()
        so_tien = self.tachTien(self.sotiengiaodich.text())
        noi_dung = self.noidunggiaodich.text().strip()
        if loai_giao_dich == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn loại giao dịch trước khi thêm.")
            return
        if so_tien <= 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số tiền hợp lệ lớn hơn 0.")
            return
        if noi_dung == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập nội dung giao dịch.")
            return
        gd = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "loai": loai_giao_dich,
            "ngay": ngay_giao_dich.toString("dd/MM/yyyy"),
            "month": ngay_giao_dich.month(),
            "year": ngay_giao_dich.year(),
            "so_tien": so_tien,
            "noi_dung": noi_dung
        }
        self.ds_giaodich.append(gd)
        QuanLyThuNhap.records = self.ds_giaodich
        self.luuFile()
        self.lamMoi()
        self.sotiengiaodich.clear()
        self.noidunggiaodich.clear()
    def xoa_giaodich(self):
        item_dang_chon = self.bangghinhan.currentItem()
        if item_dang_chon is None:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một giao dịch trong bảng để xóa.")
            return
        ma_giao_dich = item_dang_chon.data(Qt.ItemDataRole.UserRole)
        for index, gd in enumerate(self.ds_giaodich):
            if gd["id"] == ma_giao_dich:
                del self.ds_giaodich[index]
                break
        QuanLyThuNhap.records = self.ds_giaodich
        self.luuFile()
        self.lamMoi()
