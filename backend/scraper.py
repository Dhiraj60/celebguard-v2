# backend/scraper.py (updated with YouTube + Instagram API support)

import requests
import os
import re

# Load API keys from environment variables or config
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")  # For future use


def check_youtube_video(video_url):
    try:
        video_id = extract_youtube_id(video_url)
        if not video_id:
            return False

        api_url = f"https://www.googleapis.com/youtube/v3/videos?part=status&id={video_id}&key={YOUTUBE_API_KEY}"
        res = requests.get(api_url)
        if res.status_code != 200:
            print(f"[❌ YT API Error] {res.status_code}: {res.text}")
            return False

        data = res.json()
        return len(data.get("items", [])) > 0

    except Exception as e:
        print(f"[❌ YouTube Check Failed] {e}")
        return False


def extract_youtube_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url)
    return match.group(1) if match else None


def check_instagram_post(insta_url):
    # Placeholder for Instagram Graph API logic
    # Future implementation here using Business Account & Facebook App
    print(f"[ℹ️ IG API Placeholder] Currently falling back to basic check for: {insta_url}")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }
        res = requests.get(insta_url, headers=headers, timeout=10)
        return res.status_code == 200 and "Sorry, this page isn't available." not in res.text
    except:
        return False


def check_content_live(url):
    if "youtube.com" in url:
        return check_youtube_video(url)
    elif "instagram.com" in url:
        return check_instagram_post(url)
    else:
        print("[⚠️ Unknown Platform]")
        return False
