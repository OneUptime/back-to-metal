/* The site's one script.
 *
 * There used to be three: a core that owned storage and the rule for what came
 * next, a hands file for the jump box and the keyboard bindings, and a
 * dependency planner. The rail, the spine, the jump box and the planner are
 * gone, and with twenty Moves in a fixed order there is nothing left to
 * compute - so what remains is a tick box, a running total and a link you can
 * send to somebody.
 *
 * Everything here is enhancement. Every control it touches is a checkbox, a
 * link or a button the build rendered, and every figure it paints was already
 * rendered correct for a reader who has ticked nothing - which is every reader
 * on a first visit. With scripting off the site is legible, correct and
 * navigable; it just cannot remember.
 */
(() => {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  const DONE = 'btm.done.v1';   /* Move numbers ticked */
  const STEPS = 'btm.steps.v1'; /* runbook steps ticked, by Move number */
  const KIT = 'btm.kit.v1';     /* kit rows ticked, by shelf and position */
  const WEEK = 5;               /* working days, as roadmap.py counts them */

  /* Storage throws outright in a private window and in some embedded viewers,
     so every read and every write is guarded. A checklist that cannot remember
     is still a perfectly good checklist. */
  const read = (k, d) => {
    try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); }
    catch (e) { return d; }
  };
  const write = (k, v) => {
    try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* not persisted */ }
  };

  /* [num, page basename, title, effort days, was, now] - written by site.py, so
     the arithmetic below runs off the numbers the build computed rather than a
     second set typed in here. The basename carries its number, so a link is
     whatever prefix the page already uses plus `row[1] + '.html'`. */
  const MOVES = window.BTM_MOVES || [];
  const NUMS = new Set(MOVES.map(r => r[0]));
  /* An earlier edition had a hundred and twenty-two Moves and wrote its ticks
     under this same key. Anything that is not a Move any more is dropped rather
     than counted, so an old reader's checklist reads zero instead of nonsense. */
  const known = n => !NUMS.size || NUMS.has(n);
  const byNum = (a, b) => a - b;

  const done = () => new Set(read(DONE, []).filter(known));

  /* Read, change one Move, write back - never a snapshot taken when the page
     loaded. A reader with the checklist open beside a Move page would otherwise
     lose whichever of the two tabs wrote second. */
  const setDone = (n, on) => {
    const s = done();
    on ? s.add(n) : s.delete(n);
    write(DONE, [...s].sort(byNum));
  };

  /* A plan is a link you can send to whoever has to approve it, so the ticked
     set travels in the address bar and is taken as read on arrival. Only digits
     and commas are accepted, and every number is checked against the book. */
  const shared = /^#done=([\d,]*)$/.exec(location.hash);
  if (shared) write(DONE, shared[1].split(',').filter(known).sort(byNum));

  /* ---- the next line, in the header of every page ----------------------- */
  const nextLink = $('#next');

  const paintNext = d => {
    if (!nextLink || !MOVES.length) return;
    const row = MOVES.find(r => !d.has(r[0]));
    /* Nothing is next once all of them are ticked, and naming the last Move
       again would be a lie the reader can check. */
    nextLink.hidden = !row;
    if (!row) return;
    nextLink.setAttribute('href',
      nextLink.getAttribute('href').replace(/[^/]*$/, row[1] + '.html'));
    $('.next-n', nextLink).textContent = row[0];
    $('.next-t', nextLink).textContent = row[2];
  };

  /* ---- the checklist ---------------------------------------------------- */
  const said = $('#ck-said');
  const say = t => { if (said) said.textContent = t; };
  const money = v => '$' + Math.round(v).toLocaleString('en-GB');

  /* The build owns the crew size, so it is read back off the label rather than
     kept as a second copy of DEFAULT_CREW here. */
  const weeksEl = $('#s-weeks');
  const weeksLbl = weeksEl && weeksEl.nextElementSibling;
  const crew = Math.max(1, +((weeksLbl && weeksLbl.textContent.match(/\d+/)) || [2])[0]);

  /* This slot counts LABOUR, not the calendar. Ticking a Move takes somebody's
     days off the pile; it does not shorten a circuit order or a thirty-day
     window, and the elapsed figure on the front page is mostly made of those.
     The build renders the same arithmetic for zero ticks and says so in the
     label, so this only ever continues a sum that is already on the page. */
  const paintSummary = d => {
    if (!$('#s-left')) return;
    const left = MOVES.filter(r => !d.has(r[0]));
    const days = left.reduce((a, r) => a + r[3], 0);
    /* A Move with an em dash in either half of its trade states no saving, and
       the index carries null rather than zero for it - so this counts the same
       Moves totals() counts in the build, and reaches $0 at twenty ticks. */
    const save = left.reduce(
      (a, r) => a + (r[4] === null || r[5] === null ? 0 : r[4] - r[5]), 0);
    $('#s-left').textContent = left.length;
    $('#s-days').textContent = Math.round(days);
    $('#s-weeks').textContent = Math.round(days / crew / WEEK);
    $('#s-save').textContent = money(save);
  };

  const bar = $('#prog-bar');
  const pDone = $('#p-done');

  const paint = () => {
    const d = done();
    for (const box of $$('input.ck-box[data-n]')) {
      box.checked = d.has(box.dataset.n);
      const row = box.closest('.ck');
      if (row) row.classList.toggle('done', box.checked);
    }
    if (bar) for (const seg of $$('i[data-n]', bar)) {
      seg.classList.toggle('on', d.has(seg.dataset.n));
    }
    if (pDone) pDone.textContent = d.size;
    paintSummary(d);
    paintNext(d);
  };

  /* One listener for both kinds of box, on every page that has either. */
  document.addEventListener('change', e => {
    const box = e.target;
    if (!box.matches) return;
    if (box.matches('input.ck-box[data-n]')) {
      setDone(box.dataset.n, box.checked);
      paint();
    } else if (box.matches('input.kt-box[data-kit]')) {
      const cur = new Set(read(KIT, []));
      box.checked ? cur.add(box.dataset.kit) : cur.delete(box.dataset.kit);
      write(KIT, [...cur]);
    }
  });

  const reset = $('#ck-reset');
  if (reset) reset.addEventListener('click', () => {
    write(DONE, []);
    /* A cleared list under a link that still carries ticks would reinstate them
       on the next reload. */
    if (location.hash) {
      try { history.replaceState(null, '', location.pathname + location.search); }
      catch (e) { /* the ticks are gone either way */ }
    }
    paint();
    say('Every tick cleared.');
  });

  const share = $('#ck-share');
  if (share) share.addEventListener('click', () => {
    const d = [...done()].sort(byNum);
    const url = location.href.replace(/#.*$/, '') + (d.length ? '#done=' + d.join(',') : '');
    /* The address bar is the copy of record. Whatever the clipboard does or
       refuses to do, the link is on screen to be copied by hand. */
    try { history.replaceState(null, '', url); } catch (e) { /* file:// refuses */ }
    const byHand = () => {
      say(url);
      try {
        const r = document.createRange();
        r.selectNodeContents(said);
        const sel = getSelection();
        sel.removeAllRanges();
        sel.addRange(r);
      } catch (e) { /* the address bar still has it */ }
    };
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(() => say('Link copied.'), byHand);
      } else byHand();
    } catch (e) { byHand(); }
  });

  /* ---- the runbook, on a Move page -------------------------------------- */
  const steps = $('ol.steps[data-n]');
  if (steps) {
    const n = steps.dataset.n;
    /* The build renders a step number, not a control, because a runbook has to
       read as a runbook on paper and with no script. It becomes a button only
       once there is something to press it with. */
    for (const sn of $$('.sn', steps)) {
      sn.setAttribute('role', 'button');
      sn.setAttribute('tabindex', '0');
      sn.setAttribute('aria-label', `Mark step ${sn.dataset.step} done`);
    }
    const paintSteps = () => {
      const on = new Set(read(STEPS, {})[n] || []);
      for (const sn of $$('.sn', steps)) {
        const lit = on.has(+sn.dataset.step);
        sn.closest('li').classList.toggle('done', lit);
        sn.setAttribute('aria-pressed', lit ? 'true' : 'false');
      }
    };
    const toggle = sn => {
      const all = read(STEPS, {});
      const on = new Set(all[n] || []);
      const i = +sn.dataset.step;
      on.has(i) ? on.delete(i) : on.add(i);
      if (on.size) all[n] = [...on].sort(byNum); else delete all[n];
      write(STEPS, all);
      paintSteps();
    };
    steps.addEventListener('click', e => {
      const sn = e.target.closest('.sn');
      if (sn) toggle(sn);
    });
    steps.addEventListener('keydown', e => {
      const sn = e.target.closest('.sn');
      if (sn && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); toggle(sn); }
    });
    paintSteps();
  }

  /* ---- the kit, on the safety page -------------------------------------- */
  const kitOn = new Set(read(KIT, []));
  for (const box of $$('input.kt-box[data-kit]')) box.checked = kitOn.has(box.dataset.kit);

  paint();
})();
