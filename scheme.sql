CREATE TABLE IF NOT EXISTS users (
	id integer primary key autoincrement,
	first string not null,
	last string not null,
	rank string not null,
	next_rank string not null,
	squad int not null
);

CREATE TABLE IF NOT EXISTS login (
	id integer primary key autoincrement,
	username string not null,
	password string not null,
	role string not null,
	name string not null
);

CREATE TABLE IF NOT EXISTS events (
	id integer primary key autoincrement,
	title string not null,
	class string not null,
	start_date string not null,
	hourtime string not null,
	end_date string not null,
	end_time string not null,
	user_request string not null
);