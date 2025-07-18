CREATE DATABASE IF NOT EXISTS three_tier_db;
USE three_tier_db;

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255)
);

INSERT INTO messages (message) VALUES ('Hello from the DB!');
