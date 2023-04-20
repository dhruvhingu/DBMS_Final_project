-- Trigger to check if the user already exist
CREATE OR REPLACE TRIGGER USER_exist 
BEFORE INSERT ON FORM
FOR EACH ROW
DECLARE
 v_count int;
 msg VARCHAR2(50) := 'User already exists';
BEGIN
 SELECT COUNT(*) INTO v_count
 FROM form
 WHERE username = :new.username;
 IF v_count > 0 THEN
   raise_application_error(-20000,'User already exist');
 END IF;
END;
/
--Trigger to autoincrement id

CREATE OR REPLACE PROCEDURE insert_data_proc(
    username IN VARCHAR2,
    password IN varchar2,
    email IN varchar2,
    dob IN date
)
IS
BEGIN
    INSERT INTO form(username, password, email,dob)
    VALUES(username, password, email,dob);
    
    COMMIT;
END;
/
CREATE OR REPLACE TRIGGER CHK_SHOWS
BEFORE INSERT ON SHOWS
FOR EACH ROW
DECLARE
    CURSOR C_SHOWS IS SELECT * FROM SHOWS;
    R_SHOWS C_SHOWS%ROWTYPE;
BEGIN
    FOR R_SHOWS IN C_SHOWS LOOP
        IF(R_SHOWS.CINEMA_ID=:NEW.CINEMA_ID AND R_SHOWS.MOVIE_ID=:NEW.MOVIE_ID AND R_SHOWS.SHOW_TIME=:NEW.SHOW_TIME AND R_SHOWS.SHOW_DATE=:NEW.SHOW_DATE) THEN 
        raise_application_error(-20015,'A SHOW ALREADY EXIST FOR THE TIME DEFINED!');
        END IF;
    END LOOP;
END;
/
drop trigger add_shows;

insert into cinema values(11,'Extra Cinema','Dholakpur');
delete from cinema where cinema_id =11;

CREATE OR REPLACE PROCEDURE Insert_Tickets (
    ticket_id VARCHAR2, user_id VARCHAR2, show_id VARCHAR2, price NUMBER
)
is BEGIN
INSERT into TIckets values(ticket_id,user_id,show_id,price);
COMMIT;
END;
/
CREATE or Replace Trigger chk_status 
before insert on TICKETS 
for each ROW
DECLARE
    cursor c_pay is select * from payment;
    r_pay c_pay%rowtype;
BEGIN
    if  r_pay.status<>'PASS' THEN   
        raise_application_error(-20019,'Payment Failed');  
    end if; 
end;
/