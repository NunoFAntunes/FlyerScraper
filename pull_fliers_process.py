from soup_parser import get_all_posts_after, process_all_posts_into_images, process_specific_competitors
import datetime

def pull_fliers_process(year, month, day, competitors):
	posts = get_all_posts_after(datetime.datetime(year, month, day))
	#print(posts)
	print("Processing posts")
	process_specific_competitors(posts, competitors)

def pull_all_fliers_process(year, month, day, competitors):
	posts = get_all_posts_after(datetime.datetime(year, month, day))
	#print(posts)
	print("Processing posts")
	process_all_posts_into_images(posts)