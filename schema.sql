CREATE TABLE Person (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE Student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rollNumber INT,
    enrollmentDate DATETIME
);

CREATE TABLE Professor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employeeId INT,
    specialization VARCHAR(255)
);

CREATE TABLE Course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    courseId INT,
    title VARCHAR(255)
);

CREATE TABLE Department (
    id INT AUTO_INCREMENT PRIMARY KEY,
    deptId INT,
    deptName VARCHAR(255)
);

CREATE TABLE Enrollment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollmentId INT,
    status VARCHAR(255)
);
