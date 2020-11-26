-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 25, 2020 at 11:28 AM
-- Server version: 8.0.20-0ubuntu0.20.04.1
-- PHP Version: 7.4.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `perpus`
--
CREATE DATABASE IF NOT EXISTS `perpus` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `perpus`;

-- --------------------------------------------------------

--
-- Table structure for table `Buku`
--

DROP TABLE IF EXISTS `Buku`;
CREATE TABLE IF NOT EXISTS `Buku` (
  `Buku_ID` int NOT NULL AUTO_INCREMENT,
  `Buku_Judul` varchar(100) NOT NULL,
  `Buku_Pengarang` varchar(100) DEFAULT NULL,
  `Buku_Penerbitan` varchar(50) DEFAULT NULL,
  `Buku_Fisik` varchar(50) DEFAULT NULL,
  `Buku_Media` varchar(50) DEFAULT NULL,
  `Buku_Subjek` varchar(50) DEFAULT NULL,
  `Buku_Catatan` varchar(255) DEFAULT NULL,
  `Buku_Rak` varchar(20) DEFAULT NULL,
  `Buku_Copy` int NOT NULL,
  PRIMARY KEY (`Buku_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Buku`
--

INSERT INTO `Buku` (`Buku_ID`, `Buku_Judul`, `Buku_Pengarang`, `Buku_Penerbitan`, `Buku_Fisik`, `Buku_Media`, `Buku_Subjek`, `Buku_Catatan`, `Buku_Rak`, `Buku_Copy`) VALUES
(1, 'Buku Tesla', 'Tesla', 'Book', 'None', 'None', 'None', 'None', 'None', 5),
(2, 'buku Bumi', 'bumi', 'Buku', NULL, NULL, NULL, NULL, NULL, 5),
(3, 'buku Kipas', 'kipas', 'buku', NULL, NULL, NULL, NULL, NULL, 5);

-- --------------------------------------------------------

--
-- Table structure for table `Member`
--

DROP TABLE IF EXISTS `Member`;
CREATE TABLE IF NOT EXISTS `Member` (
  `Member_ID` varchar(20) NOT NULL,
  `Member_Name` varchar(30) NOT NULL,
  `Member_Alamat` varchar(100) NOT NULL,
  `Member_Level` int NOT NULL,
  PRIMARY KEY (`Member_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Member`
--

INSERT INTO `Member` (`Member_ID`, `Member_Name`, `Member_Alamat`, `Member_Level`) VALUES
('000000', 'Admin', 'Master', 2),
('000001', 'Yusuf', 'i dont have that', 1),
('000002', 'Herlangga', 'i Dont have Too', 1);

-- --------------------------------------------------------

--
-- Table structure for table `Transaksi`
--

DROP TABLE IF EXISTS `Transaksi`;
CREATE TABLE IF NOT EXISTS `Transaksi` (
  `Transaksi_ID` int NOT NULL AUTO_INCREMENT,
  `Transaksi_F_Time` date NOT NULL,
  `Transaksi_R_Time` date DEFAULT NULL,
  `Status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Dipinjam',
  `Member_ID` varchar(20) NOT NULL,
  `Buku_ID` int NOT NULL,
  PRIMARY KEY (`Transaksi_ID`,`Member_ID`,`Buku_ID`),
  KEY `fk_Transaksi_Member1_idx` (`Member_ID`),
  KEY `fk_Transaksi_Buku1_idx` (`Buku_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Transaksi`
--

INSERT INTO `Transaksi` (`Transaksi_ID`, `Transaksi_F_Time`, `Transaksi_R_Time`, `Status`, `Member_ID`, `Buku_ID`) VALUES
(1, '2020-06-23', NULL, 'Dipinjam', '000001', 3),
(2, '2020-06-23', NULL, 'Dipinjam', '000002', 2),
(3, '2020-06-23', NULL, 'Dipinjam', '000001', 2),
(4, '2020-06-23', NULL, 'Dipinjam', '000001', 2);

-- --------------------------------------------------------

--
-- Table structure for table `UserID`
--

DROP TABLE IF EXISTS `UserID`;
CREATE TABLE IF NOT EXISTS `UserID` (
  `UserID_Usr` varchar(20) NOT NULL,
  `UserID_Pwd` varchar(20) NOT NULL,
  `Member_ID` varchar(20) NOT NULL,
  PRIMARY KEY (`Member_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `UserID`
--

INSERT INTO `UserID` (`UserID_Usr`, `UserID_Pwd`, `Member_ID`) VALUES
('Admin', 'Admin', '000000'),
('Herlangga', '123456789', '000001'),
('yusuf', 'qwerty', '000002');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Transaksi`
--
ALTER TABLE `Transaksi`
  ADD CONSTRAINT `fk_Transaksi_Buku1` FOREIGN KEY (`Buku_ID`) REFERENCES `Buku` (`Buku_ID`),
  ADD CONSTRAINT `fk_Transaksi_Member1` FOREIGN KEY (`Member_ID`) REFERENCES `Member` (`Member_ID`);

--
-- Constraints for table `UserID`
--
ALTER TABLE `UserID`
  ADD CONSTRAINT `fk_UserID_Member` FOREIGN KEY (`Member_ID`) REFERENCES `Member` (`Member_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
