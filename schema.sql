CREATE DATABASE IF NOT EXISTS `uml_crud_db`;

USE `uml_crud_db`;


CREATE TABLE `Assignment` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `assignmentId` INT,
    `description` VARCHAR(255),
    `dueDate` DATETIME,
    `maxScore` INT,
    -- Foreign Key linking to Course
    `course_id` INT,
    FOREIGN KEY (`course_id`) REFERENCES `Course`(`id`)
);


CREATE TABLE `Course` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `courseCode` VARCHAR(255),
    `title` VARCHAR(255),
    `credits` INT,
    `status` VARCHAR(255),
    -- Foreign Key linking to Department
    `department_id` INT,
    FOREIGN KEY (`department_id`) REFERENCES `Department`(`id`),
    -- Foreign Key linking to Professor
    `professor_id` INT,
    FOREIGN KEY (`professor_id`) REFERENCES `Professor`(`id`)
);


CREATE TABLE `Department` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `deptId` INT,
    `name` VARCHAR(255),
    `buildingCode` VARCHAR(255)
);


CREATE TABLE `Person` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `firstName` VARCHAR(255),
    `lastName` VARCHAR(255),
    `email` VARCHAR(255)
);


CREATE TABLE `Professor` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255),
    `salary` DECIMAL(10,2)
);


CREATE TABLE `Student` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `enrollmentDate` DATETIME,
    `gpa` DECIMAL(10,2)
);


CREATE TABLE `Submission` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `submissionId` INT,
    `submissionDate` DATETIME,
    `score` DECIMAL(10,2),
    `feedback` VARCHAR(255),
    -- Foreign Key linking to Assignment
    `assignment_id` INT,
    FOREIGN KEY (`assignment_id`) REFERENCES `Assignment`(`id`),
    -- Foreign Key linking to Student
    `student_id` INT,
    FOREIGN KEY (`student_id`) REFERENCES `Student`(`id`)
);


-- Many-to-Many Junction Tables

CREATE TABLE `Course_Student` (
    `student_id` INT,
    `course_id` INT,
    FOREIGN KEY (`student_id`) REFERENCES `Student`(`id`),
    FOREIGN KEY (`course_id`) REFERENCES `Course`(`id`)
);