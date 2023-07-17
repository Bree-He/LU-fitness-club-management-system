CREATE DATABASE  IF NOT EXISTS `comp639` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `comp639`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: comp639
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `attendance_id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `attendance_date` date DEFAULT NULL,
  `attendance_type` int NOT NULL DEFAULT '1',
  `class_booking_id` int DEFAULT NULL,
  `pt_booking_id` int DEFAULT NULL,
  PRIMARY KEY (`attendance_id`),
  KEY `attendance_ibfk_1` (`member_id`),
  KEY `group_class_booking_id_idx` (`class_booking_id`),
  KEY `pt_class_booking_id_idx` (`pt_booking_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`),
  CONSTRAINT `grpclass_booking_id` FOREIGN KEY (`class_booking_id`) REFERENCES `booking` (`class_id`),
  CONSTRAINT `pt_class_booking_id` FOREIGN KEY (`pt_booking_id`) REFERENCES `pt_class_schedule` (`training_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7028 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (7001,1001,'2023-03-20',1,6001,NULL),(7002,1002,'2023-01-20',1,6002,NULL),(7003,1003,'2023-03-20',1,6003,NULL),(7004,1004,'2023-03-20',1,6004,NULL),(7005,1005,'2023-03-20',1,6005,NULL),(7006,1001,'2023-03-21',2,NULL,8000),(7007,1005,'2023-03-29',3,NULL,NULL),(7008,1005,'2023-04-01',2,NULL,8007),(7009,1001,'2023-03-29',3,NULL,NULL),(7010,1002,'2023-03-29',3,NULL,NULL),(7011,1001,'2023-03-29',3,NULL,NULL),(7012,1003,'2023-03-29',3,NULL,NULL),(7013,1003,'2023-04-04',2,NULL,8008),(7014,1004,'2023-03-29',3,NULL,NULL),(7015,1005,'2023-03-29',3,NULL,NULL),(7016,1016,'2023-03-29',3,NULL,NULL),(7017,1016,'2023-04-09',2,NULL,8009),(7018,1017,'2023-03-29',3,NULL,NULL),(7019,1017,'2023-04-05',2,NULL,8010),(7020,1017,'2023-04-05',2,NULL,8011),(7021,1018,'2023-03-29',3,NULL,NULL),(7022,1018,'2023-04-04',2,NULL,8012),(7023,1019,'2023-03-29',3,NULL,NULL),(7024,1019,'2023-04-02',2,NULL,8013),(7025,1019,'2023-03-31',2,NULL,8014),(7026,1020,'2023-03-29',3,NULL,NULL),(7027,1020,'2023-04-07',2,NULL,8015);
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `bookin_id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `class_id` int NOT NULL,
  PRIMARY KEY (`bookin_id`),
  KEY `class_id_idx` (`class_id`),
  KEY `booking_ibfk_1_idx` (`member_id`),
  CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`),
  CONSTRAINT `class_id` FOREIGN KEY (`class_id`) REFERENCES `class_schedule` (`schedule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6023 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (6001,1001,1),(6002,1002,1),(6003,1003,1),(6004,1004,1),(6005,1005,1),(6006,1005,3020),(6007,1002,13),(6008,1002,3019),(6009,1001,6),(6010,1001,3016),(6011,1003,3024),(6012,1003,3021),(6013,1004,9),(6014,1004,3025),(6015,1016,14),(6016,1016,3028),(6017,1017,9),(6018,1018,8),(6019,1019,12),(6020,1019,6),(6021,1020,3019),(6022,1020,9);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_detail`
--

DROP TABLE IF EXISTS `class_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_detail` (
  `class_id` int NOT NULL AUTO_INCREMENT,
  `class_name` varchar(20) NOT NULL,
  `class_description` varchar(120) NOT NULL,
  `equipment_needed` varchar(20) DEFAULT 'N/A',
  `level_of_difficulty` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`class_id`),
  KEY `class_name` (`class_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2010 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_detail`
--

LOCK TABLES `class_detail` WRITE;
/*!40000 ALTER TABLE `class_detail` DISABLE KEYS */;
INSERT INTO `class_detail` VALUES (2001,'BodyAttack','SPORTS-INSPIRED HIGH-ENERGY TRAINING.','N/A','4/5'),(2002,'BodyBalance','YOGA-BASED CLASS THAT INCORPORATES TAI CHI AND PILATES.','Yoga mat','2/5'),(2003,'BodyCombat','HIGH-ENERGY MARTIAL-ARTS INSPIRED WORKOUT.','N/A','4/5'),(2004,'BodyJam','ADDICTIVE DANCE STYLES AND THE HOTTEST NEW MUSIC.','N/A','3/5'),(2005,'BodyPump','TOTAL BODY WORKOUT TO GAIN STRENGTH AND LEAN, TONED MUSCLE.','Barbell','3/5'),(2006,'Chiseled','A COMBINATION OF AEROBIC AND STRENGTH EXERCISES.','N/A','4/5'),(2007,'Lincoln 45','A HIGH-INTENSITY FULL-BODY EXERCISE','Yoga mat','3/5'),(2008,'Yoga','A SYSTEM TO FOSTER WELL-BEING ON THE PHYSICAL, MENTAL, EMOTIONAL, AND SPIRITUAL LEVELS.','Yoga mat','3/5'),(2009,'Zumba','BURN OFF CALORIES BY DANCING TO DIFFERENT KINDS OF LIVELY TUNES','N/A','4/5');
/*!40000 ALTER TABLE `class_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_schedule`
--

DROP TABLE IF EXISTS `class_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `class_name` varchar(20) NOT NULL,
  `max_capacity` int NOT NULL,
  `class_day` varchar(20) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `trainer_id` int NOT NULL,
  `class_date` date NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `trainer_id` (`trainer_id`),
  KEY `class_name_idx` (`class_name`),
  CONSTRAINT `class_name` FOREIGN KEY (`class_name`) REFERENCES `class_detail` (`class_name`),
  CONSTRAINT `trainer_id` FOREIGN KEY (`trainer_id`) REFERENCES `trainers` (`trainer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3039 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_schedule`
--

LOCK TABLES `class_schedule` WRITE;
/*!40000 ALTER TABLE `class_schedule` DISABLE KEYS */;
INSERT INTO `class_schedule` VALUES (1,'BodyAttack',30,'Monday','13:00:00','14:00:00',4,'2023-03-20'),(3,'Zumba',30,'Wednesday','10:00:00','11:00:00',1,'2023-04-05'),(4,'Lincoln 45',30,'Thursday','16:00:00','17:00:00',2,'2023-04-06'),(5,'Chiseled',30,'Friday','08:00:00','09:00:00',3,'2023-03-31'),(6,'BodyAttack',28,'Monday','13:00:00','14:00:00',4,'2023-04-03'),(7,'BodyBalance',30,'Wednessday','11:00:00','12:00:00',5,'2023-04-05'),(8,'BodyPump',29,'Friday','09:00:00','10:00:00',6,'2023-03-31'),(9,'BodyCombat',27,'Tuesday','14:00:00','15:00:00',7,'2023-04-04'),(10,'BodyJam',30,'Thursday','14:00:00','15:00:00',8,'2023-04-06'),(11,'BodyPump',30,'Sunday','08:00:00','09:00:00',9,'2023-04-02'),(12,'BodyBalance',29,'Saturday','08:00:00','09:00:00',10,'2023-04-01'),(13,'Yoga',29,'Saturday','10:00:00','11:00:00',1,'2023-04-01'),(14,'Zumba',29,'Sunday','16:00:00','17:00:00',2,'2023-04-02'),(3015,'Zumba',30,'Sunday','16:00:00','17:00:00',2,'2023-04-09'),(3016,'Yoga',29,'Saturday','10:00:00','11:00:00',1,'2023-04-07'),(3017,'BodyBalance',30,'Saturday','08:00:00','09:00:00',10,'2023-04-07'),(3018,'BodyPump',30,'Sunday','08:00:00','09:00:00',9,'2023-04-09'),(3019,'BodyJam',28,'Thursday','14:00:00','15:00:00',8,'2023-04-13'),(3020,'BodyCombat',29,'Tuesday','14:00:00','15:00:00',7,'2023-04-11'),(3021,'BodyPump',29,'Friday','09:00:00','10:00:00',6,'2023-04-07'),(3022,'BodyBalance',30,'Wednessday','11:00:00','12:00:00',5,'2023-04-12'),(3023,'BodyAttack',30,'Monday','13:00:00','14:00:00',4,'2023-04-10'),(3024,'Chiseled',29,'Friday','08:00:00','09:00:00',3,'2023-04-07'),(3025,'Lincoln 45',29,'Thursday','16:00:00','17:00:00',2,'2023-04-13'),(3026,'Zumba',30,'Wednesday','10:00:00','11:00:00',1,'2023-04-12'),(3027,'Zumba',30,'Sunday','16:00:00','17:00:00',2,'2023-04-16'),(3028,'Yoga',29,'Saturday','10:00:00','11:00:00',1,'2023-04-15'),(3029,'BodyBalance',30,'Saturday','08:00:00','09:00:00',10,'2023-04-15'),(3030,'BodyPump',30,'Sunday','08:00:00','09:00:00',9,'2023-04-16'),(3031,'BodyJam',30,'Thursday','14:00:00','15:00:00',8,'2023-04-20'),(3032,'BodyCombat',30,'Tuesday','14:00:00','15:00:00',7,'2023-04-18'),(3033,'BodyPump',30,'Friday','09:00:00','10:00:00',6,'2023-04-14'),(3034,'BodyBalance',30,'Wednessday','11:00:00','12:00:00',5,'2023-04-19'),(3035,'BodyAttack',30,'Monday','13:00:00','14:00:00',4,'2023-04-17'),(3036,'Chiseled',30,'Friday','08:00:00','09:00:00',3,'2023-04-14'),(3037,'Lincoln 45',30,'Thursday','16:00:00','17:00:00',2,'2023-04-20'),(3038,'Zumba',30,'Wednesday','10:00:00','11:00:00',1,'2023-04-19');
/*!40000 ALTER TABLE `class_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members`
--

DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `members` (
  `member_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `dob` date NOT NULL,
  `address` varchar(30) NOT NULL,
  `email` varchar(80) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `subscription_status` varchar(20) NOT NULL DEFAULT 'active',
  `health_condition` varchar(120) NOT NULL DEFAULT 'N/A',
  `sub_duedate` date NOT NULL,
  `auto_pay` varchar(45) NOT NULL DEFAULT 'no',
  PRIMARY KEY (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1021 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members`
--

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (1001,'Kelly','Smith','2005-06-12','10 cover lan christchurch','kellysmith@gmail.com','02-323-45678','active','overweight','2023-04-25','no'),(1002,'Jake','Doe','2004-11-21','123 Main St','john.doe@gmail.com','02-155-51234','active','N/A','2023-03-31','no'),(1003,'Kate','Doe','2003-09-07','456 Oak Ave','jane.doe@gmail.com','02-055-55678','active','N/A','2023-04-05','no'),(1004,'Bob','Smith','2006-05-15','789 Elm St','bob.smith@gmail.com','02-255-59012','active','asthma','2023-04-04','no'),(1005,'Sam','Sun','2004-08-08','321 Maple St','sam.sun@gmail.com','02-155-53456','active','asthma','2023-04-14','yes'),(1016,'Kay','Lee','2005-10-24','13 Queen Street','k.lee@gmail.com','02-323-45678','active','N/A','2023-04-14','no'),(1017,'Kitty','Ko','2001-12-03','2/698 Epsom Road','riko@gmail.com','02-323-45678','active','back injury','2023-04-14','no'),(1018,'David','Chard','2002-04-26','337 Great North Rd','d.chard@gmail.com','02-055-56788','active','N/A','2023-04-14','no'),(1019,'Kassie','Wang','2001-02-28','86 Beach Rd','kassie.wang@gmail.com','02-323-45678','active','N/A','2023-04-14','no'),(1020,'Roy','Volk','2001-02-20','18 Landscape Ave','roy.v@gmail.com','02-111-006580','active','N/A','2023-04-25','no');
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_detail`
--

DROP TABLE IF EXISTS `payment_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_detail` (
  `member_id` int NOT NULL,
  `payment_date` date NOT NULL,
  `payment_amount` decimal(8,2) NOT NULL,
  `payment_method` varchar(45) NOT NULL,
  `payment_status` varchar(45) NOT NULL,
  KEY `member_id_idx` (`member_id`),
  CONSTRAINT `member_id` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_detail`
--

LOCK TABLES `payment_detail` WRITE;
/*!40000 ALTER TABLE `payment_detail` DISABLE KEYS */;
INSERT INTO `payment_detail` VALUES (1001,'2023-02-01',10.00,'Online','Successful'),(1002,'2023-02-01',10.00,'Online','Successful'),(1003,'2023-02-05',10.00,'Cash','Successful'),(1004,'2023-02-10',10.00,'Online','Successful'),(1005,'2023-02-15',10.00,'Eftpos','Successful'),(1017,'2023-03-15',30.00,'at gym','Successful'),(1018,'2023-03-15',30.00,'at gym','Successful'),(1019,'2023-03-15',30.00,'at gym','Successful'),(1005,'2023-03-26',30.00,'auto','Successful'),(1001,'2023-03-26',30.00,'at gym','Successful'),(1020,'2023-03-26',0.00,'signup','Successful');
/*!40000 ALTER TABLE `payment_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pt_class`
--

DROP TABLE IF EXISTS `pt_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pt_class` (
  `pt_class_id` int NOT NULL AUTO_INCREMENT,
  `pt_class_name` varchar(45) NOT NULL,
  `avail_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `capacity` tinyint(1) NOT NULL DEFAULT '1',
  `trainer_id` int NOT NULL,
  `price` decimal(8,2) NOT NULL DEFAULT '30.00',
  PRIMARY KEY (`pt_class_id`),
  KEY `trainer_idx` (`trainer_id`),
  CONSTRAINT `trainer` FOREIGN KEY (`trainer_id`) REFERENCES `trainers` (`trainer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4022 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pt_class`
--

LOCK TABLES `pt_class` WRITE;
/*!40000 ALTER TABLE `pt_class` DISABLE KEYS */;
INSERT INTO `pt_class` VALUES (4000,'CoreStrength','2023-03-21','20:00:00','21:00:00',0,7,30.00),(4001,'WeightControl','2023-04-02','18:00:00','19:00:00',1,1,30.00),(4002,'WeightLoss','2023-03-31','19:00:00','20:00:00',0,3,30.00),(4003,'FuntionalTraining','2023-04-01','18:00:00','19:00:00',1,10,30.00),(4004,'CoreStrength','2023-04-04','20:00:00','21:00:00',0,7,30.00),(4005,'FuntionalTraining','2023-04-02','19:00:00','20:00:00',0,5,30.00),(4006,'WeightControl','2023-04-05','18:00:00','19:00:00',0,6,30.00),(4007,'WeightLoss','2023-03-31','18:00:00','19:00:00',1,2,30.00),(4008,'FuntionalTraining','2023-04-01','20:00:00','21:00:00',0,9,30.00),(4009,'CoreStrength','2023-04-04','19:00:00','20:00:00',0,4,30.00),(4010,'FuntionalTraining','2023-04-05','19:00:00','20:00:00',0,8,30.00),(4011,'WeightControl','2023-04-12','18:00:00','19:00:00',1,6,30.00),(4012,'FuntionalTraining','2023-04-12','19:00:00','20:00:00',1,8,30.00),(4013,'CoreStrength','2023-04-11','20:00:00','21:00:00',1,7,30.00),(4014,'CoreStrength','2023-04-11','19:00:00','20:00:00',1,4,30.00),(4015,'WeightControl','2023-04-09','18:00:00','19:00:00',1,1,30.00),(4016,'FuntionalTraining','2023-04-09','19:00:00','20:00:00',0,5,30.00),(4017,'FuntionalTraining','2023-04-08','18:00:00','19:00:00',1,10,30.00),(4018,'FuntionalTraining','2023-04-08','20:00:00','21:00:00',1,9,30.00),(4019,'WeightLoss','2023-04-07','19:00:00','20:00:00',0,3,30.00),(4020,'WeightLoss','2023-04-07','18:00:00','19:00:00',1,2,30.00),(4021,'CoreStrength','2023-02-28','20:00:00','21:00:00',0,7,30.00);
/*!40000 ALTER TABLE `pt_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pt_class_payment`
--

DROP TABLE IF EXISTS `pt_class_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pt_class_payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `pt_class_payment_date` date NOT NULL,
  `pt_class_payment_amount` decimal(8,2) DEFAULT NULL,
  `pt_class_payment_method` varchar(45) DEFAULT NULL,
  `pt_class_payment_status` varchar(45) DEFAULT NULL,
  `pt_booking_id` int DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `member_id_idx` (`member_id`),
  KEY `traning_id_idx` (`pt_booking_id`),
  CONSTRAINT `pt_booking_id` FOREIGN KEY (`pt_booking_id`) REFERENCES `pt_class_schedule` (`training_id`),
  CONSTRAINT `pt_class_payment_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pt_class_payment`
--

LOCK TABLES `pt_class_payment` WRITE;
/*!40000 ALTER TABLE `pt_class_payment` DISABLE KEYS */;
INSERT INTO `pt_class_payment` VALUES (1,1001,'2023-03-15',30.00,'Online','Successful',8000),(2,1002,'2023-03-16',30.00,'Online','Successful',8002),(3,1003,'2023-03-16',30.00,'Online','Successful',8003),(4,1004,'2023-03-17',30.00,'Online','Successful',8004),(5,1005,'2023-03-18',30.00,'Online','Successful',8005),(6,1001,'2023-03-15',30.00,'Online','Successful',8001),(7,1002,'2023-02-20',30.00,'Online','Successful',8006),(8,1005,'2023-03-29',30.00,'Online','Successful',8007),(9,1003,'2023-03-29',30.00,'Online','Successful',8008),(10,1016,'2023-03-29',30.00,'Online','Successful',8009),(11,1017,'2023-03-29',30.00,'Online','Successful',8010),(12,1017,'2023-03-29',30.00,'Online','Successful',8011),(13,1018,'2023-03-29',30.00,'Online','Successful',8012),(14,1019,'2023-03-29',30.00,'Online','Successful',8013),(15,1019,'2023-03-29',30.00,'Online','Successful',8014),(16,1020,'2023-03-29',30.00,'Online','Successful',8015);
/*!40000 ALTER TABLE `pt_class_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pt_class_schedule`
--

DROP TABLE IF EXISTS `pt_class_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pt_class_schedule` (
  `training_id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `pt_class_id` int NOT NULL,
  PRIMARY KEY (`training_id`),
  KEY `member_id` (`member_id`),
  KEY `pt_class_id_idx` (`pt_class_id`),
  CONSTRAINT `pt_class_id` FOREIGN KEY (`pt_class_id`) REFERENCES `pt_class` (`pt_class_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8016 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pt_class_schedule`
--

LOCK TABLES `pt_class_schedule` WRITE;
/*!40000 ALTER TABLE `pt_class_schedule` DISABLE KEYS */;
INSERT INTO `pt_class_schedule` VALUES (8000,1001,4000),(8001,1001,4001),(8002,1002,4002),(8003,1003,4003),(8004,1004,4004),(8005,1005,4005),(8006,1002,4021),(8007,1005,4008),(8008,1003,4004),(8009,1016,4016),(8010,1017,4006),(8011,1017,4010),(8012,1018,4009),(8013,1019,4005),(8014,1019,4002),(8015,1020,4019);
/*!40000 ALTER TABLE `pt_class_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trainer_comment`
--

DROP TABLE IF EXISTS `trainer_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trainer_comment` (
  `comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `training_id` int NOT NULL,
  PRIMARY KEY (`training_id`),
  KEY `training_id_idx` (`training_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trainer_comment`
--

LOCK TABLES `trainer_comment` WRITE;
/*!40000 ALTER TABLE `trainer_comment` DISABLE KEYS */;
INSERT INTO `trainer_comment` VALUES ('get more protien to build up muscle!',8000),('nnnn',8004);
/*!40000 ALTER TABLE `trainer_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trainers`
--

DROP TABLE IF EXISTS `trainers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trainers` (
  `trainer_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `dob` date NOT NULL,
  `email` varchar(45) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `education` varchar(80) DEFAULT NULL,
  `expertise` varchar(45) DEFAULT 'null',
  `self_introduction` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`trainer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trainers`
--

LOCK TABLES `trainers` WRITE;
/*!40000 ALTER TABLE `trainers` DISABLE KEYS */;
INSERT INTO `trainers` VALUES (1,'Jason','Kim','1991-06-20','jason.kim@gmail.com','02-255-51234','Bachelor\'s degree in Exercise Science/ACSM-CPT','Strength and conditioning','Passionate and experienced trainer specialized in strength and conditioning. Committed to building strong foundations and personalized programs for clients to achieve their fitness goals.'),(2,'Neil','Chen','1990-04-20','neil.chen@gmail.com','02-155-55678','Bachelor\'s degree in Athletic Training/ACE-CPT','Cardiovascular training','I\'m a cardio trainer who helps improve heart health and fitness through customized exercise plans.'),(3,'Carl','Davis','1993-03-07','carl.davis@gmail.com','02-055-59012','Bachelor\'s degree in Health and Human Performance/NASM-CPT','Nutrition and weight management','Passionate trainer specializing in weight loss and body transformation. Dedicated to helping clients achieve sustainable results through lifestyle changes and personalized programs.'),(4,'Joe','Wilson','1988-07-02','joe.wilson@gmail.com','02-155-53456','Master\'s degree in Sports Science/NSCA-CPT','Functional training','Experienced trainer with a focus on strength and endurance training. Committed to helping clients improve their physical abilities and overall health.'),(5,'Jade','Brown','1988-02-22','jade.brown@gmail.com','02-155-57890','Bachelor\'s degree in Health and Human Performance/ACE-CPT','Functional training','I\'m specializes in functional fitness and works closely with clients to develop personalized programs that prioritize long-term health and wellness.'),(6,'Liam','Kim','1990-05-07','liam.kim@gmail.com','02-255-51234','Bachelor\'s degree in Sports Science/NASM-CPT','Strength and conditioning','Results-driven trainer with extensive experience in strength and conditioning. Committed to helping clients achieve their full potential and reach their fitness goals, no matter how challenging.'),(7,'Karen','Chen','1984-09-12','karen.chen@gmail.com','02-055-55678','Bachelor\'s degree in Physical Education/ACSM-CPT','Cardiovascular training','Enthusiastic trainer committed to helping clients develop healthy habits and reach their fitness goals. Specializes in designing engaging and challenging workouts that keep clients motivated and on track.'),(8,'Jerry','Davis','1992-12-01','jerry.davis@gmail.com','02-055-59012','Master\'s degree in Exercise Physiology/NSCA-CPT','Nutrition and weight management','I help people reach their health goals through personalized dietary plans and lifestyle changes.'),(9,'Caleb','Wilson','1989-01-18','caleb.wilson@gmail.com','02-155-53456','Bachelor\'s degree in Kinesiology/ACE-CPT','Functional training','Dedicated trainer with expertise in injury prevention and rehabilitation. Passionate about helping clients'),(10,'Mike','Brown','1995-10-30','mike.brown@gmail.com','02-055-57890','Bachelor\'s degree in Sports Medicine/NASM-CPT','Functional training','Passionate and knowledgeable trainer specializing in functional training and injury prevention. Devoted to helping clients lead healthier, more active lives.');
/*!40000 ALTER TABLE `trainers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `username` varchar(30) NOT NULL,
  `role` varchar(30) NOT NULL,
  `password` varchar(30) DEFAULT 'null',
  `userid` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('admin01','admin',NULL,1),('admin02','admin',NULL,2),('bob.smith@gmail.com','member',NULL,3),('caleb.wilson@gmail.com','trainer','null',4),('carl.davis@gmail.com','trainer','null',5),('jade.brown@gmail.com','trainer','null',6),('jane.doe@gmail.com','member',NULL,7),('jason.kim@gmail.com','trainer','null',8),('jerry.davis@gmail.com','trainer','null',9),('joe.wilson@gmail.com','trainer','null',10),('john.doe@gmail.com','member',NULL,11),('karen.chen@gmail.com','trainer','null',12),('k.lee@gmail.com','member',NULL,13),('kellysmith@gmail.com','member',NULL,14),('liam.kim@gmail.com','trainer','null',15),('mike.brown@gmail.com','trainer','null',16),('neil.chen@gmail.com','trainer','null',17),('sam.sun@gmail.com','member',NULL,18),('riko@gmail.com','member','null',19),('d.chard@gmail.com','member','null',20),('kassie.wang@gmail.com','member','null',21),('roy.v@gmail.com','member','null',22);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-29 16:33:35
