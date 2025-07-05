from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMessageBox
from koneksi.koneksiDB_barang import KoneksiDB
from model.model_barang import TableModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class formBarang(QWidget):  # Diubah dari formBrg
    def __init__(self):
        super().__init__()
        uic.loadUi("barang.ui", self)

        self.koneksiDB = KoneksiDB()
        data, headers = self.koneksiDB.fetch_all("barang")
        self.model = TableModel(data, headers)
        self.tabel_barang.setModel(self.model)

        # Event binding
        self.btnSimpan.clicked.connect(self.add_data)
        self.btnUbah.clicked.connect(self.update_data)
        self.btnHapus.clicked.connect(self.delete_data)
        self.tabel_barang.clicked.connect(self.on_table_click)
        self.btnCetak.clicked.connect(self.print_pdf)

        self.load_data()

    def load_data(self):
        try:
            data, headers = self.koneksiDB.fetch_all("barang")
            self.model = TableModel(data, headers)
            self.tabel_barang.setModel(self.model)
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")

    def add_data(self):
        kode_barang  = self.edit_kode_barang.text()
        nama_barang = self.edit_nama_barang.text()
        stok_barang = self.edit_stok_barang.text()
        harga_barang = self.edit_harga_barang.text()
        if kode_barang and nama_barang and stok_barang and harga_barang:
            try:
                self.koneksiDB.tambah_barang(kode_barang, nama_barang, stok_barang, harga_barang)
                self.clear_inputs()
                self.load_data()
                QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menambah data: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi")

    def update_data(self):
        kode_barang = self.edit_kode_barang.text()
        nama_barang = self.edit_nama_barang.text()
        stok_barang = self.edit_stok_barang.text()
        harga_barang = self.edit_harga_barang.text()
        if kode_barang and nama_barang and stok_barang and harga_barang:
            try:
                self.koneksiDB.ubah_barang(kode_barang, nama_barang, stok_barang, harga_barang)
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
                self.load_data()
                self.clear_inputs()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Kesalahan saat mengubah data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Semua data harus diisi.")

    def delete_data(self):
        kode_barang = self.edit_kode_barang.text()
        if kode_barang:
            try:
                self.koneksiDB.hapus_barang(kode_barang)
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Gagal menghapus data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus.")

    def clear_inputs(self):
        self.edit_kode_barang.clear()
        self.edit_nama_barang.clear()
        self.edit_stok_barang.clear()
        self.edit_harga_barang.clear()

    def on_table_click(self, index):
        try:
            row = index.row()
            if row < 0 or row >= len(self.model._data):
                raise ValueError("Indeks baris tidak valid.")

            record = self.model._data[row]
            if not record or len(record) < 4:
                raise ValueError("Data baris tidak lengkap.")

            kode_barang, nama_barang, stok_barang, harga_barang = map(str, record[:4])
            self.edit_kode_barang.setText(kode_barang)
            self.edit_nama_barang.setText(nama_barang)
            self.edit_stok_barang.setText(stok_barang)
            self.edit_harga_barang.setText(harga_barang)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def print_pdf(self):
        try:
            data = self.koneksiDB.fetch_allPDF("semua")
            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "data_barang_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 40, "Laporan Data Barang")

            def draw_table_header(c, y_position):
                c.setFont("Helvetica-Bold", 10)
                headers = ["Kode", "Nama Barang", "Stok", "Harga"]
                col_widths = [80, 200, 80, 100]
                x = 50
                for header, width in zip(headers, col_widths):
                    c.drawString(x, y_position, header)
                    x += width
                c.line(50, y_position - 5, width - 50, y_position - 5)

            y_position = height - 60
            draw_table_header(c, y_position)
            y_position -= 20
            col_widths = [80, 200, 80, 100]

            for row in data:
                if len(row) >= 4:
                    c.setFont("Helvetica", 10)
                    x = 50
                    for cell, col_width in zip(row[:4], col_widths):
                        c.drawString(x, y_position, str(cell))
                        x += col_width

                    y_position -= 18
                    if y_position < 50:
                        c.showPage()
                        c.setFont("Helvetica-Bold", 14)
                        c.drawString(50, height - 40, "Laporan Data Barang")
                        y_position = height - 60
                        draw_table_header(c, y_position)
                        y_position -= 20

            c.save()
            QMessageBox.information(self, "Sukses", f"Laporan telah dicetak ke {pdf_file}")

        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat mencetak PDF: {e}")

    def closeEvent(self, event):
        self.koneksiDB.close()
        event.accept()
