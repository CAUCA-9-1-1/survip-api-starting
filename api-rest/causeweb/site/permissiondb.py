import uuid
from .. import config
from ..session.static import Static as Session
from ..storage.db import DB


class PermissionDB:
	def get(self, feature_name=None):
		id_permission_object = self.get_id_permission_object('webuser', Session.get('userId'))
		id_permission_object_parent = self.get_id_permission_object_parent(id_permission_object)

		with DB() as db:
			if feature_name is None:
				return db.get_all(
					"""SELECT tpsf.feature_name FROM tbl_permission tp
						INNER JOIN tbl_permission_system_feature tpsf ON tpsf.id_permission_system_feature = tp.id_permission_system_feature
						WHERE tp.id_permission_system=%s AND (
							tp.id_permission_object=%s OR tp.id_permission_object=%s
						  ) AND (tp.access=True OR tpsf.default_value=True)""",
					(config.PERMISSION['systemID'], id_permission_object, id_permission_object_parent)
				)
			else:
				id_permission_system_feature = self.get_id_permission_system_feature(feature_name)

				return db.get(
					"""SELECT (CASE tpsf.feature_name WHEN %s THEN True ELSE False END) FROM tbl_permission tp
						INNER JOIN tbl_permission_system_feature tpsf ON tpsf.id_permission_system_feature = tp.id_permission_system_feature
						WHERE tp.id_permission_system=%s AND (
							tp.id_permission_object=%s OR tp.id_permission_object=%s
						  ) AND tp.id_permission_system_feature=%s AND (tp.access=True OR tpsf.default_value=True)""",
					(feature_name, config.PERMISSION['systemID'], id_permission_object, id_permission_object_parent, id_permission_system_feature)
				)

	def get_all(self, id_permission_object=None, object_table=None, generic_id=None):
		if id_permission_object is None and generic_id is not None:
			id_permission_object = self.get_id_permission_object(object_table, generic_id)

		with DB() as db:
			return db.get_all(
				"""SELECT tp.id_permission, tpsf.id_permission_system_feature, tpsf.description, tpsf.feature_name, tpsf.default_value, tp.access
					FROM tbl_permission_system_feature tpsf
					LEFT JOIN tbl_permission tp ON tp.id_permission_system_feature = tpsf.id_permission_system_feature AND tp.id_permission_object=%s
					WHERE tpsf.id_permission_system=%s;
				""",
				(id_permission_object, config.PERMISSION['systemID'])
			)

		return None

	def get_id_permission_object(self, object_table, generic_id):
		with DB() as db:
			id_permission_object = db.get(
				"SELECT id_permission_object FROM tbl_permission_object WHERE object_table=%s AND generic_id=%s;",
				(object_table, generic_id)
			)

		if id_permission_object:
			return id_permission_object

		return self.create_permission_object(object_table, generic_id)

	def get_id_permission_object_parent(self, id_permission_object):
		with DB() as db:
			return db.get(
				"SELECT id_permission_object_parent FROM tbl_permission_object WHERE id_permission_object=%s;",
				(id_permission_object,)
			)

	def get_id_permission_system_feature(self, feature_name):
		with DB() as db:
			id_permission_system_feature = db.get(
				"SELECT id_permission_system_feature FROM tbl_permission_system_feature WHERE id_permission_system=%s AND feature_name=%s;",
				(config.PERMISSION['systemID'], feature_name)
			)

		if id_permission_system_feature:
			return id_permission_system_feature

		return None

	def get_object(self, id_permission_object_parent=None):
		with DB() as db:
			items = db.get_all(
				"""SELECT tpo.id_permission_object, tpo.id_permission_object_parent, tpo.object_table, tpo.generic_id, tpo.is_group, tpo.group_name
					FROM tbl_permission_object tpo
					WHERE tpo.id_permission_system=%s AND tpo.id_permission_object_parent{0}%s ORDER BY tpo.group_name;
				""".format('=' if id_permission_object_parent else ' is '),
				(config.PERMISSION['systemID'], id_permission_object_parent)
			)

		for key, row in enumerate(items):
			children = self.get_object(row['id_permission_object'])

			if len(children) > 0:
				items[key]['children'] = children

		return items

	def create_permission(self, id_permission_object, id_permission_system_feature, access):
		Session.log('causeweb.cauca.permission', 'create_permission')

		with DB() as db:
			db.execute(
				"""INSERT INTO tbl_permission
					(id_permission, id_permission_object, id_permission_system, id_permission_system_feature, created_on, access) VALUES
					(%s, %s, %s, %s, NOW(), %s);""",
				(uuid.uuid4(), id_permission_object, config.PERMISSION['systemID'], id_permission_system_feature, access)
			)

	def modify_permission(self, id_permission, access):
		Session.log('causeweb.cauca.permission', 'modify_permission', id_permission)

		with DB() as db:
			db.execute(
				"""UPDATE tbl_permission SET access=%s
					WHERE id_permission=%s;""",
				(access, id_permission)
			)

	def create_permission_system_feature(self, description, default_value):
		Session.log('causeweb.cauca.permission', 'create_permission_system_feature')

		id = uuid.uuid4()

		with DB() as db:
			db.execute(
				"INSERT INTO tbl_permission_system_feature (id_permission_system_feature, id_permission_system, feature_name, description, default_value) VALUES (%s, %s, %s, %s, %s);",
				(id, config.PERMISSION['systemID'], '', description, default_value)
			)

		return id

	def create_permission_object(self, object_type, generic_id):
		Session.log('causeweb.cauca.permission', 'create_permission_object')

		id = uuid.uuid4()

		with DB() as db:
			db.execute(
				"INSERT INTO tbl_permission_object (id_permission_object, object_table, generic_id, id_permission_system, is_group) VALUES (%s, %s, %s, %s, %s);",
				(id, object_type, generic_id, config.PERMISSION['systemID'], False)
			)

		return id

	def set_permission_object_parent(self, id_permission_object, id_permission_object_parent):
		with DB() as db:
			db.execute(
				"UPDATE tbl_permission_object SET id_permission_object_parent=%s WHERE id_permission_object=%s;",
				(id_permission_object_parent, id_permission_object)
			)