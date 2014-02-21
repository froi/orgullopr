drop table if exists testimonials;
create table testimonials (
	id integer primary key autoincrement
	, name text not null
	, town text not null
	, proud_of text not null
	, pride_in text not null
	, youtube_link text not null
);