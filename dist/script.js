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
