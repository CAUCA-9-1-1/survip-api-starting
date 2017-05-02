create table tbl_inspection
(
	id_inspection uuid not null
		constraint tbl_inspection_pkey
			primary key,
	id_survey uuid,
	id_building uuid,
	id_webuser uuid,
	created_on timestamp,
	created_by uuid,
	is_active boolean,
	is_completed boolean
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
