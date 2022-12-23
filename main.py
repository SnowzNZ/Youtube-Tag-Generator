"""
Generates YouTube tags based off of top ranking videos.
"""

import os
from typing import List

import pyperclip  # type: ignore
from bs4 import BeautifulSoup
from requests_html import HTMLSession  # type: ignore
from tqdm import tqdm

session = HTMLSession()

query = input("Please enter a query or title\n> ")

SEARCH_QUERY = "+".join(query.split())

QUERY_URL = f"https://www.youtube.com/results?search_query={SEARCH_QUERY}"

tags: List[str] = []

video_urls = []


def get_videos(url: str):
    """Get urls of top ranking videos from search query."""

    search = session.get(url)

    search.html.render(sleep=1)

    videos = search.html.find(
        "ytd-video-renderer.style-scope.ytd-item-section-renderer"
    )

    for video in tqdm(videos):
        video_url = (
            "https://www.youtube.com"
            + video.find("a#video-title", first=True).attrs["href"]
        )

        video_urls.append(video_url)


def get_tags(url: str):
    """Gets tags from YouTube video's url."""
    video = session.get(url)
    video.html.render(sleep=0, timeout=100, keep_page=False, scrolldown=5)

    soup = BeautifulSoup(video.html.html, "lxml")

    num_chars = 0

    tag_elements = soup.find_all("meta", {"property": "og:video:tag"})

    for meta in tag_elements:
        element_content = meta.attrs.get("content")
        for element in tags:
            num_chars += len(element)
        if num_chars < 400:
            if element_content not in tags:
                tags.append(element_content)
            else:
                pass
        else:
            break


get_videos(QUERY_URL)
print("Scraping videos...")

amount = int(
    input(
        f"How many top videos out of {len(video_urls)}, do you want to take ta"
        "gs from?\nThe more videos, the longer it will take.\n> "
    )
)

print("Scraping tags...")
for i in tqdm(range(amount)):
    get_tags(video_urls[i])

TAGS = str(tags).replace("[", "").replace("]", "").replace("'", "")

os.system("cls" if os.name == "nt" else "clear")

print("Tags:")
print(TAGS)
copy = input("Do you want to copy the tags to the clipboard? [Y/N]\n> ")

if copy.capitalize() == "Y":
    pyperclip.copy(TAGS)
else:
    pass

print(
    "Thanks for using my tool! Make sure to give it a star on GitHub if you li"
    "ked it!"
)
