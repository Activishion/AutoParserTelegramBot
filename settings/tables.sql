create table history_requests (
	id int PRIMARY KEY NOT NULL,
	brand varchar(50) NOT NULL,
	model varchar(50) NOT NULL,
	years varchar NOT NULL,
	mileage varchar NOT NULL,
	price varchar NOT NULL,
	date_request timestamp,
	user_id int,
	username varchar
)

CREATE TABLE brands_nodels (
    id int PRIMARY KEY NOT NULL,
    brand_name varchar(50) NOT NULL,
    brand_id int NOT NULL,
    model_name varchar(50) NOT NULL,
    model_id int NOT NULL
)
