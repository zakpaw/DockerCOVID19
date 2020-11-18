ALTER USER 'root'@'localhost' IDENTIFIED BY 'passwel';
FLUSH PRIVILEGES; 

CREATE DATABASE covid;

USE covid;

CREATE TABLE covid19 (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    country TINYTEXT,
    confirmed INT UNSIGNED,
    active INT UNSIGNED,
    deaths INT UNSIGNED,
    recovered FLOAT(24),
    latitude FLOAT(24),
    longitude FLOAT(24),
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

