(() => {
  const finder = document.querySelector('[data-area-finder]');
  const select = document.getElementById('visit-city');
  const result = document.getElementById('visit-price');
  if (!finder || !select || !result) return;
  finder.hidden = false;
  select.addEventListener('change', () => {
    const value = select.value;
    const city = select.selectedOptions[0].textContent;
    let price = 'Care comes to you.';
    let detail = 'Select a city to see your visit price.';
    if (value === 'highlands') {
      price = 'Starting at $90';
      detail = 'An individual foot-care visit in Highlands Ranch. Contact Kirsten to confirm your appointment.';
    } else if (['100', '110', '115'].includes(value)) {
      price = `$${value} per visit`;
      detail = `Your individual foot-care visit price in ${city}. Contact Kirsten to arrange a time.`;
    } else if (value === 'nearby' || value === 'other') {
      price = 'Let’s confirm your price.';
      detail = 'Share your city and address with Kirsten for your total visit price. Pricing may vary outside the primary service area.';
    }
    result.querySelector('strong').textContent = price;
    result.querySelector('p').textContent = detail;
  });
})();
