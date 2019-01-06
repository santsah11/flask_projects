-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema beltExam
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema beltExam
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `beltExam` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema beltexam
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema beltexam
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `beltexam` DEFAULT CHARACTER SET utf8 ;
USE `beltExam` ;

-- -----------------------------------------------------
-- Table `beltExam`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beltExam`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(100) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `beltExam`.`tripschedules`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beltExam`.`tripschedules` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `destination` VARCHAR(255) NULL,
  `travel_start` DATETIME NULL,
  `travel_end` DATETIME NULL,
  `plan` VARCHAR(255) NULL,
  `action` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tripschedules_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_tripschedules_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `beltExam`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `beltExam`.`tripplans`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beltExam`.`tripplans` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `destination` VARCHAR(255) NULL,
  `travel_start` DATETIME NULL,
  `travel_end` DATETIME NULL,
  `do_you_want_join` VARCHAR(255) NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tripplans_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_tripplans_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `beltExam`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `beltexam` ;

-- -----------------------------------------------------
-- Table `beltexam`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beltexam`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(100) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beltexam`.`tripplans`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beltexam`.`tripplans` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `destination` VARCHAR(255) NULL DEFAULT NULL,
  `travel_start` DATETIME NULL DEFAULT NULL,
  `travel_end` DATETIME NULL DEFAULT NULL,
  `do_you_want_join` VARCHAR(255) NULL DEFAULT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tripplans_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_tripplans_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `beltexam`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `beltexam`.`tripschedules`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `beltexam`.`tripschedules` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `destination` VARCHAR(255) NULL DEFAULT NULL,
  `travel_start` DATETIME NULL DEFAULT NULL,
  `travel_end` DATETIME NULL DEFAULT NULL,
  `plan` VARCHAR(255) NULL DEFAULT NULL,
  `action` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tripschedules_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_tripschedules_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `beltexam`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
