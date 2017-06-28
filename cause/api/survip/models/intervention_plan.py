from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
from .picture import Picture


Base = declarative_base()


class InterventionPlan(Base):
	__tablename__ = "tbl_intervention_plan"

	id_intervention_plan = Column(String(36), primary_key=True, nullable=False)
	plan_name = Column(String(50))
	id_lane_transversal = Column(String(36))
	id_picture_site_plan = Column(String(36))
	number = Column(String(50))
	is_active = Column(Boolean, default=True)


#	@hybrid_property
#	def picture(self):
#		return Picture().get(self.id_picture_site_plan)
