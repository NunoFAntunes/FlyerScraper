from soup_parser import get_all_posts_after, process_all_posts_into_images
import datetime

posts = get_all_posts_after(datetime.datetime(2021, 3, 11))
print(posts)
print("Processing posts")
process_all_posts_into_images(posts)