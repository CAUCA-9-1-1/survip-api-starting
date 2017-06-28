import json

from geoalchemy2 import functions
from sqlalchemy import Column, Boolean, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from api.management.core.database import Database
from cause.api.management.models.language_content import LanguageContent
from ...models.lane import Lane

Base = declarative_base()


class BuildingForDisplay(Base):
	__tablename__ = "tbl_building"

	id_building = Column(String(26), primary_key=True, nullable=False)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	matricule = Column(String(18), nullable=False)
	civic_number = Column(String(15))
	civic_letter = Column(String(10))
	civic_supp = Column(String(10))
	civic_letter_supp = Column(String(10))

	id_lane = Column(String(36), ForeignKey(Lane.id_lane))
	id_utilisation_code = Column(String(36))
	id_risk_level = Column(String(36))
	is_active = Column(Boolean, default=True)

	#@hybrid_property
	#def name(self):
		#return MultiLang.get(self.id_language_content_name)

	@hybrid_property
	def geojson(self):
		with Database() as db:
			points = db.query(functions.ST_AsGeoJSON(self.coordinates)).first()

		geojson = ()
		for pos, val in enumerate(points):
			geojson = geojson + (json.loads(val),)

		return geojson
