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

  /* Every count-up in flight, by element. A figure that is repainted while
     its own animation is running - tick a Move with the summary panel on
     screen and this happens - would otherwise have the next frame of a
     nine-hundred-millisecond run to an old number written over the top of
     the new one, and the panel would sit there contradicting the rest of
     the page until something else repainted it. */
  const counting = new Map();

  const stopCount = el => {
    const id = counting.get(el);
    if (id) { cancelAnimationFrame(id); counting.delete(el); }
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
    /* The same guard paintNext has. Without a corpus there is nothing to
       subtract, and subtracting nothing from nothing printed "0 Moves left"
       and "$0 still on the table" over twenty unticked boxes - the opposite
       of the truth, and the central claim of the book. */
    if (!$('#s-left') || !MOVES.length) return;
    const left = MOVES.filter(r => !d.has(r[0]));
    const days = left.reduce((a, r) => a + r[3], 0);
    /* A Move with an em dash in either half of its trade states no saving, and
       the index carries null rather than zero for it - so this counts the same
       Moves totals() counts in the build, and reaches $0 at twenty ticks. */
    const save = left.reduce(
      (a, r) => a + (r[4] === null || r[5] === null ? 0 : r[4] - r[5]), 0);
    for (const [el, v] of [[$('#s-left'), left.length],
                           [$('#s-days'), Math.round(days)],
                           [$('#s-weeks'), Math.round(days / crew / WEEK)],
                           [$('#s-save'), money(save)]]) {
      if (!el) continue;
      stopCount(el);
      el.textContent = v;
    }
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
    if (pDone) { stopCount(pDone); pDone.textContent = d.size; }
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
  let repaintSteps = null;
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
      const all = $$('.sn', steps);
      let deep = 0;
      for (const sn of all) {
        const i = +sn.dataset.step;
        const lit = on.has(i);
        if (lit && i > deep) deep = i;
        sn.closest('li').classList.toggle('done', lit);
        sn.setAttribute('aria-pressed', lit ? 'true' : 'false');
      }
      /* How far down the runbook's hairline the Stage colour has got. It
         tracks the DEEPEST step ticked rather than the count, because the
         rule is a position in the job and not a percentage of it: a reader
         who ticked steps 1, 2 and 5 is at 5. */
      steps.style.setProperty('--done', all.length ? deep / all.length : 0);
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
    repaintSteps = paintSteps;
  }

  /* ---- the kit, on the safety page -------------------------------------- */
  const kitOn = new Set(read(KIT, []));
  for (const box of $$('input.kt-box[data-kit]')) box.checked = kitOn.has(box.dataset.kit);

  paint();

  /* ==================================================================
     MOTION
     ==================================================================
     None of this is load-bearing. Every figure it animates is already
     rendered correct in the HTML, and every element it reveals is
     already in the document at its final position.

     The failsafe is the point. Each page's <head> puts `rise` on the
     root element and arms a timer to take it off again; the stylesheet
     hides the revealable things only while that class is on. So if this
     file 404s, arrives corrupt or throws before this line, the timer
     fires and the page is a page, with nothing hidden and nothing lost.
     Clearing that timer is the first thing done here, and it is the
     only thing that earns this module the right to hide anything.
     ================================================================== */
  const root = document.documentElement;
  clearTimeout(window.BTM_RISE_T);

  /* Asked once, and asked again if the reader changes it mid-visit. A
     reader who has said they do not want motion gets the finished page
     immediately: nothing hidden, nothing counted up, nothing swept. */
  const still = matchMedia('(prefers-reduced-motion: reduce)');

  /* THE LIST THE BUILD WROTE. It is the same string site.py used to
     write the hiding rule into the stylesheet, so the two cannot
     disagree - which they could, and did, while this file kept a copy.
     If it is missing, the corpus script did not load, and the honest
     thing is to reveal everything rather than to observe a list that
     is not the one doing the hiding. */
  const RISE = window.BTM_RISE_SEL || '';

  /* One shot, and then it stops watching. A reveal that re-ran on the
     way back up the page would be a page that never settles. */
  const show = el => {
    el.classList.add('in');
    el.style.transitionDelay = '';
  };

  const armRise = () => {
    if (!RISE || still.matches || !('IntersectionObserver' in window)) {
      root.classList.remove('rise');
      return;
    }
    /* FOCUS OUTRUNS THE OBSERVER. The reveal deliberately holds back
       anything in the bottom eight per cent of the window, which is right
       for scrolling and wrong for the Tab key: a keyboard reader moving down
       the checklist reaches a row that is still at opacity 0, the focus ring
       is invisible, and the next Space ticks a Move they cannot see. Anything
       focus lands inside is shown at once and without a delay - it is not
       arriving, it has been asked for. */
    document.addEventListener('focusin', e => {
      const el = e.target && e.target.closest && e.target.closest(RISE);
      if (el && !el.classList.contains('in')) {
        el.style.transitionDelay = '0s';
        show(el);
      }
    });
    const io = new IntersectionObserver((entries, obs) => {
      /* ALREADY PAST. An observer only ever reports what is on screen,
         and a browser restoring a scroll position - or a link with a
         fragment in it - lands the reader halfway down a document whose
         top half has never intersected anything and never will. Those
         elements are shown at once and without a delay: they are not
         arriving, they are already here, and animating them would be
         animating something the reader has scrolled back to rather than
         towards. This is the branch that stops a reload leaving the top
         of a page blank. */
      const past = [], arriving = [];
      for (const e of entries) {
        if (e.isIntersecting) arriving.push(e);
        else if (e.boundingClientRect.bottom <= 0) past.push(e);
      }
      for (const e of past) {
        e.target.style.transitionDelay = '0s';
        show(e.target);
        obs.unobserve(e.target);
      }
      /* Everything that crossed the line in this frame, in document
         order, so a list of twenty Moves arrives as a list rather than
         as twenty things that happened at once. The stagger is capped:
         past about a fifth of a second the reader is waiting rather
         than watching. */
      arriving.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)
        .forEach((e, i) => {
          e.target.style.transitionDelay = Math.min(i, 6) * 45 + 'ms';
          show(e.target);
          obs.unobserve(e.target);
        });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.01 });
    for (const el of $$(RISE)) io.observe(el);
  };

  /* ---- the figures count up --------------------------------------------
     Only the ones the build wrote, and only once. The text is parsed
     rather than re-derived, so a number this file has never heard of -
     a currency, a percentage, a bare count - still counts. Whatever
     cannot be parsed is left exactly as it was rendered. */
  const NUMBER = /^(\D*?)([\d][\d,]*)(\D*)$/;

  const countUp = el => {
    const m = NUMBER.exec(el.textContent.trim());
    if (!m) return;
    const [, pre, digits, post] = m;
    const end = +digits.replace(/,/g, '');
    /* Under about twenty there is nothing to watch, and a two-frame
       flicker on "20 Moves" reads as a fault rather than as motion. */
    if (!isFinite(end) || end < 20) return;
    const grouped = digits.includes(',');
    const t0 = performance.now();
    const DUR = 900;
    let wrote = el.textContent;
    const frame = now => {
      /* If anything else has written to this element since the last frame,
         the animation has been overtaken and must not write again. */
      if (el.textContent !== wrote) { counting.delete(el); return; }
      const t = Math.min(1, (now - t0) / DUR);
      /* Fast, then a long settle: the shape of a mechanical counter
         coming to rest, not a linear sweep. */
      const v = Math.round(end * (1 - Math.pow(1 - t, 4)));
      wrote = pre + (grouped ? v.toLocaleString('en-GB') : v) + post;
      el.textContent = wrote;
      if (t < 1) counting.set(el, requestAnimationFrame(frame));
      else counting.delete(el);
    };
    stopCount(el);
    counting.set(el, requestAnimationFrame(frame));
  };

  const armCounts = () => {
    const figs = $$('.fig-n,.summary .sum b,.prog b');
    if (!figs.length) return;
    if (still.matches || !('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver((entries, obs) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        obs.unobserve(e.target);
        countUp(e.target);
      }
    }, { threshold: 0.5 });
    for (const f of figs) io.observe(f);
  };

  /* ---- how far down the page, in the header's own rule -------------------
     A hairline the width of the window, and the class that lets the
     header shrink once the masthead is behind it. One listener, one
     frame at a time, and no layout read outside it. */
  const rail = $('#rail');
  let ticking = false;

  /* WHERE A HASH LANDS. The header is sticky, so an anchor scrolled to the top
     of the document lands underneath it. `--anchor` in the stylesheet is a
     guess at its height, and a guess is wrong the moment the nav wraps to two
     rows - which it does at six items, and on every phone. Measured here and
     written back, so the offset is whatever the header actually is. */
  const topbar = $('.bar');
  const measureAnchor = () => {
    if (!topbar) return;
    const h = Math.round(topbar.getBoundingClientRect().height);
    if (h) root.style.setProperty('--anchor', (h + 16) + 'px');
  };

  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      const y = window.scrollY || 0;
      const run = Math.max(1, document.documentElement.scrollHeight - innerHeight);
      if (rail) rail.style.setProperty('--at', Math.min(1, y / run));
      root.classList.toggle('scrolled', y > 24);
    });
  };

  /* ---- put it all on ------------------------------------------------------ */
  const arm = () => {
    if (still.matches) {
      root.classList.remove('rise');
      return;
    }
    armRise();
    armCounts();
  };

  arm();
  measureAnchor();
  addEventListener('resize', measureAnchor, { passive: true });
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* BACK IS THE COMMONEST JOURNEY ON THIS SITE: open the checklist, follow a
     Move, tick it at the foot of its page, press Back. A restored page - from
     the back/forward cache or not - is not re-executed, so the checklist came
     back with the row struck through and counted, and its tick box empty.
     Repainting on pageshow re-reads storage and makes the two agree. */
  addEventListener('pageshow', () => {
    paint();
    if (typeof repaintSteps === 'function') repaintSteps();
  });

  /* A reader who turns motion off mid-visit gets the settled page, and
     one who turns it on does not get a page that suddenly hides itself. */
  const listen = still.addEventListener ? still.addEventListener.bind(still, 'change')
    : still.addListener && still.addListener.bind(still);
  if (listen) listen(() => { if (still.matches) root.classList.remove('rise'); });
})();
