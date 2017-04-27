import json
import uuid
from ..storage.db import DB
from ..utilities import Utilities


class MultiLang:
	@staticmethod
	def get(id_language_content):
		json_data = {'id_language_content': ''}

		try:
			with DB() as db:
				data = db.get_all("SELECT language_code, description FROM tbl_language_content WHERE id_language_content=%s;", (id_language_content,))

			json_data = {'id_language_content': id_language_content}
			json_data.update(Utilities.list_to_dict(data, 'language_code', 'description'))
		except:
			pass

		return json_data

	@staticmethod
	def set(description, force_create=False):
		if not isinstance(description, dict):
			description = json.loads(description)

		id_language_content = description['id_language_content'] if 'id_language_content' in description else None

		if id_language_content is None or id_language_content == '' or force_create is True:
			id_language_content = uuid.uuid4()
			MultiLang.create(id_language_content, description)
		else:
			MultiLang.modify(id_language_content, description)

		return id_language_content

	@staticmethod
	def create(id_language_content, description):
		with DB() as db:
			for language_code in description:
				if language_code != 'id_language_content':
					db.execute("INSERT INTO tbl_language_content(id_language_content, language_code, description) VALUES (%s, %s, %s);",
			                   (id_language_content, language_code, description[language_code]))

	@staticmethod
	def modify(id_language_content, description):
		with DB() as db:
			for language_code in description:
				if language_code != 'id_language_content':
					db.execute("""WITH upsert AS (
								UPDATE tbl_language_content
									SET description=%s
									WHERE id_language_content=%s AND language_code=%s RETURNING *
							  ) INSERT INTO tbl_language_content (
							    id_language_content, language_code, description
							  ) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT * FROM upsert);""", (
						description[language_code], id_language_content, language_code,
						id_language_content, language_code, description[language_code]
		           ))