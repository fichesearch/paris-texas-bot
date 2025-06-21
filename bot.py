import os
import tweepy
import pandas as pd

# Load Twitter API credentials from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Load CSV mapping
df = pd.read_csv("paris_texas_frames.csv")

# Read current progress
with open("progress.txt", "r") as f:
    index = int(f.read().strip())

if index >= len(df):
    print("All frames posted.")
    exit()

row = df.iloc[index]
filename = row['frame_filename']
caption = row['timestamp']

image_path = os.path.join("ParisFrames", filename)

# Post the image
try:
    api.update_status_with_media(status=caption, filename=image_path)
    print(f"Posted {filename} with caption '{caption}'")

    # Delete the image to save space
    os.remove(image_path)

    # Increment progress
    with open("progress.txt", "w") as f:
        f.write(str(index + 1))

except Exception as e:
    print(f"Error posting frame {filename}: {e}")
