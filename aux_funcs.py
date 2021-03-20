import re
from datetime import datetime

class AuxFunc(object):

	def __init__(self):
		pass

	def parse_date(date:str):
		date = re.search("[0-9]{2}.[0-9]{2}.[0-9]{2}", date).group(0)
		return datetime.strptime(date, "%d.%m.%y")
