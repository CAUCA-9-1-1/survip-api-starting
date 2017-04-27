from causeweb.storage.db import DB
from causeweb.apis.base import Base
from .building import Building


class Search(Base):
	mapping_method = {
		'GET': 'search',
		'PUT': 'nearme',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def search(self, search, id_city=None):
		""" Return all building information responding to a search

		:param search: String
		:param id_city: UUID
		"""
		args = (True, True)
		list_of_search = ()
		for word in search.split(','):
			word = "%{0}%".format(word)
			args += (word, word, word, word, word)
			list_of_search += ("b.civic_number LIKE %s", "b.name LIKE %s", "b.postal_code LIKE %s", "s.street_name LIKE %s", "s.full_name LIKE %s")

		with DB() as db:
			if id_city is None:
				data = db.get_all("""SELECT b.id_building
							FROM tbl_building b
							LEFT JOIN tbl_street s ON s.id_street = b.id_street AND s.is_active=%s
							WHERE b.is_active=%s AND ({0});""".format(" OR ".join(list_of_search)), (args))
			else:
				args = (id_city,) + args
				data = db.get_all("""SELECT b.id_building
							FROM tbl_building b
							LEFT JOIN tbl_street s ON s.id_street = b.id_street AND s.is_active=%s
							WHERE s.id_city=%s AND b.is_active=%s AND ({0});""".format(" OR ".join(list_of_search)), (args))

			for key, row in enumerate(data):
				data[key] = Building().get(row['id_building'])['data']

		return {
			'data': data
		}

	def nearme(self, args):
		if 'longitude' not in args or 'latitude' not in args or 'radius' not in args:
			return {
				'data': ()
			}

		args['radius'] = int(args['radius']) * 1000

		with DB() as db:
			data = db.get_all("""SELECT id_building, distance
						FROM(
						  SELECT
						    id_building,
						    ST_Distance(coordinates, ST_SetSRID(ST_MakePoint(%s, %s), 4326), True) AS distance
						  FROM tbl_building
						  WHERE ST_DWithin(coordinates, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, True)
						) feature
						ORDER BY distance;""", (args['longitude'], args['latitude'], args['longitude'], args['latitude'], args['radius']))

		for key, row in enumerate(data):
			data[key] = Building().get(row['id_building'])['data']
			data[key].update({
				'distance': row['distance']
			})

		return {
			'data': data
		}