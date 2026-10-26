USE company;

INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno) VALUES 
(101, 'Ali', 'Ahmed', '1985-05-12', 'Cairo', 'M', 5000.00, NULL),
(102, 'Fatma', 'Mohamed', '1990-08-20', 'Alexandria', 'F', 6000.00, NULL),
(103, 'Omar', 'Khaled', '1988-02-15', 'Giza', 'M', 5500.00, NULL);

INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES 
(1, 'HR', 101, '2020-01-01'),
(2, 'IT', 102, '2019-05-10'),
(3, 'Finance', 103, '2021-03-15');

UPDATE EMPLOYEE SET Dno = 1 WHERE ssn = 101;
UPDATE EMPLOYEE SET Dno = 2 WHERE ssn = 102;
UPDATE EMPLOYEE SET Dno = 3 WHERE ssn = 103;

INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES 
(10, 'Alpha', 'Cairo', 1),
(20, 'Beta', 'Alexandria', 2),
(30, 'Gamma', 'Giza', 3);