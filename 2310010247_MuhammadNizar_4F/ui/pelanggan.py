from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMessageBox

from koneksi.koneksiDB_pelanggan import KoneksiDB
from model.model_pelanggan import TableModel

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class formPlg(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("pelanggan.ui", self)

        self.koneksiDB = KoneksiDB()
        data, headers = self.koneksiDB.fetch_all("pelanggan")

        self.model = TableModel(data, headers)
        self.tabel_pelanggan.setModel(self.model)

        # Event handling
        self.btnSimpan.clicked.connect(self.add_data)
        self.btnUbah.clicked.connect(self.update_data)
        self.btnHapus.clicked.connect(self.delete_data)
        self.tabel_pelanggan.clicked.connect(self.on_table_click)
        self.btnCetak.clicked.connect(self.print_pdf)

        self.load_data()

    def load_data(self):
        try:
            data, headers = self.koneksiDB.fetch_all("pelanggan")
            self.model = TableModel(data, headers)
            self.tabel_pelanggan.setModel(self.model)
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")

    def add_data(self):
        id_pelanggan  = self.edit_id_pelanggan.text()
        nama_pelanggan = self.edit_nama_pelanggan.text()
        alamat = self.edit_alamat.text()
        no_hp = self.edit_no_hp.text()
        if id_pelanggan and nama_pelanggan and alamat and no_hp:
            self.koneksiDB.tambah_pelanggan(id_pelanggan ,nama_pelanggan , alamat, no_hp)
            self.load_data()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi")

    def update_data(self):
        id_pelanggan = self.edit_id_pelanggan.text()
        nama_pelanggan = self.edit_nama_pelanggan.text()
        alamat = self.edit_alamat.text()
        no_hp = self.edit_no_hp.text()
        if id_pelanggan and nama_pelanggan and alamat and no_hp:
            try:
                self.koneksiDB.ubah_pelanggan(id_pelanggan, nama_pelanggan, alamat, no_hp)
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
                self.load_data()
                self.clear_inputs()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Kesalahan saat mengubah data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Semua data harus diisi.")

    def delete_data(self):
        id_pelanggan = self.edit_id_pelanggan.text()
        if id_pelanggan:
            try:
                self.koneksiDB.hapus_pelanggan(id_pelanggan)
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Gagal menghapus data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus.")

    def clear_inputs(self):
        self.edit_id_pelanggan.clear()
        self.edit_nama_pelanggan.clear()
        self.edit_alamat.clear()
        self.edit_no_hp.clear()

    def on_table_click(self, index):
        try:
            row = index.row()
            if row < 0 or row >= len(self.model._data):
                raise ValueError("Indeks baris tidak valid.")

            record = self.model._data[row]
            if not record or len(record) < 4:
                raise ValueError("Data baris tidak lengkap.")

            id_pelanggan, nama_pelanggan, alamat, no_hp = map(str, record[:4])

            self.edit_id_pelanggan.setText(id_pelanggan)
            self.edit_nama_pelanggan.setText(nama_pelanggan)
            self.edit_alamat.setText(alamat)
            self.edit_no_hp.setText(no_hp)

        except ValueError as ve:
            print(f"Kesalahan validasi: {ve}")
            QMessageBox.warning(self, "Kesalahan", str(ve))
        except Exception as e:
            print(f"Kesalahan saat memproses klik: {e}")
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def print_pdf(self):
        try:
            data = self.koneksiDB.fetch_allPDF("semua")

            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "data_pelanggan_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 40, "Laporan Data Pelanggan")

            def draw_table_header(c, y_position):
                c.setFont("Helvetica-Bold", 10)
                headers = ["ID", "Nama", "Alamat", "No Hp"]
                col_widths = [50, 120, 200, 100]
                x_position = 50
                for header, col_width in zip(headers, col_widths):
                    c.drawString(x_position, y_position, header)
                    x_position += col_width
                c.line(50, y_position - 5, width - 50, y_position - 5)

            y_position = height - 60
            draw_table_header(c, y_position)
            y_position -= 20

            col_widths = [50, 120, 200, 100]
            row_count = 0

            for row in data:
                if len(row) >= 4:
                    c.setFont("Helvetica", 10)
                    x_position = 50
                    for cell, col_width in zip(row[:4], col_widths):
                        c.drawString(x_position, y_position, str(cell))
                        x_position += col_width

                    y_position -= 18
                    row_count += 1

                    if y_position < 50:
                        c.showPage()
                        c.setFont("Helvetica-Bold", 14)
                        c.drawString(50, height - 40, "Laporan Data Pelanggan")
                        y_position = height - 60
                        draw_table_header(c, y_position)
                        y_position -= 20

            c.save()
            QMessageBox.information(self, "Sukses", f"Laporan telah dicetak ke {pdf_file}")
        except Exception as e:
            print(f"Kesalahan saat mencetak PDF: {e}")
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat mencetak PDF: {e}")

    def closeEvent(self, event):
        self.koneksiDB.close()
        event.accept()
