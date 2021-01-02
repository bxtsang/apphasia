SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
SET time_zone = "+08:00";

--
-- Database: `volunteer`
--
CREATE DATABASE IF NOT EXISTS `volunteer` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `volunteer`;

-- --------------------------------------------------------

--
-- Table structure for table `volunteer`
--

DROP TABLE IF EXISTS `volunteer`;
CREATE TABLE IF NOT EXISTS `volunteer` (
  `userID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(32) NOT NULL,
  `email` VARCHAR(64) NOT NULL,
  `phone` INT check (`phone` between 00000000 and 99999999),
  `password` VARCHAR(128) NOT NULL,

  UNIQUE(`email`),
  PRIMARY KEY (`userID`)
);

--
-- Dumping data for table `volunteer`
--

INSERT INTO `volunteer` VALUES
(NULL,'Beng Lieh',"englieh@gmail.com", 94847464, "kuasimikua78"),
(NULL,'Hwee Purple', "hweepink@gmail.com", 95857565, "aiuhdsjkfn78"),
(NULL,'Moon Jun', "sunjun@gmail.com", 96867664, "sakfjklfsa890");
