(() => {
  document.querySelector('[data-print-article]')?.addEventListener('click', () => window.print());
  const cards = Array.from(document.querySelectorAll('[data-article]'));
  if (!cards.length) return;
  const input = document.getElementById('article-search');
  const buttons = Array.from(document.querySelectorAll('[data-topic]'));
  const count = document.getElementById('article-count');
  const empty = document.getElementById('article-empty');
  let topic = 'All articles';
  const update = () => {
    const terms = input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let shown = 0;
    cards.forEach(card => {
      const visible = (topic === 'All articles' || card.dataset.category === topic)
        && terms.every(term => card.dataset.search.includes(term));
      card.hidden = !visible;
      if (visible) shown++;
    });
    count.textContent = shown === cards.length ? `${shown} articles` : `${shown} of ${cards.length} articles`;
    empty.hidden = shown > 0;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.topic === topic)));
  };
  document.querySelector('[data-filter-tools]').hidden = false;
  input.addEventListener('input', update);
  buttons.forEach(button => button.addEventListener('click', () => { topic = button.dataset.topic; update(); }));
  document.querySelector('[data-reset-search]').addEventListener('click', () => {
    topic = 'All articles'; input.value = ''; update(); input.focus();
  });
})();
