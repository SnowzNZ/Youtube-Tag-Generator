from requests_html import HTMLSession
from bs4 import BeautifulSoup

s = HTMLSession()

query = input("Enter a title or phrase: ")

split_query = query.split()

search_query = "+".join(split_query)

url = f"https://www.youtube.com/results?search_query={search_query}"

tags = []


def get_videos(url):
    global video_urls
    video_urls = []

    search = s.get(url)

    search.html.render(sleep=1)

    videos = search.html.find(
        "ytd-video-renderer.style-scope.ytd-item-section-renderer"
    )

    for video in videos:
        video_url = (
            "https://www.youtube.com"
            + video.find("a#video-title", first=True).attrs["href"]
        )

        video_urls.append(video_url)


def get_tags(url):
    video = s.get(url)
    video.html.render(sleep=0, timeout=100, keep_page=False, scrolldown=5)

    soup = BeautifulSoup(video.html.html, "html.parser")

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

amount = int(
    input(f"How many videos should be searched for tags out of {len(video_urls)}? ")
)

for i in range(amount):
    get_tags(video_urls[i])

print(tags)
