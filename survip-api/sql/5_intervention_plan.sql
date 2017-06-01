create table tbl_alarm_panel_type
(
	id_alarm_panel_type uuid not null
		constraint tbl_alarm_panel_type_pkey
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

create table tbl_fire_hydrant
(
	id_fire_hydrant uuid not null
		constraint tbl_fire_hydrant_pkey
			primary key,
	id_city uuid,
	id_lane uuid,
	id_intersection uuid,
	id_fire_hydrant_type uuid,
	coordinates geometry,
	altitude double precision,
	fire_hydrant_number varchar(10),
	id_operator_type_rate uuid,
	rate_from varchar(5),
	rate_to varchar(5),
	id_unit_of_measure_rate uuid,
	id_operator_type_pressure uuid,
	pressure_from varchar(5),
	pressure_to varchar(5),
	id_unit_of_measure_pressure uuid,
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
	id_unit_of_measure_diameter uuid,
	id_fire_hydrant_connection_type uuid,
	created_on timestamp default now(),
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
	id_lane_transversal uuid,
	id_picture_site_plan uuid,
	other_information text,
	created_on timestamp default now(),
	revised_on timestamp,
	approved_on timestamp,
	is_active boolean
)
;

create table tbl_intervention_plan_building
(
	id_intervention_plan_building uuid not null
		constraint tbl_intervention_plan_building_id_intervention_plan_building_pk
			primary key,
	id_intervention_plan uuid,
	id_building uuid,
	additional_information text,
	height double precision,
	id_unit_of_measure_height uuid,
	estimated_water_flow integer,
	id_unit_of_measure_ewf uuid,
	id_construction_type uuid,
	id_construction_type_for_joits uuid,
	pipeline_location varchar(200),
	sprinkler_type varchar(50),
	sprinkler_floor varchar(50),
	sprinkler_wall varchar(50),
	sprinkler_sector varchar(50),
	alarm_panel_type uuid,
	alarm_panel_floor varchar(50),
	alarm_panel_wall varchar(50),
	alarm_panel_sector varchar(50),
	created_on timestamp,
	is_active boolean
)
;

create table tbl_intervention_plan_course
(
	id_intervention_plan_course uuid not null
		constraint tbl_intervention_plan_course_pkey
			primary key,
	id_firestation uuid,
	course text,
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