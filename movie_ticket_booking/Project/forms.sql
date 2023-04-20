Drop table form;

CREATE TABLE FORM (
    USERNAME VARCHAR2(30) ,
    PASSWORD VARCHAR(30),
    EMAIL VARCHAR2(30) PRIMARY KEY,
    DOB DATE
);
INSERT INTO form VALUES(
    'FireGumz',
    '123',
    'aagam@gmail.com',
    '19-NOV-2002'
);
INSERT INTO form VALUES(
    'Saumil',
    'pizza',
    'saumil@gmail.com',
    '4-Nov-2003'
);
INSERT INTO form VALUES(
    'SabkeDaddy',
    '123',
    'preet@gmail.com',
    '5-APR-2004'
);
INSERT INTO form VALUES(
    'Dhruv',
    'buddy',
    'dhruv@gmail.com',
    '26-MAR-2003'
);
drop table movies;

create table movies(
   movie_id int primary key,
   title varchar2(256),
   description varchar2(512),
   duration int,
   language varchar2(20),
   release_date date,
   genre varchar2(20));
   

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
insert into movies values(DEFAULT,'Demon slayer','anime',120,'japenese','25-MAR-2023','Action');
insert into movies values(DEFAULT,'Avatar 2','nice cinematogrphy',180,'English','01-MAR-2023','Sci-fi');
insert into movies values(DEFAULT,'Jurasic World','dinosaurs',150,'Hinglish','01-APR-2023','Biology');
insert into movies values(DEFAULT,'Vikram','dinosaurs',150,'Hinglish','01-APR-2023','Biology');
insert into movies values(DEFAULT,'Fire Starter','dinosaurs',150,'Hinglish','01-APR-2023','Biology');
insert into movies values(DEFAULT,'Jurasic World','dinosaurs',150,'Hinglish','01-APR-2023','Biology');
select * from movies;
