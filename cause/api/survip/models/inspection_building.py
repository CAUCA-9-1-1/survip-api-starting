from sqlalchemy import desc
from sqlalchemy.ext.hybrid import hybrid_property
from cause.api.management.core.database import Database
from .building import Building
from .inspection import Inspection


class InspectionBuilding(Building):
	@hybrid_property
	def last_inspection(self):
		with Database() as db:
			inspection = db.query(Inspection).filter(
				Inspection.id_building == self.id_building,
			    Inspection.is_active == True
			).order_by(desc(Inspection.created_on)).first()

		return inspection.created_on if inspection else None
