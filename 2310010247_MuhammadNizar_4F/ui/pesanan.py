from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMessageBox
from koneksi.koneksiDB_pesanan import KoneksiDB
from model.model_pesanan import TableModel
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

class formPesanan(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("pesanan.ui", self)

        self.koneksiDB = KoneksiDB()
        data, headers = self.koneksiDB.fetch_all("pesanan")
        self.model = TableModel(data, headers)
        self.tabel_pesanan.setModel(self.model)

        self.btnSimpan.clicked.connect(self.add_data)
        self.btnUbah.clicked.connect(self.update_data)
        self.btnHapus.clicked.connect(self.delete_data)
        self.tabel_pesanan.clicked.connect(self.on_table_click)
        self.btnCetak.clicked.connect(self.print_pdf)

        self.load_data()

    def load_data(self):
        try:
            data, headers = self.koneksiDB.fetch_all("pesanan")
            self.model = TableModel(data, headers)
            self.tabel_pesanan.setModel(self.model)
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")

    def add_data(self):
        kode_pesanan = self.edit_kode_pesanan.text()
        kode_barang = self.edit_kode_barang.text()
        kode_pelanggan = self.edit_kode_pelanggan.text()
        tgl_pesanan = self.edit_tgl_pesanan.text()
        harga = self.edit_harga.text()
        jml_beli = self.edit_jml_beli.text()
        total_bayar = self.edit_total_bayar.text()

        if all([kode_pesanan, kode_barang, kode_pelanggan, tgl_pesanan, harga, jml_beli, total_bayar]):
            try:
                self.koneksiDB.tambah_pesanan(kode_pesanan, kode_barang, kode_pelanggan, tgl_pesanan, harga, jml_beli, total_bayar)
                self.clear_inputs()
                self.load_data()
                QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menambah data: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi")

    def update_data(self):
        kode_pesanan = self.edit_kode_pesanan.text()
        kode_barang = self.edit_kode_barang.text()
        kode_pelanggan = self.edit_kode_pelanggan.text()
        tgl_pesanan = self.edit_tgl_pesanan.text()
        harga = self.edit_harga.text()
        jml_beli = self.edit_jml_beli.text()
        total_bayar = self.edit_total_bayar.text()

        if all([kode_pesanan, kode_barang, kode_pelanggan, tgl_pesanan, harga, jml_beli, total_bayar]):
            try:
                self.koneksiDB.ubah_pesanan(kode_pesanan, kode_barang, kode_pelanggan, tgl_pesanan, harga, jml_beli, total_bayar)
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
                self.load_data()
                self.clear_inputs()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Kesalahan saat mengubah data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Semua data harus diisi.")

    def delete_data(self):
        kode_pesanan = self.edit_kode_pesanan.text()
        if kode_pesanan:
            try:
                self.koneksiDB.hapus_pesanan(kode_pesanan)
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Gagal menghapus data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus.")

    def clear_inputs(self):
        self.edit_kode_pesanan.clear()
        self.edit_kode_barang.clear()
        self.edit_kode_pelanggan.clear()
        self.edit_tgl_pesanan.clear()
        self.edit_harga.clear()
        self.edit_jml_beli.clear()
        self.edit_total_bayar.clear()

    def on_table_click(self, index):
        try:
            row = index.row()
            if row < 0 or row >= len(self.model._data):
                raise ValueError("Indeks baris tidak valid.")

            record = self.model._data[row]
            if len(record) < 7:
                raise ValueError("Data baris tidak lengkap.")

            kode_pesanan, kode_barang, kode_pelanggan, tgl_pesanan, harga, jml_beli, total_bayar = map(str, record[:7])

            self.edit_kode_pesanan.setText(kode_pesanan)
            self.edit_kode_barang.setText(kode_barang)
            self.edit_kode_pelanggan.setText(kode_pelanggan)
            self.edit_tgl_pesanan.setText(tgl_pesanan)
            self.edit_harga.setText(harga)
            self.edit_jml_beli.setText(jml_beli)
            self.edit_total_bayar.setText(total_bayar)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def print_pdf(self):
        try:
            data = self.koneksiDB.fetch_allPDF("semua")
            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            headers = ["Kode Pesanan", "Kode Barang", "Kode Pelanggan", "Tgl Pesanan", "Harga", "Jumlah Beli", "Total Bayar"]
            col_widths = [100, 100, 100, 100, 80, 80, 100]
            row_height = 22
            pdf_file = "data_pesanan_report.pdf"
            page_width = sum(col_widths) + 100
            page_height = 11 * inch

            c = canvas.Canvas(pdf_file, pagesize=(page_width, page_height))
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, page_height - 40, "Laporan Data Pesanan")

            def draw_table_header(c, y_pos):
                c.setFont("Helvetica-Bold", 9)
                x_pos = 50
                for header, col_width in zip(headers, col_widths):
                    c.drawString(x_pos, y_pos, header)
                    x_pos += col_width
                c.line(50, y_pos - 5, page_width - 50, y_pos - 5)

            y = page_height - 60
            draw_table_header(c, y)
            y -= row_height

            for row in data:
                if len(row) >= 7:
                    c.setFont("Helvetica", 8)
                    x = 50
                    for item, col_width in zip(row[:7], col_widths):
                        text = str(item)
                        if len(text) > col_width // 6:
                            text = text[:col_width // 6 - 3] + "..."
                        c.drawString(x, y, text)
                        x += col_width
                    y -= row_height
                    if y < 50:
                        c.showPage()
                        c.setFont("Helvetica-Bold", 14)
                        c.drawString(50, page_height - 40, "Laporan Data Pesanan")
                        y = page_height - 60
                        draw_table_header(c, y)
                        y -= row_height

            c.save()
            QMessageBox.information(self, "Sukses", f"Laporan berhasil dicetak ke {pdf_file}")
        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat mencetak PDF: {e}")

    def closeEvent(self, event):
        self.koneksiDB.close()
        event.accept()
