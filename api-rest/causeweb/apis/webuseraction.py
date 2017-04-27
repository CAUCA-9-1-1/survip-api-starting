import json
import uuid
import hmac
import hashlib
from causeweb import config
from causeweb.session.static import Static as Session
from causeweb.storage.db import DB
from causeweb.utilities import Utilities
from .base import Base


class WebuserAction(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': 'create',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self):
		""" Return all webuser action information
		"""
		with DB() as db:
			data = db.get_all("""SELECT tbl_webuser_action.*, CONCAT(attr1.attribute_value, ' ', attr2.attribute_value) AS user FROM tbl_webuser_action
								LEFT JOIN tbl_webuser wu ON wu.id_webuser=tbl_webuser_action.id_webuser
								LEFT JOIN tbl_webuser_attributes attr1 ON attr1.id_webuser = wu.id_webuser AND attr1.attribute_name='first_name'
								LEFT JOIN tbl_webuser_attributes attr2 ON attr2.id_webuser = wu.id_webuser AND attr2.attribute_name='last_name';""")

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new webuseraction

		:param args: {
			id_webuser: UUID,
			object: String,
			name: String,
			param: JSON
		}
		"""
		with DB() as db:
			db.execute("""INSERT INTO tbl_webuser_action(id_webuser_action, id_webuser, action_time, action_object, action_name, action_param)
			           VALUES (uuid_generate_v4(), %s, NOW(), %s, %s, %s);""", (
				args['id_webuser'], args['object'], args['name'], args['param']
			))

		return {
			'message': 'webuser action successfully added'
		}
