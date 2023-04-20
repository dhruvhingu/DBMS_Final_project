CREATE TABLE user (
    USERNAME VARCHAR2(30) ,
    PASSWORD VARCHAR(30),
    EMAIL VARCHAR2(30) PRIMARY KEY,
    DOB DATE
);

Create table cinema (
    CINEMA_ID VARCHAR2(10) Primary KEY,
    CINEMA_NAME VARCHAR2(30),
    CITY VARCHAR2(30)
);
create table movies(
   MOVIE_ID int primary key,
   TITLE varchar2(256),
   DESCRIPTION varchar2(512),
   LENGTH int,
   LANG varchar2(20),
   RELEASE_DATE DATE,
   GENRE varchar2(20),
   Price Number(8,2)
);

DROP Sequence movies_seq;
CREATE SEQUENCE movies_seq
start with 1
maxvalue 9999999
minvalue 1
CYCLE
NOCACHE
NOORDER;


create or replace trigger A_trigger
    before insert on movies
    for each ROW
BEGIN
    if :new.movie_id is null THEN
        :new.movie_id := movies_seq.nextval;
    end if;
END;
/




CREATE TABLE shows (
    show_ID VARCHAR2(20),
    Cinema_Id VARCHAR2(10),
    FOREIGN KEY (CINEMA_ID) REFERENCES CINEMA(CINEMA_ID),
    MOVIE_ID INT,
    FOREIGN KEY (MOVIE_ID) REFERENCES MOVIES(MOVIE_ID),
    show_date DATE,
    show_time VARCHAR2(30),
    AVAILABLE_SEATS INT DEFAULT 60,
    Constraint show_Id PRIMARY Key (SHOW_ID)
);


DROP Sequence shows_seq;
CREATE SEQUENCE shows_seq
start with 1
maxvalue 9999999
minvalue 1
CYCLE
NOCACHE
NOORDER;


create or replace trigger B_trigger
    before insert on shows
    for each ROW
BEGIN
    if :new.show_id is null THEN
        :new.show_id := shows_seq.nextval;
    end if;
END;
/




-- select * from shows;
CREATE TABLE SEATS (
    Show_ID VARCHAR2(10),
    CONSTRAINT book_show FOREIGN KEY (Show_Id) REFERENCES SHOWS(show_Id),
    AVAILABLE_SEAT INT
);

CREATE OR REPLACE TRIGGER SEATS_ADD     
AFTER INSERT ON SHOWS
FOR EACH ROW
BEGIN
    INSERT INTO SEATS VALUES (:NEW.SHOW_ID,:NEW.AVAILABLE_SEATS);
END;
/


CREATE TABLE PAYMENT(
    TICKET_ID INT PRIMARY KEY,
    PAYMENT_METHOD VARCHAR2(20),
    STATUS CHAR(5)
);

DROP Sequence payment_seq;
CREATE SEQUENCE payment_seq
start with 1
maxvalue 9999999
minvalue 1
CYCLE
NOCACHE
NOORDER;


create or replace trigger C_trigger
    before insert on payment
    for each ROW
BEGIN
    if :new.TICKET_ID is null THEN
        :new.ticket_ID := payment_seq.nextval;
    end if;
END;
/
CREATE TABLE TICKETS(
    TICKET_ID INT,
    CONSTRAINT TICKET_ticket FOREIGN KEY (TICKET_ID) REFERENCES payment(TICKET_ID),
    USER_ID VARCHAR2(30),
    CONSTRAINT TICKET_user FOREIGN KEY (USER_ID) REFERENCES form(email),
    SHOW_ID varchar(20),
    CONSTRAINT ticket_show FOREIGN Key (Show_ID) REFERENCEs Shows(show_ID),
    SEAT_IDS VARCHAR2(20)
);

select * from payment;
CREATE TABLE BILLS(
    USER_ID VARCHAR2(30),
    CONSTRAINT bill_user_id FOReign KEY (USER_ID) REFERENCES form(email),
    SHOW_ID varchar(20),
    CONSTRAINT bill_show_id FOREIGN Key (Show_ID) REFERENCEs Shows(show_ID),
    Total_cost FLOAT
);
select *from bills;

INSERT INTO CINEMA VALUES('1','MetroPolis','Spain');
INSERT INTO CINEMA VALUES('2','Rajhansh Cinema','Ahmedabad');
INSERT INTO CINEMA VALUES('3','IMax','Ahmedabad');
INSERT INTO CINEMA VALUES('4','Cinemplex','Ahmedabad');
INSERT INTO CINEMA VALUES('5','PVR','Surat');
INSERT INTO CINEMA VALUES('6','ABMiniplex','Bhuj');
INSERT INTO CINEMA VALUES('7','INox','Rajkot');
INSERT INTO CINEMA VALUES('8','DriveIn','Delhi');
INSERT INTO CINEMA VALUES('9','City Pulse','Gandhinagar');
INSERT INTO CINEMA VALUES('10','City Gold','Bejing');

insert into movies values(DEFAULT,'Avatar2','Blue aliens fights with human.',180,'English','01-MAR-2023','SCIENCE',200);
INSERT INTO MOVIES VALUES(DEFAULT,'Jurassic World','Dinos eats Human',135,'English','12-JUN-2023','THRILLER',200);
INSERT INTO MOVIES VALUES(DEFAULT,'Vikram','Gangsters fight with Police',340,'Telugu','01-APR-2023','ACTION',200);
INSERT INTO MOVIES VALUES(DEFAULT,'Firestarter','Story of a child playing with ghost.',120,'Spanish','18-APR-2023','THRILLER',200);
INSERT INTO MOVIES VALUES(DEFAULT,'Vash','Kuch hoga movie me dekh lena',130,'Gujarati','6-APR-2023','HORROR',200);
INSERT INTO MOVIES VALUES(DEFAULT,'Jodha Akbar','All about Jodha and Akbar ',121,'Hindi','18-MAR-2023','HISTORY',200);
INSERT INTO MOVIES VALUES(DEFAULT,'Lucy','Drug helps gain more intelligence.',140,'English','01-MAY-2023','SCIENCE',150);
INSERT INTO MOVIES VALUES(DEFAULT,'Doreamon','Nobita,Sizuka and Gadgets',30,'Japanese','08-FEB-2022','ANIMATION',150);
INSERT INTO MOVIES VALUES(DEFAULT,'Bharamastra','Copy of Marvel',143,'Hindi','31-MAR-2023','FANTASY',150);
INSERT INTO MOVIES VALUES(DEFAULT,'Harry Porter','Waste of Time(read book instead)',179,'English','31-MAR-2023','FANTASY',250);

insert into shows values(DEFAULT,'1',4,'20-APR-2023','Morning',DEFAULT);
insert into shows values(DEFAULT,'1',8,'20-APR-2023','Noon',DEFAULT);
insert into shows values(DEFAULT,'1',7,'20-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'2',3,'20-APR-2023','Evening',DEFAULT);
insert into shows values(DEFAULT,'3',5,'20-APR-2023','Morning',DEFAULT);
insert into shows values(DEFAULT,'3',1,'21-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'4',3,'21-APR-2023','Noon',DEFAULT);
insert into shows values(DEFAULT,'4',8,'21-APR-2023','Noon',DEFAULT);
insert into shows values(DEFAULT,'5',6,'21-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'5',1,'21-APR-2023','Morning',DEFAULT);
insert into shows values(DEFAULT,'6',2,'21-APR-2023','Evening',DEFAULT);
insert into shows values(DEFAULT,'6',6,'21-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'6',5,'21-APR-2023','Morning',DEFAULT);
insert into shows values(DEFAULT,'7',10,'20-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'7',5,'20-APR-2023','Evening',DEFAULT);
insert into shows values(DEFAULT,'8',2,'20-APR-2023','Morning',DEFAULT);
insert into shows values(DEFAULT,'9',8,'22-APR-2023','Noon',DEFAULT);
insert into shows values(DEFAULT,'9',6,'22-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'10',4,'20-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'10',1,'20-APR-2023','Evening',DEFAULT);
insert into shows values(DEFAULT,'1',6,'22-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'2',5,'22-APR-2023','Morning',DEFAULT);
insert into shows values(DEFAULT,'3',10,'20-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'4',5,'20-APR-2023','Evening',DEFAULT);
insert into shows values(DEFAULT,'5',2,'21-APR-2023','Morning',DEFAULT);
insert into shows values(DEFAULT,'6',8,'21-APR-2023','Noon',DEFAULT);
insert into shows values(DEFAULT,'7',6,'20-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'8',4,'21-APR-2023','Night',DEFAULT);
insert into shows values(DEFAULT,'9',1,'20-APR-2023','Evening',DEFAULT);
insert into shows values(DEFAULT,'3',3,'21-APR-2023','Night',DEFAULT);
create table user_shows(
    user_id varchar2(30),
    CONSTRAINT conn_user FOREIGN KEY (USER_ID) REFERENCES form(email),
    SHOW_ID varchar(20),
    CONSTRAINT conn_show FOREIGN Key (Show_ID) REFERENCEs Shows(show_ID)
);
drop table BILLS;
DROP Table SEATS;
DROP Table TICKETS;
DROP Table PAYMENT;
drop table user_shows;
DROP Table shows;
DROP Table movies;
DROP Table cinema;
DROP Table user;
Desc user;
Desc cinema;
DESC movies;
DESC shows;
desc user_shows;
DESC PAYMENT;
DESC TICKETS
DESC seats;
DESC bills;

