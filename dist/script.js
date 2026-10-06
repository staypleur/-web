const toggle = document.querySelector('.menu');
const nav = document.querySelector('#nav');
toggle.addEventListener('click', () => { const open = toggle.getAttribute('aria-expanded') !== 'true'; toggle.setAttribute('aria-expanded', String(open)); nav.classList.toggle('open', open); });
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => { toggle.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); }));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('open')) { toggle.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); toggle.focus(); } });
