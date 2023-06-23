-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Graduation_In_Life
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `Graduation_In_Life` ;

-- -----------------------------------------------------
-- Schema Graduation_In_Life
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Graduation_In_Life` DEFAULT CHARACTER SET utf8 ;
USE `Graduation_In_Life` ;

-- -----------------------------------------------------
-- Table `Graduation_In_Life`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Graduation_In_Life`.`users` ;

CREATE TABLE IF NOT EXISTS `Graduation_In_Life`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(200) NOT NULL,
  `last_name` VARCHAR(200) NOT NULL,
  `email` VARCHAR(200) NOT NULL,
  `password` VARCHAR(200) NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `Graduation_In_Life`.`events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Graduation_In_Life`.`events` ;

CREATE TABLE IF NOT EXISTS `Graduation_In_Life`.`events` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NOT NULL,
  `date` DATE NOT NULL,
  `time` TIME NOT NULL,
  `location` TEXT NOT NULL,
  `description` TEXT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT NULL,
  `maker_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_events_users_idx` (`maker_id` ASC) VISIBLE,
  CONSTRAINT `fk_events_users`
    FOREIGN KEY (`maker_id`)
    REFERENCES `Graduation_In_Life`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `Graduation_In_Life`.`users_has_events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Graduation_In_Life`.`users_has_events` ;

CREATE TABLE IF NOT EXISTS `Graduation_In_Life`.`users_has_events` (
  `user_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  INDEX `fk_users_has_events_events1_idx` (`event_id` ASC) VISIBLE,
  INDEX `fk_users_has_events_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_events_events1`
    FOREIGN KEY (`event_id`)
    REFERENCES `Graduation_In_Life`.`events` (`id`),
  CONSTRAINT `fk_users_has_events_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `Graduation_In_Life`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
