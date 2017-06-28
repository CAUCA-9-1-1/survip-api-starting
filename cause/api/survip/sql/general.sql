create table tbl_fire_safety_department
(
	id_fire_safety_department uuid not null
		constraint tbl_fire_safety_department_pkey
			primary key,
	id_language_content_name uuid,
	id_county uuid,
	language varchar(2),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_fire_safety_department_city_serving
(
	id_fire_safety_department_city_serving uuid not null
		constraint tbl_fire_safety_department_city_serving_pkey
			primary key,
	id_fire_safety_department uuid not null,
	id_city uuid not null,
	id_sector_type uuid,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_firestation
(
	id_firestation uuid not null
		constraint tbl_firestation_pkey
			primary key,
	id_fire_safety_department uuid,
	station_name varchar(30),
	phone_number varchar(10),
	fax_number varchar(10),
	email varchar(70),
	id_building uuid,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_picture
(
	id_picture uuid not null
		constraint picture_pkey
			primary key,
	id_language_content_name uuid,
	picture bytea,
	transfered boolean default false not null,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;