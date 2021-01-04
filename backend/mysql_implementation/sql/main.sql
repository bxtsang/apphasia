SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
SET time_zone = "+08:00";

--
-- Database: `aphasia`
--
CREATE DATABASE IF NOT EXISTS `aphasia` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `aphasia`;

-- --------------------------------------------------------

--
-- Dropping all tables
--

SET AUTOCOMMIT = 1;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `user_project`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `task`;
DROP TABLE IF EXISTS `resource`;
DROP TABLE IF EXISTS `project`;
SET FOREIGN_KEY_CHECKS = 1;
-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `userID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `email` VARCHAR(64) NOT NULL,
  `phone` INT check (`phone` between 00000000 and 99999999),
  `password` VARCHAR(128) NOT NULL,
  `role` VARCHAR(128) NOT NULL,
  CONSTRAINT check_type CHECK (`role` IN ('intern', 'core', 'volunteer')),

  UNIQUE(`email`),
  PRIMARY KEY (`userID`)
) ENGINE = INNODB;

--
-- Dumping data for table `user`
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

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE IF NOT EXISTS `task` (
    `taskID` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(128) NOT NULL,

    PRIMARY KEY (`taskID`)
) ENGINE = INNODB;

--
-- Dumping data for table `task`
--

INSERT INTO `task` VALUES
(NULL,"task1"),
(NULL,"task2");

-- --------------------------------------------------------

--
-- Table structure for table `resource`
--

CREATE TABLE IF NOT EXISTS `resource` (
    `resourceID` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(128) NOT NULL,

    PRIMARY KEY (`resourceID`)
) ENGINE = INNODB;

--
-- Dumping data for table `resource`
--

INSERT INTO `resource` VALUES
(NULL,"resource1");

-- --------------------------------------------------------

--
-- Table structure for table `project`
--

CREATE TABLE IF NOT EXISTS `project` (
  `projectID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `description` VARCHAR(128) NOT NULL,
  `recurring` TINYINT(1) NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `archived` TINYINT(1) NOT NULL,
 
  PRIMARY KEY (`projectID`)
) ENGINE = INNODB;

--
-- Dumping data for table `project`
--

INSERT INTO `project` VALUES
(NULL, 'Wa meng ti',"Singing with them peeps", 0, "2020-11-12", "2021-01-23", 0),
(NULL, 'Night night',"Reading with them peeps", 0, "2022-9-21", "2023-01-18", 0),
(NULL, 'Zoomba',"Dancing with them peeps, online", 0, "2020-03-15", "2022-06-30", 0);

-- --------------------------------------------------------

--
-- Table structure for table `user_project`
--

CREATE TABLE IF NOT EXISTS `user_project` (
    `userID` INT NOT NULL,
    `projectID` INT NOT NULL,
 
  PRIMARY KEY (`userID`, `projectID`),
  CONSTRAINT fk_userID FOREIGN KEY (`userID`) REFERENCES  user(`userID`),
  CONSTRAINT fk_projectID FOREIGN KEY (`projectID`) REFERENCES  project(`projectID`)
) ENGINE=INNODB;

--
-- Dumping data for table `user_project`
--

INSERT INTO `user_project` VALUES
(2,2),
(1,3),
(1,2);