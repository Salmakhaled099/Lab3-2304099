# DB Lab 3 - Foreign Keys, Simple SQL & Library Management System

## Team Members
* Salma Khaled - ID : 2304099

## Tech Stack
* Back-end: Python (Flask), PyMySQL
* Front-end: HTML5 / CSS3 / Bootstrap 5
* Database: MySQL

## Project Structure & How to Run
1. Problem 1 (Company Database):
   - Run problem1_DDL.sql in MySQL to create the company database and tables.
   - Run problem1_DML.sql to insert seed data.
   - Review answers and outputs in problem1_Answers.txt.

2. Problem 2 (Library Management System):
   - Run problem2_DDL.sql and problem2_DML.sql to set up the library database.
   - Install requirements: pip install flask pymysql bcrypt python-dotenv
   - Start the server: python app.py
   - Open http://127.0.0.1:5000 in your browser

## Features & Deliverables
- Problem 1: DDL schema, DML records, and answers to Q1.1-Q1.3.
- Problem 2 Website: 
  - Full CRUD for Books and Authors (F2.1 - F2.5).
  - Navigation bridge between To-Do App and Library System.
- Bonus: Image uploads for book covers and author photos stored securely in static/uploads/.

## Conceptual Questions & Answers
### (a) Why do UPDATE and DELETE contain AND user_id = ? and what changes if you remove it?
- Answer: It ensures database-level authorization. Without it, any user could modify or delete other users' tasks by guessing their todo_id.

### (b) What happens if you insert a to-do for a user_id that does not exist, and which constraint of the lecture is that?
- Answer: MySQL rejects it with a Foreign Key error, which enforces the Referential Integrity Constraint.

### (c) Why do you store a hash and not the password?
- Answer: To protect user security during database breaches using one-way salted hashes like bcrypt.

### (d) The name column is NOT NULL: why did you still need your own check for an empty name?
- Answer: Because NOT NULL accepts empty strings "" or spaces " ", so application checks are needed to ensure valid text.