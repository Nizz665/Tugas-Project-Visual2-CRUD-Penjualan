import pymysql

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

    def fetch_all(self, barang):
        self.cursor.execute(f"SELECT * FROM {barang}")
        data = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]
        return data, headers

    def fetch_allPDF(self, barang):
        try:
            self.cursor.execute(f"SELECT * FROM barang {barang}")
            results = self.cursor.fetchall()
            print("Results fetched:", results)  # Tambahkan ini untuk debugging
            return results
        except pymysql.connector.Error as err:
            print(f"Kesalahan saat mengambil data : {err}")
            return []

    def tambah_barang(self, kode_barang, nama_barang, stok_barang, harga_barang):
        self.cursor.execute("INSERT INTO barang (kode_barang, nama_barang, stok_barang, harga_barang) VALUES (%s, %s, %s, %s)", (kode_barang, nama_barang, stok_barang, harga_barang))
        self.connection.commit()

    def ubah_barang(self, kode_barang, nama_barang, stok_barang, harga_barang):
        self.cursor.execute("UPDATE barang SET nama_barang = %s, stok_barang = %s, harga_barang = %s  WHERE kode_barang = %s",(nama_barang, stok_barang, harga_barang, kode_barang))
        self.connection.commit()

    def hapus_barang(self, kode_barang ):
        self.cursor.execute("DELETE FROM barang WHERE kode_barang  = %s", (kode_barang))
        self.connection.commit()

    def close(self):
        self.connection.close()