-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: btb_trip_db
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bus_models`
--

DROP TABLE IF EXISTS `bus_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_models` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `total_seats` int NOT NULL,
  `deck_count` int NOT NULL DEFAULT '1',
  `status` varchar(8) NOT NULL DEFAULT 'ACTIVE',
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_models`
--

LOCK TABLES `bus_models` WRITE;
/*!40000 ALTER TABLE `bus_models` DISABLE KEYS */;
INSERT INTO `bus_models` VALUES 
(1,'Sleeper 40 (2-deck)',40,2,'ACTIVE','2025-11-12 16:39:01','2025-11-12 16:39:01'),
(2,'Seater 45 (1-deck)',20,1,'ACTIVE','2025-11-12 16:39:01','2025-11-12 16:39:01');
/*!40000 ALTER TABLE `bus_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `buses`
--

DROP TABLE IF EXISTS `buses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buses` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bus_model_id` bigint NOT NULL,
  `plate_number` varchar(15) NOT NULL,
  `status` varchar(11) NOT NULL DEFAULT 'ACTIVE',
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `plate_number` (`plate_number`),
  KEY `ix_buses_bus_model_id` (`bus_model_id`),
  CONSTRAINT `buses_ibfk_1` FOREIGN KEY (`bus_model_id`) REFERENCES `bus_models` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buses`
--

LOCK TABLES `buses` WRITE;
/*!40000 ALTER TABLE `buses` DISABLE KEYS */;
INSERT INTO `buses` VALUES 
(1,1,'92N1-123456','ACTIVE','2025-11-12 16:47:49','2025-11-12 16:47:49'),
(2,2,'92N1-123444','ACTIVE','2025-11-12 16:47:49','2025-11-12 16:47:49'),
(3,1,'51B-123.45','ACTIVE','2025-11-12 17:21:42','2025-11-12 17:21:42'),

(4,1,'51B-678.90','ACTIVE','2025-11-12 17:21:42','2025-11-12 17:21:42'),

(5,2,'65B-111.22','ACTIVE','2025-11-12 17:21:42','2025-11-12 17:21:42'),

(6,1,'72B-555.66','ACTIVE','2025-11-12 17:21:42','2025-11-12 17:21:42');
/*!40000 ALTER TABLE `buses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `routes`
--

DROP TABLE IF EXISTS `routes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `routes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `origin` varchar(100) NOT NULL,
  `origin_code` varchar(100) DEFAULT NULL,
  `destination` varchar(100) NOT NULL,
  `destination_code` varchar(100) DEFAULT NULL,
  `base_price` decimal(10,2) NOT NULL,
  `distance_km` decimal(6,1) DEFAULT NULL,
  `estimated_duration` int DEFAULT NULL,
  `status` varchar(8) NOT NULL DEFAULT 'ACTIVE',
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_routes_origin_destination` (`origin`,`destination`),
  UNIQUE KEY `uq_routes_origincode_destinationcode` (`origin_code`,`destination_code`),
  KEY `ix_routes_destination` (`destination`),
  KEY `ix_routes_origin_code` (`origin_code`),
  KEY `ix_routes_destination_code` (`destination_code`),
  KEY `ix_routes_origin` (`origin`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `routes`
--

LOCK TABLES `routes` WRITE;
/*!40000 ALTER TABLE `routes` DISABLE KEYS */;
INSERT INTO `routes` VALUES 
(1,'TP. Hồ Chí Minh','tp-ho-chi-minh','Đà Nẵng','da-nang',850000.00,960.0,1150,'ACTIVE','2025-11-12 16:37:56','2025-11-12 16:37:56'),
(2,'TP. Hồ Chí Minh','tp-ho-chi-minh','Huế','hue',920000.00,1050.0,1260,'ACTIVE','2025-11-12 16:37:56','2025-11-12 16:37:56'),
(3,'TP. Hồ Chí Minh','tp-ho-chi-minh','Quy Nhơn','quy-nhon',650000.00,650.0,780,'ACTIVE','2025-11-12 16:37:56','2025-11-12 16:37:56'),
(4,'TP. Hồ Chí Minh','tp-ho-chi-minh','Hà Nội','ha-noi',1200000.00,1700.0,2040,'ACTIVE','2025-11-12 16:37:56','2025-11-12 16:37:56'),
(5,'Cần Thơ','can-tho','Đà Nẵng','da-nang',900000.00,1100.0,1320,'ACTIVE','2025-11-12 16:37:56','2025-11-12 16:37:56'),
(6,'Vũng Tàu','vung-tau','Nha Trang','nha-trang',420000.00,500.0,600,'ACTIVE','2025-11-12 16:37:56','2025-11-12 16:37:56'),
(30,'TP. Hồ Chí Minh','tp-ho-chi-minh','Nha Trang','nha-trang',350000.00,430.0,520,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(31,'TP. Hồ Chí Minh','tp-ho-chi-minh','Phan Rang','phan-rang',280000.00,340.0,410,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(32,'TP. Hồ Chí Minh','tp-ho-chi-minh','Phan Thiết','phan-thiet',220000.00,200.0,250,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(33,'TP. Hồ Chí Minh','tp-ho-chi-minh','Buôn Ma Thuột','buon-ma-thuot',320000.00,320.0,390,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(34,'TP. Hồ Chí Minh','tp-ho-chi-minh','Pleiku','pleiku',600000.00,630.0,760,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(35,'TP. Hồ Chí Minh','tp-ho-chi-minh','Đà Lạt','da-lat',300000.00,310.0,380,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(36,'TP. Hồ Chí Minh','tp-ho-chi-minh','Vinh','vinh',1100000.00,1350.0,1620,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(37,'TP. Hồ Chí Minh','tp-ho-chi-minh','Đồng Hới','dong-hoi',980000.00,1200.0,1440,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(38,'TP. Hồ Chí Minh','tp-ho-chi-minh','Hải Phòng','hai-phong',1250000.00,1750.0,2100,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(39,'TP. Hồ Chí Minh','tp-ho-chi-minh','Thanh Hóa','thanh-hoa',1150000.00,1500.0,1800,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(40,'TP. Hồ Chí Minh','tp-ho-chi-minh','Ninh Bình','ninh-binh',1180000.00,1600.0,1920,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(41,'Cần Thơ','can-tho','Nha Trang','nha-trang',450000.00,600.0,720,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(42,'Cần Thơ','can-tho','Quy Nhơn','quy-nhon',700000.00,820.0,980,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
(43,'Cần Thơ','can-tho','Huế','hue',970000.00,1190.0,1420,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),(
  44,'Cần Thơ','can-tho','Hà Nội','ha-noi',1300000.00,1870.0,2240,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
  (45,'Vũng Tàu','vung-tau','Đà Nẵng','da-nang',880000.00,1020.0,1220,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
  (46,'Biên Hòa','bien-hoa','Nha Trang','nha-trang',330000.00,400.0,480,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
  (47,'Biên Hòa','bien-hoa','Đà Nẵng','da-nang',820000.00,930.0,1120,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
  (48,'Mỹ Tho','my-tho','Nha Trang','nha-trang',400000.00,500.0,600,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
  (49,'Mỹ Tho','my-tho','Đà Nẵng','da-nang',850000.00,1000.0,1200,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
  (50,'Rạch Giá','rach-gia','Đà Nẵng','da-nang',990000.00,1250.0,1500,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36'),
  (51,'Cà Mau','ca-mau','Hà Nội','ha-noi',1400000.00,2000.0,2400,'ACTIVE','2025-11-13 01:53:36','2025-11-13 01:53:36');
/*!40000 ALTER TABLE `routes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seat_templates`
--

DROP TABLE IF EXISTS `seat_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seat_templates` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bus_model_id` bigint NOT NULL,
  `seat_number` varchar(10) NOT NULL,
  `floor` int DEFAULT NULL,
  `row_index` int DEFAULT NULL,
  `col_index` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_seattemplates_busmodel_seatnumber` (`bus_model_id`,`seat_number`),
  KEY `ix_seat_templates_bus_model_id` (`bus_model_id`),
  CONSTRAINT `seat_templates_ibfk_1` FOREIGN KEY (`bus_model_id`) REFERENCES `bus_models` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ck_seattemplates_floor_1_2` CHECK (((`floor` is null) or (`floor` in (1,2))))
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seat_templates`
--

LOCK TABLES `seat_templates` WRITE;
/*!40000 ALTER TABLE `seat_templates` DISABLE KEYS */;
INSERT INTO `seat_templates` VALUES (44,1,'A01',1,1,1),
(45,1,'A02',1,2,1),
(46,1,'A03',1,3,1),(47,1,'A04',1,4,1)
,(48,1,'A05',1,5,1)
,(49,1,'A06',1,6,1)
,(50,1,'A07',1,7,1)
,(51,1,'A08',1,8,1)
,(52,1,'A09',1,9,1)
,(53,1,'A10',1,10,1)
,(54,1,'A11',1,1,2)
,(55,1,'A12',1,2,2)
,(56,1,'A13',1,3,2)
,(57,1,'A14',1,4,2)
,(58,1,'A15',1,5,2)
,(59,1,'A16',1,6,2)
,(60,1,'A17',1,7,2)
,(61,1,'A18',1,8,2)
,(62,1,'A19',1,9,2)
,(63,1,'A20',1,10,2)
,(64,1,'B01',1,1,1)
,(65,1,'B02',1,2,1)
,(66,1,'B03',1,3,1)
,(67,1,'B04',1,4,1)
,(68,1,'B05',1,5,1)
,(69,1,'B06',1,6,1)
,(70,1,'B07',1,7,1)
,(71,1,'B08',1,8,1)
,(72,1,'B09',1,9,1)
,(73,1,'B10',1,10,1)
,(74,1,'B11',1,1,2)
,(75,1,'B12',1,2,2)
,(76,1,'B13',1,3,2)
,(77,1,'B14',1,4,2)
,(78,1,'B15',1,5,2)
,(79,1,'B16',1,6,2)
,(80,1,'B17',1,7,2)
,(81,1,'B18',1,8,2)
,(82,1,'B19',1,9,2)
,(83,1,'B20',1,10,2);
/*!40000 ALTER TABLE `seat_templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trips`
--

DROP TABLE IF EXISTS `trips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trips` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `route_id` bigint NOT NULL,
  `bus_id` bigint DEFAULT NULL,
  `departure_time` datetime NOT NULL,
  `arrival_time` datetime DEFAULT NULL,
  `total_seats` int NOT NULL,
  `status` varchar(9) NOT NULL DEFAULT 'SCHEDULED',
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_trips_departure_time` (`departure_time`),
  KEY `ix_trips_route_id` (`route_id`),
  KEY `ix_trips_bus_id` (`bus_id`),
  CONSTRAINT `trips_ibfk_1` FOREIGN KEY (`route_id`) REFERENCES `routes` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `trips_ibfk_2` FOREIGN KEY (`bus_id`) REFERENCES `buses` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `ck_trips_total_gt0` CHECK ((`total_seats` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trips`
--

LOCK TABLES `trips` WRITE;
/*!40000 ALTER TABLE `trips` DISABLE KEYS */;
INSERT INTO `trips` VALUES 
(1,1,3,'2025-12-12 13:00:00','2025-12-13 08:10:00',40,'SCHEDULED','2025-11-12 17:21:42','2025-11-12 17:21:42'),
(2,1,3,'2025-12-13 13:00:00','2025-12-14 08:10:00',40,'SCHEDULED','2025-11-12 17:21:42','2025-11-12 17:21:42'),
(3,2,4,'2025-12-12 12:30:00','2025-12-13 09:30:00',40,'SCHEDULED','2025-11-12 17:21:42','2025-11-12 17:21:42'),
(4,5,5,'2025-12-12 13:00:00','2025-12-13 11:00:00',20,'SCHEDULED','2025-11-12 17:21:42','2025-11-12 17:21:42'),
(5,6,6,'2025-12-14 12:30:00','2025-12-14 22:30:00',40,'SCHEDULED','2025-11-12 17:21:42','2025-11-12 17:21:42');
/*!40000 ALTER TABLE `trips` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-13  8:57:54
