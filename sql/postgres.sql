CREATE EXTENSION "uuid-ossp";

CREATE EXTENSION postgis;

create type enum_question_type as enum ('text', 'choice', 'date')
;

create type enum_survey_type as enum ('residential', 'general', 'agricultural')
;

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

create table tbl_webuser_attributes
(
	id_webuser uuid not null,
	attribute_name varchar(50) not null,
	attribute_value varchar(200),
	constraint tbl_webuser_attributes_pkey
		primary key (id_webuser, attribute_name)
)
;

create table tbl_webuser_action
(
	id_webuser_action uuid not null
		constraint tbl_webuser_action_pkey
			primary key,
	id_webuser uuid,
	action_time timestamp,
	action_object varchar(50),
	action_name varchar(50),
	action_param text
)
;

create table tbl_access_token
(
	id_access_token uuid
		constraint tbl_access_token_idaccess_token_pk
			unique,
	id_webuser uuid,
	access_token varchar(100),
	refresh_token varchar(100),
	created_on timestamp default now(),
	expires_in integer
)
;

create table tbl_lane
(
	id_lane uuid not null
		constraint tbl_street_pkey
			primary key,
	public_lane_code varchar(50),
	generic_code varchar(50),
	public_lane varchar(50),
	id_language_content_name uuid,
	id_city uuid,
	direction varchar(10),
	lane_prefix varchar(30),
	broke_up_generic_code varchar(2),
	broke_up_lane_code varchar,
	broke_up_name varchar(30),
	created_on timestamp default now(),
	is_valid boolean,
	is_active boolean
)
;

create table tbl_building
(
	id_building uuid not null
		constraint tbl_building_pkey
			primary key,
	id_language_content_name uuid,
	civic_number varchar(15),
	civic_letter varchar(10),
	civic_supp varchar(10),
	civic_letter_supp varchar(10),
	appartment_number varchar(10),
	floor varchar(10),
	number_of_floors integer,
	number_of_appartment integer,
	number_of_building integer,
	vacant_land boolean,
	year_of_construction integer,
	building_value double precision,
	id_lane uuid,
	postal_code varchar(6),
	id_utilisation_code uuid,
	id_sector uuid,
	id_mutual_aid_sector uuid,
	id_jaws_extrication_sector uuid,
	id_sled_sector uuid,
	suite integer,
	id_risk_level uuid,
	source varchar(25),
	is_parent boolean,
	utilisation_description varchar(255),
	show_in_resources boolean,
	id_resource_category varchar(50),
	id_association_building varchar(50),
	id_association_type varchar(50),
	id_unit_type varchar(50),
	matricule varchar(18),
	coordinates geography,
	coordinates_source varchar(50),
	details text,
	created_on timestamp default now(),
	is_active boolean
)
;

create index idx_tbl_building_coordinates
	on tbl_building (coordinates)
;

create table tbl_utilisation_code
(
	id_utilisation_code uuid not null
		constraint tbl_utilisation_code_pkey
			primary key,
	cubf varchar(5),
	scian varchar(10),
	id_language_content_description uuid,
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

create table tbl_inspection_answer
(
	id_inspection_answer uuid not null
		constraint tbl_inspection_answer_pkey
			primary key,
	id_inspection uuid,
	id_webuser uuid,
	answered_on timestamp,
	has_refuse boolean,
	reason_for_refusal varchar(250),
	is_absent boolean,
	is_seasonal boolean,
	is_vacant boolean
)
;

create table tbl_inspection_question
(
	id_inspection_question uuid not null
		constraint tbl_inspection_question_pkey
			primary key,
	id_inspection_answer uuid,
	id_survey_question uuid,
	id_survey_choice uuid,
	answer varchar(200)
)
;

create table tbl_inspection
(
	id_inspection uuid not null
		constraint tbl_inspection_pkey
			primary key,
	id_survey uuid,
	id_building uuid,
	id_webuser uuid,
	created_on timestamp default now(),
	created_by uuid,
	is_active boolean,
	is_completed boolean default false
)
;

create table tbl_survey
(
	id_survey uuid not null
		constraint tbl_survey_pkey
			primary key,
	id_language_content_name uuid,
	survey_type enum_survey_type,
	created_on timestamp default now(),
	is_active boolean
)
;

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
	code_3_letter varchar(3),
	email_address varchar(100),
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_building_hazardous_material
(
	id_building uuid not null,
	id_hazardous_material uuid not null,
	quantity integer,
	container varchar(100),
	capacity_container varchar(7),
	id_unit_of_measure uuid,
	place varchar(150),
	floor varchar(4),
	id_image uuid,
	gas_inlet varchar(100),
	security_perimeter text,
	other_information text,
	created_on timestamp default now(),
	is_active boolean,
	constraint tbl_building_hazardous_material_id_building_id_harzardous_mater
		primary key (id_building, id_hazardous_material)
)
;

create table tbl_building_contact
(
	id_building_contact uuid not null
		constraint tbl_building_resource_pkey
			primary key,
	id_building uuid,
	status varchar(40),
	first_name varchar(30),
	last_name varchar(30),
	call_priority integer,
	other_address boolean,
	other_id_building uuid,
	phone_number varchar(10),
	phone_number_extension varchar(10),
	pager_number varchar(10),
	pager_code varchar(10),
	cellphone_number varchar(10),
	other_number varchar(10),
	other_number_extension varchar(10),
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_picture
(
	id_picture uuid not null
		constraint picture_pkey
			primary key,
	picure_name varchar(150),
	transfered boolean,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_building_person_requiring_assistance
(
	id_building_person_requiring_assistance uuid not null
		constraint tbl_building_with_pra_pkey
			primary key,
	id_building uuid,
	id_building_information uuid,
	id_person_requiring_assistence_type uuid,
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
	is_active boolean
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
	is_active boolean
)
;

create table tbl_intervention_plan
(
	id_intervention_plan uuid not null
		constraint tbl_intervention_plan_pkey
			primary key,
	plan_number varchar(50),
	plan_name varchar(50),
	id_city uuid,
	id_intersection1 uuid,
	id_intersection2 uuid,
	plan_course1 text,
	plan_course2 text,
	plan_course3 text,
	id_firestation_course1 uuid,
	id_firestation_course2 uuid,
	id_firestation_course3 uuid,
	other_information text,
	created_on timestamp default now(),
	revised_on timestamp,
	approved_on timestamp,
	is_active boolean
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

create table tbl_fire_hydrant
(
	id_fire_hydrant uuid not null
		constraint tbl_fire_hydrant_pkey
			primary key,
	id_city uuid,
	id_lane uuid,
	id_intersection uuid,
	id_fire_hydrant_type uuid,
	coordinates geography,
	altitude double precision,
	fire_hydrant_number varchar(10),
	id_operator_type_rate uuid,
	rate_from varchar(5),
	rate_to varchar(5),
	id_rate_type uuid,
	id_operator_type_pressure uuid,
	pressure_from varchar(5),
	pressure_to varchar(5),
	id_pressure_type uuid,
	color varchar(50),
	comments text,
	physical_position varchar(50),
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_fire_hydrant_connection
(
	id_fire_hydrant_connection uuid not null
		constraint tbl_fire_hydrant_connection_pkey
			primary key,
	id_fire_hydrant uuid,
	diameter double precision,
	id_diameter_type uuid,
	id_fire_hydrant_connection_type uuid,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_permission
(
	id_permission uuid not null
		constraint tbl_permissions_pkey
			primary key,
	id_permission_object uuid,
	id_permission_system uuid,
	id_permission_system_feature uuid,
	created_on timestamp default now(),
	comments varchar(400),
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

create table tbl_county
(
	id_county uuid not null
		constraint tbl_county_pkey
			primary key,
	id_language_content_name uuid,
	id_administrative_region uuid,
	id_state uuid,
	created_on timestamp default now(),
	is_active boolean
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

create unique index tbl_external_import_id_external_import_uindex
	on tbl_external_import (id_external_import)
;

create table tbl_intervention_plan_structure
(
	id_intervention_plan_structure uuid not null
		constraint tbl_intervention_plan_structure_pkey
			primary key,
	id_intervention_plan uuid,
	sprinkler_type varchar(50),
	sprinkler_floor varchar(50),
	sprinkler_wall varchar(50),
	sprinkler_sector varchar(50),
	id_construction_type uuid,
	id_construction_type_for_joits uuid,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_fire_hydrant_type
(
	id_fire_hydrant_type uuid not null
		constraint tbl_fire_hydrant_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_operator_type
(
	id_operator_type uuid not null
		constraint tbl_operator_type_pkey
			primary key,
	type_name varchar(3),
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_rate_type
(
	id_rate_type uuid not null
		constraint tbl_rate_type_pkey
			primary key,
	id_language_content_name uuid,
	is_rate boolean,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_pressure_type
(
	id_pressure_type uuid not null
		constraint tbl_pressure_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_intervention_plan_fire_hydrant
(
	id_intervention_plan_fire_hydrant uuid not null
		constraint tbl_intervention_plan_fire_hydrant_pkey
			primary key,
	id_intervention_plan uuid not null,
	id_fire_hydrant uuid not null,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_region
(
	id_region uuid not null
		constraint tbl_region_pkey
			primary key,
	code varchar(2),
	id_language_content_name varchar(50),
	id_state uuid,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_city_type
(
	id_city_type uuid not null
		constraint tbl_city_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_construction_type
(
	id_construction_type uuid not null
		constraint tbl_construction_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean
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
	is_active boolean
)
;

create table tbl_diameter_type
(
	id_diameter_type uuid not null
		constraint tbl_diameter_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_fire_hydrant_connection_type
(
	id_fire_hydrant_connection_type uuid not null
		constraint tbl_fire_hydrant_connection_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean
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

create table tbl_hazardous_material
(
	id_hazardous_material uuid not null
		constraint tbl_hazardous_material_pkey
			primary key,
	material_number varchar(50),
	material_name varchar(150),
	guide_number varchar(255),
	reaction_to_water boolean,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_person_requiring_assistance_type
(
	id_person_requiring_assistance_type uuid not null
		constraint tbl_person_requiring_assistance_type_pkey
			primary key,
	type_name varchar(50),
	created_on timestamp default now(),
	is_active boolean
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
	is_active boolean
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
	is_active boolean
)
;

create table tbl_survey_choice
(
	id_survey_choice uuid not null
		constraint tbl_survey_choice_pkey
			primary key,
	id_survey_question uuid,
	sequence integer,
	id_language_content uuid,
	id_survey_question_next uuid,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_survey_question
(
	id_survey_question uuid not null
		constraint tbl_survey_question_pkey
			primary key,
	id_survey uuid,
	id_language_content_title uuid,
	id_language_content_description uuid,
	id_survey_question_next uuid,
	sequence integer,
	question_type enum_question_type,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_unit_of_measure
(
	id_unit_of_measure uuid not null
		constraint tbl_unit_of_measure_pkey
			primary key,
	id_language_content_name uuid,
	abbreviation varchar(5),
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
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_webuser_fire_safety_department
(
	id_webuser_fire_safety_department uuid not null
		constraint tbl_webuser_fire_safety_dept_id_user_fire_safety_dept_pk
			primary key,
	id_webuser uuid,
	id_fire_safety_department uuid not null,
	created_on timestamp default now(),
	is_active boolean
)
;

create table tbl_apis_action
(
	id_apis_update uuid not null
		constraint tbl_field_update_pkey
			primary key,
	id_webuser uuid,
	action_time timestamp default now(),
	action_table varchar(50),
	action_table_id uuid
)
;

create unique index tbl_field_update_id_field_update_uindex
	on tbl_apis_action (id_apis_update)
;

