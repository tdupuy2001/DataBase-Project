SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema base
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `base` ;

-- -----------------------------------------------------
-- Schema base
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `base` DEFAULT CHARACTER SET utf8 ;
USE `base` ;

-- -----------------------------------------------------
-- Table `base`.`Administrator`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Administrator` ;

CREATE TABLE IF NOT EXISTS `base`.`Administrator` (
  `id_admin` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `birth_date` DATE NULL,
  `email` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `role` VARCHAR(45) NULL,
  PRIMARY KEY (`id_admin`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Operators`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Operators` ;

CREATE TABLE IF NOT EXISTS `base`.`Operators` (
  `id_operators` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `birth_date` DATE NULL,
  `email` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `role` VARCHAR(45) NULL,
  `approved` INT NULL,
  PRIMARY KEY (`id_operators`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Schools`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Schools` ;

CREATE TABLE IF NOT EXISTS `base`.`Schools` (
  `id_school` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `phone_number` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `director_name` VARCHAR(45) NULL,
  `Administrator_id_admin` INT NOT NULL,
  `Operators_id_operators` INT NOT NULL,
  PRIMARY KEY (`id_school`),
  INDEX `fk_Schools_Administrator1_idx` (`Administrator_id_admin` ASC) VISIBLE,
  INDEX `fk_Schools_Operators1_idx` (`Operators_id_operators` ASC) VISIBLE,
  CONSTRAINT `fk_Schools_Administrator1`
    FOREIGN KEY (`Administrator_id_admin`)
    REFERENCES `base`.`Administrator` (`id_admin`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Schools_Operators1`
    FOREIGN KEY (`Operators_id_operators`)
    REFERENCES `base`.`Operators` (`id_operators`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Roles` ;

CREATE TABLE IF NOT EXISTS `base`.`Roles` (
  `role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`role`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Users` ;

CREATE TABLE IF NOT EXISTS `base`.`Users` (
  `id_user` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `birth_date` DATE NULL,
  `email` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `approved` VARCHAR(45) NULL,
  `Roles_role` VARCHAR(45) NOT NULL,
  `Schools_id_school` INT NOT NULL,
  PRIMARY KEY (`id_user`),
  INDEX `fk_Users_Roles_idx` (`Roles_role` ASC) VISIBLE,
  INDEX `fk_Users_Schools1_idx` (`Schools_id_school` ASC) VISIBLE,
  CONSTRAINT `fk_Users_Roles`
    FOREIGN KEY (`Roles_role`)
    REFERENCES `base`.`Roles` (`role`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Users_Schools1`
    FOREIGN KEY (`Schools_id_school`)
    REFERENCES `base`.`Schools` (`id_school`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Books`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Books` ;

CREATE TABLE IF NOT EXISTS `base`.`Books` (
  `ISBN` VARCHAR(45) NOT NULL,
  `title` VARCHAR(45) NULL,
  `publication_date` DATE NULL,
  `publisher` VARCHAR(45) NULL,
  `number_of_pages` INT NULL,
  `summary` LONGTEXT NULL,
  `available_copies` INT NULL,
  `language` VARCHAR(45) NULL,
  `image` BLOB NULL,
  `keywords` VARCHAR(45) NULL,
  `Schools_id_school` INT NOT NULL,
  PRIMARY KEY (`ISBN`),
  INDEX `fk_Books_Schools1_idx` (`Schools_id_school` ASC) VISIBLE,
  CONSTRAINT `fk_Books_Schools1`
    FOREIGN KEY (`Schools_id_school`)
    REFERENCES `base`.`Schools` (`id_school`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Authors`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Authors` ;

CREATE TABLE IF NOT EXISTS `base`.`Authors` (
  `id_author` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `birth_date` DATE NULL,
  PRIMARY KEY (`id_author`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Categories` ;

CREATE TABLE IF NOT EXISTS `base`.`Categories` (
  `category_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`category_name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Borrow`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Borrow` ;

CREATE TABLE IF NOT EXISTS `base`.`Borrow` (
  `Users_id_user` INT NOT NULL,
  `Books_ISBN` VARCHAR(45) NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NULL,
  `approved` INT NULL,
  PRIMARY KEY (`Users_id_user`, `Books_ISBN`, `start_date`),
  INDEX `fk_Users_has_Books_Books1_idx` (`Books_ISBN` ASC) VISIBLE,
  INDEX `fk_Users_has_Books_Users1_idx` (`Users_id_user` ASC) VISIBLE,
  CONSTRAINT `fk_Users_has_Books_Users1`
    FOREIGN KEY (`Users_id_user`)
    REFERENCES `base`.`Users` (`id_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Users_has_Books_Books1`
    FOREIGN KEY (`Books_ISBN`)
    REFERENCES `base`.`Books` (`ISBN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Reserve`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Reserve` ;

CREATE TABLE IF NOT EXISTS `base`.`Reserve` (
  `Users_id_user` INT NOT NULL,
  `Books_ISBN` VARCHAR(45) NOT NULL,
  `date` DATE NOT NULL,
  `approved` INT NULL,
  PRIMARY KEY (`Users_id_user`, `Books_ISBN`, `date`),
  INDEX `fk_Users_has_Books_Books2_idx` (`Books_ISBN` ASC) VISIBLE,
  INDEX `fk_Users_has_Books_Users2_idx` (`Users_id_user` ASC) VISIBLE,
  CONSTRAINT `fk_Users_has_Books_Users2`
    FOREIGN KEY (`Users_id_user`)
    REFERENCES `base`.`Users` (`id_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Users_has_Books_Books2`
    FOREIGN KEY (`Books_ISBN`)
    REFERENCES `base`.`Books` (`ISBN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Review`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Review` ;

CREATE TABLE IF NOT EXISTS `base`.`Review` (
  `Users_id_user` INT NOT NULL,
  `Books_ISBN` VARCHAR(45) NOT NULL,
  `date` DATE NOT NULL,
  `grade` INT NULL,
  `comment` LONGTEXT NULL,
  `approved` INT NULL,
  PRIMARY KEY (`Users_id_user`, `Books_ISBN`, `date`),
  INDEX `fk_Users_has_Books_Books3_idx` (`Books_ISBN` ASC) VISIBLE,
  INDEX `fk_Users_has_Books_Users3_idx` (`Users_id_user` ASC) VISIBLE,
  CONSTRAINT `fk_Users_has_Books_Users3`
    FOREIGN KEY (`Users_id_user`)
    REFERENCES `base`.`Users` (`id_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Users_has_Books_Books3`
    FOREIGN KEY (`Books_ISBN`)
    REFERENCES `base`.`Books` (`ISBN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Authors_Books`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Authors_Books` ;

CREATE TABLE IF NOT EXISTS `base`.`Authors_Books` (
  `Authors_id_author` INT NOT NULL,
  `Books_ISBN` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Authors_id_author`, `Books_ISBN`),
  INDEX `fk_Authors_has_Books_Books1_idx` (`Books_ISBN` ASC) VISIBLE,
  INDEX `fk_Authors_has_Books_Authors1_idx` (`Authors_id_author` ASC) VISIBLE,
  CONSTRAINT `fk_Authors_has_Books_Authors1`
    FOREIGN KEY (`Authors_id_author`)
    REFERENCES `base`.`Authors` (`id_author`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Authors_has_Books_Books1`
    FOREIGN KEY (`Books_ISBN`)
    REFERENCES `base`.`Books` (`ISBN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base`.`Categories_Books`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `base`.`Categories_Books` ;

CREATE TABLE IF NOT EXISTS `base`.`Categories_Books` (
  `Categories_category_name` VARCHAR(45) NOT NULL,
  `Books_ISBN` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Categories_category_name`, `Books_ISBN`),
  INDEX `fk_Categories_has_Books_Books1_idx` (`Books_ISBN` ASC) VISIBLE,
  INDEX `fk_Categories_has_Books_Categories1_idx` (`Categories_category_name` ASC) VISIBLE,
  CONSTRAINT `fk_Categories_has_Books_Categories1`
    FOREIGN KEY (`Categories_category_name`)
    REFERENCES `base`.`Categories` (`category_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Categories_has_Books_Books1`
    FOREIGN KEY (`Books_ISBN`)
    REFERENCES `base`.`Books` (`ISBN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
