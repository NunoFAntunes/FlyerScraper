import requests
from bs4 import BeautifulSoup
from Post import Post
from datetime import datetime
import os
from random import randint
import re
from docx import Document
from docx.shared import Inches

with open("competitors.conf", "r", encoding='utf8') as file:
	competitors = [line.rstrip('\n') for line in file]
URL = "https://blog200porcento.com/?skip="
MAIN_FOLDER = os.path.dirname(os.path.realpath(__file__))

def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)

def open_html(path):
    with open(path, 'rb') as f:
        return f.read()

def find_posts(html):
	soup = BeautifulSoup(html, 'lxml')
	tags = soup.find_all("div", {"class": "posttexto"})
	return tags

# Aux for get_posts_after
def get_title_date_image_from_tag(tag):
	main_info = tag.find("h2")
	title = main_info.text
	date = tag.find("div", {"class": "date"}).text
	image_page = main_info.find('a')['href']
	return title, date, image_page

def get_posts_after(posts, timestamp):
	folhetos = []
	continue_flag = True
	for post in posts:
		title, date, image = get_title_date_image_from_tag(post)
		folheto = Post(str(title), str(date), image)
		if folheto.check_post_after(timestamp):
			folhetos.append(folheto)
			print(title)
			print(date)
			print(image)
		else:
			continue_flag = False
	return folhetos, continue_flag

def parse_page(url, timestamp):
	r = requests.get(url)
	save = save_html(r.content, "html_saved")
	html = open_html("html_saved")
	posts = find_posts(html)
	folhetos, continue_flag = get_posts_after(posts, timestamp)
	return folhetos, continue_flag

def get_all_posts_after(timestamp):
	continue_flag = True
	iterator = 0
	folhetos = []
	while continue_flag == True:
		url = URL + str(iterator)
		folhetos_da_pag, cont = parse_page(url, timestamp)
		continue_flag = cont
		folhetos= folhetos + folhetos_da_pag
		iterator = iterator + 5
	return folhetos

def process_subpage(url, competitor, date, title):
	r = requests.get(url)
	save_subpage = save_html(r.content, "html_subpage")
	html = open_html("html_subpage")
	soup = BeautifulSoup(html, 'lxml')
	post = soup.find("div", {"class": "posttexto"})
	img_tags = post.find_all('img')
	urls = [img['src'] for img in img_tags]

	competitor_raw_path = os.path.join(MAIN_FOLDER, "raw_images", competitor)
	competitor_word_path = os.path.join(MAIN_FOLDER, "catalogues", competitor)


	title = re.sub('[!@#$<>:"\\/|?*]', '', title)
	
	folder_raw = os.path.join(competitor_raw_path, date.strftime('%b%Y'), title)
	folder_word = os.path.join(competitor_word_path, date.strftime('%b%Y'))
	if not os.path.exists(folder_raw):
		os.makedirs(folder_raw)
	if not os.path.exists(folder_word):
		os.makedirs(folder_word)
	i = 0

	# WORD PROCESSING
	document = Document()

	# IMAGES PROCESSING
	for img_url in urls:
		filename = competitor + " " + date.strftime('%Y%m%d') + " " + str(i) + " " + str(randint(0, 999999))
		completeName = os.path.join(folder_raw, filename+".png")
		with open(completeName, 'wb') as f:
			response = requests.get(img_url)
			f.write(response.content)
		document.add_picture(completeName, width=Inches(6.1))
		i+=1
	document.save(os.path.join(folder_word, '{title}.docx'.format(title=title)))


def process_all_posts_into_images(folhetos):
	for folheto in folhetos:
		# Checkar qual o concorrente responsável pelo folheto
		title = str(folheto.get_post_title()).lower()
		date = folheto.get_post_date()
		flyer_competitor = "outros"
		for competitor in competitors:
			if competitor in title:
				flyer_competitor = competitor
		image = folheto.get_post_image()
		process_subpage(image, flyer_competitor, date, title)


def process_specific_competitors(folhetos, competitors_to_search):
	for folheto in folhetos:
		# Checkar qual o concorrente responsável pelo folheto
		title = str(folheto.get_post_title()).lower()
		date = folheto.get_post_date()
		flyer_competitor = "outros"
		for competitor in competitors_to_search:
			if competitor in title:
				flyer_competitor = competitor
				image = folheto.get_post_image()
				process_subpage(image, flyer_competitor, date, title)
			else:
				pass