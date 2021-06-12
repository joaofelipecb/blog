drop table if exists users;
drop table if exists posts;

create table users (
	user_id serial,
	user_username text unique not null,
	user_password text not null,
	primary key(user_id)
);

create table posts (
	post_id serial,
	user_id integer not null,
	post_created timestamp not null default current_timestamp,
	post_title text not null,
	post_body text not null,
	primary key(post_id),
	constraint posts_fk_users foreign key(user_id) references users(user_id)
);

