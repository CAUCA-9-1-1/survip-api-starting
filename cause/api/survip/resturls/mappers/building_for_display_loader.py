from sqlalchemy.orm import joinedload

from api.management.core.database import Database
from api.management.core.multilang import MultiLang
from ...models.lane import Lane
from ...models.risk_level import RiskLevel
from ...models.utilisation_code import UtilisationCode
from ...resturls.mappers.lane_light_mapper import LaneLightMapper


class BuildingForDisplayLoader:
	@staticmethod
	def set_address_description(language, building):
		print('full address')
		building.full_address = BuildingForDisplayLoader._get_building_description(language, building)
		print('alias name')
		building.alias_name = MultiLang.get_by_language(language, building.id_language_content_name)
		print('risk level name')
		building.risk_level_name = BuildingForDisplayLoader._get_risk_level(language, building.id_risk_level)
		building.utilisation_code_name = BuildingForDisplayLoader._get_utilisation_code(language, building.id_utilisation_code)

	@classmethod
	def _get_building_description(cls, language, building):
		lane = cls._get_lane(language, building.id_lane)
		return '%s%s, %s' % (building.civic_number, building.civic_letter, lane)

	@classmethod
	def _get_lane(cls, language, id_lane):
		with Database() as db:
			raw_data = db.query(Lane).\
				filter_by(id_lane=id_lane).\
				options(joinedload(Lane.lane_public_code), joinedload(Lane.lane_generic_code)).\
				first()
			return LaneLightMapper.generate_row(raw_data, language)['fullName']

	@classmethod
	def _get_risk_level(cls, language, id_risk_level):
		with Database() as db:
			data = db.query(RiskLevel).filter(RiskLevel.id_risk_level==id_risk_level).first()
			if data is not None:
				return MultiLang.get_name_by_language(language, data.name)
			else:
				return ''

	@classmethod
	def _get_utilisation_code(cls, language, id_utilisation_code):
		with Database() as db:
			data = db.query(UtilisationCode).filter(UtilisationCode.id_utilisation_code==id_utilisation_code).first()
			if data is not None:
				return MultiLang.get_name_by_language(language, data.name)
			else:
				return ''
