const copyAddress = document.querySelector('[data-copy-address]');
copyAddress?.addEventListener('click', async () => {
  const status = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText(copyAddress.dataset.copyAddress);
    status.textContent = '센터 주소를 복사했습니다.';
  } catch {
    status.textContent = '주소 복사가 되지 않았습니다. 위 주소를 선택해 복사해 주세요.';
  }
});

const guideChoices = document.querySelectorAll('[data-guide]');
guideChoices.forEach(choice => choice.addEventListener('click', () => {
  guideChoices.forEach(button => {
    const selected = button === choice;
    button.setAttribute('aria-pressed', String(selected));
    document.querySelector(`#guide-${button.dataset.guide}`).hidden = !selected;
  });
}));

// A public feed maintained by GitHub Actions; no visitor credentials are used.
const blogDataRoot = 'https://raw.githubusercontent.com/staypleur/-web/main/dist/blog/';
async function refreshBlogCards(root) {
  try {
    const response = await fetch(`${root}posts.json?t=${Math.floor(Date.now() / 900000)}`, { cache: 'no-store', signal: AbortSignal.timeout(10000) });
    if (!response.ok) throw new Error('Blog feed unavailable');
    const feed = await response.json();
    if (!Array.isArray(feed.posts) || feed.posts.length !== 3) throw new Error('Invalid blog feed');
    const cards = feed.posts.map(post => {
      if (!/^https:\/\/blog\.naver\.com\/gilbert61\/\d+$/.test(post.url) || typeof post.title !== 'string' || !/^\d{4}\.\d{2}\.\d{2}$/.test(post.date)) throw new Error('Invalid post');
      const card = document.createElement('a');
      card.href = post.url;
      card.target = '_blank';
      card.rel = 'noopener noreferrer';
      if (typeof post.image === 'string' && /^latest-\d+\.(png|jpg|webp)$/.test(post.image)) {
        const image = document.createElement('img');
        image.className = 'news-background';
        image.src = root + post.image;
        image.alt = '';
        image.loading = 'lazy';
        card.append(image);
      }
      const date = document.createElement('small');
      date.textContent = `블로그 소식 · ${post.date}`;
      const title = document.createElement('h3');
      title.textContent = post.title;
      const read = document.createElement('span');
      read.textContent = '블로그에서 읽기 ↗';
      card.append(date, title, read);
      return card;
    });
    const grid = document.querySelector('.news-grid');
    // Do not replace a card while someone is navigating it with the keyboard.
    if (grid && !grid.contains(document.activeElement)) grid.replaceChildren(...cards);
  } catch {
    // Keep the last available cards when the feed or network is unavailable.
  }
}
(async () => {
  await refreshBlogCards('blog/');
  await refreshBlogCards(blogDataRoot);
})();
setInterval(() => refreshBlogCards(blogDataRoot), 900000);
