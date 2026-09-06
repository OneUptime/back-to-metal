(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ------------------------------------------------------------------ *
   * The checklist.
   *
   * Progress lives in localStorage, which means it is per-browser and never
   * leaves the machine. That is the right trade for a book: no account, no
   * server, nothing to lose, and it works on a laptop in a datacentre with
   * no signal. Every read and write is guarded, because storage throws
   * outright in a private window and in some embedded viewers, and a
   * checklist that cannot remember is still a perfectly good checklist.
   * ------------------------------------------------------------------ */
  const KEY = 'btm.done.v1';

  const load = () => {
    try { return new Set(JSON.parse(localStorage.getItem(KEY) || '[]')); }
    catch (e) { return new Set(); }
  };
  const save = set => {
    try { localStorage.setItem(KEY, JSON.stringify([...set])); }
    catch (e) { /* private window, or storage disabled: ticks just do not persist */ }
  };

  const list = $('.stg ol.ck');
  if (list) {
    const done = load();
    const items = $$('ol.ck > li');
    const nextEl = $('#now-next'), pctEl = $('#now-pct'), fillEl = $('#now-fill');

    const depsOf = li => (li.dataset.deps || '').split(',').filter(Boolean);

    function paint() {
      /* per-Move state */
      for (const li of items) {
        const n = li.dataset.n;
        const on = done.has(n);
        li.classList.toggle('done', on);
        const box = $('input', li);
        if (box) box.checked = on;
        /* a Move whose prerequisites are not ticked is flagged, not disabled:
           the reader may well know better than the graph does */
        const blocked = depsOf(li).some(d => !done.has(d));
        const need = $('.ck-need', li);
        if (need) need.classList.toggle('ck-blocked', blocked && !on);
      }
      /* per-stage counters */
      for (const stg of $$('.stg[data-stage]')) {
        const li = $$('ol.ck > li', stg);
        if (!li.length) continue;
        const n = li.filter(x => done.has(x.dataset.n)).length;
        const bar = $('.stg-prog .track i', stg);
        const cnt = $('.stg-prog .cnt', stg);
        if (bar) bar.style.width = (100 * n / li.length) + '%';
        if (cnt) cnt.textContent = `${n}/${li.length}`;
        stg.classList.toggle('done', n === li.length);
      }
      /* the headline: how far, and what to do next */
      const total = items.length, n = items.filter(x => done.has(x.dataset.n)).length;
      if (pctEl) pctEl.textContent = `${n} of ${total} done`;
      if (fillEl) fillEl.style.width = (100 * n / total) + '%';
      if (!nextEl) return;
      const ready = items.find(li =>
        !done.has(li.dataset.n) && depsOf(li).every(d => done.has(d)));
      const blockedNext = items.find(li => !done.has(li.dataset.n));
      if (!blockedNext) {
        nextEl.innerHTML = 'Every Move is ticked. The last one closes the cloud account, '
          + 'so if that is done too, you are finished.';
        return;
      }
      const li = ready || blockedNext;
      const stg = li.closest('.stg');
      const stage = stg ? $('.stg-n', stg).textContent : '';
      const doing = stg ? $('.stg-h h2', stg).textContent.toLowerCase() : '';
      const a = $('a[href^="m/"]', li);
      const title = $('.ck-t', li).textContent;
      const num = li.dataset.n;
      nextEl.innerHTML = ready
        ? `Next up, in ${stage.toLowerCase()} &mdash; ${doing}: `
          + `<a href="${a.getAttribute('href')}"><b>${num}</b> ${title}</a>. `
          + `Everything it needs is done.`
        : `Nothing is unblocked. The next Move is `
          + `<a href="${a.getAttribute('href')}"><b>${num}</b> ${title}</a>, `
          + `which needs ${depsOf(li).filter(d => !done.has(d)).join(', ')} first.`;
    }

    list.closest('.main').addEventListener('change', e => {
      const box = e.target.closest('input[data-move]');
      if (!box) return;
      box.checked ? done.add(box.dataset.move) : done.delete(box.dataset.move);
      save(done);
      paint();
    });

    const reset = $('#ck-reset');
    if (reset) reset.addEventListener('click', () => {
      done.clear(); save(done); paint();
    });

    paint();
  }

  /* ---------------- a Move page: tick steps as you run them ---------------- */
  $$('.sdone').forEach(b => b.addEventListener('click', () => {
    b.closest('.step').classList.toggle('done');
  }));
})();
