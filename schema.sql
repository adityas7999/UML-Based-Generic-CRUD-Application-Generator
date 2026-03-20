CREATE DATABASE IF NOT EXISTS `uml_crud_db`;

USE `uml_crud_db`;


CREATE TABLE `Address` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `streetLine1` VARCHAR(255),
    `city` VARCHAR(255),
    `state` VARCHAR(255),
    `zipCode` VARCHAR(255),
    `country` VARCHAR(255),
    -- Foreign Key linking to User
    `user_id` INT,
    FOREIGN KEY (`user_id`) REFERENCES `User`(`id`)
);


CREATE TABLE `Admin` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `department` VARCHAR(255),
    `clearanceLevel` INT
);


CREATE TABLE `Category` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `categoryId` INT,
    `name` VARCHAR(255),
    `slug` VARCHAR(255),
    -- Foreign Key linking to Category
    `parent_category_id` INT,
    FOREIGN KEY (`parent_category_id`) REFERENCES `Category`(`id`)
);


CREATE TABLE `CreditCardPayment` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `cardNumberMasked` VARCHAR(255),
    `cardHolderName` VARCHAR(255),
    `expirationMonthYear` VARCHAR(255)
);


CREATE TABLE `Customer` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `loyaltyPoints` INT,
    `isPremium` TINYINT(1)
);


CREATE TABLE `Order` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `orderId` INT,
    `orderDate` DATETIME,
    `totalAmount` DECIMAL(10,2),
    `status` VARCHAR(255),
    -- Foreign Key linking to Customer
    `customer_id` INT,
    FOREIGN KEY (`customer_id`) REFERENCES `Customer`(`id`),
    -- Foreign Key linking to Payment
    `payment_id` INT UNIQUE,
    FOREIGN KEY (`payment_id`) REFERENCES `Payment`(`id`)
);


CREATE TABLE `OrderItem` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `itemId` INT,
    `quantity` INT,
    `priceAtPurchase` DECIMAL(10,2),
    -- Foreign Key linking to Order
    `order_id` INT,
    FOREIGN KEY (`order_id`) REFERENCES `Order`(`id`),
    -- Foreign Key linking to Product
    `product_id` INT,
    FOREIGN KEY (`product_id`) REFERENCES `Product`(`id`)
);


CREATE TABLE `PayPalPayment` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `paypalEmail` VARCHAR(255),
    `transactionReference` VARCHAR(255)
);


CREATE TABLE `Payment` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `paymentId` INT,
    `amount` DECIMAL(10,2),
    `paymentDate` DATETIME,
    `isSuccessful` TINYINT(1)
);


CREATE TABLE `Product` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `productId` INT,
    `sku` VARCHAR(255),
    `name` VARCHAR(255),
    `description` VARCHAR(255),
    `currentPrice` DECIMAL(10,2),
    `stockLevel` INT
);


CREATE TABLE `User` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(255),
    `email` VARCHAR(255),
    `passwordHash` VARCHAR(255),
    `createdAt` DATETIME
);


-- Many-to-Many Junction Tables

CREATE TABLE `Category_Product` (
    `product_id` INT,
    `category_id` INT,
    FOREIGN KEY (`product_id`) REFERENCES `Product`(`id`),
    FOREIGN KEY (`category_id`) REFERENCES `Category`(`id`)
);