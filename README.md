# Library Management System
This project is for security coursework 2.
The project chosen for the coursework is library-management-system from "https://github.com/hamzaavvan/library-management-system". This project is a library management system built using Flask and MySQL. It allows users to manage books, users, and reservations.
The objective of the coursework is to enhance the security for the project.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Run the project](#run-the-project)

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your machine.
- MySQL server installed and running.
- Git installed on your machine.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cf0615/security_cw2.git
   cd security_cw2/library-management-system
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Import the SQL dump file located in `db/lms.sql` into your MySQL server to create the necessary tables and initial data.
   ```bash
   cd to path/security_cw2/library-management-system/db
   mysql -u root -p
   ```
   ```mysql
   CREATE DATABASE lms;
   exit;
   ```
   -exit the MYSQL, and run the MYSQL lms again
   ```bash
   mysql -u -root -p lms
   source lms.sql;
   ```

## Run the project

1. Set Environment Variables
   ```bash
   set FLASK_APP=app.py 
   ```
   
2. Run the flask
   ```bash
   flask run --cert=server.crt --key=server.key
   ```

   or

   ```bash
   python -m flask run --cert=server.crt --key=server.key
   ```
