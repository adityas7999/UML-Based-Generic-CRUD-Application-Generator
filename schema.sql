CREATE DATABASE IF NOT EXISTS `uml_crud_db`;

USE `uml_crud_db`;


CREATE TABLE `Course` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `courseId` INT,
    `title` VARCHAR(255),
    -- Foreign Key linking to Department
    `department_id` INT,
    FOREIGN KEY (`department_id`) REFERENCES `Department`(`id`)
);


CREATE TABLE `Department` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `deptId` INT,
    `deptName` VARCHAR(255)
);


CREATE TABLE `Enrollment` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `enrollmentId` INT,
    `status` VARCHAR(255),
    -- Foreign Key linking to Course
    `course_id` INT UNIQUE,
    FOREIGN KEY (`course_id`) REFERENCES `Course`(`id`),
    -- Foreign Key linking to Student
    `student_id` INT,
    FOREIGN KEY (`student_id`) REFERENCES `Student`(`id`)
);


CREATE TABLE `Person` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255)
);


CREATE TABLE `Professor` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `employeeId` INT,
    `specialization` VARCHAR(255),
    -- Foreign Key linking to Department
    `department_id` INT UNIQUE,
    FOREIGN KEY (`department_id`) REFERENCES `Department`(`id`)
);


CREATE TABLE `Student` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `rollNumber` INT,
    `enrollmentDate` DATETIME
);
