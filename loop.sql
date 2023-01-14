DROP TABLE IF EXISTS drivers_copy; 
create table drivers_copy as select * from drivers; 
delete from drivers_copy;

DO $$
 DECLARE
     driver_id   drivers_copy.id%TYPE;
     code  drivers_copy.code%TYPE;

 BEGIN
     driver_id := 0;
     FOR counter IN 1..10
         LOOP
            INSERT INTO drivers_copy (driver_id, code)
             VALUES (counter + driver_id, code);
         END LOOP;
 END;
 $$