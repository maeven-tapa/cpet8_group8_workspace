-- MySQL script to create tables for the EALS application

-- Table for storing admin credentials
CREATE TABLE Admin (
    admin_id VARCHAR(20) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    password_changed BOOLEAN DEFAULT FALSE
);

-- Table for storing employee details
CREATE TABLE Employee (
    employee_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_initial CHAR(1),
    birthday DATE NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL,
    department VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    schedule ENUM('6am to 2pm', '2pm to 10pm', '10pm to 6am') NOT NULL,
    is_hr BOOLEAN DEFAULT FALSE,
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    password VARCHAR(255) NOT NULL
);

-- Table for storing HR-specific details (if needed)
CREATE TABLE HR (
    hr_id VARCHAR(20) PRIMARY KEY,
    employee_id VARCHAR(20),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

-- Example data insertion for admin
INSERT INTO Admin (admin_id, password, password_changed) 
VALUES ('admin-01-0001', 'defaultpassword', FALSE);