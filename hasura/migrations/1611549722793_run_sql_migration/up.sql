CREATE SEQUENCE volunteers_id_seq;

-- Use it to provide a new value for each project ID
ALTER TABLE volunteers
ALTER id 
SET DEFAULT NEXTVAL('volunteers_id_seq');
