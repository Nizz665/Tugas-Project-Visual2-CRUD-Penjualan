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

    def fetch_all(self, pembayaran):
        self.cursor.execute(f"SELECT * FROM {pembayaran}")
        data = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]
        return data, headers

    def fetch_allPDF(self, pembayaran):
        try:
            self.cursor.execute(f"SELECT * FROM pembayaran")
            results = self.cursor.fetchall()
            print("Results fetched:", results)  # Tambahkan ini untuk debugging
            return results
        except pymysql.connector.Error as err:
            print(f"Kesalahan saat mengambil data : {err}")
            return []

    def tambah_pembayaran(self, kode_bayar, kode_pesanan, tgl_bayar, uang_bayar, uang_kembali):
        self.cursor.execute("INSERT INTO pembayaran (kode_bayar, kode_pesanan, tgl_bayar, uang_bayar, uang_kembali) "
                            "VALUES (%s, %s, %s, %s, %s)", (kode_bayar, kode_pesanan, tgl_bayar, uang_bayar, uang_kembali))
        self.connection.commit()

    def ubah_pembayaran(self, kode_bayar, kode_pesanan, tgl_bayar, uang_bayar, uang_kembali):
        self.cursor.execute("UPDATE pembayaran SET kode_pesanan = %s, tgl_bayar = %s, uang_bayar = %s, uang_kembali = %s WHERE kode_bayar = %s",
                            (kode_pesanan, tgl_bayar, uang_bayar, uang_kembali, kode_bayar))
        self.connection.commit()

    def hapus_pembayaran(self, kode_bayar ):
        self.cursor.execute("DELETE FROM pembayaran WHERE kode_bayar = %s", (kode_bayar))
        self.connection.commit()

    def close(self):
        self.connection.close()