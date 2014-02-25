-- People's testimonials and videos
drop table if exists testimonials;
create table testimonials (
	id integer primary key autoincrement
	, name text not null
	, town text not null
	, proud_of text not null
	, pride_in text not null
	, youtube_link text not null
);

-- This might not be needed with new design
drop table if exists municipios;
create table municipios (
	id integer primary key autoincrement
	, name text not null
);