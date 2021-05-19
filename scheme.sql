CREATE TABLE IF NOT EXISTS users (
	id integer primary key autoincrement,
	first string not null,
	last string not null,
	rank string not null,
	squad int not null
);

CREATE TABLE IF NOT EXISTS login (
	id integer primary key autoincrement,
	username string not null,
	password string not null,
	role string not null
);

CREATE TABLE IF NOT EXISTS events (
	id integer primary key autoincrement,
	title string not null,
	class string not null,
	start_date date not null default (datetime('now', 'localtime')),
	end_date date not null,
	user_request string not null
);