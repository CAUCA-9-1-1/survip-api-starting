from sqlalchemy import Column, Boolean, String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InterventionPlanFireHydrant(Base):
	__tablename__ = "tbl_intervention_plan_fire_hydrant"

	id_intervention_plan_fire_hydrant = Column(String(36), primary_key=True, nullable=False)
	id_intervention_plan = Column(String(36), ForeignKey('tbl_intervention_plan.id_intervention_plan'))
	id_fire_hydrant = Column(String(36), nullable=False)
	created_on = Column(DateTime)
	deleted_on = Column(DateTime)
	is_active = Column(Boolean, default=True)
