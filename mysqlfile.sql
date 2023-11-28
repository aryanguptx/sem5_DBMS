CREATE DATABASE bank_management_system;

USE bank_management_system;

-- Create Users table
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL
);

-- Create Accounts table
CREATE TABLE Accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    account_type ENUM('savings', 'checking') NOT NULL,
    balance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create Payment_Instruments table
CREATE TABLE Payment_Instruments (
    payment_instrument_id INT PRIMARY KEY AUTO_INCREMENT,
    type ENUM('debit card', 'credit card') NOT NULL,
    number VARCHAR(20) NOT NULL,
    expiry DATE NOT NULL,
    pin_hash VARCHAR(255) NOT NULL,
    account_id INT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

-- Create Personal_Information table
CREATE TABLE Personal_Information (
    personal_information_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create Audit Trail table
CREATE TABLE Audit_Trail (
    audit_trail_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    action_type ENUM('create', 'read', 'update', 'delete') NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id INT NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create Transactions table
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_number VARCHAR(20) NOT NULL,
    payment_method ENUM('debit card', 'credit card', 'bank transfer') NOT NULL,
    destination_account_number VARCHAR(20),
    amount DECIMAL(10,2) NOT NULL,
    transaction_date DATETIME NOT NULL DEFAULT NOW(),
    FOREIGN KEY (account_number) REFERENCES Accounts(account_number)
);

-- Create trigger to update balances on transaction
DELIMITER $$
CREATE TRIGGER update_balances_on_transaction AFTER INSERT ON Transactions
FOR EACH ROW BEGIN
    UPDATE Accounts
    SET balance = balance + NEW.amount
    WHERE account_number = NEW.account_number;

    IF (NEW.destination_account_number IS NOT NULL AND NEW.destination_account_number != '') THEN
        UPDATE Accounts
        SET balance = balance - NEW.amount
        WHERE account_number = NEW.destination_account_number;
    END IF;
END$$
DELIMITER ;

-- Example INNER JOIN query to retrieve user details with corresponding accounts
SELECT p.first_name, p.last_name, p.email, a.account_number, a.account_type, a.balance
FROM Personal_Information p
INNER JOIN Accounts a ON p.user_id = a.user_id;

-- Example LEFT JOIN query to identify users without accounts
SELECT p.first_name, p.last_name, p.email, a.account_number, a.account_type, a.balance
FROM Personal_Information p
LEFT JOIN Accounts a ON p.user_id = a.user_id
WHERE a.account_number IS NULL;

-- Example RIGHT JOIN query to list all accounts with user information
SELECT a.account_number, a.account_type, a.balance, p.first_name, p.last_name, p.email
FROM Accounts a
RIGHT JOIN Personal_Information p ON a.user_id = p.user_id;

-- MySQL does not support FULL OUTER JOIN, but you can use UNION of LEFT and RIGHT JOIN
SELECT p.first_name, p.last_name, p.email, a.account_number, a.account_type, a.balance
FROM Personal_Information p
LEFT JOIN Accounts a ON p.user_id = a.user_id
UNION
SELECT p.first_name, p.last_name, p.email, a.account_number, a.account_type, a.balance
FROM Personal_Information p
RIGHT JOIN Accounts a ON p.user_id = a.user_id;
