from PyQt6.QtWidgets import QWidget, QPushButton, QApplication
import sys
from PyQt6 import uic

from barang import formBarang
from pelanggan import formPlg
from pesanan import formPesanan
from pembayaran import formPembayaran

class formUtama(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("utama.ui", self)

        self.btn_brg=self.findChild(QPushButton, "btn_brg")
        self.btn_brg.clicked.connect(self.tampil_barang)

        self.btn_plg = self.findChild(QPushButton, "btn_plg")
        self.btn_plg.clicked.connect(self.tampil_pelanggan)

        self.btn_psn = self.findChild(QPushButton, "btn_psn")
        self.btn_psn.clicked.connect(self.tampil_pesanan)

        self.btn_byr = self.findChild(QPushButton, "btn_byr")
        self.btn_byr.clicked.connect(self.tampil_pembayaran)

    def tampil_barang(self):
        self.barang = formBarang()
        self.barang.show()

    def tampil_pelanggan(self):
        self.pelanggan = formPlg()
        self.pelanggan.show()

    def tampil_pesanan(self):
        self.pesanan = formPesanan()
        self.pesanan.show()

    def tampil_pembayaran(self):
        self.pembayaran = formPembayaran()
        self.pembayaran.show()

app = QApplication(sys.argv)
window = formUtama()
window.show()
sys.exit(app.exec())