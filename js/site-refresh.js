(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#primary-nav');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (toggle && nav) {
    const closeMenu = () => {
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
      nav.classList.remove('open');
      document.body.classList.remove('nav-open');
      const label = toggle.querySelector('.sr-only');
      if (label) label.textContent = 'Open menu';
    };
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      nav.classList.toggle('open', !open);
      document.body.classList.toggle('nav-open', !open);
      const label = toggle.querySelector('.sr-only');
      if (label) label.textContent = open ? 'Open menu' : 'Close menu';
    });
    nav.addEventListener('click', closeMenu);
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && nav.classList.contains('open')) {
        closeMenu();
        toggle.focus();
      }
      if (event.key === 'Tab' && nav.classList.contains('open')) {
        const links = [...nav.querySelectorAll('a[href]')];
        const last = links[links.length - 1];
        if (event.shiftKey && document.activeElement === toggle) {
          event.preventDefault(); last?.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault(); toggle.focus();
        }
      }
    });
    document.addEventListener('click', event => {
      if (!event.target.closest('.site-header')) closeMenu();
    });
    window.matchMedia('(max-width: 960px)').addEventListener('change', closeMenu);
  }
  document.querySelectorAll('[data-year]').forEach((item) => {
    item.textContent = new Date().getFullYear();
  });

  const mobileQuery = window.matchMedia('(max-width: 680px)');
  const syncDisclosures = () => {
    document.querySelectorAll('.info-disclosure').forEach((item) => {
      if (mobileQuery.matches) item.removeAttribute('open');
      else item.setAttribute('open', '');
    });
  };
  syncDisclosures();
  mobileQuery.addEventListener?.('change', syncDisclosures);

  const mobileCall = document.querySelector('.mobile-call');
  const pageIntro = document.querySelector('.hero, .page-hero');
  if (mobileCall && pageIntro && 'IntersectionObserver' in window) {
    const callObserver = new IntersectionObserver(([entry]) => {
      mobileCall.classList.toggle('is-visible', !entry.isIntersecting);
    }, { threshold: 0.1 });
    callObserver.observe(pageIntro);
  }

  const reviewTrack = document.querySelector('.review-track');
  document.querySelectorAll('[data-review-direction]').forEach((button) => {
    button.addEventListener('click', () => {
      const direction = Number(button.dataset.reviewDirection);
      reviewTrack?.scrollBy({ left: direction * reviewTrack.clientWidth * 0.85, behavior: reducedMotion.matches ? 'auto' : 'smooth' });
    });
  });
})();
