/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.28-MariaDB : Database - directmarketingagriculture
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`directmarketingagriculture` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;

USE `directmarketingagriculture`;

/*Table structure for table `buyers` */

DROP TABLE IF EXISTS `buyers`;

CREATE TABLE `buyers` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `bname` varchar(200) DEFAULT NULL,
  `bemail` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `contact` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `profile` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `buyers` */

insert  into `buyers`(`id`,`bname`,`bemail`,`password`,`contact`,`address`,`profile`,`status`) values (1,'buyer','buyer@gmail.com','708175b3fdb269c4ebe8e7751bb3fccd','9966441122','bangalore','static/profiles/wallpaper.jpg','pending'),(2,'b','b@gmail.com','65c3549fed9ff494ff34ad5678d6f516','9652145698','bangalore','static/profiles/new.jpg','pending');

/*Table structure for table `cropinfo` */

DROP TABLE IF EXISTS `cropinfo`;

CREATE TABLE `cropinfo` (
  `id` int(200) NOT NULL AUTO_INCREMENT,
  `cropname` varchar(200) DEFAULT NULL,
  `category` varchar(200) DEFAULT NULL,
  `Minimumcost` varchar(200) DEFAULT NULL,
  `myfile` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `cropinfo` */

insert  into `cropinfo`(`id`,`cropname`,`category`,`Minimumcost`,`myfile`) values (1,'Rice','Grains','150','static/profiles/rice.jpg'),(2,'Wheat','Grains','150','static/profiles/wheat.jpg'),(3,'Almonds','Nuts','700','static/profiles/Lentils.jpg'),(4,'Walnuts','Nuts','800','static/profiles/Jowar.jpg'),(5,'Mustard Seeds','Seeds','250','static/profiles/Bajra.jpg'),(6,'Sesame Seeds','Seeds','1200','static/profiles/Lentils.jpg');

/*Table structure for table `croporder` */

DROP TABLE IF EXISTS `croporder`;

CREATE TABLE `croporder` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `cropname` varchar(200) DEFAULT NULL,
  `category` varchar(200) DEFAULT NULL,
  `mincost` varchar(200) DEFAULT NULL,
  `quantity` varchar(200) DEFAULT NULL,
  `myorder` varchar(200) DEFAULT NULL,
  `season` varchar(200) DEFAULT NULL,
  `totalquantity` varchar(200) DEFAULT NULL,
  `semail` varchar(200) DEFAULT NULL,
  `bemail` varchar(200) DEFAULT NULL,
  `amount` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  `imgfile` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `croporder` */

insert  into `croporder`(`id`,`cropname`,`category`,`mincost`,`quantity`,`myorder`,`season`,`totalquantity`,`semail`,`bemail`,`amount`,`status`,`imgfile`) values (1,'Rice','Grains','150','2500','100','2024-12-21','2400','kumar@gmail.com','buyer@gmail.com','15000','Accepted','static/profiles/rice.jpg');

/*Table structure for table `cropprice` */

DROP TABLE IF EXISTS `cropprice`;

CREATE TABLE `cropprice` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `cropname` varchar(200) DEFAULT NULL,
  `category` varchar(200) DEFAULT NULL,
  `mincost` varchar(200) DEFAULT NULL,
  `quantity` varchar(200) DEFAULT NULL,
  `Yieldtime` varchar(200) DEFAULT NULL,
  `myfile` varchar(200) DEFAULT NULL,
  `semail` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `amount` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  `totalquantity` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `cropprice` */

insert  into `cropprice`(`id`,`cropname`,`category`,`mincost`,`quantity`,`Yieldtime`,`myfile`,`semail`,`address`,`amount`,`status`,`totalquantity`) values (1,'Rice','Grains','150','2500','2024-12-21','static/profiles/rice.jpg','farmer@gmail.com','bangalore',NULL,'pending','2400'),(2,'Wheat','Grains','150','1500','2024-12-21','static/profiles/wheat.jpg','farmer@gmail.com','bangalore',NULL,'pending','1500'),(3,'Rice','Grains','150','2000','2024-11-09','static/profiles/rice.jpg','kumar@gmail.com','tirupati',NULL,'pending','2400'),(4,'Walnuts','Nuts','800','2000','2024-11-14','static/profiles/Bajra.jpg','kumar@gmail.com','tirupati',NULL,'pending','2000'),(5,'Mustard Seeds','Seeds','250','200','2024-11-21','static/profiles/Bajra.jpg','kumar@gmail.com','tirupati',NULL,'pending','200');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `Amount` varchar(200) DEFAULT NULL,
  `Cardname` varchar(200) DEFAULT NULL,
  `Cardnumber` varchar(100) DEFAULT NULL,
  `expmonth` varchar(200) DEFAULT NULL,
  `cvv` varchar(200) DEFAULT NULL,
  `Email` varchar(200) DEFAULT NULL,
  `semail` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `payment` */

insert  into `payment`(`id`,`Amount`,`Cardname`,`Cardnumber`,`expmonth`,`cvv`,`Email`,`semail`,`status`) values (1,'15000','Preeti Desai','9685745896547896','12/26','258','buyer@gmail.com','kumar@gmail.com','Completed');

/*Table structure for table `sellers` */

DROP TABLE IF EXISTS `sellers`;

CREATE TABLE `sellers` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `sname` varchar(200) DEFAULT NULL,
  `semail` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `contact` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `Profile` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `sellers` */

insert  into `sellers`(`id`,`sname`,`semail`,`password`,`contact`,`address`,`Profile`,`status`) values (1,'nani','nani@gmail.com','2f3785ca4c0f3e08e78b7aec9e25271b','6363379953','kakinada','static/profiles/balaram_5Mt8CGB_vVeJEa6.png','pending'),(2,'kumar','Kumar@gmail.com','181478ad7869aed751fb556c11ed7a0b','6363379953','kakinada','static/profiles/wallpaper.jpg','pending'),(3,'a','a@gmail.com','87f63909c0c85fefc712cb53cd63807b','9966558877','kakinada','static/profiles/CLASS.png','pending');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
