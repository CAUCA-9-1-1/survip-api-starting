from sqlalchemy.orm import joinedload

from api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.lane import Lane as Table, Lane
from ..resturls.mappers.lane_light_mapper import LaneLightMapper


class CityLanes(Base):
	table_name = 'tbl_lane'
	mapping_method = {
		'GET': 'get'
	}

	def get(self, language, id_city_filter):
		""" Return all lane information

        param id_city_filter: uuid
        language: string
		"""
		with Database() as db:
			rawdata = db.query(Table).\
				filter_by(is_active='1', id_city=id_city_filter).\
				options(joinedload(Lane.lane_public_code), joinedload(Lane.lane_generic_code)).\
				all()
			data = []
			for lane in rawdata :
				data.append(LaneLightMapper.generate_row(lane, language))  #({'id': lane.id_lane, 'fullName': lane.get_full_name(language)})

		return {
			'data': data
		}
