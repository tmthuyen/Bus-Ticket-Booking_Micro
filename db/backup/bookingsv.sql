-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: btb_booking_db
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
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id` char(36) NOT NULL,
  `trip_id` int NOT NULL,
  `booking_code` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `status` varchar(9) NOT NULL DEFAULT 'PENDING',
  `seat_quantity` int NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `hold_until` datetime DEFAULT NULL COMMENT 'Thời gian hết hạn giữ chỗ tạm thời',
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_bookings_booking_code` (`booking_code`),
  KEY `ix_bookings_id` (`id`),
  KEY `ix_bookings_trip_id` (`trip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES ('00edcb9d-ef14-4828-85ec-e91644cfcc6f',3,'BK231125XFIB','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,920000.00,'2025-11-23 19:25:07','2025-11-23 18:25:07','2025-11-23 19:25:33'),('0584a8b3-8e2d-4099-a9ce-74dd92ce4048',1,'BK2411255XCA','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 11:50:07','2025-11-24 10:50:07','2025-11-24 11:50:14'),('0bb9c0bb-b123-4e85-9308-afb2ea7dd421',3,'BK231125M48K','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,920000.00,'2025-11-23 19:27:56','2025-11-23 18:27:56','2025-11-23 19:28:33'),('127a19ed-302f-4b74-a38f-4b089c2ff20f',3,'BK231125R0E7','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,920000.00,'2025-11-23 19:32:05','2025-11-23 18:32:05','2025-11-23 19:32:33'),('16d6d13a-4d5f-4086-bbff-de76902f953e',3,'BK2311257AKW','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,920000.00,'2025-11-23 19:48:08','2025-11-23 18:48:08','2025-11-23 19:48:33'),('1f620480-0a9a-4619-b8ee-06b6e5d03ed7',1,'BK241125XYPS','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 12:06:35','2025-11-24 11:06:35','2025-11-24 12:06:44'),('231a91c6-f96d-4f64-aaba-75f4370adfd2',1,'BK2411254439','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 09:27:06','2025-11-24 08:27:06','2025-11-24 09:27:31'),('24ffe576-dbd8-4171-96cf-fa24710ddb8b',3,'BK231125Z2Z2','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,920000.00,'2025-11-23 19:21:31','2025-11-23 18:21:31','2025-11-23 19:21:33'),('297a1d2b-5289-4160-a261-c925842cb06a',3,'BK2311254VU0','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,920000.00,'2025-11-23 19:55:41','2025-11-23 18:55:41','2025-11-23 19:56:33'),('35c7e443-c8a7-4586-b754-ac01f7214e2b',1,'BK241125MT98','Nguyen Chi Tam (Thuyen)','0373436163','ngctam.3108@gmail.com','PAID',1,850000.00,'2025-11-24 05:25:23','2025-11-24 04:25:23','2025-11-24 04:27:52'),('36d55ce4-7e2a-461f-8a9a-4ec4311e1f55',3,'BK241125Z8QJ','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,920000.00,'2025-11-24 08:28:58','2025-11-24 07:28:58','2025-11-24 08:29:01'),('5285d169-c7e2-4d46-a2fb-e4cd4e14eb59',1,'BK241125WJZN','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 11:47:56','2025-11-24 10:47:56','2025-11-24 11:48:14'),('5446a863-2233-4088-abe6-2dc03ec85408',1,'BK231125A3YB','Nguyen Chi Tam (Thuyen)','0373436163','ngctam.3108@gmail.com','PAID',1,850000.00,'2025-11-23 20:03:14','2025-11-23 19:03:14','2025-11-23 19:06:10'),('552cbc4f-567c-4459-8184-68693c769972',1,'BK241125WFRI','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 09:46:19','2025-11-24 08:46:19','2025-11-24 09:46:31'),('581a95a0-3854-4df3-84ef-7ba38263108d',1,'BK241125N7O0','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 12:17:52','2025-11-24 11:17:52','2025-11-24 12:18:14'),('6abc64dc-7314-4012-a852-5047dabb8174',1,'BK241125DKUG','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 12:19:56','2025-11-24 11:19:56','2025-11-24 11:20:04'),('6aecb91c-2bea-4a2f-93d4-4979a789014e',1,'BK231125M32C','Nguyen Chi Tam (Thuyen)','0373436163','ngctam.3108@gmail.com','CANCELLED',1,850000.00,'2025-11-23 20:20:46','2025-11-23 19:20:46','2025-11-24 04:23:59'),('7ca5a339-ee4b-45e9-b73b-cf55e3a0e6f1',1,'BK2411259ZRV','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','PAID',2,1700000.00,'2025-11-24 17:57:59','2025-11-24 15:57:59','2025-11-24 16:00:18'),('95b068c0-9eaa-47b9-951f-c0357e76f660',3,'BK2311250V3U','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,920000.00,'2025-11-23 19:47:21','2025-11-23 18:47:21','2025-11-23 19:47:33'),('9ba575cd-f24e-4c4d-a13a-dc5e0ecfb599',3,'BK231125Z3V2','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','PAID',1,920000.00,'2025-11-23 19:55:57','2025-11-23 18:55:57','2025-11-23 18:57:50'),('b6ee0b91-a9ca-47ff-becc-4f06a09e7fc4',1,'BK241125QMOZ','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','PAID',1,850000.00,'2025-11-24 09:48:15','2025-11-24 08:48:15','2025-11-24 09:38:10'),('bda6a56e-394b-4702-86f7-e6a11a33b412',1,'BK241125ICP7','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 11:56:17','2025-11-24 10:56:17','2025-11-24 11:56:44'),('bfb13c11-5e1d-4088-957d-c6be2e37fa66',3,'BK2311255K51','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,920000.00,'2025-11-23 19:37:01','2025-11-23 18:37:01','2025-11-23 19:37:33'),('c57e3cd1-6831-4b79-975f-f59f44414fdc',1,'BK24112504L5','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 09:38:51','2025-11-24 08:38:51','2025-11-24 09:39:00'),('c7c509dd-6757-42b3-89da-ae0f2da25b77',3,'BK2411259ZLC','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','PAID',1,920000.00,'2025-11-24 08:30:38','2025-11-24 07:30:38','2025-11-24 07:33:12'),('d9d65425-0ae6-40aa-b3c1-2046c28b5385',1,'BK241125Q3QO','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 09:34:52','2025-11-24 08:34:52','2025-11-24 09:35:00'),('db7a7cc6-f9d2-487d-bcd2-5db441bd764e',3,'BK241125RXOS','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','PAID',1,920000.00,'2025-11-24 09:14:11','2025-11-24 08:14:11','2025-11-24 08:17:54'),('dd4979fe-493c-4ffe-89a5-aac4fd23fcff',1,'BK241125MW4Z','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','PAID',1,850000.00,'2025-11-24 11:04:11','2025-11-24 10:04:11','2025-11-24 10:07:41'),('e1ab6da2-4162-4c0b-a069-c2f2e95c08f0',1,'BK231125T7VI','Nguyen Chi Tam (Thuyen)','0373436163','ngctam.3108@gmail.com','PAID',1,850000.00,'2025-11-23 20:25:10','2025-11-23 19:25:10','2025-11-23 19:27:42'),('eb2ee51a-1532-49f2-9e0e-774563693928',3,'BK2311253DTB','Tran Minh Thuyen','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,920000.00,'2025-11-23 19:29:50','2025-11-23 18:29:50','2025-11-23 19:30:33'),('ef96afbb-31b7-479b-be5d-cd8d32d18d16',1,'BK241125XQSM','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 12:35:39','2025-11-24 11:35:39','2025-11-24 12:35:44'),('fbb912c5-f57a-4b75-8b63-4022738e4013',1,'BK241125UUHV','Nguyen Chi Tam (Thuyen)','0373436163','tranthuyen2222@gmail.com','CANCELLED',1,850000.00,'2025-11-24 09:28:59','2025-11-24 08:28:59','2025-11-24 09:29:00');
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seat_assignments`
--

DROP TABLE IF EXISTS `seat_assignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seat_assignments` (
  `id` char(36) NOT NULL,
  `booking_id` char(36) NOT NULL,
  `trip_id` int NOT NULL,
  `seat_number` varchar(10) NOT NULL,
  `status` varchar(8) NOT NULL DEFAULT 'RESERVED',
  `created_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_seat_assignments_booking_id` (`booking_id`),
  KEY `ix_seat_assignments_trip_id` (`trip_id`),
  KEY `ix_seat_assignments_id` (`id`),
  CONSTRAINT `seat_assignments_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seat_assignments`
--

LOCK TABLES `seat_assignments` WRITE;
/*!40000 ALTER TABLE `seat_assignments` DISABLE KEYS */;
INSERT INTO `seat_assignments` VALUES ('04ee159c-653b-430c-885b-6388ee650e06','7ca5a339-ee4b-45e9-b73b-cf55e3a0e6f1',1,'A06','BOOKED','2025-11-24 15:57:59'),('599b7e4f-9301-4c94-ada2-49fd403b28e8','db7a7cc6-f9d2-487d-bcd2-5db441bd764e',3,'A02','BOOKED','2025-11-24 08:14:11'),('5fa722dc-72ea-433d-9cc6-f31bf00c3be7','5446a863-2233-4088-abe6-2dc03ec85408',1,'A01','BOOKED','2025-11-23 19:03:14'),('6380d17a-1dd4-4c22-8605-af34207dc66c','c7c509dd-6757-42b3-89da-ae0f2da25b77',3,'A09','BOOKED','2025-11-24 07:30:38'),('66917e26-3a0b-4351-860c-6ef6fc3405a9','7ca5a339-ee4b-45e9-b73b-cf55e3a0e6f1',1,'A05','BOOKED','2025-11-24 15:57:59'),('79f7c536-2a19-408a-b2ac-de1b114d052c','b6ee0b91-a9ca-47ff-becc-4f06a09e7fc4',1,'A09','BOOKED','2025-11-24 08:48:15'),('a4c62bcd-816f-4e7e-8b64-7aa9dcb9b36a','dd4979fe-493c-4ffe-89a5-aac4fd23fcff',1,'A04','BOOKED','2025-11-24 10:04:11'),('babc9128-85e6-49a1-afb7-4e0e3c5a35fe','9ba575cd-f24e-4c4d-a13a-dc5e0ecfb599',3,'A10','BOOKED','2025-11-23 18:55:57'),('f1da21ca-5526-441c-9f32-b3d96f2aa9ed','e1ab6da2-4162-4c0b-a069-c2f2e95c08f0',1,'A03','BOOKED','2025-11-23 19:25:10'),('f9ac89d2-1c09-4685-9e6a-7a4831a178ba','35c7e443-c8a7-4586-b754-ac01f7214e2b',1,'A02','BOOKED','2025-11-24 04:25:23');
/*!40000 ALTER TABLE `seat_assignments` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-24 23:28:54
