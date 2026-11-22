CREATE TABLE IF NOT EXISTS work_logs (id SERIAL PRIMARY KEY, first_name VARCHAR(100) NOT NULL, last_name VARCHAR(100) NOT NULL, date DATE NOT NULL, start_hour TIME NOT NULL, end_hour TIME NOT NULL, description TEXT DEFAULT '');
CREATE TEMP TABLE import_work_logs (first_name TEXT, last_name TEXT, date TEXT, start_hour TEXT, end_hour TEXT, description TEXT);
COPY import_work_logs FROM '/data/work_logs.csv' WITH (FORMAT CSV, HEADER TRUE, DELIMITER ';', ENCODING 'UTF8');
INSERT INTO work_logs (first_name, last_name, date, start_hour, end_hour, description)
SELECT first_name, last_name, date::DATE, start_hour::TIME, end_hour::TIME, COALESCE(description, '') FROM import_work_logs;