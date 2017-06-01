from ..config import setup as config
from ..manage.database import Database
from ..models.permission import Permission, PermissionObject, PermissionSystemFeature as Table
from .base import Base


class PermissionSystemFeature(Base):
	table_name = 'tbl_permission_system_feature'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, featureName=None):
		with Database() as db:
			if featureName is None:
				data = db.query(Table).filter(
					Table.id_permission_system == config.PERMISSION['systemID']
				).all()
			else:
				data = db.query(Table).filter(
					Table.id_permission_system == config.PERMISSION['systemID'],
					Table.feature_name == featureName
				).all()

		return {
			'data': data
		}
