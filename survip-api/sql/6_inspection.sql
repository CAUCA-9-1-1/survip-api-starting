create table tbl_inspection
(
	id_inspection uuid not null
		constraint tbl_inspection_pkey
			primary key,
	id_survey uuid,
	id_intervention_plan uuid,
	id_building uuid,
	id_webuser uuid,
	created_on timestamp default now(),
	created_by uuid not null,
	is_completed boolean default false not null,
	is_active boolean default true not null
)
;

create table tbl_inspection_answer
(
	id_inspection_answer uuid not null
		constraint tbl_inspection_answer_pkey
			primary key,
	id_inspection uuid not null,
	id_webuser uuid not null,
	answered_on timestamp default now(),
	has_refuse boolean default false not null,
	reason_for_refusal varchar(250),
	is_absent boolean default false not null,
	is_seasonal boolean default false not null,
	is_vacant boolean default false not null
)
;

create table tbl_inspection_question
(
	id_inspection_question uuid not null
		constraint tbl_inspection_question_pkey
			primary key,
	id_inspection_answer uuid not null,
	id_survey_question uuid not null,
	id_survey_choice uuid,
	answer varchar(200)
)
;
