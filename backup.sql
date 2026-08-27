-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: the_smart_bazaar
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'admin','admin123'),(2,'sandeep','sandeep123');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Electronics','electronics.jpg'),(27,'Fashion','fashion.jpg'),(31,'Home & Furniture','home.jpg'),(32,'Books','books.jpg'),(33,'Toys','toys.jpg'),(34,'Sports','sports.jpg'),(35,'Jewellery','jewelery.jpg'),(36,'Shoes','banner.jpg');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` varchar(20) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `product_name` text DEFAULT NULL,
  `total_amount` int(11) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (41,'ORD81909',5,'Basketball Official Size',799,'Online Payment','B/707 Sai Enclave Near Waman Dhaba Naigaon East','9175392813','sp5.jpg','Pending','2026-05-15 02:40:20'),(42,'ORD37568',5,'Black Graphic T-Shirt',599,'Online Payment','B/707 Sai Enclave Near Waman Dhaba Naigaon East','9175392813','tshirt1.jpg','Pending','2026-05-15 04:47:19'),(43,'ORD21226',5,'Gold Plated Necklace Set',1999,'Online Payment','B/707 Sai Enclave Near Waman Dhaba Naigaon East','9175392813','jw1.jpg','Pending','2026-05-15 05:20:50'),(44,'ORD70406',2,'Samsung Galaxy S26 5G',87999,'Online Payment','B/707 Sai Enclave Near Waman Dhaba Naigaon East','9175392813','mob1.jpg','Pending','2026-05-15 08:40:40'),(45,'ORD60738',2,'Basketball Official Size',799,'Online Payment','B/707 Sai Enclave Near Waman Dhaba Naigaon East','9175392813','sp5.jpg','Pending','2026-05-16 05:36:06'),(46,'ORD69540',2,'Leather Cricket Ball',299,'Online Payment','Naigaon E Rd','9175392813','sp3.jpg','Pending','2026-05-19 05:08:10'),(47,'ORD83118',2,'Smart Watch',2999,'Online Payment','B/707 Sai Enclave Near Waman Dhaba Naigaon East','9175392813','smartwatch.jpg','Pending','2026-05-30 14:17:44'),(48,'ORD20623',6,'Leather Cricket Ball',299,'Online Payment','Naigaon E Rd','8855444646','sp3.jpg','Pending','2026-08-27 08:58:03'),(49,'ORD74818',6,'Smart Watch',2999,'Online Payment','Naigaon E Rd','9175392813','smartwatch.jpg','Pending','2026-08-27 08:59:15'),(50,'ORD58567',6,'Xiaomi Smart TV 43',24999,'Online Payment','Naigaon E Rd','9175392813','tv.jpg','Pending','2026-08-27 09:00:30');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (5,'Oversized Beige T-Shirt',699,'Loose fit streetwear style t-shirt.','tshirt2.jpg',27),(6,'Black Graphic T-Shirt',599,'Trendy printed t-shirt with soft fabric.','tshirt1.jpg',27),(7,'Smart Watch',2999,'Stylish smartwatch with health tracking','smartwatch.jpg',1),(9,'Samsung Galaxy S26 5G',87999,'Flagship phone with AMOLED display.','mob1.jpg',1),(10,'Vivo V70 5G',45999,'50MP camera with fast charging.','mob2.jpg',1),(11,'Infinix Note 60 Pro',19999,'Budget 5G phone with long battery.','mob3.jpg',1),(12,'boAt Airdopes 441',2499,'Wireless earbuds with deep bass.','ear1.jpg',1),(13,'OnePlus Nord Buds 2',2999,'Noise cancellation earbuds.','ear2.jpg',1),(14,'Realme Buds Air 5',3499,'ANC earbuds for gaming.','ear3.jpg',1),(15,'Xiaomi Smart TV 43',24999,'4K Ultra HD Android TV.','tv.jpg',1),(16,'JBL Cinema SB241',8999,'Dolby Digital soundbar.','sb.jpg',1),(17,'Formal White Shirt',1299,'Cotton formal shirt for office wear.','shirt1.jpg',27),(18,'Checked Casual Shirt',999,'Stylish checked shirt for daily wear.','shirt2.jpg',27),(19,'Slim Fit Blue Jeans',1499,'Stretchable slim fit denim jeans.','jeans1.jpg',27),(20,'Black Regular Jeans',1399,'Classic black jeans for everyday use.','jeans2.jpg',27),(21,'Leather Jacket',2499,'Stylish leather jacket for winter.','jacket1.jpg',27),(23,'Denim Jacket',1999,'Stylish denim jacket for daily use.','jacket2.jpg',27),(48,'Wooden Dining Chair',3499,'Comfortable wooden chair with cushion','chair.jpeg',31),(49,'Modern Coffee Table',6999,'Stylish wooden coffee table','table.jpeg',31),(50,'3-Seater Sofa',18999,'Comfortable fabric sofa','sofa.jpeg',31),(51,'Bookshelf Rack',5499,'Storage shelf for books','booshelf.jpeg',31),(52,'Soft Carpet',2299,'Cozy floor carpet','carpet.jpeg',31),(53,'Table Lamp',1799,'Decorative lamp','lamp.jpeg',31),(54,'Wooden Bed',14999,'Queen size bed','bed.jpeg',31),(55,'Drawer Cabinet',8499,'Storage drawer unit','drawer.jpeg',31),(56,'The Psychology of Money',399,'Wealth and mindset lessons','book1.jpg',32),(57,'Atomic Habits',499,'Build powerful habits','book2.jpg',32),(58,'Rich Dad Poor Dad',349,'Financial education guide','book3.jpg',32),(59,'Ikigai',299,'Japanese life philosophy','book4.jpg',32),(60,'Do Epic Shit',299,'Motivation and growth','book5.jpg',32),(61,'Think and Grow Rich',399,'Success mindset classic','book6.jpg',32),(62,'The Alchemist',249,'Dream and destiny story','book7.jpg',32),(63,'You Can Win',299,'Self improvement guide','book8.jpg',32),(64,'LEGO Building Blocks Set',799,'Creative building blocks for kids learning & fun','toy1.jpg',33),(65,'Remote Control Car',1299,'High-speed RC car with rechargeable battery','toy2.jpg',33),(66,'Teddy Bear Soft Toy',499,'Cute fluffy teddy bear for kids & gifting','toy3.jpg',33),(67,'Puzzle Game Set',349,'Brain-boosting puzzle game for kids learning skills','toy4.jpg',33),(68,'Kids Kitchen Toy Set',899,'Mini kitchen set for roleplay & creativity','toys5.jpg',33),(69,'Toy Train Set',1499,'Electric toy train with tracks and lights','toys6.jpg',33),(70,'Doll House Play Set',2199,'Beautiful multi-room doll house for kids','toy7.jpg',33),(71,'Alphabet Learning Board',299,'Learning board for alphabets & early education','toy8.jpg',33),(72,'Football Pro Match Ball',899,'FIFA standard durable football for professional matches','sp1.jpg',34),(73,'English Willow Cricket Bat',2499,'High-quality bat for powerful shots and tournaments','sp2.jpg',34),(74,'Leather Cricket Ball',299,'Strong stitched leather ball for practice and matches','sp3.jpg',34),(75,'Badminton Racket Set',999,'Lightweight rackets with high tension strings for better control','sp4.jpg',34),(76,'Basketball Official Size',799,'Grip-friendly basketball suitable for indoor and outdoor games','sp5.jpg',34),(77,'Speed Skipping Rope',199,'Adjustable skipping rope for cardio and fitness training','sp6.jpg',34),(78,'Gym Dumbbells Set (10kg)',1499,'Home workout dumbbells set for strength training','sp7.jpg',34),(79,'Table Tennis Paddle Set',599,'Professional paddle set with high control and spin','sp8.jpg',34),(80,'Gold Plated Necklace Set',1999,'Elegant gold plated necklace with matching earrings for festive wear','jw1.jpg',35),(81,'Diamond Style Ring',1499,'Sparkling diamond-style ring perfect for parties and engagement','jw2.jpg',35),(82,'Traditional Bangles Set',799,'Beautiful ethnic bangles set for traditional occasions','jw3.jpg',35),(83,'Pearl Earrings Set',599,'Classic pearl earrings suitable for daily and formal wear','jw4.jpg',35),(84,'Bridal Jewellery Set',4999,'Complete bridal jewellery set with premium design and shine','jw5.jpg.webp',35),(85,'Silver Anklet Pair',899,'Stylish silver anklets with detailed traditional design','jw6.jpg',35),(86,'American Diamond Necklace',1799,'Shiny AD necklace perfect for parties and functions','jw7.jpg',35),(87,'Designer Nose Ring (Nath)',599,'Traditional designer nose ring for ethnic Indian look','jw8.jpg',35),(88,'Running Sports Shoes',1299,'Lightweight running shoes for daily fitness and jogging','sh1.jpg',36),(89,'Casual Sneakers',999,'Stylish sneakers for everyday casual wear','sh2.jpeg',36),(90,'Formal Leather Shoes',1599,'Premium leather formal shoes for office and meetings','sh3.jpg',36),(91,'High Ankle Sports Shoes',1799,'Strong grip ankle shoes for outdoor sports','sh4.jpg',36),(92,'Walking Comfort Shoes',899,'Soft cushion shoes for long walking comfort','sh5.jpg',36),(93,'Gym Training Shoes',1199,'Flexible shoes designed for gym workouts and training','sh6.jpg',36),(94,'Skateboard Shoes',1399,'Durable shoes designed for skateboarding and street style','sh7.jpg',36),(95,'Slip-On Casual Shoes',799,'Easy slip-on shoes for daily quick use and comfort','sh8.jpg',36);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tsb_regs_record`
--

DROP TABLE IF EXISTS `tsb_regs_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tsb_regs_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tsb_regs_record`
--

LOCK TABLES `tsb_regs_record` WRITE;
/*!40000 ALTER TABLE `tsb_regs_record` DISABLE KEYS */;
INSERT INTO `tsb_regs_record` VALUES (1,'sandeep kumhar','sandeepkumhar00@gmail.com','9175392813','260904','2026-04-03 07:04:39'),(2,'Sandeep Kumhar','Sandeepkumhar26@gmail.com','9175392813','sandeep26','2026-04-03 07:56:28'),(4,'kfkfk','Sandeep@gmail.com','9977552232','45545454','2026-04-03 11:31:14'),(5,'deva','deva123@gmail.com','9158236974','pass123','2026-05-15 02:35:04'),(6,'sam','sam@gmail.com','9175399999','scrypt:32768:8:1$ig4b1XAKtQfyizO5$decc48659321cdabbd5b4028ef5bdee3b9422b1eaaa13e12484f86b4287d23fe623b190723151e663b259e6353677521d5e4d3a6ebf7f6798f1283e021c5dd16','2026-08-27 08:32:25');
/*!40000 ALTER TABLE `tsb_regs_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist`
--

DROP TABLE IF EXISTS `wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wishlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist`
--

LOCK TABLES `wishlist` WRITE;
/*!40000 ALTER TABLE `wishlist` DISABLE KEYS */;
INSERT INTO `wishlist` VALUES (8,2,9);
/*!40000 ALTER TABLE `wishlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-27 15:53:31
