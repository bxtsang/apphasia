SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
SET time_zone = "+08:00";

--
-- Database: `core`
--
CREATE DATABASE IF NOT EXISTS `core` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `core`;

-- --------------------------------------------------------

--
-- Table structure for table `core`
--

DROP TABLE IF EXISTS `core`;
CREATE TABLE IF NOT EXISTS `core` (
  `userID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(32) NOT NULL,
  `email` VARCHAR(64) NOT NULL,
  `phone` INT check (`phone` between 00000000 and 99999999),
  `password` VARCHAR(128) NOT NULL,

  UNIQUE(`email`),
  PRIMARY KEY (`userID`)
);

--
-- Dumping data for table `core`
--

INSERT INTO `core` VALUES
(NULL,'Cliffen Lee Jun Yi',"cliffen123@gmail.com", 69798999, "testtest"),
(NULL,'Glen See Saw', "glenwaves@gmail.com", 99887766, "test32"),
(NULL,'Mary Had Little Lamb', "marydonut@gmail.com", 98897667, "test324");
