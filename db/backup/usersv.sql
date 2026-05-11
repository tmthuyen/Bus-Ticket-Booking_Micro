-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: btb_user_db
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
-- Table structure for table `refresh_tokens`
--

DROP TABLE IF EXISTS `refresh_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `refresh_tokens` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `jti` varchar(36) NOT NULL,
  `token_hash` varchar(255) NOT NULL,
  `user_id` bigint NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `expires_at` datetime NOT NULL,
  `revoked_at` datetime DEFAULT NULL,
  `device_id` varchar(255) DEFAULT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `rotated_to` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_refresh_tokens_jti` (`jti`),
  KEY `ix_refresh_tokens_id` (`id`),
  KEY `ix_refresh_tokens_user_id` (`user_id`),
  CONSTRAINT `refresh_tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `refresh_tokens`
--

LOCK TABLES `refresh_tokens` WRITE;
/*!40000 ALTER TABLE `refresh_tokens` DISABLE KEYS */;
INSERT INTO `refresh_tokens` VALUES (1,'1990a9d7-0639-4512-956c-434acdb136e5','0cbc27b9c9266d3ada723a42327b552b94ecd68fd2fda87f5b7b7d7d6faa605e',1,'2025-10-30 01:07:46','2025-11-06 01:07:46',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',NULL),(2,'d83a592d-e846-4d8e-a3cd-d61cf1260c11','717dce4da46faa1469e0e793f8974a91d0a86765e25f3d4fd2f2d7231df77aad',1,'2025-10-30 01:07:47','2025-11-06 01:07:47',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',NULL),(3,'db07f316-4228-4cc4-aa53-1641891e4d15','063c6b07e6226feb9bf835ac01ca394243202d42058c4d2d08cdd54c9da3e68b',1,'2025-10-30 01:15:34','2025-11-06 01:15:34',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',NULL),(4,'de42a5f3-f2ce-4ca5-844a-0500789d4b68','f895bded27dbfa33ab74c01ecf56b1787b39afe8f49a8aab4ee4110dead38ab0',1,'2025-10-30 01:15:34','2025-11-06 01:15:34',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',NULL),(5,'9ceb6eb8-ebf8-4d90-beba-b2215eef875e','4258540e6ea096583ca386fc7d58891c1559485f806201c004ff877891528def',1,'2025-10-30 01:27:46','2025-11-06 01:27:46',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',NULL),(6,'7144914a-1eae-4b36-9447-8ba141ede348','74b760c06f7bd3794966fe1831b85d8f72b783c07f711078172e5eb0f9d7a3dd',1,'2025-10-30 01:27:46','2025-11-06 01:27:46',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',NULL),(7,'60cc537e-762a-4e7f-9739-cf48590d20ee','aafce5f98325349e20436e89e619660710cba6d8330d821b481724169db9b8c3',1,'2025-10-30 01:27:50','2025-11-06 01:27:50',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',NULL),(8,'e0fbe73a-c265-421d-9abd-f6b9864856ea','0a475739c435dc1929fa4991191ea30419b4b34afcd20c72a9051f6a671cbdf1',1,'2025-10-30 01:27:50','2025-11-06 01:27:50',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',NULL),(9,'d75f270a-4de5-4171-861e-e5199794ca7e','fb392723832d586012f786a73dc4f467d428034b159037979b65335e958a463f',1,'2025-10-30 01:36:44','2025-11-06 01:36:44',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',NULL),(10,'37e92f85-1a71-4c33-bb38-b2bb501b592f','5be9eaa30d4346b55a0215961737bd568d6ae92af93092ce53a2175c5eb01f81',1,'2025-10-30 01:36:44','2025-11-06 01:36:44',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',NULL),(11,'90953032-1cb9-4dac-ace3-5a1dc6ec2bff','779b5b023cbba7635f16f206784b9deb2b8e17527cbcade6528e897193ed9b41',2,'2025-10-30 03:42:25','2025-11-06 03:42:25',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',NULL),(12,'08d4e483-7a59-4cfe-ae9c-496bf2d5c10d','354c5aa9383a0515576cc85ce51becc7f47e5ff108b56a11af073bdd7aa5d825',2,'2025-10-30 03:42:26','2025-11-06 03:42:26',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',NULL),(13,'b3b9f54e-a566-44e7-9890-4a680db77a8d','c0cae3fc0d842a58bf7ba7550e1edce15aec614a465683a00cf99cc296b1d37d',3,'2025-11-14 05:27:36','2025-11-21 05:27:36',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(14,'3b9a6940-99c5-4945-b5d8-2ec1ad6e759f','cc1afe95085c8ed4ff8f3c9014ec82d6b94b20e1e547d08530ec0db48fd77ede',3,'2025-11-14 05:29:34','2025-11-21 05:29:34',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(15,'edefa24a-aee9-495e-9270-8b4c7222ecfd','2434c45de286653d80bd709156b2f848e7a01eeef2cbfc870896c4ccc99d53bb',3,'2025-11-14 05:29:38','2025-11-21 05:29:38',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(16,'40114d54-c327-4fe8-b86f-e2d760bafc09','4738e2524c2ab533275fa7e8afae1073e3c4eb11eb5c5ae210ec6711f0fd2717',3,'2025-11-14 05:30:53','2025-11-21 05:30:53',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(17,'9480b371-de32-4c9c-b9d1-34f0161bad2d','f92e1170240a1f306281efc6af0fc631998b3e6059cc043c2e51a043b9cdd675',3,'2025-11-14 05:31:39','2025-11-21 05:31:39',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(18,'00efcc06-cc8d-4383-946c-efb594516a16','a0363dce4c13e3d79fbcd87f8f53ffdf9e084be458331a5536c0548d2e6eab8f',3,'2025-11-14 05:57:09','2025-11-21 05:57:09',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(19,'9c781b66-831f-48f9-9b4d-37e9c5f63ad1','4035669cf07031576b67ecffd09e745a85e79a6a8d47c14c62c6ad6b08bea3a6',3,'2025-11-14 05:57:48','2025-11-21 05:57:48',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(20,'a5c8e271-0ba7-4030-9fcb-50650f9fb275','c9a64d26e50e450c32194855e09124eca626ea237e3012e68ad0861da3dcf93d',1,'2025-11-22 09:11:58','2025-11-29 09:11:58',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',NULL),(21,'8b2362ad-0244-4204-b026-6b569afc4651','e60b5da299982164860fa0dd63bd38cc63975015afffcb377479970f0157dda3',1,'2025-11-22 09:12:03','2025-11-29 09:12:03',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(22,'8fe040a2-40cc-41df-96b4-48aec3b85641','8b9c77b522cdea5a2cd361a07512bd109db97b4676c026d3c2f553592468e47d',1,'2025-11-22 09:18:46','2025-11-29 09:18:46',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(23,'f81b4085-3a07-412e-a128-7e82486b4f09','71bd1935eca607b3c9a1449ef4db21ae398a60b49aa3f842def9d8041d78f03a',1,'2025-11-22 09:19:01','2025-11-29 09:19:01',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(24,'d3637308-3877-4096-97ae-1ede938fcd0b','cddc8c381f14d3a9976fce334d433ba127a1566696a3f510d8a6c74dcddd98a4',1,'2025-11-22 09:20:09','2025-11-29 09:20:09',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(25,'6019ac2a-9e5d-454e-8755-89bb72947a8b','a981405fbcdea34eabeb4fe1cf92c8dc51adf35fad5fad21a59e9a4a85feebe7',1,'2025-11-22 09:20:14','2025-11-29 09:20:14',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(26,'3e6c88d5-6049-4604-a4e2-b85e6222775b','af5d2c29b18bd9159523e89ec1c98aa841c774ee92b2f41bbd5f6bd8b9d57a52',1,'2025-11-22 09:20:15','2025-11-29 09:20:15',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(27,'086c04ec-0877-4fb2-b475-3d6c4093e6af','23f2b332ad8aeb5786373dbfa331cc527f7b1a82542403c0e5dc2ab2870d54df',1,'2025-11-22 09:21:48','2025-11-29 09:21:48',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(28,'5e2c64d0-fdaa-4ab9-9eba-89c9d2cc3c71','45e20eb4bfa27ae5446559c76607ed8989843a6866ad5bd3a394fdf02523ec21',1,'2025-11-22 09:26:58','2025-11-29 09:26:58',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(29,'8f25bd7b-1390-450d-a6e8-3e03b3b86f55','1422f182b8af4d464b079371b63f99179f0885ec7a7bf7e08ad99679c1e8381a',1,'2025-11-22 09:28:44','2025-11-29 09:28:44',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(30,'2af70221-1054-4ae0-86c9-aa247153809f','b48a6d2e6d305f2467d30079516cf92e39c31098c365e0a96c334f1d92556b0a',1,'2025-11-22 09:28:58','2025-11-29 09:28:58',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(31,'ba201c3f-ca5f-46f5-bfb3-e9d9b799dd05','aca9b22a15a2d7f0ef0eada4b18ff89dbb17191bb89c8dc6b6b9a47446d17810',1,'2025-11-22 09:29:12','2025-11-29 09:29:12',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(32,'68acc678-137d-4591-b357-bd44332cd273','fbabd65683907853a3aaa644a193356640a5d0cebad7a4c41ee722eb5da149f0',1,'2025-11-22 09:32:00','2025-11-29 09:32:00',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(33,'43f831ba-1d15-4965-919d-e861087f7a37','e9e37e22c44bc86dfe2a732b9dd0437fdb075bc76b24259a166b1763ad5e1a62',1,'2025-11-22 09:33:21','2025-11-29 09:33:21',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(34,'025b5490-b508-487a-81fe-f6b2ee9a7c49','53b628fac7f9c434974ffe3a65be7552c2399b1f12b953d38c94192ec3c816a0',1,'2025-11-22 09:36:56','2025-11-29 09:36:56',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL),(35,'34f4ae96-654d-402d-83bc-4648ff93a69f','026ba8a34b1dee1cbcacbef57a85723f385b2631bb4e7e7e034158cb55f9c5a1',1,'2025-11-22 09:38:08','2025-11-29 09:38:08',NULL,'unknown','172.20.0.12','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36',NULL);
/*!40000 ALTER TABLE `refresh_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(40) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `status` enum('ACTIVE','PAYING','INACTIVE','BANNED') DEFAULT NULL,
  `role` enum('CUSTOMER','ADMIN') DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'tranthuyen2222@gmail.com','$2b$12$MGqTbTiFheiJBp5DngTfBeNram.yQYpIq7WJKhu.t48j08HShQVze','Trần Minh Thuyên','0373436163','ACTIVE','ADMIN','2025-10-24 17:32:47','2025-10-24 17:58:42'),(2,'52300070@gmail.com','$2b$12$WwQHZJVHZDSkfmf0dD3tR.1c4QbWIWGQTFsRXmH4r3onryW8K1YMK','Trần Minh Thuận','0373436164','ACTIVE','CUSTOMER','2025-10-30 03:31:37','2025-10-30 03:31:37'),(3,'52300060@gmail.com','$2b$12$qShy0SPn47myOBvxU8Ryu.1uDpdAs83S0oslQ1RhuKYpEvf6e/lma','admin','0373436165','ACTIVE','CUSTOMER','2025-11-14 05:25:54','2025-11-14 05:25:54');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-24 23:26:12
