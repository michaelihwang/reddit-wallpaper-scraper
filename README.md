# Reddit Wallpaper Scraper
Get 100 images from /r/wallpapers's hot tab via [Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html).

By default, the script saves images in directory `/Users/<User>/Pictures/Reddit_Wallpapers` that are **at least 200KB** in size and that has a resolution of **at least** your current screen resolution. Feel free to change the destination folder path.

Use `$ python script.py` to run the script.

## Setup and Running Script

1. Clone this repository

2. Use `pip install -r requirements.txt` to install dependencies if they are missing

3. Create directory `/Users/<User>/Pictures/Reddit_Wallpapers` (or change destination directory in the script).

4. Log into your reddit account and follow [this link](https://www.reddit.com/prefs/apps) and click **create app** or **create another app** button at the bottom left.

5. Create your application by providing a name, descripotion, and select the **script** option. Put `http://localhost:8080` in the redirect uri field (from [praw docs](https://praw.readthedocs.io/en/latest/getting_started/authentication.html)).

6. Click **create app** and take note of your 14-char **personal use script** and 27-char **secret**.

7. Create `.env` in the respository directory and create the following variables:
```
PERSONAL_USE_SCRIPT="lololol"
SECRET_KEY="lalala"
REDDIT_USERNAME="my_derpy_username"
REDDIT_PASSWORD="my_derpy_password"
```

8. In `script.py` modify constants: `MAX_NUM_IMAGES` and/or `IMAGE_DIRECTORY_PATH` if you wish.

9. On the command line, run `$ python script.py`

10. Open Desktop & Screensaver via Settings and add `Reddit_Wallpapers` (or your directory if you changed it). Cycle it and/or randomize it as you wish.

11. DONE!

## License
MIT License Copyright © 2020 Michael Hwang
