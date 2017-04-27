import json
import uuid
import decimal
import datetime


class JsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.strftime("%Y/%m/%d %H:%M:%S")
		elif isinstance(obj, datetime.date):
			return obj.strftime("%Y/%m/%d")
		if isinstance(obj, datetime.time):
			return obj.strftime("%H:%M:%S")
		elif isinstance(obj, uuid.UUID):
			return str(obj)
		elif isinstance(obj, decimal.Decimal):
			return str(obj)
		elif isinstance(obj, Exception):
			return str(obj)

		return json.JSONEncoder.default(self, obj)
