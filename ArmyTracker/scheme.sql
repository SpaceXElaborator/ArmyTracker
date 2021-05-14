CREATE TABLE IF NOT EXISTS users (
	id integer primary key autoincrement,
	first string not null,
	last string not null,
	rank string not null,
	squad int not null
);