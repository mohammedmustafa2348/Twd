PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS t_login_det;
DROP TABLE IF EXISTS t_user_msg;
DROP TABLE IF EXISTS t_user_data;


CREATE TABLE t_user_data(email varchar(64), firstname varchar(30), familyname varchar(30), gender varchar(6), city varchar(30), country varchar(30),
constraint user_pk primary key(email));


CREATE TABLE t_login_det(email varchar(64), pwd varchar(32), token char(128), constraint login_pk primary key(email), constraint user_login_fk foreign key(email) references t_user_data(email) on delete cascade on update cascade, constraint login_uk unique(token));

CREATE TABLE t_user_msg(email varchar(64), message varchar(3000), posted_by varchar(64), twt_time time default current_timestamp not null, constraint user_msg_fk1 foreign key(email) references t_user_data(email) on delete cascade on update cascade , constraint user_msg_fk2 foreign key(posted_by) references t_user_data(email) on
delete cascade on update cascade);

INSERT INTO "t_user_data" VALUES('test1@abc.com','Hayder','Alansari','Male','Mjölby','Svergie');
INSERT INTO "t_user_data" VALUES('test2@abc.com','Mustafa','Akram','Male','Linkoping','Sweden');
INSERT INTO "t_login_det" VALUES('test1@abc.com','1234',null);
INSERT INTO "t_login_det" VALUES('test2@abc.com','1234',null);
INSERT INTO "t_user_msg" VALUES('test1@abc.com','a new message..please add this','test1@abc.com','2016-02-27 19:22:00.362390');
INSERT INTO "t_user_msg" VALUES('test1@abc.com','<b>TEST</b>','test2@abc.com','2016-02-27 19:24:38.113572');
COMMIT;

/*
CREATE TABLE t_user_data(email varchar(30), firstname varchar(30), familyname varchar(30), gender varchar(6), city varchar(15), country varchar(15), constraint user_pk primary key(email));
CREATE TABLE t_login_det(email varchar(64), pwd varchar(32), token char(128), constraint login_pk primary key(email), constraint user_login_fk foreign key(email) references t_user_data(email) on delete cascade on update cascade, constraint login_uk unique(token));
CREATE TABLE t_user_msg(email varchar(64), message varchar(30), post_by varchar(30), twt_time time, foreign key(email) references t_user_data(email),foreign key(email) references t_user_data(email) on delete cascade on update cascade);

*/

/*
INSERT INTO "t_user_data" VALUES('test1@abc.com','akram','bcd','male','linkoping','sweden');
INSERT INTO "t_user_data" VALUES('test2@abc.com','akram','bcd','male','linkoping','sweden');
INSERT INTO "t_user_data" VALUES('test3@abc.com','akram','bcd','male','linkoping','sweden');
INSERT INTO "t_user_data" VALUES('test4@abc.com','akram','bcd','male','linkoping','sweden');
INSERT INTO "t_login_det" VALUES('test1@abc.com','1234','a32554akb');
INSERT INTO "t_login_det" VALUES('test2@abc.com','1234','a95991akb');
INSERT INTO "t_login_det" VALUES('test3@abc.com','1234','15');
INSERT INTO "t_login_det" VALUES('test4@abc.com','1234','17');
*/
