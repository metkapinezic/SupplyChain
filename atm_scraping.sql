Create table best_atm(
	company_id int not null primary key,
	company_name varchar not null,
	trustscore float,
	total_reviews integer,
	domain varchar not null);