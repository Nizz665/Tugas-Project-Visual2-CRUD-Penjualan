-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.7.2-MariaDB-log - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for muhammad-nizar_2310010247_penjualan
CREATE DATABASE IF NOT EXISTS `muhammad-nizar_2310010247_penjualan` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `muhammad-nizar_2310010247_penjualan`;

-- Dumping structure for table muhammad-nizar_2310010247_penjualan.barang
CREATE TABLE IF NOT EXISTS `barang` (
  `kode_barang` varchar(20) NOT NULL,
  `nama_barang` varchar(50) NOT NULL,
  `stok_barang` varchar(50) NOT NULL,
  `harga_barang` varchar(100) NOT NULL,
  PRIMARY KEY (`kode_barang`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table muhammad-nizar_2310010247_penjualan.barang: ~1 rows (approximately)
INSERT INTO `barang` (`kode_barang`, `nama_barang`, `stok_barang`, `harga_barang`) VALUES
	('BRG001', 'Samsung Galaxy A15', '10', '2500000');

-- Dumping structure for table muhammad-nizar_2310010247_penjualan.pelanggan
CREATE TABLE IF NOT EXISTS `pelanggan` (
  `id_pelanggan` varchar(20) NOT NULL,
  `nama_pelanggan` varchar(50) NOT NULL,
  `alamat` varchar(50) NOT NULL,
  `no_hp` varchar(15) NOT NULL,
  PRIMARY KEY (`id_pelanggan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table muhammad-nizar_2310010247_penjualan.pelanggan: ~1 rows (approximately)
INSERT INTO `pelanggan` (`id_pelanggan`, `nama_pelanggan`, `alamat`, `no_hp`) VALUES
	('PLG001', 'Muhammad Nizar', 'Jl. Subur Bastari', '083133238449');

-- Dumping structure for table muhammad-nizar_2310010247_penjualan.pembayaran
CREATE TABLE IF NOT EXISTS `pembayaran` (
  `kode_bayar` varchar(25) NOT NULL,
  `kode_pesanan` varchar(25) NOT NULL,
  `tgl_bayar` varchar(50) NOT NULL,
  `uang_bayar` varchar(50) NOT NULL,
  `uang_kembali` varchar(50) NOT NULL,
  PRIMARY KEY (`kode_bayar`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table muhammad-nizar_2310010247_penjualan.pembayaran: ~1 rows (approximately)
INSERT INTO `pembayaran` (`kode_bayar`, `kode_pesanan`, `tgl_bayar`, `uang_bayar`, `uang_kembali`) VALUES
	('BYR001', 'PSN001', '28-06-2025', '6000000', '1000000');

-- Dumping structure for table muhammad-nizar_2310010247_penjualan.pesanan
CREATE TABLE IF NOT EXISTS `pesanan` (
  `kode_pesanan` varchar(25) NOT NULL,
  `kode_barang` varchar(20) NOT NULL,
  `kode_pelanggan` varchar(20) NOT NULL,
  `tgl_pesanan` varchar(20) NOT NULL,
  `harga` varchar(20) NOT NULL,
  `jml_beli` varchar(20) NOT NULL,
  `total_bayar` varchar(20) NOT NULL,
  PRIMARY KEY (`kode_pesanan`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table muhammad-nizar_2310010247_penjualan.pesanan: ~1 rows (approximately)
INSERT INTO `pesanan` (`kode_pesanan`, `kode_barang`, `kode_pelanggan`, `tgl_pesanan`, `harga`, `jml_beli`, `total_bayar`) VALUES
	('PSN001', 'BRG001', 'PLG001', '28-06-2025', '2500000', '2', '5000000');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
