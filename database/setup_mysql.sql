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
CREATE TABLE IF NOT EXISTS goals(
       goal VARCHAR(500) NOT NULL,
       deadline VARCHAR(255) NOT NULL,
       friends_email VARCHAR(255) NOT NULL,
       pledge VARCHAR(500) NOT NULL,
       username VARCHAR(50) NOT NULL,
       password VARCHAR(50),
       PRIMARY KEY (username)
);
INSERT INTO goals(goal, deadline, friends_email, pledge, username, password) VALUES ("find a job", "November 20th, 2018", "cheersmelissa@gmail.com", "treat Melissa to Fogo De Chao", "Mel", "testpw");
