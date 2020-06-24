#! usr/bin/env python3
import praw
import requests
import sys
import os

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.parse

from dotenv import load_dotenv
load_dotenv()

# Change the constants below to modify the number of max images to fetch and
# the destination directory of these images
MAX_NUM_IMAGES = 100
IMAGE_DIRERCTORY_PATH = os.path.expanduser("~") + "/Pictures/Reddit_Wallpapers"

if os.path.exists(IMAGE_DIRERCTORY_PATH):
    os.chdir("/Users/michaelihwang/Pictures/Reddit_Wallpapers")
    print("Sucessfully navigated to directory: /Users/<User>/Pictures/Reddit_Wallpapers")
else:
    raise OSError(
        "The directory path: /Users/<User>/Pictures/Reddit_Wallpapers does not exist...")

reddit = praw.Reddit(client_id=os.getenv("PERSONAL_USE_SCRIPT"),
                     client_secret=os.getenv("SECRET_KEY"),
                     user_agent="get-reddit-wallpapers-script by /u/doctorblowhole",
                     username=os.getenv("REDDIT_USERNAME"),
                     password=os.getenv("REDDIT_PASSWORD"))

subreddit = reddit.subreddit("wallpaper")

# PHASE 1: get submission links from /r/wallpaper
submission_links = []
for submission in subreddit.hot(limit=MAX_NUM_IMAGES):
    submission_links.append("https://reddit.com" + submission.permalink)

# PHASE 2: from submission links, get unique submission image links
image_links = set()
for i in range(len(submission_links)):
    sys.stdout.write(f"\rProcessing wallpaper image {i+1} of {MAX_NUM_IMAGES}.")
    image_link_URL = submission_links[i][:21] + \
        urllib.parse.quote(submission_links[i][21:])
    req = Request(image_link_URL, headers={"User-Agent": "Mozilla/5.0"})
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")
    for link in soup.findAll("a"):
        href = link.get("href")
        if "https://i.redd.it/" in str(href)[0:18] and href not in image_links:
            image_links.add(link.get("href"))

# PHASE 3: go through image links and save them in IMAGE_DIRERCTORY_PATH
i, count = 0, 0
for image_link in image_links:
    sys.stdout.write(f"\rDownloading wallpaper image {i+1} of {len(image_links)}.")
    image_data = requests.get(image_link).content
    with open(f"reddit_wallpaper_{i+1}.jpg", "wb+") as img_file:
        img_file.write(image_data)
        count += 1

        # height of image (in 2 bytes) is at 164th position
        img_file.seek(163)
        a = img_file.read(2)    # read the 2 bytes
        height = (a[0] << 8) + a[1]
        a = img_file.read(2)    # next 2 bytes is width
        width = (a[0] << 8) + a[1]

        # filter under 200 KB or ranything less than 2880x1800 (MBP 15-inch resolution)
        if os.stat(f"reddit_wallpaper_{i+1}.jpg").st_size < 200000 or width < 2880 or height < 1800:
            os.remove(f"reddit_wallpaper_{i+1}.jpg")
            count -= 1
    i += 1

print(f"\rSuccessfully Downloaded {count} wallpapers from /r/wallpaper's top {MAX_NUM_IMAGES} hottest submissions")
