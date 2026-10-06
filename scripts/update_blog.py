"""Refresh public Naver blog cards. Uses only Python's standard library."""
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'dist' / 'blog'
FEED = 'https://rss.blog.naver.com/gilbert61.xml'

def download(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'DahamBlogUpdater/1.0'})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read(8_000_001)
        if len(data) > 8_000_000:
            raise ValueError('Source exceeds size limit')
        return data, response.headers.get_content_type()

def refresh():
    feed, _ = download(FEED)
    items = ET.fromstring(feed).findall('./channel/item')
    entries = []
    images = {}
    for item in items:
        link = html.unescape(item.findtext('link', '')).strip()
        parsed = urlparse(link)
        post_id = re.search(r'(?:/|logNo=)(\d{10,})', link)
        if parsed.hostname != 'blog.naver.com' or not post_id or 'gilbert61' not in link:
            continue
        date = parsedate_to_datetime(item.findtext('pubDate')).astimezone(timezone(timedelta(hours=9)))
        title = html.unescape(item.findtext('title', '')).strip()
        if not title:
            continue
        entries.append({'id': post_id[1], 'title': title, 'url': 'https://blog.naver.com/gilbert61/' + post_id[1], 'date': date.strftime('%Y.%m.%d'), 'image': ''})
        match = re.search(r'<img\b[^>]*src=[\"\']([^\"\']+)', item.findtext('description', ''), re.I)
        if match:
            image_url = html.unescape(match[1])
            host = urlparse(image_url).hostname or ''
            if urlparse(image_url).scheme == 'https' and host.endswith('.pstatic.net'):
                images[post_id[1]] = image_url
    entries.sort(key=lambda entry: entry['date'], reverse=True)
    entries = entries[:3]
    if len(entries) != 3:
        raise ValueError('Feed must provide three valid posts; keeping existing data')
    DEST.mkdir(parents=True, exist_ok=True)
    # Fetch everything before publishing metadata. A failed fetch leaves the prior feed intact.
    pending = []
    for entry in entries:
        if entry['id'] in images:
            data, content_type = download(images[entry['id']])
            if content_type not in ('image/jpeg', 'image/png', 'image/webp'):
                raise ValueError('Unexpected image response')
            extension = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp'}[content_type]
            entry['image'] = 'latest-' + entry['id'] + extension
            pending.append((DEST / entry['image'], data))
    for path, data in pending:
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
    target = DEST / 'posts.json'
    previous = json.loads(target.read_text(encoding='utf-8')) if target.exists() else {}
    updated_at = previous.get('updatedAt') if previous.get('posts') == entries else None
    updated_at = updated_at or datetime.now(timezone.utc).isoformat(timespec='seconds')
    checked_month = datetime.now(timezone.utc).strftime('%Y-%m')
    payload = json.dumps({'source': FEED, 'updatedAt': updated_at, 'checkedMonth': checked_month, 'posts': entries}, ensure_ascii=False, indent=2) + '\n'
    if not target.exists() or target.read_text(encoding='utf-8') != payload:
        temporary = target.with_suffix('.tmp')
        temporary.write_text(payload, encoding='utf-8')
        temporary.replace(target)
    print('Latest blog posts: ' + ', '.join(entry['id'] for entry in entries))

if __name__ == '__main__':
    refresh()
