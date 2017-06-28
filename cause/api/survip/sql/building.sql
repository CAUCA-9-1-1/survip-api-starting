CREATE EXTENSION postgis;

create table tbl_building
(
	id_building uuid not null
		constraint tbl_building_pkey
			primary key,
	id_language_content_name uuid,
	id_lane uuid,
	id_risk_level uuid,
	id_utilisation_code uuid,
	id_sector uuid,
	id_mutual_aid_sector uuid,
	id_jaws_extrication_sector uuid,
	id_sled_sector uuid,
	id_resource_category varchar(50),
	id_association_building varchar(50),
	id_association_type varchar(50),
	id_unit_type varchar(50),
	civic_number varchar(15),
	civic_letter varchar(10),
	civic_supp varchar(10),
	civic_letter_supp varchar(10),
	appartment_number varchar(10),
	floor varchar(10),
	number_of_floors integer,
	number_of_appartment integer,
	number_of_building integer,
	vacant_land boolean default false not null,
	year_of_construction integer,
	building_value double precision,
	postal_code varchar(6),
	suite integer,
	source varchar(25),
	is_parent boolean default false not null,
	utilisation_description varchar(255),
	show_in_resources boolean default false not null,
	matricule varchar(18),
	coordinates geometry,
	coordinates_source varchar(50),
	details text,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create index idx_tbl_building_coordinates
	on tbl_building (coordinates)
;

create table tbl_building_contact
(
	id_building_contact uuid not null
		constraint tbl_building_resource_pkey
			primary key,
	id_building uuid not null,
	status varchar(40),
	first_name varchar(30),
	last_name varchar(30),
	call_priority integer,
	other_id_building uuid,
	phone_number varchar(10),
	phone_number_extension varchar(10),
	pager_number varchar(10),
	pager_code varchar(10),
	cellphone_number varchar(10),
	other_number varchar(10),
	other_number_extension varchar(10),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_building_hazardous_material
(
  id_building_hazardous_material uuid not null
		constraint tbl_building_hazardous_material_pkey
			primary key,
  id_hazardous_material uuid not null,
	id_building uuid not null,
	id_unit_of_measure uuid,
	id_image uuid,
	quantity integer,
	container varchar(100),
	capacity_container varchar(7),
	place varchar(150),
	floor varchar(4),
	gas_inlet varchar(100),
	security_perimeter text,
	other_information text,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_building_person_requiring_assistance
(
	id_building_person_requiring_assistance uuid not null
		constraint tbl_building_with_pra_pkey
			primary key,
	id_building uuid not null,
	id_person_requiring_assistence_type uuid not null,
	day_resident_count integer,
	evening_resident_count integer,
	night_resident_count integer,
	day_is_approximate boolean,
	evening_is_approximate boolean,
	night_is_approximate boolean,
	description text,
	pra_name varchar(60),
	floor varchar(3),
	local varchar(10),
	contact_name varchar(60),
	contact_phone_number varchar(10),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_hazardous_material
(
	id_hazardous_material uuid not null
		constraint tbl_hazardous_material_pkey
			primary key,
	id_language_content_name uuid,
	number varchar(50),
	guide_number varchar(255),
	reaction_to_water boolean default false not null,
	toxic_inhalation_hazard boolean default false not null,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_person_requiring_assistance_type
(
	id_person_requiring_assistance_type uuid not null
		constraint tbl_person_requiring_assistance_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_risk_level
(
	id_risk_level uuid not null
		constraint tbl_risk_level_pkey
			primary key,
	id_language_content_name uuid,
	sequence integer,
	code integer,
	color varchar(10),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_utilisation_code
(
	id_utilisation_code uuid not null
		constraint tbl_utilisation_code_pkey
			primary key,
	id_language_content_description uuid,
	cubf varchar(5),
	scian varchar(10),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;