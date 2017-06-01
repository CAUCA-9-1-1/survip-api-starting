create type enum_survey_type as enum ('residential', 'general', 'agricultural', 'intervention_plan')
;

create type enum_question_type as enum ('text', 'choice', 'date')
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