from sqlalchemy import Column, Boolean, DateTime, Float, Numeric, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from .language_content import LanguageContent
from .lane import Lane


Base = declarative_base()


class Building(Base):
	__tablename__ = "tbl_building"

	id_building = Column(String(26), primary_key=True, nullable=False)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	matricule = Column(String(18), nullable=False)
	civic_number = Column(String(15))
	civic_letter = Column(String(10))
	civic_supp = Column(String(10))
	civic_letter_supp = Column(String(10))
	appartment_number = Column(String(10))
	floor = Column(String(10))
	suite = Column(String(Numeric))
	number_of_appartment = Column(Numeric)
	number_of_building = Column(Numeric)
	vacant_land = Column(Boolean)
	year_of_construction = Column(Numeric)
	building_value = Column(Float)
	id_lane = Column(String(36), ForeignKey(Lane.id_lane), nullable=False)
	postal_code = Column(String(6))
	id_utilisation_code = Column(String(36))
	id_sector = Column(String(36))
	id_mutual_aid_sector = Column(String(36))
	id_jaws_extrication_sector = Column(String(36))
	id_sled_sector = Column(String(36))
	id_risk_level = Column(String(36))
	source = Column(String(25))
	is_parent = Column(Boolean)
	utilisation_description = Column(String(255))
	show_in_resources = Column(Boolean)
	id_resource_category = Column(String(50))
	id_association_building = Column(String(50))
	id_association_type = Column(String(50))
	id_unit_type = Column(String(50))
	coordinates = Column(String)
	coordinates_source = Column(String(50))
	details = Column(Text)
	created_on = Column(DateTime)
	is_active = Column(Boolean)

	name = relationship(LanguageContent, lazy='joined')
	lane = relationship(Lane, lazy='joined')

	@hybrid_property
	def address(self):
		if isinstance(self.lane.name, object):
			return self.civic_number + ' ' + self.lane.name.description
		else:
			return self.civic_number + ' ' + self.lane.name[0].description
