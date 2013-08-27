drop table if exists logincred;
create table logincred (
    id integer primary key autoincrement,
    fname string not null, 
    lname string not null, 
    email string not null, 
    password string not null
);
