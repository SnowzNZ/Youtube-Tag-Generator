import pyperclip
import lxml
import cchardet
import os
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from tqdm import tqdm

session = HTMLSession()

query = input("Please enter a query or title\n> ")

split_query = query.split()

search_query = "+".join(split_query)

url = f"https://www.youtube.com/results?search_query={search_query}"

tags = []


def get_videos(url: str):
    global video_urls
    video_urls = []

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
    video = session.get(url)
    video.html.render(sleep=0, timeout=100, keep_page=False, scrolldown=5)

    soup = BeautifulSoup(video.html.html, "lxml")

    num_chars = 0

    f = soup.find_all("meta", {"property": "og:video:tag"})

    for meta in f:
        a = meta.attrs.get("content")
        for element in tags:
            num_chars += len(element)
        if num_chars < 400:
            if a not in tags:
                tags.append(a)
            else:
                pass
        else:
            break


get_videos(url)
print("Scraping videos...")

amount = int(
    input(
        f"How many top videos out of {len(video_urls)}, do you want to take tags from?\nThe more videos, the longer it will take.\n> "
    )
)

print("Scraping tags...")
for i in tqdm(range(amount)):
    get_tags(video_urls[i])

my_list_str = str(tags).replace("[", "").replace("]", "").replace("'", "")

os.system("cls" if os.name == "nt" else "clear")

print("Tags:")
print(my_list_str)
copy = input("Do you want to copy the tags to the clipboard? [Y/N]\n> ")

if copy.capitalize() == "Y":
    pyperclip.copy(my_list_str)
else:
    pass

print(
    "Thanks for using my tool! Make sure to give it a star on GitHub if you liked it!"
)
