DROP DATABASE IF EXISTS company;
CREATE DATABASE company;
USE company;

CREATE TABLE EMPLOYEE (
    ssn INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    bdate DATE,
    address VARCHAR(50),
    gender CHAR(1),
    salary DECIMAL(10,2),
    Dno INT,
    PRIMARY KEY (ssn)
);

CREATE TABLE DEPARTMENT (
    Dnumber INT NOT NULL,
    Dname VARCHAR(30),
    mgr_ssn INT,
    mgr_start_date DATE,
    PRIMARY KEY (Dnumber),
    FOREIGN KEY (mgr_ssn) REFERENCES EMPLOYEE(ssn)
);

CREATE TABLE PROJECT (
    Pnumber INT NOT NULL,
    Pname VARCHAR(30),
    Plocation VARCHAR(30),
    Dno INT,
    PRIMARY KEY (Pnumber),
    FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber)
);
ALTER TABLE EMPLOYEE ADD FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber);