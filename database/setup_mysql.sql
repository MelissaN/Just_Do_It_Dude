-- prepares a MySQL database with sample data in database
-- GRANT USAGE ON *.* TO 'root'@'localhost';

CREATE DATABASE IF NOT EXISTS justdoitdude_dev_db;
-- CREATE USER IF NOT EXISTS justdoitdude_dev@localhost IDENTIFIED BY '';
USE justdoitdude_dev_db;
GRANT ALL PRIVILEGES ON justdoitdude_dev_db TO 'root'@'localhost';
USE performance_schema;
GRANT SELECT ON performance_schema.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

USE justdoitdude_dev_db;
DROP TABLE IF EXISTS goals;
CREATE TABLE IF NOT EXISTS goals(
       goal VARCHAR(500) NOT NULL,
       deadline DATE,
       accountability_partner VARCHAR(255) NOT NULL,
       partner_email VARCHAR(255) NOT NULL,
       pledge VARCHAR(500) NOT NULL,
       PRIMARY KEY (goal)
);
INSERT INTO goals(goal, deadline, accountability_partner, partner_email, pledge) VALUES ("find a job", "November 20th, 2018", Amy, "amy.tai0120@gmail.com", "treat Amy to Fogo De Chao");
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users(
       first_name VARCHAR(255) NOT NULL,
       last_name VARCHAR(255) NOT NULL,
       password VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL,
       goal VARCHAR(255) NOT NULL,
       PRIMARY KEY (email),
       FOREIGN KEY (goal) REFERENCES goals(goal)
);
INSERT INTO users(first_name, last_name, password, email, goal) VALUES ("Melissa", "Ng", "testpw", "cheersmelissa@gmail.com", "find a job");
