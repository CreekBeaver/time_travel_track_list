-- Creating Database Information

-- CREATE DATABASE cs340_db;

--
-- Access The DATABASE
--
-- USE cs_340_db;
-- source scratch.sql
--
-- Build Tables in DATABASE
--

--
-- Employee Table
--

DROP TABLE IF EXISTS `employees`;

CREATE TABLE `employees` (
	`employee_id` int(11) NOT NULL AUTO_INCREMENT,
	`first_name` varchar(255) NOT NULL,
	`last_name` varchar(255) NOT NULL,
	`employment_start_date` date NOT NULL,
	`employment_end_date` date DEFAULT NULL,
	`title` varchar(255) NOT NULL,
	`salary` float NOT NULL,
	PRIMARY KEY(`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dump info Into Employees
--

LOCK TABLES `employees` WRITE;
INSERT INTO `employees` VALUES (1, 'Kyle', 'Creek', '1992-1-1', NULL, 'King', 100.00), (2, 'Lucy', 'Bouffiou', '1993-9-6', NULL, 'Queen', 200.00);
UNLOCK TABLES;

--
-- Jet Data TABLE
-- 

DROP TABLE IF EXISTS `jet_data`;
CREATE TABLE `jet_data` (
	`jet_id` int(11) NOT NULL AUTO_INCREMENT,
	`derivative id` int(11) NOT NULL,
	`purchase_date` date NOT NULL,
	`relinquish_date` date DEFAULT NULL,
	`market_value` int(11) NOT NULL,
	`status` varchar(255) NOT NULL,
	PRIMARY KEY(`jet_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dump info into Jet Data'
--

LOCK TABLES `jet_data` WRITE;
INSERT INTO `jet_data` VALUES (1, 2, '1992-1-1', NULL, 190, 'Owned');
UNLOCK TABLES;

--
-- Derivative Data TABLE
-- DROP TABLE IF EXISTS `derivative_data`;

CREATE TABLE `derivative_data` (
	`derivative_id` int(11) NOT NULL AUTO_INCREMENT,
	`model_derivative` varchar(255) NOT NULL,
	`body_style` varchar(255) NOT NULL, 
	`primary_use` varchar(255) NOT NULL,
	`flight_range` int(11) NOT NULL,
	`seats` int(11) NOT NULL,
	`fuel_efficiency` float NOT NULL,
	`max_take_off_weight` float NOT NULL,
	PRIMARY KEY(`derivative_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Customers TABLE
-- DROP TABLE IF EXISTS `customers`

CREATE TABLE `customers` (
	`customer_id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL,
	`lease_id` int(11) NOT NULL,
	`request_id` int(11) NOT NULL,
	PRIMARY KEY(`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Lease Requests TABLE
-- DROP TABLE IF EXISTS `lease)requests`

CREATE TABLE `lease_requests` (
	`request_id` int(11) NOT NULL AUTO_INCREMENT,
	`derivative` int(11) NOT NULL,
	`ground_staff_included` boolean NOT NULL,
	`crew_included` boolean NOT NULL,
	PRIMARY KEY(`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Active Leases TABLE
-- DROP TABLE IF EXISTS `leases`

CREATE TABLE `leases` (
	`lease_id` int(11) NOT NULL AUTO_INCREMENT,
	`customer_id` int(11) NOT NULL,
	`jet_id` int(11) NOT NULL,
	`status` varchar(255) NOT NULL,
	`lease_start_date` date NOT NULL,
	`lease_end_date` date NOT NULL,
	`duration` int(11) DEFAULT NULL,
	`ground_staff_included` boolean NOT NULL,
	`crew_included` boolean NOT NULL,
	`lease_value` int(11) NOT NULL,
	`payment_to_date` boolean NOT NULL,
	`payment_remaining` int(11) NOT NULL,
	`employee_id` int(11) NOT NULL,
	PRIMARY KEY(`lease_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
	
