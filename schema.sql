CREATE DATABASE IF NOT EXISTS employee_crm;
USE employee_crm;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    emp_code VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(100)
);

INSERT INTO employees (name, emp_code, password, department) 
VALUES ('Admin User', '1001', '1001', 'Management');