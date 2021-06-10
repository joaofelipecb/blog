drop table if exists user;
drop table if exists post;

create table user (
	user_id integer primary key autoincrement,
	user_username text unique not null,
	user_password text not null
);

create table post (
	post_id integer primary key autoincrement,
	user_id integer not null,
	post_created timestamp not null default current_timestamp,
	post_title text not null,
	post_body text not null,
	foreign key (user_id) references user (user_id)
);

