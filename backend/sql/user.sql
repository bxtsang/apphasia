SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
SET time_zone = "+08:00";

--
-- Database: `core`
--
CREATE DATABASE IF NOT EXISTS `user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user`;

-- --------------------------------------------------------

--
-- Table structure for table `core`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `userID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(32) NOT NULL,
  `email` VARCHAR(64) NOT NULL,
  `phone` INT check (`phone` between 00000000 and 99999999),
  `password` VARCHAR(128) NOT NULL,
  `type` VARCHAR(128) NOT NULL,

  UNIQUE(`email`),
  PRIMARY KEY (`userID`)
);

--
-- Dumping data for table `core`
--

INSERT INTO `user` VALUES
(NULL,'Cliffen Lee Jun Yi',"cliffen123@gmail.com", 69798999, "testtest", "core"),
(NULL,'Glen See Saw', "glenwaves@gmail.com", 99887766, "test32", "core"),
(NULL,'Mary Had Little Lamb', "marydonut@gmail.com", 98897667, "test324", "core"),
(NULL,'Beng Lieh',"englieh@gmail.com", 94847464, "kuasimikua78", "volunteer"),
(NULL,'Hwee Purple', "hweepink@gmail.com", 95857565, "aiuhdsjkfn78", "volunteer"),
(NULL,'Moon Jun', "sunjun@gmail.com", 96867664, "sakfjklfsa890", "volunteer"),
(NULL,'Brix Phua',"arix@gmail.com", 91817161, "asiodfhiuyesa2", "intern"),
(NULL,'Bao Xi', "baoxian@gmail.com", 92827262, "981237kjhsdf", "intern"),
(NULL,'Smaen Mae', "eunice@gmail.com", 93837363, "aiushfiuh2398", "intern");


