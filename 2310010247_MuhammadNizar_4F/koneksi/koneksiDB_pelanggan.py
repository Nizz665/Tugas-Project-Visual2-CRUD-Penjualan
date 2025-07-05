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

    def fetch_all(self, pelanggan):
        self.cursor.execute(f"SELECT * FROM {pelanggan}")
        data = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]
        return data, headers

    def fetch_allPDF(self, pelanggan):
        try:
            self.cursor.execute(f"SELECT * FROM pelanggan {pelanggan}")
            results = self.cursor.fetchall()
            print("Results fetched:", results)  # Tambahkan ini untuk debugging
            return results
        except pymysql.connector.Error as err:
            print(f"Kesalahan saat mengambil data : {err}")
            return []

    def tambah_pelanggan(self, id_pelanggan, nama_pelanggan, alamat, no_hp):
        self.cursor.execute("INSERT INTO pelanggan (id_pelanggan, nama_pelanggan,alamat, no_hp) "
                            "VALUES (%s, %s, %s, %s)", (id_pelanggan,nama_pelanggan, alamat, no_hp))
        self.connection.commit()

    def ubah_pelanggan(self, id_pelanggan, nama_pelanggan, alamat, no_hp):
        self.cursor.execute("UPDATE pelanggan SET alamat = %s, no_hp = %s, nama_pelanggan = %s  WHERE id_pelanggan = %s",
                            (alamat, no_hp, nama_pelanggan, id_pelanggan))
        self.connection.commit()

    def hapus_pelanggan(self, id_pelanggan ):
        self.cursor.execute("DELETE FROM pelanggan WHERE id_pelanggan = %s", (id_pelanggan))
        self.connection.commit()

    def close(self):
        self.connection.close()