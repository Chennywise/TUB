DROP DATABASE IF EXISTS `sql_clubs`;
CREATE DATABASE `sql_clubs` ;
USE `sql_clubs` ;

#SET NAMES utf8 ;
#SET charecter_set_client = ctf8mb4 ;

CREATE TABLE `club_list` (
	`club_id` int(11) NOT NULL AUTO_INCREMENT,
	`club_name` varchar(50) NOT NULL,
	`club_school` varchar(50) NOT NULL,
	`descr` varchar(500),
	`stat` varchar(20) NOT NULL,
	`creation_date` date NOT NULL DEFAULT '000-00-00',
	PRIMARY KEY(`club_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `club_members` (
	`club_id` int(11) NOT NULL,
	`member_id` int(11) NOT NULL AUTO_INCREMENT,
	`user_id` int(11) NOT NULL,
	`role` varchar(50) NOT NULL,
	`admin_stat` tinyint(1) NOT NULL DEFAULT 0,
	`rank` int(11) NOT NULL,
	PRIMARY KEY(`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `users` (
	`user_id` int(11) NOT NULL AUTO_INCREMENT,
	`username` varchar(15) NOT NULL,
	`password` varchar(20) NOT NULL,
	`email` varchar(50) NOT NULL,
	`creation_date` date NOT NULL DEFAULT '0000-00-00',
	`bio` varchar(500),
	PRIMARY KEY(`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `club_applications` (
	`application_id` int(11) NOT NULL AUTO_INCREMENT,
	`club_id` int(11) NOT NULL,
	`user_id` int(11) NOT NULL,
	`application_date` date NOT NULL DEFAULT '0000-00-00',
	PRIMARY KEY(`application_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `club_events` (
	`event_id` int(11) NOT NULL AUTO_INCREMENT,
	`club_id` int(11) NOT NULL,
	`user_id` int(11) NOT NULL,
	`event_title` varchar(2000) NOT NULL,
	`event_description` varchar(2000) NOT NULL,
	`creation_date` date NOT NULL DEFAULT '0000-00-00',
	`event_date` date NOT NULL DEFAULT '0000-00-00',
	PRIMARY KEY(`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `club_posts` (
	`post_id` int(11) NOT NULL AUTO_INCREMENT,
	`club_id` int(11) NOT NULL,
	`user_id` int(11) NOT NULL,
	`post_type` varchar(50) NOT NULL,
	`post_title` varchar(2000) NOT NULL,
	`post_text` varchar(2000) NOT NULL,
	`poll_options` varchar(500),
	`poll_results` varchar(500),
	`post_date` date NOT NULL DEFAULT '0000-00-00',
	PRIMARY KEY(`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


