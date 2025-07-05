from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMessageBox

from koneksi.koneksiDB_pembayaran import KoneksiDB
from model.model_pembayaran import TableModel

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class formPembayaran(QWidget):
    def __init__(self):
        super().__init__()

        # Memuat file .ui
        uic.loadUi("pembayaran.ui", self)

        # Instance DatabaseManager
        self.koneksiDB = KoneksiDB()
        data, headers = KoneksiDB().fetch_all("pembayaran")

        self.model = TableModel(data, headers)
        self.tabel_pembayaran.setModel(self.model)

        # Menyambungkan fungsi ke tombol
        self.btnSimpan.clicked.connect(self.add_data)
        self.btnUbah.clicked.connect(self.update_data)
        self.btnHapus.clicked.connect(self.delete_data)
        self.tabel_pembayaran.clicked.connect(self.on_table_click)
        self.btnCetak.clicked.connect(self.print_pdf)

    def load_data(self):
        try:
            data, headers = self.koneksiDB.fetch_all("pembayaran")
            self.model = TableModel(data, headers)
            self.tabel_pembayaran.setModel(self.model)
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")

    def add_data(self):
        kode_bayar = self.edit_kode_bayar.text()
        kode_pesanan = self.edit_kode_pesanan.text()
        tgl_bayar = self.edit_tgl_bayar.text()
        uang_bayar = self.edit_uang_bayar.text()
        uang_kembali = self.edit_uang_kembali.text()

        if kode_bayar and kode_pesanan and tgl_bayar and uang_bayar and uang_kembali:
            self.koneksiDB.tambah_pembayaran(kode_bayar, kode_pesanan, tgl_bayar, uang_bayar, uang_kembali)
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi")

    def update_data(self):
        kode_bayar = self.edit_kode_bayar.text()
        kode_pesanan = self.edit_kode_pesanan.text()
        tgl_bayar = self.edit_tgl_bayar.text()
        uang_bayar = self.edit_uang_bayar.text()
        uang_kembali = self.edit_uang_kembali.text()

        if kode_bayar and kode_pesanan and tgl_bayar and uang_bayar and uang_kembali:
            try:
                self.koneksiDB.ubah_pembayaran(kode_bayar, kode_pesanan, tgl_bayar, uang_bayar, uang_kembali)
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
                self.load_data()
                self.clear_inputs()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Kesalahan saat mengubah data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Semua data harus diisi dan baris harus dipilih.")

    def delete_data(self):
        kode_bayar = self.edit_kode_bayar.text()
        self.koneksiDB.hapus_pembayaran(kode_bayar)
        self.load_data()
        self.clear_inputs()

    def clear_inputs(self):
        self.edit_kode_bayar.clear()
        self.edit_kode_pesanan.clear()
        self.edit_tgl_bayar.clear()
        self.edit_uang_bayar.clear()
        self.edit_uang_kembali.clear()

    def on_table_click(self, index):
        try:
            row = index.row()
            if row < 0 or row >= len(self.model._data):
                raise ValueError("Indeks baris tidak valid.")

            record = self.model._data[row]
            if not record or len(record) < 5:
                raise ValueError("Data baris tidak lengkap.")

            kode_bayar, kode_pesanan, tgl_bayar, uang_bayar, uang_kembali = map(str, record[:5])

            self.edit_kode_bayar.setText(kode_bayar)
            self.edit_kode_pesanan.setText(kode_pesanan)
            self.edit_tgl_bayar.setText(tgl_bayar)
            self.edit_uang_bayar.setText(uang_bayar)
            self.edit_uang_kembali.setText(uang_kembali)
        except ValueError as ve:
            QMessageBox.warning(self, "Kesalahan", str(ve))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def print_pdf(self):
        try:
            data = self.koneksiDB.fetch_allPDF("pembayaran")

            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "data_pembayaran_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 40, "Laporan Pembayaran")

            def draw_table_header(c, y):
                headers = ["Kode Bayar", "Kode Pesanan", "Tanggal Bayar", "Uang Bayar", "Uang Kembali"]
                col_widths = [80, 100, 120, 90, 90]
                x = 50
                c.setFont("Helvetica-Bold", 10)
                for header, width_col in zip(headers, col_widths):
                    c.drawString(x, y, header)
                    x += width_col
                c.line(50, y - 5, width - 50, y - 5)

            y_position = height - 60
            draw_table_header(c, y_position)
            y_position -= 20

            col_widths = [80, 100, 120, 90, 90]
            row_count = 0

            for row in data:
                if len(row) >= 5:
                    c.setFont("Helvetica", 10)
                    x = 50
                    for cell, width_col in zip(row, col_widths):
                        c.drawString(x, y_position, str(cell))
                        x += width_col

                    y_position -= 18
                    row_count += 1

                    if y_position < 100:
                        c.showPage()
                        c.setFont("Helvetica-Bold", 14)
                        c.drawString(50, height - 40, "Laporan Pembayaran")
                        y_position = height - 60
                        draw_table_header(c, y_position)
                        y_position -= 20

            c.save()
            QMessageBox.information(self, "Sukses", f"Laporan berhasil disimpan ke {pdf_file}")
        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Gagal mencetak PDF: {e}")

    def closeEvent(self, event):
        self.koneksiDB.close()
        event.accept()
