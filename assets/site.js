/* Shared navigation, local command search, and optional public statistics. */
(() => {
  'use strict';
  const search = document.querySelector('#command-search');
  if (search) {
    let category = 'all';
    const cards = [...document.querySelectorAll('.command-card')];
    const status = document.querySelector('#result-status');
    const empty = document.querySelector('#command-empty');
    search.value = new URLSearchParams(location.search).get('q') || '';
    const filter = () => {
      const words = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      let visible = 0;
      cards.forEach(card => {
        const haystack = `${card.textContent} ${card.dataset.keywords || ''}`.toLowerCase();
        const match = (category === 'all' || card.dataset.category === category) && words.every(w => haystack.includes(w));
        card.hidden = !match; visible += Number(match);
      });
      status.textContent = `${visible} of ${cards.length} entry points${words.length ? ' match your search' : ''}`;
      empty.hidden = visible > 0;
    };
    search.addEventListener('input', filter);
    document.querySelectorAll('.filter-button').forEach(button => button.addEventListener('click', () => {
      category = button.dataset.filter;
      document.querySelectorAll('.filter-button').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      filter();
    }));
    document.querySelectorAll('.copy-command').forEach(button => button.addEventListener('click', async () => {
      try {
        await Promise.race([
          navigator.clipboard.writeText(button.dataset.command),
          new Promise((_, reject) => setTimeout(() => reject(new Error('Clipboard unavailable')), 1500))
        ]);
        button.textContent = 'Copied';
        button.setAttribute('aria-label', `${button.dataset.command} copied`);
        setTimeout(() => { button.textContent = 'Copy command'; }, 1800);
      } catch {
        const command = button.closest('.command-card').querySelector('h2 code');
        const range = document.createRange();
        range.selectNodeContents(command);
        const selection = window.getSelection();
        selection.removeAllRanges(); selection.addRange(range);
        button.textContent = 'Selected — use your Copy action';
        button.setAttribute('aria-label', `${button.dataset.command} selected; use your device's Copy action`);
      }
    }));
    filter();
  }
  const statsStatus = document.querySelector('#stats-status');
  if (statsStatus) {
    const renderRows = (target, rows, nameKey, valueKey) => {
      target.replaceChildren();
      rows.slice(0, 5).forEach(row => {
        if (!row || typeof row[nameKey] !== 'string') return;
        const li = document.createElement('li');
        const name = document.createElement('span');
        const value = document.createElement('span');
        name.textContent = nameKey === 'command_name' ? `/${row[nameKey].replace(/^\//, '')}` : row[nameKey];
        value.textContent = String(row[valueKey] ?? '');
        li.append(name, value); target.append(li);
      });
      if (!target.childElementCount) { const li = document.createElement('li'); li.textContent = 'No activity reported yet.'; target.append(li); }
    };
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 6000);
    fetch('/api/stats', { signal: controller.signal, headers: { Accept: 'application/json' } })
      .then(response => { if (!response.ok) throw new Error('Statistics unavailable'); return response.json(); })
      .then(data => {
        if (!Array.isArray(data.popular_commands) || !Array.isArray(data.station_popularity)) throw new Error('Invalid statistics');
        renderRows(document.querySelector('#popular-commands'), data.popular_commands, 'command_name', 'usage_count');
        renderRows(document.querySelector('#popular-stations'), data.station_popularity, 'station_name', 'listen_time_str');
        statsStatus.textContent = 'Activity feed connected';
      })
      .catch(() => {
        statsStatus.textContent = 'Activity feed unavailable';
        document.querySelectorAll('.stats-placeholder').forEach(p => { p.textContent = 'Public statistics are unavailable right now. You can still explore the guide and play in Discord.'; });
      })
      .finally(() => clearTimeout(timeout));
  }
})();
