-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: printx
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `order_id` varchar(255) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `line1` varchar(255) DEFAULT NULL,
  `line2` varchar(255) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pin` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `addresses_ibfk_1` (`user_id`),
  CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
INSERT INTO `addresses` VALUES (7,9,'ORD202509251424059',NULL,NULL,'shipping','Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(8,11,'ORD2025092515455211',NULL,NULL,'shipping','Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(9,11,'ORD2025092516145011',NULL,NULL,'shipping','Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(10,11,'ORD2025092516384611',NULL,NULL,'shipping','Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(11,11,'ORD2025092516410211',NULL,NULL,'shipping','Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(12,11,'COD2025092612000811',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(13,11,'ORD2025092612282311',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(14,12,'COD2025092615514912',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(15,11,'COD2025092700074111',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(19,11,'COD2025092700512911',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(20,11,'COD2025092701005711',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(23,13,'COD2025092901294413',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(24,13,'ORD2025092909125213',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(25,13,'ORD2025092923490813',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(26,8,'COD202509301311408',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(27,8,'COD202509302145598',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043'),(28,8,'ORD202509302146578',NULL,'07900019832',NULL,'Building no.95 , Room no.706','PMGP Colony , New Mhada Vasahat , Mankhurd , Mumbai','Mumbai','Maharashtra','400043');
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_cancel`
--

DROP TABLE IF EXISTS `admin_cancel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_cancel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` varchar(255) NOT NULL,
  `customer_name` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_cancel`
--

LOCK TABLES `admin_cancel` WRITE;
/*!40000 ALTER TABLE `admin_cancel` DISABLE KEYS */;
INSERT INTO `admin_cancel` VALUES (1,'ORD202509302146578','Admin',NULL,'admin@printx.com','2025-09-30 16:23:22');
/*!40000 ALTER TABLE `admin_cancel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `quantity` int DEFAULT '1',
  `added_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `size` varchar(50) DEFAULT NULL,
  `border_color` varchar(50) DEFAULT NULL,
  `border_width` varchar(50) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (109,8,9,'Cool Wall Sticker',199.00,1,'2025-09-30 16:39:45','Default',NULL,NULL,NULL);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `message` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,'omkar','omkar.kamble312@gmail.com','8454800234','hiee','2025-09-25 18:52:22'),(2,'Rohan Kamble','designbykamble@gmail.com','07900019832','hieee','2025-09-25 19:24:40'),(3,'Rohan Kamble','designbykamble@gmail.com','07900019832','ashfakh urf chandu','2025-09-26 10:25:10');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` varchar(50) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `size` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `product_name` varchar(255) DEFAULT NULL,
  `border_color` varchar(50) DEFAULT NULL,
  `border_width` varchar(50) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (3,'ORD202509251424059',9,1,'Asethetic Frame',900.00,1,'A3','2025-09-25 08:54:05',NULL,NULL,NULL,NULL),(4,'ORD2025092515455211',11,10,'Custom Name Sticker',299.00,1,'One Size','2025-09-25 10:15:52',NULL,NULL,NULL,NULL),(5,'ORD2025092516145011',11,9,'Cool Wall Sticker',199.00,1,'Default','2025-09-25 10:44:50',NULL,NULL,NULL,NULL),(6,'ORD2025092516384611',11,6,'Backside Spiderman Printed Oversized T-shirt',400.00,1,'S','2025-09-25 11:08:46',NULL,NULL,NULL,NULL),(7,'ORD2025092516410211',11,1,'Asethetic Frame',900.00,1,'A3','2025-09-25 11:11:02',NULL,NULL,NULL,NULL),(8,'COD2025092612000811',11,101,'Photo Frame',600.00,1,'A4','2025-09-26 06:30:08',NULL,'#000000','1','uploads/WhatsApp_Image_2025-09-15_at_6.32.23_PM_1.jpeg'),(9,'ORD2025092612282311',11,101,'Photo Frame',1560.00,1,'A4','2025-09-26 06:58:23',NULL,'#ff0000','4','uploads/WhatsApp_Image_2025-09-15_at_6.32.24_PM.jpeg'),(10,'COD2025092615514912',12,1,'Asethetic Frame',900.00,1,'A3','2025-09-26 10:21:49',NULL,NULL,NULL,'uploads/Screenshot_2024-07-02_232114.png'),(11,'COD2025092700074111',11,7,'Personalized Couple Hoodies (16/8/2008 - sam / 12/12/2001 - omi)',800.00,1,'S-sam / L-omi','2025-09-26 18:37:41',NULL,NULL,NULL,NULL),(12,'COD202509270029328',8,1,'Asethetic Frame',900.00,1,'A3','2025-09-26 18:59:32',NULL,NULL,NULL,'/static/images/f1.jpeg'),(13,'COD2025092700512911',11,1,'Asethetic Frame',900.00,1,'A3','2025-09-26 19:21:29',NULL,NULL,NULL,'/static/images/f1.jpeg'),(14,'ORD-1001',11,1,'Beautiful Photo Frame',999.00,1,'M','2025-09-26 19:27:39','Classic Frame',NULL,NULL,NULL),(15,'COD2025092701005711',11,2,'3D Car Frame',1000.00,1,'A4','2025-09-26 19:30:57',NULL,NULL,NULL,'/static/images/f2.jpeg'),(16,'COD2025092723241713',13,1,'Asethetic Frame',900.00,1,'A3','2025-09-27 17:54:17',NULL,NULL,NULL,'/static/images/f1.jpeg'),(17,'COD2025092901294413',13,NULL,'Banner (Normal)',560.00,1,'4ft x 7ft','2025-09-28 19:59:44',NULL,NULL,'3 inch','uploads/Screenshot_2024-07-02_232114.png'),(18,'ORD2025092909125213',13,1,'Asethetic Frame',900.00,1,'A3','2025-09-29 03:42:52',NULL,NULL,NULL,'uploads/Screenshot_2024-07-02_232114.png'),(19,'ORD2025092923490813',13,1,'Asethetic Frame',900.00,1,'A3','2025-09-29 18:19:08',NULL,NULL,NULL,'/static/images/f1.jpeg'),(20,'COD202509301311408',8,NULL,'Banner (Normal)',400.00,1,'4ft x 5ft','2025-09-30 07:41:40',NULL,NULL,'2 inch','uploads/pathamesh_sarak_copy.jpg'),(21,'COD202509302145598',8,2,'3D Car Frame',1000.00,1,'A4','2025-09-30 16:15:59',NULL,NULL,NULL,'/static/images/f2.jpeg'),(22,'ORD202509302146578',8,5,'Backside Wolf Printed Oversized T-shirt',400.00,1,'S','2025-09-30 16:16:57',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_updates`
--

DROP TABLE IF EXISTS `order_updates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_updates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `text` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `order_updates_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_updates`
--

LOCK TABLES `order_updates` WRITE;
/*!40000 ALTER TABLE `order_updates` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_updates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` varchar(50) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `payment_method` varchar(20) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  `order_status` varchar(50) DEFAULT 'Pending',
  `size` varchar(50) DEFAULT NULL,
  `width` float DEFAULT NULL,
  `height` float DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `border_color` varchar(20) DEFAULT NULL,
  `border_width` int DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'ORD-1001',11,'2025-09-27',999.00,'COD','Paid','Delivered',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_resets`
--

DROP TABLE IF EXISTS `password_resets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_resets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `otp` varchar(10) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_resets`
--

LOCK TABLES `password_resets` WRITE;
/*!40000 ALTER TABLE `password_resets` DISABLE KEYS */;
INSERT INTO `password_resets` VALUES (1,'hunter@gmail.com','590287','2025-09-24 16:32:14'),(2,'hunter@gmail.com','165581','2025-09-24 16:32:17'),(3,'hunter@gmail.com','761095','2025-09-24 16:32:20'),(4,'hunter@gmail.com','181941','2025-09-24 16:35:44'),(5,'hunter@gmail.com','811583','2025-09-24 16:35:48'),(6,'omkara.kamble312@gmail.com','208857','2025-09-25 09:10:24'),(7,'omkara.kamble312@gmail.com','151841','2025-09-25 09:26:57'),(8,'omkara.kamble312@gmail.com','123871','2025-09-25 09:28:04'),(9,'omkara.kamble312@gmail.com','614281','2025-09-25 09:28:06'),(10,'omkara.kamble312@gmail.com','754489','2025-09-25 09:36:52'),(11,'omkara.kamble312@gmail.com','937579','2025-09-25 09:36:56'),(12,'omkara.kamble312@gmail.com','892181','2025-09-25 09:37:37'),(13,'omkara.kamble312@gmail.com','163351','2025-09-25 09:37:39'),(14,'omkara.kamble312@gmail.com','590476','2025-09-25 09:38:15'),(15,'omkara.kamble312@gmail.com','287637','2025-09-25 09:40:58'),(16,'omkara.kamble312@gmail.com','171494','2025-09-25 09:41:01'),(17,'omkara.kamble312@gmail.com','135044','2025-09-27 17:51:52'),(18,'omkar.kamble312@gmail.com','977144','2025-09-27 18:06:24');
/*!40000 ALTER TABLE `password_resets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `order_id` varchar(255) DEFAULT NULL,
  `razorpay_order_id` varchar(255) DEFAULT NULL,
  `payment_id` varchar(255) DEFAULT NULL,
  `amount` int DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `order_status` varchar(50) DEFAULT 'Pending',
  `payment_status` varchar(50) DEFAULT 'PENDING',
  `payment_method` varchar(20) DEFAULT 'ONLINE',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (6,9,'ORD202509251424059',NULL,NULL,999,'Delivered','2025-09-25 08:54:05','Pending','PENDING','ONLINE'),(7,11,'ORD2025092515455211',NULL,NULL,398,'Delivered','2025-09-25 10:15:52','Pending','PENDING','ONLINE'),(8,11,'ORD2025092516145011',NULL,NULL,298,'Delivered','2025-09-25 10:44:50','Delivered','PENDING','ONLINE'),(9,11,'ORD2025092516384611',NULL,NULL,499,NULL,'2025-09-25 11:08:46','Delivered','PAID (COD)','COD'),(10,11,'ORD2025092516410211','order_RLoTUeEhcRp3g8','pay_RLoThKGyyt84s5',999,NULL,'2025-09-25 11:11:02','Pending','SUCCESS','ONLINE'),(12,11,'COD2025092612000811',NULL,NULL,699,NULL,'2025-09-26 06:30:08','Delivered','SUCCESS','COD'),(13,11,'ORD2025092612282311','order_RM8hiFbJ6BWflK','pay_RM8hw08q0TxfE2',1560,NULL,'2025-09-26 06:58:23','Out for Delivery','SUCCESS','ONLINE'),(14,12,'COD2025092615514912',NULL,NULL,999,NULL,'2025-09-26 10:21:49','Delivered','SUCCESS','COD'),(15,11,'COD2025092700074111',NULL,NULL,899,NULL,'2025-09-26 18:37:41','Delivered','SUCCESS','COD'),(16,8,'COD202509270029328',NULL,NULL,999,NULL,'2025-09-26 18:59:32','Delivered','SUCCESS','COD'),(17,11,'COD2025092700512911',NULL,NULL,999,NULL,'2025-09-26 19:21:29','Pending','COD PENDING','COD'),(18,11,'COD2025092701005711',NULL,NULL,1000,NULL,'2025-09-26 19:30:57','Pending','COD PENDING','COD'),(19,13,'COD2025092723241713',NULL,NULL,999,NULL,'2025-09-27 17:54:17','Pending','COD PENDING','COD'),(20,13,'COD2025092901294413',NULL,NULL,659,NULL,'2025-09-28 19:59:44','Delivered','SUCCESS','COD'),(21,13,'ORD2025092909125213','order_RNGyOxk8cHyCEH','pay_RNGyg2XK1DdJJ6',999,NULL,'2025-09-29 03:42:52','Pending','SUCCESS','ONLINE'),(22,13,'ORD2025092923490813','order_RNVu4hUC50MWbm','pay_RNVuIb2G3yXEcd',999,NULL,'2025-09-29 18:19:08','Exchanged','SUCCESS','ONLINE'),(23,8,'COD202509301311408',NULL,NULL,499,NULL,'2025-09-30 07:41:40','Delivered','SUCCESS','COD'),(24,8,'COD202509302145598',NULL,NULL,1000,NULL,'2025-09-30 16:15:59','Pending','COD PENDING','COD'),(25,8,'ORD202509302146578','order_RNsM9QdCM5v8JF','pay_RNsMKfc3USBibF',499,NULL,'2025-09-30 16:16:57','Cancelled','SUCCESS','ONLINE');
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `page_link` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Trending birthday frame','/product1'),(2,'3D Car Frame','/product2'),(3,'Birthday/Anniversary collage frame','/product3'),(4,'Secret Eye Mini Frame','/product4'),(5,'Backside Wolf Printed Oversized T-shirt','/product5'),(6,'Backside Spiderman Printed Oversized T-shirt','/product6'),(7,'Personalized Couple Hoodies','/product7'),(8,'Custom Best Friend Sweatshirt','/product8'),(9,'Cool Wall Sticker','/product9'),(10,'Custom Name Sticker','/product10'),(11,'Laptop Sticker Pack','/product11'),(12,'Car Bumper Sticker','/product12');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `return_requests`
--

DROP TABLE IF EXISTS `return_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `return_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` varchar(50) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `request_type` enum('return','exchange') DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `upi` varchar(100) DEFAULT NULL,
  `details` text,
  `image` varchar(255) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `return_requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `return_requests`
--

LOCK TABLES `return_requests` WRITE;
/*!40000 ALTER TABLE `return_requests` DISABLE KEYS */;
INSERT INTO `return_requests` VALUES (1,'ORD2025092923490813',13,'designbykamble@gmail.com','return','wrong_item','omkar@123','ok','ORD2025092923490813_Screenshot_2024-07-02_232114.png','Exchanged','2025-09-29 18:26:44');
/*!40000 ALTER TABLE `return_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `role` varchar(20) DEFAULT 'customer',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'chandu','chandu@gmail.com','scrypt:32768:8:1$lKBB533ndzOj8KGv$d9dce58fcc700515598618f6ac2ccfc436aaac3c256b196a0c1fb9395cbafb8f44abffd2f9a5a91f8b02cb6bf52932fe4c8edc9bf01692cc34131c260886889e',NULL,NULL,'customer'),(4,'chandu','chandu@gmail.com','scrypt:32768:8:1$AHrePEyZ9oWBxi5U$e3f441993746f25f23d5bcd12965162ff238f1150c16b7332b9cd73a1ac1dbd0f14bb946001fd1c1ce3a824ad61a450c34b7df0c51082f3050f3b7837ff6bed3',NULL,NULL,'customer'),(6,'hunter','hunter@gmail.com','scrypt:32768:8:1$oAeMKTasqTOovyBm$769e6348a52ef3eeba8a0acbc35ce0e2f5fe36f244e2ed5dd0ecf8b8230932caadb95ccdaa1a0d4543610c01a16d95e8621cfee5a2c9f714fa34d028138b6e76',NULL,NULL,'customer'),(8,'Admin','admin@printx.com','$2b$12$8MMCE.gnl.tVp7OAsJT9VukUvJAz7qx4uv8gnrgmj9i8HWvrqiCFK',NULL,NULL,'admin'),(9,'omkar','omiii@gmail.com','$2b$12$eDIiRZNeOl8V7VKy..d7xepEBgmxKJjDUyBYT1L2klz3JBxcGXKr.',NULL,NULL,'customer'),(11,'omkar','omkara.kamble312@gmail.com','scrypt:32768:8:1$dK2ZeCTI8bYZOwAV$386fa6fbc8499056594e1e029ce0188f04b93f8fe47d8be4fcd044faa9bff2a84e7a0050fc4bfffa54ce7e861571d961bc11136a9be4437d80e32f8acd9f7948',NULL,NULL,'customer'),(12,'ok','ravana@gmail.com','$2b$12$SBbV8A0I42GRP6YcJYxHOeXHUOxOdfvkPKgqAhZZqznvSoBfLAdty',NULL,NULL,'customer'),(13,'sami','omkar.kamble312@gmail.com','$2b$12$/Vc5YwhYHVB2j/UM5lAvbe1b2VbN7d6R0h6WAREp8/7ngWTne3Ufi','8454800234','2025-11-27','customer');
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

-- Dump completed on 2025-10-03 23:47:30
