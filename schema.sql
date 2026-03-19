CREATE DATABASE IF NOT EXISTS `uml_crud_db`;
USE `uml_crud_db`;

CREATE TABLE `Person` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `personId` INT,
    `name` VARCHAR(255),
    -- Foreign Key linking to Passport
    `passport_id` INT,
    FOREIGN KEY (`passport_id`) REFERENCES `Passport`(`id`)
);

CREATE TABLE `Passport` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `passportNumber` INT,
    `nationality` VARCHAR(255)
);
