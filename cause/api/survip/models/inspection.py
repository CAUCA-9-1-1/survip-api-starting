from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cause.api.management.core.manage.database import Database
from .building import Building

Base = declarative_base()


class Inspection(Base):
	__tablename__ = "tbl_inspection"

	id_inspection = Column(String(36), primary_key=True, nullable=False)
	id_building = Column(String(36), ForeignKey(Building.id_building), nullable=False)
	id_survey = Column(String(36))
	id_intervention_plan = Column(String(36))
	id_webuser = Column(String(36))
	created_on = Column(DateTime, default=datetime.now)
	created_by = Column(String(36))
	is_active = Column(Boolean, default=True)
	is_completed = Column(Boolean, default=False)

	@hybrid_property
	def address(self):
		with Database() as db:
			return db.query(Building).get(self.id_building).address

	@hybrid_property
	def id_risk_level(self):
		with Database() as db:
			return db.query(Building).get(self.id_building).id_risk_level

	@hybrid_property
	def matricule(self):
		with Database() as db:
			return db.query(Building).get(self.id_building).matricule

	def __init__(self, id_inspection, id_survey, id_building, id_webuser):
		self.id_inspection = id_inspection
		self.id_survey = id_survey
		self.id_building = id_building
		self.id_webuser = id_webuser