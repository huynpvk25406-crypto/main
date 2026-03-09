from PyQt6.QtWidgets import QApplication
from code import DangNhap
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DangNhap()
    w.show()
    sys.exit(app.exec())