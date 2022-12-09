from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

url = "https://www.youtube.com/watch?v=eiRtB7CTxkI"

session = HTMLSession()

response = session.get(url)
# Execute Javascript
response.html.render(sleep=1)

soup = bs(response.html.html, "html.parser")

video_meta = {}

video_meta["tags"] = ", ".join(
    [
        meta.attrs.get("content")
        for meta in soup.find_all("meta", {"property": "og:video:tag"})
    ]
)

print(video_meta)
