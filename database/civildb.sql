create database Civil;
use Civil;

 CREATE TABLE options (
     labour VARCHAR(100)  ,
     machinery VARCHAR(255) ,
     material VARCHAR(255) 
 );

 CREATE TABLE category (
     id VARCHAR(15) NOT NULL,
     name VARCHAR(100)  NOT NULL,
     type VARCHAR(255) NOT NULL,
     PRIMARY KEY (id)
 );


 CREATE TABLE projects (
     projectname VARCHAR(100) UNIQUE NOT NULL,
     quotedamount INT NOT NULL,
     totexpense INT DEFAULT 0 NOT NULL,
     PRIMARY KEY (projectname)
 );


 CREATE TABLE payments1 (
     projectname VARCHAR(100) NOT NULL,
     type VARCHAR(255) NOT NULL,
     estamount BIGINT NOT NULL,
     expense BIGINT NOT NULL,
     FOREIGN KEY (projectname) REFERENCES projects(projectname) ON DELETE CASCADE
 );


 CREATE TABLE payments2 (
     projectname VARCHAR(100) NOT NULL,
     id VARCHAR(15) NOT NULL,
     date DATE NOT NULL,
     amount INT NOT NULL,
     FOREIGN KEY (projectname) REFERENCES projects(projectname) ON DELETE CASCADE,
 	FOREIGN KEY (id) REFERENCES category(id) ON DELETE CASCADE
 );


INSERT INTO options (material, labour, machinery) 
VALUES 
  ('Cement', 'Mason', 'Excavator'),
  ('Bricks', 'Shuttering', 'Tipper'),
  ('M Sand', 'Carpenter', 'Tractor'),
  ('Metal', 'Painter', 'Dozer'),
  ('Steel', 'Tiles Work', 'Roller'),
  ('Shuttering Materials', 'Electrician', 'Water Tanker'),
  ('Wood', 'Plumber', 'Transport');


 INSERT INTO options (material,labour) VALUES ('Hardwares','RR Mason');

 INSERT INTO options (material) VALUES('Paint Shop'),('Tiles'),('Tiles Paste'),('Electrical Materials'),('Plumbing Materials'),('Soling'),('RR Stones');


ALTER TABLE options ADD COLUMN sno INT AUTO_INCREMENT PRIMARY KEY;
ALTER TABLE payments1 ADD COLUMN pid INT AUTO_INCREMENT PRIMARY KEY;
ALTER TABLE payments2 ADD COLUMN uid INT AUTO_INCREMENT PRIMARY KEY;




