-- prepares a MySQL database with sample data in database
-- GRANT USAGE ON *.* TO 'root'@'localhost';

CREATE DATABASE
IF NOT EXISTS justdoitdude_dev_db;
-- CREATE USER IF NOT EXISTS justdoitdude_dev@localhost IDENTIFIED BY '';
USE justdoitdude_dev_db;
GRANT ALL PRIVILEGES ON justdoitdude_dev_db TO 'root'@'localhost';
USE performance_schema;
GRANT SELECT ON performance_schema.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

USE justdoitdude_dev_db;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS goals;
CREATE TABLE
IF NOT EXISTS goals
(
       id INT UNIQUE NOT NULL AUTO_INCREMENT,
       goal VARCHAR
(500) NOT NULL,
       deadline DATE,
       accountability_partner VARCHAR
(255) NOT NULL,
       partner_email VARCHAR
(255) NOT NULL,
       pledge VARCHAR
(500) NOT NULL,
       start_date DATE,
       PRIMARY KEY
(id)
);
INSERT INTO goals
    (goal, deadline, accountability_partner, partner_email, pledge)
VALUES
    ("find a job", "2018-11-20", "Amy", "amy.tai0120@gmail.com", "treat Amy to Fogo De Chao");
CREATE TABLE
IF NOT EXISTS users
(
       id INT UNIQUE NOT NULL AUTO_INCREMENT,
       first_name VARCHAR
(255) NOT NULL,
       password VARCHAR
(255) NOT NULL,
       email VARCHAR
(255) NOT NULL,
       goal_id INT,
       PRIMARY KEY
(id),
       FOREIGN KEY
(goal_id) REFERENCES justdoitdude_dev_db.goals
(id)
);
INSERT INTO users
    (first_name, password, email)
VALUES
    ("Melissa", "testpw", "cheersmelissa@gmail.com");
