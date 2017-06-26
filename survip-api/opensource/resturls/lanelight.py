from sqlalchemy.orm import joinedload

from framework.manage.database import Database
from framework.resturls.base import Base
from opensource.resturls.mappers.lane_light_mapper import LaneLightMapper
from ..models.lane import Lane as Table, Lane


class LaneLight(Base):
	table_name = 'tbl_lane'
	mapping_method = {
		'GET': 'get'
	}

	def get(self, language, id_lane):
		"""
		Returns specific lane.
		:param id_lane: specific lane's id.
		:param language: language.
		:return: specific lane.
		"""
		with Database() as db:
			rawdata = db.query(Table).\
				filter_by(is_active='1', id_lane=id_lane).\
				options(joinedload(Lane.lane_public_code), joinedload(Lane.lane_generic_code)).\
				all()
			data = []
			for lane in rawdata :
				data.append(LaneLightMapper.generate_row(lane, language))

		return {'data': data}