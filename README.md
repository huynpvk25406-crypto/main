#  HỆ THỐNG QUẢN LÝ BÁN HÀNG THỜI TRANG (DESKTOP APP)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green)
![Status](https://img.shields.io/badge/Status-Hoàn%20thành-success)

---

##  Giới thiệu

Đây là hệ thống quản lý bán hàng thời trang được xây dựng dưới dạng **ứng dụng desktop** sử dụng **PyQt6**.
Hệ thống hỗ trợ quản lý toàn diện từ sản phẩm, kho hàng, đơn hàng đến nhân viên và doanh thu.

---

##  Chức năng chính

###  Người dùng

* Xem sản phẩm
* Thêm vào giỏ hàng
* Thanh toán (COD / QR)

###  Quản trị viên

* Quản lý sản phẩm (thêm / sửa / xóa)
* Quản lý tồn kho
* Quản lý nhân viên
* Quản lý doanh thu

---

##  Thiết kế giao diện (Figma)

 Link Figma:
https://www.figma.com/design/k6w9qz3VUFy57wrt8C8pDP/Figma-basics

###  Mô tả thiết kế

* Thiết kế layout trước khi lập trình
* Xây dựng luồng người dùng (user flow)
* Đảm bảo UI/UX trực quan, dễ sử dụng

###  Các màn hình chính

*  Đăng nhập / đăng ký
*  Trang chủ (banner tự động)
*  Danh sách sản phẩm
*  Chi tiết sản phẩm
*  Giỏ hàng
*  Thanh toán (COD + QR)
*  Trang quản lý
*  Quản lý kho
*  Quản lý nhân viên
*  Quản lý doanh thu

---

##  Công nghệ sử dụng

* Python
* PyQt6
* JSON (lưu trữ dữ liệu)
* Qt Designer

---

##  Cấu trúc thư mục

```
project/
│── data/
│   ├── user.json
│   ├── products.json
│   ├── nhanvien.json
│   ├── doanhthu.json
│
│── image/
│── *.py
```

---

##  Hướng dẫn chạy chương trình

### 1. Clone project

```
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Cài thư viện

```
pip install PyQt6
```

### 3. Chạy chương trình

```
python main.py
```

---

##  Tài khoản demo

```
admin1 / 123
admin2 / 123
```

---

##  Logic hệ thống

* Giỏ hàng lưu tạm trong bộ nhớ (list)
* Kiểm tra tồn kho trước khi thanh toán
* Tự động trừ số lượng sau khi đặt hàng
* Cập nhật doanh thu theo tháng

---

##  Lưu trữ dữ liệu

Hệ thống sử dụng JSON:

* `products.json` → sản phẩm
* `user.json` → tài khoản
* `nhanvien.json` → nhân viên
* `doanhthu.json` → doanh thu

---

##  Kết luận

Hệ thống đã xây dựng đầy đủ chức năng quản lý bán hàng thời trang từ cơ bản đến nâng cao.
Việc kết hợp thiết kế Figma và lập trình PyQt6 giúp hệ thống có giao diện trực quan và dễ sử dụng.

---
