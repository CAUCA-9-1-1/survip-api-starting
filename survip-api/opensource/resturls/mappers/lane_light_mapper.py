from framework.manage.multilang import MultiLang


class LaneLightMapper:
	@staticmethod
	def generate_row(lane, language):
		return {'id': lane.id_lane, 'fullName': LaneLightMapper._generate_full_name(lane, language)}

	@classmethod
	def _generate_full_name(cls, lane, language):
		name = MultiLang.get_name_by_language(language, lane.name)
		name = cls._add_generic_code_to_name(lane, name)
		name = cls._add_public_code_to_name(lane, name)
		return name

	@classmethod
	def _add_public_code_to_name(cls, lane, name):
		if lane.lane_public_code is not None and lane.lane_public_code.description != '':
			name = "%s %s" % (lane.lane_public_code.description, name)
		return name

	@classmethod
	def _add_generic_code_to_name(cls, lane, name):
		if lane.lane_generic_code is not None and lane.lane_generic_code.add_white_space_after:
			name = "%s %s" % (lane.lane_generic_code.description, name)
		elif lane.lane_generic_code is not None:
			name = "%s%s" % (lane.lane_generic_code.description, name)
		return name