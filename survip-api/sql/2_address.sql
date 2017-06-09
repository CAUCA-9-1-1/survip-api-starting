create table tbl_city
(
	id_city uuid not null
		constraint tbl_city_pkey
			primary key,
	id_language_content_name uuid,
	id_building uuid,
	id_city_type uuid,
	id_county uuid,
	code varchar(5),
	code3_letter varchar(3),
	email_address varchar(100),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_city_type
(
	id_city_type uuid not null
		constraint tbl_city_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_country
(
	id_country uuid not null
		constraint tbl_country_pkey
			primary key,
	id_language_content_name uuid,
	code_alpha2 varchar(2),
	code_alpha3 varchar(3),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_county
(
	id_county uuid not null
		constraint tbl_county_pkey
			primary key,
	id_language_content_name uuid,
	id_region uuid,
	id_state uuid,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_intersection
(
	id_intersection uuid not null
		constraint tbl_intersection_pkey
			primary key,
	id_city uuid,
	id_lane uuid,
	id_lane_transversal uuid,
	id_fire_sector uuid,
	id_jaws_sector uuid,
	id_mutual_aid_sector uuid,
	id_rescue_sector uuid,
	id_fire_sub_sector uuid,
	coordinates geometry,
	create_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_lane
(
	id_lane uuid not null
		constraint tbl_street_pkey
			primary key,
	id_language_content_name uuid,
	id_city uuid,
	public_lane_code varchar(50),
	generic_code varchar(50),
	created_on timestamp default now(),
	is_valid boolean default false not null,
	is_active boolean default true not null
)
;

create table tbl_region
(
	id_region uuid not null
		constraint tbl_region_pkey
			primary key,
	id_language_content_name varchar(50),
	id_state uuid,
	code varchar(2),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_state
(
	id_state uuid not null
		constraint tbl_state_id_state_pk
			primary key,
	id_language_content_name uuid,
	id_country uuid,
	ansi_code varchar(2),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;