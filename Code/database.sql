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

insert  into `buyers`(`id`,`bname`,`bemail`,`password`,`contact`,`address`,`profile`,`status`) values (1,'Buyer','buyer@gmail.com','Preeti@123','9632587410','bangalore','static/profiles/Lentils.jpg','pending'),(2,'ravi','ravi@gmail.com','Preeti@123','9652145698','bangalore','static/profiles/Bajra.jpg','pending');

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

insert  into `cropinfo`(`id`,`cropname`,`category`,`Minimumcost`,`myfile`) values (1,'Rice','Grains','800','static/profiles/Jowar.jpg'),(2,'Wheat','Grains','250','static/profiles/wheat.jpg'),(3,'Almonds','Nuts','1200','static/profiles/Lentils.jpg'),(4,'Pistachios','Nuts','120','static/profiles/rice.jpg'),(5,'Sesame Seeds','Seeds','700','static/profiles/Lentils.jpg'),(6,'Flaxseeds','Seeds','150','static/profiles/Bajra.jpg');

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `croporder` */

insert  into `croporder`(`id`,`cropname`,`category`,`mincost`,`quantity`,`myorder`,`season`,`totalquantity`,`semail`,`bemail`,`amount`,`status`,`imgfile`) values (1,'Pistachios','Nuts','120','2000','100','2024-03-07','1900','kumar@gmail.com','buyer@gmail.com','12000','Accepted','static/profiles/wheat.jpg'),(2,'Flaxseeds','Seeds','150','2500','34','2024-10-04','2466','kumar@gmail.com','buyer@gmail.com','5100','Accepted','static/profiles/Jowar.jpg'),(3,'Rice','Grains','800','200','150','2024-03-09','50','kumar@gmail.com','buyer@gmail.com','120000','Accepted','static/profiles/rice.jpg');

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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `cropprice` */

insert  into `cropprice`(`id`,`cropname`,`category`,`mincost`,`quantity`,`Yieldtime`,`myfile`,`semail`,`address`,`amount`,`status`,`totalquantity`) values (1,'Rice','Grains','800','200','2024-03-09','static/profiles/rice.jpg','farmer@gmail.com','bangalore',NULL,'pending','50'),(2,'Wheat','Grains','250','200','2024-02-03','static/profiles/Bajra.jpg','farmer@gmail.com','bangalore',NULL,'pending','200'),(3,'Almonds','Nuts','1200','200','2024-12-01','static/profiles/Bajra.jpg','farmer@gmail.com','bangalore',NULL,'pending','200'),(4,'Pistachios','Nuts','120','2000','2024-03-07','static/profiles/wheat.jpg','kumar@gmail.com','tirupati',NULL,'pending','1900'),(5,'Sesame Seeds','Seeds','700','2500','2024-11-20','static/profiles/Jowar.jpg','kumar@gmail.com','tirupati',NULL,'pending','2500'),(6,'Flaxseeds','Seeds','150','2500','2024-10-04','static/profiles/Jowar.jpg','kumar@gmail.com','tirupati',NULL,'pending','2466');

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

insert  into `payment`(`id`,`Amount`,`Cardname`,`Cardnumber`,`expmonth`,`cvv`,`Email`,`semail`,`status`) values (1,'12000','Preeti Desai','7896587458965478','12/25','258','buyer@gmail.com','kumar@gmail.com','Completed');

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `sellers` */

insert  into `sellers`(`id`,`sname`,`semail`,`password`,`contact`,`address`,`Profile`,`status`) values (1,'farmer','farmer@gmail.com','Preeti@123','9685745896','bangalore','static/profiles/farmer1.jpg','pending'),(2,'kumar','kumar@gmail.com','Preeti@123','9685745896','tirupati','static/profiles/Jowar.jpg','pending');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
