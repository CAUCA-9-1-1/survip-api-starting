from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from api.management.core.multilang import MultiLang
from cause.api.management.models.language_content import LanguageContent

Base = declarative_base()


class HazardousMaterial(Base):
	__tablename__ = "tbl_hazardous_material"

	id_hazardous_material = Column(String(36), primary_key=True)
	number = Column(String(50))
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	guide_number = Column(String(255))
	reaction_to_water = Column(Boolean)
	toxic_inhalation_hazard = Column(Boolean)
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_hazardous_material, number, id_language_content,
	             guide_number, reaction_to_water, toxic_inhalation_hazard):
		self.id_hazardous_material = id_hazardous_material
		self.number = number
		self.id_language_content_name = id_language_content
		self.guide_number = guide_number
		self.reaction_to_water = reaction_to_water
		self.toxic_inhalation_hazard = toxic_inhalation_hazard