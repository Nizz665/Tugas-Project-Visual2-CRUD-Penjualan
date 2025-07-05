import pymysql
from mysql.connector import Error

class KoneksiDB:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',  # Ganti dengan username MySQL Anda
                password='',  # Ganti dengan password MySQL Anda
                database='muhammad-nizar_2310010247_penjualan'  # Ganti dengan nama database Anda
            )

            # Memastikan koneksi berhasil
            if self.connection.open:
                print("Koneksi berhasil")
                self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    def fetch_all(self, pesanan):
        self.cursor.execute(f"SELECT * FROM {pesanan}")
        data = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]
        return data, headers

    def fetch_allPDF(self, pesanan):
        try:
            self.cursor.execute(f"SELECT * FROM pesanan {pesanan}")
            results = self.cursor.fetchall()
            print("Results fetched:", results)  # Tambahkan ini untuk debugging
            return results
        except pymysql.connector.Error as err:
            print(f"Kesalahan saat mengambil data : {err}")
            return []

    def tambah_pesanan(self, kode_pesanan, kode_barang, kode_pelanggan, tgl_pesanan, harga, jml_beli, total_bayar):

        self.cursor.execute("INSERT INTO pesanan (kode_pesanan, kode_barang, kode_pelanggan, tgl_pesanan, harga, jml_beli, total_bayar)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (kode_pesanan, kode_barang, kode_pelanggan, tgl_pesanan, harga, jml_beli, total_bayar))
        self.connection.commit()

    def ubah_pesanan(self, kode_pesanan, kode_barang, kode_pelanggan, tgl_pesanan, harga, jml_beli, total_bayar):
        self.cursor.execute("UPDATE pesanan SET kode_barang = %s, kode_pelanggan = %s, tgl_pesanan = %s, harga = %s, jml_beli = %s, total_bayar = %s WHERE kode_pesanan = %s",
                            (kode_barang, kode_pelanggan, tgl_pesanan, harga, jml_beli, total_bayar, kode_pesanan))
        self.connection.commit()

    def hapus_pesanan(self, kode_pesanan ):
        self.cursor.execute("DELETE FROM pesanan WHERE kode_pesanan = %s", (kode_pesanan))
        self.connection.commit()

    def close(self):
        self.connection.close()