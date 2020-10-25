#! usr/bin/env python3
import os
import sys
import urllib.parse
from urllib.request import Request, urlopen

import praw
import pyautogui
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PIL import Image

# Change the constants below to modify the number of max images to fetch and
# the destination directory of these images
MAX_NUM_IMAGES = 100
if len(sys.argv):
    MAX_NUM_IMAGES = int(sys.argv[1])
print("MAX_NUM_IMAGES:", MAX_NUM_IMAGES)

SYSTEM_SCREEN_WIDTH, SYSTEM_SCREEN_HEIGHT = pyautogui.size()
print("SYSTEM_SCREEN_RESOLUTION:", SYSTEM_SCREEN_WIDTH, "x", SYSTEM_SCREEN_HEIGHT)

HOME = os.path.expanduser("~")
IMAGE_DIRECTORY_PATH = f"{HOME}/Pictures/Reddit_Wallpapers"
print("IMAGE_DIRERCTORY_PATH:", IMAGE_DIRECTORY_PATH, "\n")

def setup():
    load_dotenv()

    # PHASE 0: ensure destination directory exists
    if os.path.exists(IMAGE_DIRECTORY_PATH):
        os.chdir(IMAGE_DIRECTORY_PATH)
        print(f"Sucessfully navigated to directory: {IMAGE_DIRECTORY_PATH}\n")
    else:
        raise OSError("The directory path: /Users/<User>/Pictures/Reddit_Wallpapers does not exist...")

    reddit = praw.Reddit(client_id=os.getenv("PERSONAL_USE_SCRIPT"),
                        client_secret=os.getenv("SECRET_KEY"),
                        user_agent="get-reddit-wallpapers-script by /u/" + os.getenv("REDDIT_USERNAME"),
                        username=os.getenv("REDDIT_USERNAME"),
                        password=os.getenv("REDDIT_PASSWORD"))
    return reddit.subreddit("wallpaper")


def main():
    subreddit = setup()
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
        with open(f"reddit_wallpaper_{i+1}.jpg", "wb+") as image_file:
            image_file.write(image_data)
            count += 1

        with Image.open(f"reddit_wallpaper_{i+1}.jpg") as image_file:
            width, height = image_file.size
            # filter under 200 KB or anything less than system screen resolution
            if os.stat(f"reddit_wallpaper_{i+1}.jpg").st_size < 200000 or width < SYSTEM_SCREEN_WIDTH or height < SYSTEM_SCREEN_HEIGHT:
                os.remove(f"reddit_wallpaper_{i+1}.jpg")
                count -= 1
        i += 1

    print(f"\rSuccessfully Downloaded {count} wallpapers from /r/wallpaper's top {MAX_NUM_IMAGES} hottest submissions")

if __name__ == "__main__":
    main()
