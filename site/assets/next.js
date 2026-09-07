/* ------------------------------------------------------------------ *
 * The core: storage, the rule that decides what to do next, and the two
 * readouts every page carries.
 *
 * One selection rule, and every page that shows an answer calls it, so
 * the front page, the checklist and a stage page cannot disagree about
 * which Move is next.
 *
 * The answer is already in the HTML when this runs: the build renders
 * Move 01, which is the correct answer for a reader who has ticked
 * nothing, and that is every reader on a first visit. This file only
 * substitutes a later Move once there is a tick to substitute it from.
 * Nothing here is required for the page to be legible, correct or
 * navigable.
 *
 * On the two pages that paint an answer above the fold it is a classic
 * in-body script, so it runs the moment the elements above it have been
 * parsed and no wrong Move is ever on screen. Everywhere else it is
 * deferred, because the only thing it writes there is a 3px rule.
 * ------------------------------------------------------------------ */
(() => {
  'use strict';

  const KEY = 'btm.done.v1';   /* which Moves are ticked */
  const FROM = 'btm.from.v1';  /* the stage the reader said they start at */
  const NUMS = 'btm.nums.v1';  /* whether the checklist shows every figure */
  const STEPS = 'btm.steps.v1';/* which runbook steps are ticked, by Move */
  const KIT = 'btm.kit.v1';    /* which kit rows are ticked */
  const OPEN = 'btm.open.v1';  /* which checklist stages are folded shut */

  /* Storage throws outright in a private window and in some embedded
     viewers, so every read and write is guarded. A checklist that cannot
     remember is still a perfectly good checklist. */
  const read = (k, d) => {
    try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); }
    catch (e) { return d; }
  };
  const write = (k, v) => {
    try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* not persisted */ }
  };
  const drop = k => { try { localStorage.removeItem(k); } catch (e) { /* nothing to do */ } };

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  /* Quotes too: app.js writes the result of this into an attribute value,
     and a title carrying one would escape it. */
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/"/g, '&quot;');

  const BTM = window.BTM = {
    KEY, FROM, NUMS, STEPS, KIT, OPEN, read, write, drop, $, $$, esc,
    done: () => new Set(read(KEY, [])),
    saveDone: s => write(KEY, [...s]),
    floor: () => read(FROM, null),

    /* Read, change one Move, write back - never write a snapshot taken
       when the page loaded. Four page types tick now, and a reader with
       two of them open would otherwise lose whichever tab wrote second. */
    tick(n, on) {
      const cur = new Set(read(KEY, []));
      on ? cur.add(n) : cur.delete(n);
      write(KEY, [...cur]);
      return cur;
    },

    /* Book order is already a valid execution order - every dependency
       points at a lower-numbered Move - so the next Move is the first one
       that is not ticked and whose prerequisites are all met. One pass,
       no search.

       A floor is what the reader said when they picked a sentence on the
       front page: everything below it belongs to a stage they are past,
       so it is neither offered nor counted against them, and it satisfies
       a dependency the way a tick would. */
    pick(records, done, floor) {
      const before = n => floor != null && (+n) < (+floor);
      const pool = records.filter(r => !done.has(r.n) && !before(r.n));
      if (!pool.length) return { state: 'finished', floor };
      const met = r => r.deps.every(d => done.has(d) || before(d));
      const ready = pool.find(met);
      const m = ready || pool[0];
      const then = pool.filter(r => r !== m).slice(0, 2);
      if (ready) return { state: 'ready', m, then };
      return {
        state: 'blocked', m, then,
        /* numeric, not lexicographic: '99' sorts after '101' as text */
        unmet: m.deps.filter(d => !done.has(d) && !before(d)).sort((a, b) => (+a) - (+b)),
      };
    },

    /* The records the front page and the planner work from, inlined by the
       build so neither makes a request and both work from a file:// URL. */
    records() {
      const el = $('#moves-data');
      if (!el) return null;
      try { return JSON.parse(el.textContent); } catch (e) { return null; }
    },

    /* The corpus, for the jump box. It arrives in its own cached file, so
       on the two pages where this script runs mid-body it may not be here
       yet - which is why nothing above depends on it. */
    census() {
      return (window.BTM_MOVES || []).map(r => ({ n: r[0], slug: r[1], t: r[2] }));
    },

    /* The two readouts in the chrome. The total is stamped on the element
       by the build, so the count is right before anything else loads. */
    progress(done) {
      const pct = $('#now-pct');
      const total = pct ? +pct.dataset.total : 0;
      const n = done.size;
      if (pct && total) pct.textContent = `${n} / ${total}`;
      const restart = $('#ck-restart');
      if (restart) restart.hidden = BTM.floor() == null;
      return { n, total };
    },

    /* Seven segments, one per stage, filled as they are ticked.

       Each segment carries the Move numbers it spans, so this needs nothing
       but the ticks - which matters, because most of the site's pages are a
       single Move and carry no list to count. It used to read zero on all of
       them while the counter three pixels above it read the truth. */
    spine(done) {
      const el = $('#spine');
      if (!el) return;
      for (const seg of $$('i[data-from]', el)) {
        const from = +seg.dataset.from, to = +seg.dataset.to, of = +seg.dataset.n;
        if (!of) continue;
        let n = 0;
        done.forEach(x => { const v = +x; if (v >= from && v <= to) n++; });
        const bar = $('b', seg);
        if (bar) bar.style.setProperty('--f', (100 * Math.min(n, of) / of) + '%');
      }
    },

    /* The front page. Everything it writes, the build wrote first. */
    answer(records, done, floor) {
      const sec = $('#answer');
      if (!sec) return null;
      const r = BTM.pick(records, done, floor);
      const note = $('#ans-note'), where = $('#q-where'), said = $('#ans-said');
      const parts = ['.ans-hd', '.ans-hook', '.ans-facts', '.ans-then', '#ans-open']
        .map(s => $(s, sec)).filter(Boolean);

      if (r.state === 'finished') {
        parts.forEach(e => { e.hidden = true; });
        $('#ans-tick').hidden = true;
        $('.ans-k', sec).textContent = 'Finished';
        note.hidden = false;
        note.innerHTML = esc(BTM.finished(records, floor))
          + (floor != null
            ? ' <button class="lnk" type="button" id="ans-restart">Start from the beginning</button>' : '');
        if (where) where.textContent = '';
        if (said) said.textContent = 'Every Move you were asked about is ticked.';
        return r;
      }

      const m = r.m;
      parts.forEach(e => { e.hidden = false; });
      sec.dataset.part = m.p;
      sec.dataset.n = m.n;
      $('.ans-k', sec).textContent = `Stage ${m.stage} · ${m.doing}`;
      $('#ans-n').textContent = m.n;
      const t = $('#ans-a');
      t.textContent = m.t;
      t.href = 'm/' + m.slug + '.html';
      $('#ans-hook').textContent = m.hook;
      $('#ans-facts').innerHTML = BTM.facts(m);
      const then = $('.ans-then', sec);
      if (then) {
        then.innerHTML = r.then.length
          ? 'Then ' + r.then.map(x =>
            `<a href="m/${x.slug}.html">${x.n} ${esc(x.t)}</a>`).join(', ') + '.'
          : '';
        then.hidden = !r.then.length;
      }
      const open = $('#ans-open');
      open.href = 'm/' + m.slug + '.html';
      open.textContent = `Open Move ${m.n}`;
      const all = $('#ans-all');
      if (all) all.href = `checklist.html#m-${m.n}`;
      const tick = $('#ans-tick');
      tick.hidden = false;
      tick.textContent = `Mark ${m.n} done`;
      if (where) where.textContent = `Stage ${m.stage} of ${BTM.stageCount(records)}`;
      /* The whole purpose of the page changes under the reader when they
         tick, and a screen reader was never told. */
      if (said) said.textContent = `Next: Move ${m.n}, ${m.t}`;

      const lines = [];
      if (r.state === 'blocked') {
        lines.push(`Nothing is unblocked. ${m.n} needs ${r.unmet.join(', ')} first.`);
      }
      if (floor != null) {
        const f = records.find(x => x.n === floor);
        const i = records.indexOf(f);
        if (f && i > 0) {
          lines.push(`You said you are at stage ${f.stage}, so Moves ${records[0].n}`
            + `–${records[i - 1].n} are not being asked about.`);
        }
      }
      note.innerHTML = lines.length
        ? esc(lines.join(' ')) + (floor != null
          ? ' <button class="lnk" type="button" id="ans-restart">Start from the beginning</button>' : '')
        : '';
      note.hidden = !lines.length;
      return r;
    },

    facts(m) {
      const bits = [['cutover', m.cut + ' min'], ['risk', m.r],
                    ['effort', m.effs],
                    ['back out', m.oneway ? 'Cannot be undone' : m.rev]];
      if (m.wait && m.wait !== '—') bits.push(['then wait', m.wait]);
      return bits.map(([k, v]) => `<span><i>${esc(k)}</i>${esc(v)}</span>`).join('');
    },

    stageCount(records) {
      return new Set(records.map(r => r.stage)).size;
    },

    /* A reader who said they start at stage 3 and has ticked everything
       from there has finished what they were asked about, which is not the
       same claim as finishing the book. Saying the second while earlier
       Moves sit unticked is the one way this page could lie to somebody. */
    finished(records, floor) {
      const f = floor != null && records.find(x => x.n === floor);
      return f
        ? `Everything from stage ${f.stage} on is ticked. The last Move closes the `
          + `cloud account, so if that is done too, you are out.`
        : 'Every Move is ticked. The last one closes the cloud account, so if that '
          + 'is done too, you are out.';
    },

    /* The rows a list page works from, read back off the markup it already
       renders rather than shipping the payload twice. Used by the
       checklist and by each stage page, which render the same component. */
    rowRecords() {
      return $$('ol.ck > li').map(li => {
        const a = $('a.ck-t', li);
        return {
          n: li.dataset.n,
          deps: (li.dataset.deps || '').split(',').filter(Boolean),
          slug: a.getAttribute('href').replace(/^(\.\.\/)?m\//, '').replace(/\.html$/, ''),
          t: a.textContent,
          stage: +li.dataset.stage,
          li,
        };
      });
    },

    /* The checklist's one-line version of the same answer. */
    sentence(records, done, floor, up = '') {
      const el = $('#now-next');
      if (!el) return null;
      const r = BTM.pick(records, done, floor);
      if (r.state === 'finished') {
        el.textContent = BTM.finished(records, floor);
        return r;
      }
      const m = r.m;
      const link = `<a href="${up}m/${m.slug}.html"><b>${m.n}</b> ${esc(m.t)}</a>`;
      el.innerHTML = r.state === 'ready'
        ? `Next up: ${link}. Everything it needs is done.`
        : `Nothing is unblocked. The next Move is ${link}, `
          + `which needs ${r.unmet.join(', ')} first.`;
      return r;
    },
  };

  /* ---- first paint ---------------------------------------------------- */
  const done = BTM.done();
  const floor = BTM.floor();
  const records = BTM.records();

  BTM.progress(done);
  BTM.spine(done);

  if (records) {
    /* The front page, and the planner, which carries the same payload. */
    BTM.answer(records, done, floor);
    /* Old bookmarks pointed at #iron ... #watch on this page. The stages
       live on the checklist and on seven pages of their own now, so send
       them somewhere real rather than leaving a link that lands nowhere.
       An explicit list, not "any fragment this page does not have": the
       front page has ids of its own that must not be redirected. */
    const STAGE_KEYS = ['iron', 'site', 'cluster', 'platform', 'data', 'edge', 'watch'];
    const h = location.hash.slice(1);
    if (STAGE_KEYS.includes(h) && !document.getElementById(h)) {
      location.replace('s/' + h + '.html');
    }
  }
  /* The checklist and the stage pages are painted by app.js instead: their
     rows are parsed after this point in the document, and they have
     interaction to wire up anyway. */
})();
