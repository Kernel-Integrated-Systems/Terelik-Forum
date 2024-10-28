-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema forum_api_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forum_api_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forum_api_db` ;
USE `forum_api_db` ;

-- -----------------------------------------------------
-- Table `forum_api_db`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`categories` (
  `category_id` INT(11) NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(100) NOT NULL,
  `is_private` TINYINT(1) NULL DEFAULT 0,
  `is_locked` TINYINT(1) NULL DEFAULT 0,
  `created_at` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`category_id`),
  UNIQUE INDEX `category_name` (`category_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 2;


-- -----------------------------------------------------
-- Table `forum_api_db`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`roles` (
  `user_role` INT(11) NOT NULL,
  `role_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_role`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_api_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `user_role` INT(11) NULL DEFAULT NULL,
  `is_active` TINYINT(1) NULL DEFAULT 1,
  `created_at` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `username` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email` (`email` ASC) VISIBLE,
  INDEX `user_role` (`user_role` ASC) VISIBLE,
  CONSTRAINT `users_ibfk_1`
    FOREIGN KEY (`user_role`)
    REFERENCES `forum_api_db`.`roles` (`user_role`))
ENGINE = InnoDB
AUTO_INCREMENT = 10;


-- -----------------------------------------------------
-- Table `forum_api_db`.`useraccesslevel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`useraccesslevel` (
  `user_access_id` INT(11) NOT NULL,
  `access_level` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_access_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_api_db`.`categoryaccess`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`categoryaccess` (
  `user_id` INT(11) NOT NULL,
  `category_id` INT(11) NOT NULL,
  `access_level` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`, `category_id`),
  INDEX `category_id` (`category_id` ASC) VISIBLE,
  INDEX `access_level` (`access_level` ASC) VISIBLE,
  CONSTRAINT `categoryaccess_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_api_db`.`users` (`user_id`),
  CONSTRAINT `categoryaccess_ibfk_2`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_api_db`.`categories` (`category_id`),
  CONSTRAINT `categoryaccess_ibfk_3`
    FOREIGN KEY (`access_level`)
    REFERENCES `forum_api_db`.`useraccesslevel` (`user_access_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_api_db`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`messages` (
  `message_id` INT(11) NOT NULL AUTO_INCREMENT,
  `sender_id` INT(11) NULL DEFAULT NULL,
  `recipient_id` INT(11) NULL DEFAULT NULL,
  `content` TEXT NOT NULL,
  `created_at` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`message_id`),
  INDEX `sender_id` (`sender_id` ASC) VISIBLE,
  INDEX `recipient_id` (`recipient_id` ASC) VISIBLE,
  CONSTRAINT `messages_ibfk_1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `forum_api_db`.`users` (`user_id`),
  CONSTRAINT `messages_ibfk_2`
    FOREIGN KEY (`recipient_id`)
    REFERENCES `forum_api_db`.`users` (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 9;


-- -----------------------------------------------------
-- Table `forum_api_db`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`topics` (
  `topic_id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `content` TEXT NOT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `category_id` INT(11) NULL DEFAULT NULL,
  `is_locked` TINYINT(1) NULL DEFAULT 0,
  `created_at` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  `best_reply_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`topic_id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `category_id` (`category_id` ASC) VISIBLE,
  CONSTRAINT `topics_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_api_db`.`users` (`user_id`),
  CONSTRAINT `topics_ibfk_2`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_api_db`.`categories` (`category_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 14;


-- -----------------------------------------------------
-- Table `forum_api_db`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`replies` (
  `reply_id` INT(11) NOT NULL AUTO_INCREMENT,
  `content` TEXT NOT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `topic_id` INT(11) NULL DEFAULT NULL,
  `created_at` DATE NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`reply_id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `topic_id` (`topic_id` ASC) VISIBLE,
  CONSTRAINT `replies_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_api_db`.`users` (`user_id`),
  CONSTRAINT `replies_ibfk_2`
    FOREIGN KEY (`topic_id`)
    REFERENCES `forum_api_db`.`topics` (`topic_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 9;


-- -----------------------------------------------------
-- Table `forum_api_db`.`secretkeys`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`secretkeys` (
  `secret` VARCHAR(100) NULL DEFAULT NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_api_db`.`votetypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`votetypes` (
  `vote_id` INT(11) NOT NULL,
  `vote_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`vote_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_api_db`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_api_db`.`votes` (
  `vote_id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NULL DEFAULT NULL,
  `reply_id` INT(11) NULL DEFAULT NULL,
  `vote_type` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`vote_id`),
  UNIQUE INDEX `user_id` (`user_id` ASC, `reply_id` ASC) VISIBLE,
  INDEX `reply_id` (`reply_id` ASC) VISIBLE,
  INDEX `vote_type` (`vote_type` ASC) VISIBLE,
  CONSTRAINT `votes_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_api_db`.`users` (`user_id`),
  CONSTRAINT `votes_ibfk_2`
    FOREIGN KEY (`reply_id`)
    REFERENCES `forum_api_db`.`replies` (`reply_id`),
  CONSTRAINT `votes_ibfk_3`
    FOREIGN KEY (`vote_type`)
    REFERENCES `forum_api_db`.`votetypes` (`vote_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 9;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
