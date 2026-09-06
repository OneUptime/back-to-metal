/* The migration planner.
 *
 * Tick the Moves you need; this closes the dependency set, orders it, and totals
 * the downtime, the effort and the saving. It runs the same closure the book's
 * deps.py runs, against the same data: because every dependency is a
 * lower-numbered Move, book order is already a safe execution order, so the
 * "sort" is a sort and not a topological search.
 *
 * The selection lives in the address bar, so a plan is a link you can send to
 * the person who has to approve it.
 */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const picker = $('.picker');
  if (!picker) return;

  const out = {
    empty: $('#p-empty'), sum: $('#p-sum'), order: $('#p-order'), note: $('#p-note'),
    count: $('#p-count'), cut: $('#p-cut'), weeks: $('#p-weeks'),
    save: $('#p-save'),
  };
  let MOVES = [], BY = {};
  const chosen = new Set();

  /* Effort arrives already in days from the build, so the planner and the
     roadmap cannot disagree about what a Move costs. */
  const WEEK = 5, CREW = 3;

  /* The same greedy list schedule the roadmap draws: lowest-numbered ready Move
     to the first free pair of hands. Book order is topological, so one pass. */
  function weeksFor(nums) {
    const free = new Array(CREW).fill(0), finish = {};
    let end = 0;
    for (const n of nums) {
      const m = BY[n]; if (!m) continue;
      const ready = (m.deps || []).reduce((a, d) => Math.max(a, finish[d] || 0), 0);
      let w = 0;
      for (let i = 1; i < free.length; i++) if (free[i] < free[w]) w = i;
      const s = Math.max(ready, free[w]);
      finish[n] = s + (m.eff || 0);
      free[w] = finish[n];
      if (finish[n] > end) end = finish[n];
    }
    return end / WEEK;
  }
  const money = v => v >= 1000 ? `$${Math.round(v / 1000)}k` : `$${Math.round(v)}`;

  function close(sel) {
    const want = new Set(), queue = [...sel];
    while (queue.length) {
      const n = queue.pop();
      if (want.has(n) || !BY[n]) continue;
      want.add(n);
      (BY[n].deps || []).forEach(d => queue.push(d));
    }
    return [...want].sort();
  }

  function render() {
    const full = close(chosen);
    out.empty.hidden = full.length > 0;
    out.sum.hidden = full.length === 0;
    out.note.hidden = full.length === chosen.size || full.length === 0;

    let cut = 0, save = 0;
    out.order.innerHTML = full.map(n => {
      const m = BY[n];
      cut += m.cut;
      if (m.was != null && m.now != null) save += m.was - m.now;
      const pulled = chosen.has(n) ? '' : ' class="pulled"';
      return `<li${pulled}><i style="color:${m.c}">${m.n}</i>` +
             `<a href="m/${m.slug}.html">${m.t}</a></li>`;
    }).join('');

    out.count.textContent = full.length;
    out.cut.textContent = cut;
    out.weeks.textContent = Math.max(1, Math.round(weeksFor(full)));
    out.save.textContent = money(save);

    const q = full.length ? '?m=' + [...chosen].sort().join(',') : location.pathname;
    history.replaceState(null, '', full.length ? q : location.pathname);
  }

  function setBox(cb, on) {
    cb.checked = on;
    cb.closest('.pk').classList.toggle('on', on);
    on ? chosen.add(cb.value) : chosen.delete(cb.value);
  }

  picker.addEventListener('change', e => {
    if (e.target.matches('input[type=checkbox]')) { setBox(e.target, e.target.checked); render(); }
  });
  $$('[data-all]').forEach(b => b.addEventListener('click', () => {
    const boxes = $$(`.pk[data-layer="${b.dataset.all}"] input`);
    const on = !boxes.every(c => c.checked);
    boxes.forEach(c => setBox(c, on));
    render();
  }));
  $('#p-clear').addEventListener('click', () => {
    $$('.pk input').forEach(c => setBox(c, false));
    render();
  });
  $('#p-print').addEventListener('click', () => window.print());

  fetch('assets/moves.json')
    .then(r => r.json())
    .then(data => {
      MOVES = data;
      BY = Object.fromEntries(data.map(m => [m.n, m]));
      const pre = new URLSearchParams(location.search).get('m');
      if (pre) {
        const want = new Set(pre.split(',').filter(Boolean));
        $$('.pk input').forEach(c => { if (want.has(c.value)) setBox(c, true); });
      }
      render();
    })
    .catch(() => {
      /* The plan is an enhancement, not the content: if the payload cannot be
         fetched (opened from a file:// URL, say) the picker stays usable and
         says so rather than sitting silently broken. */
      out.empty.textContent = 'The planner needs to be served over http to load its data. '
        + 'The Moves themselves work either way.';
    });
})();
