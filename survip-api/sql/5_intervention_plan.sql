create table tbl_alarm_panel_type
(
	id_alarm_panel_type uuid not null
		constraint tbl_alarm_panel_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_construction_type
(
	id_construction_type uuid not null
		constraint tbl_construction_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_fire_hydrant
(
	id_fire_hydrant uuid not null
		constraint tbl_fire_hydrant_pkey
			primary key,
	id_city uuid not null,
	id_lane uuid not null,
	id_intersection uuid,
	id_fire_hydrant_type uuid,
	id_operator_type_rate uuid,
	id_unit_of_measure_rate uuid,
	id_operator_type_pressure uuid,
	id_unit_of_measure_pressure uuid,
	coordinates geometry,
	altitude double precision,
	fire_hydrant_number varchar(10),
	rate_from varchar(5),
	rate_to varchar(5),
	pressure_from varchar(5),
	pressure_to varchar(5),
	color varchar(50),
	comments text,
	physical_position varchar(50),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_fire_hydrant_connection
(
	id_fire_hydrant_connection uuid not null
		constraint tbl_fire_hydrant_connection_pkey
			primary key,
	id_fire_hydrant uuid,
	id_unit_of_measure_diameter uuid,
	id_fire_hydrant_connection_type uuid,
	diameter double precision,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_fire_hydrant_connection_type
(
	id_fire_hydrant_connection_type uuid not null
		constraint tbl_fire_hydrant_connection_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_fire_hydrant_type
(
	id_fire_hydrant_type uuid not null
		constraint tbl_fire_hydrant_type_pkey
			primary key,
	id_language_content_name uuid,
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_operator_type
(
	id_operator_type uuid not null
		constraint tbl_operator_type_pkey
			primary key,
	type_name varchar(3),
	created_on timestamp default now(),
	is_active boolean default true
)
;

create table tbl_unit_of_measure
(
	id_unit_of_measure uuid not null
		constraint tbl_unit_of_measure_pkey
			primary key,
	id_language_content_name uuid,
	abbreviation varchar(5),
	type varchar(20),
	created_on timestamp default now(),
	is_active boolean default true not null
)
;

create table tbl_intervention_plan
(
	id_intervention_plan uuid not null
		constraint tbl_intervention_plan_pkey
			primary key,
	id_lane_transversal uuid,
	id_picture_site_plan uuid,
	number varchar(50),
	plan_name varchar(50),
	other_information text,
	created_on timestamp default now(),
	revised_on timestamp,
	approved_on timestamp,
	is_active boolean default true not null
)
;

create table tbl_intervention_plan_building
(
	id_intervention_plan_building uuid not null
		constraint tbl_intervention_plan_building_id_intervention_plan_building_pk
			primary key,
	id_intervention_plan uuid,
	id_building uuid,
	id_picture uuid,
	id_unit_of_measure_height uuid,
	id_unit_of_measure_ewf uuid,
	id_construction_type uuid,
	id_construction_type_for_joits uuid,
	building_plan_number varchar(50),
	additional_information text,
	height double precision,
	estimated_water_flow integer,
	pipeline_location varchar(200),
	sprinkler_type varchar(50),
	sprinkler_floor varchar(50),
	sprinkler_wall varchar(50),
	sprinkler_sector varchar(50),
	id_alarm_panel_type uuid,
	alarm_panel_floor varchar(50),
	alarm_panel_wall varchar(50),
	alarm_panel_sector varchar(50),
	created_on timestamp default now(),
	is_parent boolean default true not null,
	is_active boolean default true not null
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
	is_active boolean default true not null
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
	is_active boolean default true not null
)
;