create table sale(
    id int not null auto_increment,
    sale text not null,
    start_time timestamp default CURRENT_TIMESTAMP,
    end_time timestamp,
    primary key(id)
);

create table contacts(
    id int not null auto_increment,
    contact_name text not null,
    contact_email text not null,
    meet_date date,
    ship_condition text,
    new_customer boolean,
    primary key (id)
);
INSERT INTO contacts (contact_name,contact_email,meet_date,ship_condition,new_customer)

INSERT INTO sale (sale) VALUES ("test1");
update sale set end_time=CURRENT_TIMESTAMP where end_time is NULL;

SELECT * FROM sale ORDER BY start_time desc limit 3;
