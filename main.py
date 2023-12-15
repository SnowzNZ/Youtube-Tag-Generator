import pyperclip
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from tqdm import tqdm

session = HTMLSession()


def get_videos(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    search = session.get(search_url)
    search.html.render(sleep=1)
    videos = search.html.find(
        "ytd-video-renderer.style-scope.ytd-item-section-renderer"
    )
    video_urls = [
        f"https://www.youtube.com{video.find('a#video-title', first=True).attrs['href']}"
        for video in tqdm(videos)
    ]
    return video_urls


def get_tags(url, max_chars=400):
    video = session.get(url)
    video.html.render(sleep=0, timeout=100, keep_page=False, scrolldown=5)
    soup = BeautifulSoup(video.html.html, "lxml")
    tag_elements = soup.find_all("meta", {"property": "og:video:tag"})
    tags = []
    num_chars = 0

    for meta in tag_elements:
        element_content = meta.attrs.get("content")
        for element in tags:
            num_chars += len(element)
        if num_chars < max_chars:
            if element_content not in tags:
                tags.append(element_content)
        else:
            break

    return tags


def main():
    query = input("Query: ").replace(" ", "+")

    video_urls = get_videos(query)

    print(f"Scraping {len(video_urls)} videos...")

    amount = int(input(f"How many videos do you scrap tags from?: "))

    tags = []
    print("Scraping tags...")
    for i in tqdm(range(min(amount, len(video_urls)))):
        tags.extend(get_tags(video_urls[i]))

    tags_str = str(tags).replace("[", "").replace("]", "").replace("'", "")

    print("\033c")  # clear screen

    print("Tags:")
    print(tags_str)

    copy = input("Do you want to copy the tags to the clipboard? [Y/N]\n> ")

    if copy.capitalize() == "Y":
        pyperclip.copy(tags_str)


if __name__ == "__main__":
    main()
