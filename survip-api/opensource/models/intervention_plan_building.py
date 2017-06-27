from sqlalchemy import Column, Boolean, String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from opensource.models.building import Building
from opensource.models.intervention_plan import InterventionPlan

Base = declarative_base()


class InterventionPlanBuilding(Base):
	__tablename__ = "tbl_intervention_plan_building"

	id_intervention_plan_building = Column(String(36), primary_key=True, nullable=False)
	id_intervention_plan = Column(String(36), ForeignKey(InterventionPlan.id_intervention_plan))
	id_building = Column(String(36), ForeignKey(Building.id_building))
	additional_information = Column(String)
	height = Column(Numeric)
	id_unit_of_measure_height = Column(String(36), nullable=False)
	estimated_water_flow = Column(Integer)
	id_unit_of_measure_ewf = Column(String(36), nullable=False)
	created_on = Column(DateTime)
	is_active = Column(Boolean, default=True)
	sprinkler_type = Column(String(50))
	sprinkler_floor = Column(String(50))
	sprinkler_wall = Column(String(50))
	sprinkler_sector = Column(String(50))
	id_construction_type = Column(String(36))
	id_construction_type_for_joist = Column(String(36))
	pipeline_location = Column(String(200))
	id_alarm_panel_type = Column(String(36))
	alarm_panel_floor = Column(String(50))
	alarm_panel_wall = Column(String(50))
	alarm_panel_sector = Column(String(50))
	building_plan_number = Column(String(50))
	is_parent = Column(Boolean)
	id_picture = Column(String(36))

	building = relationship(Building)