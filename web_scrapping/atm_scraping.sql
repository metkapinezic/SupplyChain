Create table best_atm(
	company_id int not null primary key,
	company_name varchar not null,
	trustscore float,
	total_reviews integer,
	domain varchar not null);

Select * from best_atm;

Create table company_details(
	company_name varchar not null,
	rating_class varchar,
	star_5 varchar,
	star_4 varchar,
	star_3 varchar,
	star_2 varchar,
	star_1 varchar,
	total_reviews varchar);

Select * from company_details;

Create table reviews(
	company_name varchar not null,
	review_star varchar,
	review_title varchar,
	reviewer_name varchar,
	review_text varchar,
	experience_date varchar,
	review_date varchar,
	reply_date varchar,
	reply_text varchar);