-- MySQL Script generated by MySQL Workbench
-- Thu Jun 16 22:05:58 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema securebank
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema securebank
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `securebank` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema accounts
-- -----------------------------------------------------
-- This schema was created for a stub table

-- -----------------------------------------------------
-- Schema accounts
--
-- This schema was created for a stub table
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `accounts` ;
USE `securebank` ;

-- -----------------------------------------------------
-- Table `securebank`.`accounts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securebank`.`accounts` (
  `id` CHAR(20) NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  `surname` VARCHAR(20) NOT NULL,
  `password` VARCHAR(128) NULL,
  `balance` BIGINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `securebank`.`transfers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securebank`.`transfers` (
  `id` CHAR(36) NOT NULL,
  `sender_id` CHAR(20) NOT NULL,
  `receiver_id` CHAR(20) NULL,
  `amount` BIGINT NOT NULL,
  `description` VARCHAR(45) NULL,
  `time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `sender_id_idx` (`sender_id` ASC) ,
  INDEX `receiver_id_idx` (`receiver_id` ASC) ,
  CONSTRAINT `sender_id`
    FOREIGN KEY (`sender_id`)
    REFERENCES `securebank`.`accounts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `receiver_id`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `securebank`.`accounts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `accounts` ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
