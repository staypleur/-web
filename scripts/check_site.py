"""Check local site references and blog data without network access."""

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "dist"


class PageReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"Duplicate ID: {attrs['id']}")
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.references.append(attrs[key])
        for target in attrs.get("aria-controls", "").split():
            self.references.append("#" + target)


def check():
    page = PageReferences()
    page.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    css = (ROOT / "style.css").read_text(encoding="utf-8")
    page.references.extend(re.findall(r"url\(['\"]?([^)'\"]+)['\"]?\)", css))
    for reference in page.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            continue
        if url.path and not (ROOT / unquote(url.path).lstrip("/")).is_file():
            page.errors.append(f"Missing local file: {reference}")
        if not url.path and url.fragment and url.fragment not in page.ids:
            page.errors.append(f"Missing anchor: {reference}")

    posts = json.loads((ROOT / "blog/posts.json").read_text(encoding="utf-8"))["posts"]
    if len(posts) != 3:
        page.errors.append("Expected three blog posts")
    for post in posts:
        if not re.fullmatch(r"https://blog\.naver\.com/gilbert61/\d+", post["url"]):
            page.errors.append(f"Invalid blog URL: {post['url']}")
        image = post.get("image", "")
        if image and (
            not re.fullmatch(r"latest-\d+\.(png|jpg|webp)", image)
            or not (ROOT / "blog" / image).is_file()
        ):
            page.errors.append(f"Invalid or missing blog image: {image}")
    if page.errors:
        raise SystemExit("\n".join(page.errors))
    print("PASS: local assets, anchors, guide targets and blog references")


if __name__ == "__main__":
    check()
