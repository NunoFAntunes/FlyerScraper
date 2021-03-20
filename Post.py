from aux_funcs import AuxFunc

class Post(object):
	def __init__(self, title, date, image):
		self.title = title
		self.date = AuxFunc.parse_date(date)
		self.image = image


	# INCLUDES DAY 
	def check_post_after(self, timestamp):
		if self.date < timestamp:
			return False
		return True

	def get_post_title(self):
		return self.title

	def get_post_date(self):
		return self.date

	def get_post_image(self):
		return self.image
