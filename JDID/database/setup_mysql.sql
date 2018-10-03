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
DROP TABLE IF EXISTS goals;
DROP TABLE IF EXISTS users;

CREATE TABLE
IF NOT EXISTS users
(
       id INT UNIQUE NOT NULL AUTO_INCREMENT,
       first_name VARCHAR(255) NOT NULL,
       password VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL, PRIMARY KEY(id)
);
INSERT INTO users
    (first_name, password, email)
VALUES
    ("Melissa", "testpw", "cheersmelissa@gmail.com");

CREATE TABLE
IF NOT EXISTS goals
(
       id INT UNIQUE NOT NULL AUTO_INCREMENT,
       goal VARCHAR(500) NOT NULL,
       deadline DATE,
       accountability_partner VARCHAR(255) NOT NULL,
       partner_email VARCHAR(255) NOT NULL,
       pledge VARCHAR(500) NOT NULL,
       start_date DATE,
       user_id INT, 
       FOREIGN KEY(user_id) REFERENCES users(id),
       completed BOOLEAN,
       partner_validation VARCHAR,
       PRIMARY KEY(id)
);
INSERT INTO goals
    (goal, deadline, accountability_partner, partner_email, pledge, start_date)
VALUES
    ("find a job", "2018-11-20", "Amy", "amy.tai0120@gmail.com", "treat Amy to Fogo De Chao", "2018-09-01");
INSERT INTO goals
    (goal, deadline, accountability_partner, partner_email, pledge, start_date)
VALUES
    ("run the upcoming 5K marathon", "2019-10-20", "Melissa", "cheersmelissa@gmail.com", "treat Holberton staff to first round of drinks", "2018-09-10");

INSERT INTO goals
    (goal, deadline, accountability_partner, partner_email, pledge, start_date)
VALUES
    ("launch 3 apps", "2019-01-20", "Melissa", "cheersmelissa@gmail.com", "do 100 push ups while Suzie records", "2018-08-10");

INSERT INTO goals
    (goal, deadline, accountability_partner, partner_email, pledge, start_date)
VALUES
    ("sucessfully land an airplane", "2019-05-20", "Melissa", "cheersmelissa@gmail.com", "buy round trip tickets to Brazil for all my classmates at Fly Academy", "2018-09-20");
