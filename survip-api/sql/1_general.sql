CREATE EXTENSION "uuid-ossp";

CREATE EXTENSION postgis;

create table tbl_access_secretkey
(
	id_access_secretkey uuid not null
		constraint tbl_access_secretkey_pkey
			primary key,
	id_webuser uuid,
	application_name varchar(50),
	randomkey varchar(100),
	secretkey varchar(100),
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_access_token
(
	id_access_token uuid not null
		constraint tbl_access_token_id_access_token_pk
			primary key,
	id_webuser uuid,
	access_token varchar(100),
	refresh_token varchar(100),
	created_on timestamp default now(),
	expires_in integer
)
;

create table tbl_apis_action
(
	id_apis_update uuid not null
		constraint tbl_field_update_pkey
			primary key,
	id_webuser uuid,
	method varchar(10),
	params text,
	action_object varchar(50),
	action_object_id uuid,
	action_time timestamp default now()
)
;

create table tbl_external_import
(
	id_external_import uuid not null
		constraint tbl_external_import_pkey
			primary key,
	internal_id uuid,
	internal_table varchar(50),
	external_id varchar(50),
	external_table varchar(50),
	imported_on timestamp
)
;

create table tbl_fire_safety_department
(
	id_fire_safety_department uuid not null
		constraint tbl_fire_safety_department_pkey
			primary key,
	id_language_content_name uuid,
	id_county uuid,
	language varchar(5),
	created_on timestamp default now(),
	is_active boolean
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
	is_active boolean
)
;

create table tbl_language_content
(
	id_language_content uuid not null,
	language_code varchar(5) not null,
	description varchar(250),
	constraint tbl_language_content_pkey
		primary key (id_language_content, language_code)
)
;

create table tbl_permission
(
	id_permission uuid not null
		constraint tbl_permission_pkey
			primary key,
	id_permission_object uuid,
	id_permission_system uuid,
	id_permission_system_feature uuid,
	comments varchar(400),
	created_on timestamp,
	access boolean
)
;

create table tbl_permission_object
(
	id_permission_object uuid not null
		constraint tbl_permission_object_pkey
			primary key,
	id_permission_object_parent uuid,
	object_table varchar(255),
	generic_id varchar(50),
	id_permission_system uuid,
	is_group boolean,
	group_name varchar(255)
)
;

create table tbl_permission_system
(
	id_permission_system uuid not null
		constraint tbl_permission_system_pkey
			primary key,
	description varchar(400)
)
;

create table tbl_permission_system_feature
(
	id_permission_system_feature uuid not null
		constraint tbl_permission_system_feature_pkey
			primary key,
	id_permission_system uuid,
	feature_name varchar(50),
	description varchar(255),
	default_value boolean
)
;

create table tbl_picture
(
	id_picture uuid not null
		constraint picture_pkey
			primary key,
	id_language_content_name uuid,
	picture bytea,
	transfered boolean,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_webuser
(
	id_webuser uuid not null
		constraint tbl_webuser_pkey
			primary key,
	username varchar(100),
	password varchar(100),
	is_active boolean,
	created_on timestamp default now()
)
;

create table tbl_webuser_attributes
(
	id_webuser uuid not null,
	attribute_name varchar(50) not null,
	attribute_value varchar(200),
	constraint tbl_webuser_attributes_pkey
		primary key (id_webuser, attribute_name)
)
;

create table tbl_webuser_fire_safety_department
(
	id_webuser_fire_safety_department uuid not null
		constraint tbl_webuser_fire_safety_dept_id_user_fire_safety_dept_pk
			primary key,
	id_webuser uuid,
	id_fire_safety_department uuid not null,
	is_active boolean,
	created_on timestamp default now()
)
;
