-- MySQL dump 10.13  Distrib 8.0.31, for Linux (x86_64)
--
-- Host: localhost    Database: flask_db
-- ------------------------------------------------------
-- Server version	8.0.31-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `carts`
--

DROP TABLE IF EXISTS `carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `carts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carts`
--

LOCK TABLES `carts` WRITE;
/*!40000 ALTER TABLE `carts` DISABLE KEYS */;
INSERT INTO `carts` VALUES (9,6),(3,7),(4,8),(5,9),(6,10),(7,11),(8,12),(11,13);
/*!40000 ALTER TABLE `carts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carts_products`
--

DROP TABLE IF EXISTS `carts_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carts_products` (
  `cart_id` int NOT NULL,
  `product_id` int NOT NULL,
  `date_of_insertion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cart_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `carts_products_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `carts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `carts_products_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carts_products`
--

LOCK TABLES `carts_products` WRITE;
/*!40000 ALTER TABLE `carts_products` DISABLE KEYS */;
INSERT INTO `carts_products` VALUES (3,4,'2022-11-19 22:10:14'),(3,5,'2022-11-19 22:10:13'),(3,9,'2022-11-19 22:10:11'),(3,10,'2022-11-19 22:10:10'),(3,11,'2022-11-19 22:10:10'),(3,12,'2022-11-19 22:10:11'),(3,13,'2022-11-19 22:10:12'),(3,16,'2022-11-19 22:10:15'),(3,17,'2022-11-19 22:10:15'),(4,6,'2022-11-19 22:11:33'),(4,10,'2022-11-19 22:11:33'),(4,13,'2022-11-19 22:11:13'),(4,14,'2022-11-19 22:11:13'),(4,15,'2022-11-19 22:11:14'),(4,16,'2022-11-19 22:11:14'),(9,2,'2022-11-19 22:08:59'),(9,5,'2022-11-19 22:08:51'),(9,7,'2022-11-19 22:08:50'),(9,9,'2022-11-19 22:08:51'),(9,13,'2022-11-19 22:08:55'),(9,16,'2022-11-19 22:08:57');
/*!40000 ALTER TABLE `carts_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `product_code` varchar(12) DEFAULT NULL,
  `price` float NOT NULL,
  `date_of_withdrawal` datetime DEFAULT CURRENT_TIMESTAMP,
  `seller_id` int NOT NULL,
  `category` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_code` (`product_code`),
  KEY `seller_id` (`seller_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Iphone 11','878708482652',493.93,'2022-12-14 21:03:00',2,'Phones'),(2,'Iphone 13','431714871612',888.72,'2022-12-08 23:04:00',2,'Phones'),(3,'Samsung Galaxy A53','913390257924',329.67,'2023-01-25 12:09:00',2,'Phones'),(4,'Samsung Galaxy A13','505460209471',158.88,'2023-02-23 13:09:00',2,'Phones'),(5,'Samsung Galaxy S22','526718963608',1198.99,'2023-02-23 11:09:00',2,'Phones'),(6,'LG 24TL510V-PZ TN TV Monitor 2','388901594264',147.9,'2023-03-03 14:10:00',2,'TV/Monitor'),(7,'LG 24TQ510S-PZ Smart Monitor','556980485917',182.9,'2023-03-23 23:10:00',2,'TV/Monitor'),(8,'Samsung Smart LED UE43AU7172','305671856796',357.34,'2023-02-01 21:09:00',3,'TV/Monitor'),(9,'Samsung Smart LED UE50AU7172','853032506228',379.99,'2023-02-10 23:14:00',3,'TV'),(10,'Samsung OLED TV 55S95B 55','444533416396',1279.99,'2023-05-18 23:13:00',4,'TV'),(11,'Dell Vostro 3500 15.6','563677672638',476.88,'2022-12-30 11:13:00',4,'Laptop'),(12,'Apple MacBook Air 13.3\" (2020)','447470354193',1179,'2023-02-23 13:17:00',4,'Laptop'),(13,'Lenovo V15 G2 ALC 15.6','259729116675',464.78,'2023-01-18 21:13:00',4,'Laptop'),(14,'Apple MacBook Air 13.3','789724977056',1101.86,'2023-05-02 23:16:00',3,'Laptop'),(15,'Lenovo IdeaPad Gaming 3','297222014142',776.99,'2023-02-16 21:14:00',3,'Laptop'),(16,'HP 255 G8 15.6\" IPS FHD','374312252858',349,'2023-03-22 01:48:00',2,'Laptop'),(17,'Apple MacBook Air 13.3','914856703333',1079.99,'2023-04-12 23:49:00',2,'Laptop'),(18,'Apple MacBook Pro 16','104116250407',3950.99,'2023-02-02 23:50:00',2,'Laptop');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `surname` varchar(30) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(64) NOT NULL,
  `email` varchar(60) NOT NULL,
  `role` enum('ADMIN','PRODUCTSELLER','USER') NOT NULL,
  `confirmed` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'mike','theologitis','admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918','mtheologitis@tuc.gr','ADMIN',1),(2,'mihaela','kwnstantinou','productseller1','badf6f1989f67e31c2e0afe3e2b8d482d952246f1fbfa422c9cf58cef01e0a7e','productseller1@tuc.gr','PRODUCTSELLER',1),(3,'thanos','grapsas','productseller2','85f32525868db8b1c689df25dd108a58a42e397e7797cc92e72de27f4e5943f1','productseller2@tuc.gr','PRODUCTSELLER',1),(4,'aris','douvis','productseller3','b234f9595ea52d433fd0a5cb953c59daa5a94ca9fa919ad10f047e6b40b12ed2','productseller3@tuc.gr','PRODUCTSELLER',1),(5,'iasonas','theodorou','productseller4','3957dc13afc50678bfd71ae8fd1b0957bff61d6443888c2d23c14f7cba290a81','productseller4@tuc.gr','PRODUCTSELLER',0),(6,'Thanasis','Tomas','user1','0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90','user1@tuc.gr','USER',1),(7,'stathis','giannaris','user2','6025d18fe48abd45168528f18a82e265dd98d421a7084aa09f61b341703901a3','user2@tuc.gr','USER',1),(8,'panagiwtis','papadopoulos','user3','5860faf02b6bc6222ba5aca523560f0e364ccd8b67bee486fe8bf7c01d492ccb','user3@tuc.gr','USER',1),(9,'alex','ziogas','user4','5269ef980de47819ba3d14340f4665262c41e933dc92c1a27dd5d01b047ac80e','user4@tuc.gr','USER',0),(10,'alex','vavvas','user5','5a39bead318f306939acb1d016647be2e38c6501c58367fdb3e9f52542aa2442','user5@tuc.gr','USER',0),(11,'aristotelis','plakas','user6','ecb48a1cc94f951252ec462fe9ecc55c3ef123fadfe935661396c26a45a5809d','user6@tuc.gr','USER',1),(12,'nikolas','kaloglou','user7','3268151e52d97b4cacf97f5b46a5c76c8416e928e137e3b3dc447696a29afbaa','user7@tuc.gr','USER',0),(13,'giannis','steiakakis','user8','f60afa4989a7db13314a2ab9881372634b5402c30ba7257448b13fa388de1b78','user8@tuc.gr','USER',1);
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

-- Dump completed on 2022-11-19 22:20:25
