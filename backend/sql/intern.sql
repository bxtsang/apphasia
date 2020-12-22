SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
SET time_zone = "+08:00";

--
-- Database: `intern`
--
CREATE DATABASE IF NOT EXISTS `intern` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `intern`;

-- --------------------------------------------------------

--
-- Table structure for table `intern`
--

DROP TABLE IF EXISTS `intern`;
CREATE TABLE IF NOT EXISTS `intern` (
  `userID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(32) NOT NULL,
  `email` VARCHAR(64) NOT NULL,
  `phone` INT check (`phone` between 00000000 and 99999999),
  `password` VARCHAR(128) NOT NULL,

  UNIQUE(`email`),
  PRIMARY KEY (`userID`)
);

--
-- Dumping data for table `intern`
--

INSERT INTO `intern` VALUES
(NULL,'Brix Phua',"arix@gmail.com", 91817161, "asiodfhiuyesa2"),
(NULL,'Bao Xi', "baoxian@gmail.com", 92827262, "981237kjhsdf"),
(NULL,'Smaen Mae', "eunice@gmail.com", 93837363, "aiushfiuh2398");
