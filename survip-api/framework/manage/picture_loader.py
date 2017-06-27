import base64
import json
import uuid
import logging

from framework.models.picture import Picture
from .database import Database


class PictureLoader:
	@staticmethod
	def get(id_picture):
		json_data = {'id_language_content': ''}

		try:
			with Database() as db:
				data = db.query(Picture).filter(Picture.id_picture == id_picture).first()
			json_data = {'id_language_content': id_picture, 'data': data}
		except Exception as e:
			logging.info("Error on get of PictureLoader : %s" % e)

		return json_data