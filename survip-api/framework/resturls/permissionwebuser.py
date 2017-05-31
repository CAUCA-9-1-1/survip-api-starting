from ..config import setup as config
from ..manage.database import Database
from ..models.permission import Permission as Table
from .base import Base
from .permissionsystemfeature import PermissionSystemFeature


class PermissionWebuser(Base):
	active = False
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_permission_object):
		data = ()
		features = PermissionSystemFeature().get()

		if 'data' in features:
			for feature in features['data']:
				feature.webuser_value = False

				with Database() as db:
					user_permission = db.query(Table).filter(
						Table.id_permission_system == config.PERMISSION['systemID'],
						Table.id_permission_object == id_permission_object,
						Table.id_permission_system_feature == feature.id_permission_system_feature
					).first()

					if user_permission is not None:
						feature.webuser_value = user_permission.access

				data = data + (feature,)

		return {
			'data': data
		}
