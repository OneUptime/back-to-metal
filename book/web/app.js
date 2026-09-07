/* The hands.
 *
 * next.js owns the storage, the rule that decides what is next, and the
 * two readouts in the chrome. This file wires up everything a reader can
 * press: the jump box and the keyboard bindings, which are on all 131
 * pages, and then whichever of the page behaviours applies here.
 *
 * Everything below is enhancement. Every control it touches is a real
 * link, a real button or a real checkbox that the build rendered, and the
 * page is legible, correct and navigable before this file runs.
 */
(() => {
  'use strict';

  const B = window.BTM;
  if (!B) return;
  const { $, $$, esc } = B;

  const up = /\/(m|s)\/[^/]*$/.test(location.pathname) ? '../' : '';

  /* ------------------------------------------------------------------ *
   * THE JUMP BOX - on every page
   *
   * A Move had no address before this: 122 pages reachable only by
   * scrolling a list seven thousand pixels long. The corpus arrives in
   * one cached file rather than inlined into every page, this fills the
   * native datalist from it, and a number goes straight to the numeric
   * stub rather than needing a slug table.
   * ------------------------------------------------------------------ */
  const jump = $('#jump'), out = $('#jump-out');
  if (jump && out && B.census().length) {
    const rows = B.census();
    let picked = -1;

    /* The input keeps a native type-ahead of its own, built here rather
       than rendered into all 131 pages. */
    const dl = $('#moves-list');
    if (dl) dl.innerHTML = rows.map(r =>
      `<option value="${esc(r.n)} ${esc(r.t)}">`).join('');

    const hide = () => { out.hidden = true; out.innerHTML = ''; picked = -1; };

    const match = q => {
      const s = q.trim().toLowerCase();
      if (!s) return [];
      if (/^\d{1,3}$/.test(s)) {
        const exact = rows.filter(r => r.n === s.padStart(2, '0') || r.n === s);
        if (exact.length) return exact;
      }
      return rows.filter(r => (r.n + ' ' + r.t).toLowerCase().includes(s)).slice(0, 8);
    };

    const paint = () => {
      const hits = match(jump.value);
      if (!jump.value.trim()) return hide();
      out.hidden = false;
      picked = hits.length ? 0 : -1;
      out.innerHTML = hits.length
        ? hits.map((r, i) => `<a class="${i ? '' : 'on'}" href="${up}m/${r.slug}.html">`
          + `<i>${esc(r.n)}</i><span>${esc(r.t)}</span></a>`).join('')
        : '<p>No Move matches that. The checklist has all of them.</p>';
    };

    const move = d => {
      const links = $$('a', out);
      if (!links.length) return;
      links[Math.max(picked, 0)].classList.remove('on');
      picked = (picked + d + links.length) % links.length;
      links[picked].classList.add('on');
      links[picked].scrollIntoView({ block: 'nearest' });
    };

    jump.addEventListener('input', paint);
    jump.addEventListener('focus', () => { if (jump.value) paint(); });
    jump.addEventListener('keydown', e => {
      if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
      else if (e.key === 'Escape') { hide(); jump.blur(); }
      else if (e.key === 'Enter') {
        /* Enter never leaves the site. The result list is what it goes to,
           and when nothing matched, the box has already said so - taking
           the reader to a page that does not exist, or to a query string
           nothing reads, is worse than staying put. */
        e.preventDefault();
        const links = $$('a', out);
        if (links.length && picked >= 0) location.href = links[picked].href;
      }
    });
    document.addEventListener('click', e => {
      if (!e.target.closest('.jump')) hide();
    });

    /* `/` is the binding every reader of a technical site already has in
       their fingers. Guarded so it never eats a keystroke meant for a
       field, and never fights a browser or OS shortcut. */
    document.addEventListener('keydown', e => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.target.closest('input,textarea,select,[contenteditable]')) return;
      if (e.key === '/') { e.preventDefault(); jump.focus(); jump.select(); return; }
      if (e.key >= '1' && e.key <= '7') {
        const seg = $(`.rail .r-s[data-stage="${e.key}"]`);
        if (seg) { e.preventDefault(); location.href = seg.href; }
        return;
      }
      /* Turning the page on a Move, from the arrows already in the bar. */
      const rel = e.key === 'ArrowLeft' ? 'prev' : e.key === 'ArrowRight' ? 'next' : null;
      if (rel) {
        const a = $(`.bar-tools .pn[rel="${rel}"]`);
        if (a) location.href = a.href;
      }
    });
  }

  /* ------------------------------------------------------------------ *
   * A MOVE PAGE
   * Tick steps off as you run them, and mark the Move done without
   * navigating away to find its row on another page.
   * ------------------------------------------------------------------ */
  const steps = $('#steps');
  if (steps) {
    const n = steps.dataset.move;
    const all = $$('.step', steps);
    const count = $('#step-count');
    let ticked = new Set(B.read(B.STEPS, {})[n] || []);

    const save = () => {
      const cur = B.read(B.STEPS, {});
      if (ticked.size) cur[n] = [...ticked]; else delete cur[n];
      B.write(B.STEPS, cur);
    };
    all.forEach((li, i) => {
      const o = $('.sdone', li);
      o.setAttribute('role', 'button');
      o.setAttribute('tabindex', '0');
      o.setAttribute('aria-label', `Mark step ${o.textContent} done`);
    });
    const paint = () => {
      all.forEach((li, i) => {
        const on = ticked.has(i);
        li.classList.toggle('done', on);
        $('.sdone', li).setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      if (count) count.textContent = `${ticked.size} of ${all.length} done`;
    };
    const toggle = b => {
      const i = +b.dataset.step;
      ticked.has(i) ? ticked.delete(i) : ticked.add(i);
      save();
      paint();
    };
    steps.addEventListener('click', e => {
      const b = e.target.closest('.sdone');
      if (b) toggle(b);
    });
    steps.addEventListener('keydown', e => {
      const b = e.target.closest('.sdone');
      if (b && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); toggle(b); }
    });
    paint();

    /* The pre-flight boxes, kept under the same key so a half-run Move
       survives a reload - which is the whole point of a runbook you are
       standing in front of a rack with. */
    const pre = $$('.prelist input');
    let pk = new Set(B.read(B.STEPS, {})['pre-' + n] || []);
    pre.forEach((box, i) => {
      box.checked = pk.has(i);
      box.addEventListener('change', () => {
        box.checked ? pk.add(i) : pk.delete(i);
        const cur = B.read(B.STEPS, {});
        if (pk.size) cur['pre-' + n] = [...pk]; else delete cur['pre-' + n];
        B.write(B.STEPS, cur);
      });
    });

    const mark = $('#mv-tick');
    if (mark) {
      const nxt = $('.bar-tools .pn[rel="next"]');
      const paintMark = () => {
        const on = B.done().has(n);
        mark.textContent = on ? `Move ${n} is done` : `Mark ${n} done`;
        mark.classList.toggle('btn-p', on);
        mark.setAttribute('aria-pressed', on ? 'true' : 'false');
        const go = $('#mv-next');
        if (go) go.hidden = !on || !nxt;
      };
      if (nxt) mark.insertAdjacentHTML('afterend',
        ` <a class="btn" id="mv-next" href="${nxt.getAttribute('href')}" hidden>`
        + `Open the next Move</a>`);
      mark.addEventListener('click', () => {
        const on = B.done().has(n);
        B.tick(n, !on);
        B.progress(B.done());
        paintMark();
      });
      paintMark();
    }
  }

  /* ------------------------------------------------------------------ *
   * THE KIT PAGE
   * Forty-six procurement boxes that remembered nothing, on a page whose
   * whole job is to be worked through with a supplier.
   * ------------------------------------------------------------------ */
  const kit = $('#kit') || $('.shelf');
  if (kit && $('.shelf input')) {
    const state = B.read(B.KIT, {});
    const shelves = $$('.shelf');
    const paint = () => shelves.forEach(sh => {
      const boxes = $$('input', sh);
      const c = $('.cnt', sh);
      if (c) c.textContent = `${boxes.filter(b => b.checked).length}/${boxes.length}`;
    });
    shelves.forEach(sh => {
      const key = sh.dataset.kit || '';
      const on = new Set(state[key] || []);
      $$('input', sh).forEach((box, i) => {
        box.checked = on.has(i);
        box.addEventListener('change', () => {
          box.checked ? on.add(i) : on.delete(i);
          const cur = B.read(B.KIT, {});
          if (on.size) cur[key] = [...on]; else delete cur[key];
          B.write(B.KIT, cur);
          paint();
        });
      });
    });
    paint();
    const reset = $('#kit-reset');
    if (reset) reset.addEventListener('click', () => {
      B.drop(B.KIT);
      $$('.shelf input').forEach(b => { b.checked = false; });
      paint();
    });
  }

  /* ------------------------------------------------------------------ *
   * THE FRONT PAGE
   * ------------------------------------------------------------------ */
  let done = B.done();
  let floor = B.floor();
  const tick = (n, on) => { done = B.tick(n, on); };

  /* Two pages write ticks and each links to the other, so having both open
     is the ordinary way to use the site. Every write is a read-modify-write
     against storage rather than a blind replacement of the whole set, and
     each page re-reads when it is woken or written to from another tab -
     otherwise the older tab's snapshot silently undoes the newer one. */
  const wake = repaint => {
    const reread = () => { done = B.done(); floor = B.floor(); repaint(); };
    window.addEventListener('storage', e => {
      if (e.key === B.KEY || e.key === B.FROM || e.key === null) reread();
    });
    window.addEventListener('pageshow', e => { if (e.persisted) reread(); });
  };

  const answer = $('#answer');
  if (answer) {
    const records = B.records() || [];
    let undoable = null;   /* this page-load only, so "undo" is never ambiguous */

    const paint = () => {
      B.answer(records, done, floor);
      B.progress(done);
      B.spine(done);
      const undo = $('#ans-undo');
      undo.hidden = !undoable;
      if (undoable) undo.textContent = `Undo ${undoable}`;
      $$('.route').forEach(r => r.classList.toggle('on', r.dataset.floor === floor));
    };

    $('#ans-tick').addEventListener('click', () => {
      undoable = answer.dataset.n;
      tick(undoable, true);
      paint();
    });

    $('#ans-undo').addEventListener('click', () => {
      if (!undoable) return;
      tick(undoable, false);
      undoable = null;
      paint();
    });

    /* Picking a sentence says which stage you start at. It does not tick
       anything: the Moves below it are somebody else's work or already
       true, not work this reader did, and the count should not claim
       otherwise. It is a button rather than a link, because it does not
       navigate and a link that calls preventDefault lies about that. */
    $$('.route').forEach(a => a.addEventListener('click', () => {
      floor = a.dataset.floor;
      B.write(B.FROM, floor);
      undoable = null;
      paint();
      answer.focus();
      answer.scrollIntoView({ block: 'nearest' });
    }));

    document.addEventListener('click', e => {
      if (!e.target.closest('#ans-restart')) return;
      floor = null;
      B.drop(B.FROM);
      paint();
    });

    wake(paint);
    paint();
  }

  /* ------------------------------------------------------------------ *
   * THE CHECKLIST, AND EVERY STAGE PAGE
   * They render the same row component against the same storage, so
   * ticking on one cannot disagree with the other.
   * ------------------------------------------------------------------ */
  const list = $('ol.ck');
  if (list) {
    const rows = B.rowRecords();
    const stages = $$('.stg[data-stage]');
    const chips = $$('.filters .chip');

    function counts() {
      for (const stg of stages) {
        const li = $$('ol.ck > li', stg);
        if (!li.length) continue;
        const n = li.filter(x => done.has(x.dataset.n)).length;
        const bar = $('.stg-prog .track i', stg);
        const cnt = $('.stg-prog .cnt', stg);
        if (bar) bar.style.setProperty('--f', (100 * n / li.length) + '%');
        if (cnt) cnt.textContent = `${n}/${li.length}`;
        stg.classList.toggle('done', n === li.length);
      }
      /* The rail carries the same figure, on the checklist and on a stage
         page alike. */
      for (const w of $$('.rail .r-w [data-stage]')) {
        const mine = rows.filter(r => String(r.stage) === w.dataset.stage);
        if (!mine.length) continue;
        const n = mine.filter(r => done.has(r.n)).length;
        w.textContent = `${n}/${mine.length}`;
        const bar = $('.track i', w.parentNode);
        if (bar) bar.style.setProperty('--f', (100 * n / mine.length) + '%');
      }
      for (const li of $$('.r-moves li')) {
        li.classList.toggle('done', done.has(li.dataset.n));
      }
    }

    function filter() {
      if (!chips.length) return;
      const want = chips.filter(c => c.dataset.stage && c.getAttribute('aria-pressed') === 'true')
        .map(c => c.dataset.stage);
      const todo = $('.filters .chip[data-todo]');
      const onlyTodo = todo && todo.getAttribute('aria-pressed') === 'true';
      let shown = 0;
      for (const r of rows) {
        const ok = (!want.length || want.includes(String(r.stage)))
          && (!onlyTodo || !done.has(r.n));
        r.li.hidden = !ok;
        if (ok) shown++;
      }
      const filtering = want.length > 0 || onlyTodo;
      for (const stg of stages) {
        const li = $$('ol.ck > li', stg);
        stg.hidden = li.length > 0 && li.every(x => x.hidden);
        /* A stage the reader folded shut stays shut until they filter, at
           which point showing them a closed summary bar and a count of rows
           they cannot see would be a lie. */
        if (filtering && !stg.hidden) stg.open = true;
      }
      const c = $('#ck-count');
      if (c) c.textContent = `${shown} of ${rows.length}`;
    }

    function paint() {
      for (const r of rows) {
        const on = done.has(r.n);
        r.li.classList.toggle('done', on);
        const box = $('input', r.li);
        if (box) box.checked = on;
        /* A Move whose prerequisites are not ticked is marked, not
           disabled - the reader may well know better than the graph does -
           and it is marked only inside the figures strip, which is hidden
           until asked for, and only once something has been ticked. On a
           fresh checklist all but the first Move is waiting on something,
           and a mark on every row is wallpaper rather than a warning. */
        const need = $('.ck-need', r.li);
        if (need) {
          const blocked = done.size > 0 && r.deps.some(
            d => !done.has(d) && !(floor != null && (+d) < (+floor)));
          need.classList.toggle('ck-blocked', blocked && !on);
        }
        r.li.classList.remove('ck-next');
      }
      counts();
      B.progress(done);
      B.spine(done);
      const r = B.sentence(rows, done, floor, up);
      if (r && r.m) {
        const row = rows.find(x => x.n === r.m.n);
        if (row) row.li.classList.add('ck-next');
      }
      filter();
    }

    list.closest('.main').addEventListener('change', e => {
      const box = e.target.closest('input[data-move]');
      if (!box) return;
      tick(box.dataset.move, box.checked);
      paint();
    });

    chips.forEach(c => c.addEventListener('click', () => {
      c.setAttribute('aria-pressed',
        c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
      filter();
    }));

    const fold = $('#ck-fold');
    if (fold) fold.addEventListener('click', () => {
      const anyOpen = stages.some(s => s.open);
      stages.forEach(s => { s.open = !anyOpen; });
      fold.textContent = anyOpen ? 'Expand all' : 'Collapse all';
      B.write(B.OPEN, stages.filter(s => !s.open).map(s => s.dataset.stage));
    });
    /* A fold the reader chose is remembered; a stage they have finished is
       folded for them the first time, because sixty Moves in the page
       should open on the work rather than on Move 01. */
    if (stages.length) {
      const stored = B.read(B.OPEN, null);
      const shut = new Set(stored !== null ? stored : stages.filter(s => {
        const li = $$('ol.ck > li', s);
        return li.length && li.every(x => done.has(x.dataset.n));
      }).map(s => s.dataset.stage));
      stages.forEach(s => { s.open = !shut.has(s.dataset.stage); });
      stages.forEach(s => s.addEventListener('toggle', () => {
        B.write(B.OPEN, stages.filter(x => !x.open).map(x => x.dataset.stage));
      }));
    }

    /* Clearing every tick is not undoable, so it asks once. */
    const reset = $('#ck-reset');
    if (reset) {
      const label = reset.textContent;
      let armed = null;
      reset.addEventListener('click', () => {
        if (!armed) {
          reset.textContent = `Really clear ${done.size} tick${done.size === 1 ? '' : 's'}?`;
          armed = setTimeout(() => { reset.textContent = label; armed = null; }, 5000);
          return;
        }
        clearTimeout(armed); armed = null;
        reset.textContent = label;
        done = new Set(); B.saveDone(done);
        floor = null; B.drop(B.FROM);
        paint();
      });
    }
    const restart = $('#ck-restart');
    if (restart) restart.addEventListener('click', () => {
      floor = null; B.drop(B.FROM);
      paint();
    });

    /* The figures toggle is a checkbox the CSS reads, so it works with no
       script at all; this only remembers the answer between visits. */
    const nums = $('#nums');
    if (nums) {
      nums.checked = !!B.read(B.NUMS, false);
      nums.addEventListener('change', () => B.write(B.NUMS, nums.checked));
    }

    /* Which stage the rows under the cursor belong to. The rail used to
       show seven identical entries with nothing marked on the one page
       where position is the whole question. */
    if (stages.length && 'IntersectionObserver' in window) {
      const seen = new Set();
      const mark = () => {
        const first = stages.find(s => seen.has(s.dataset.stage));
        if (!first) return;
        $$('.rail .r-s').forEach(a =>
          a.classList.toggle('on', a.dataset.stage === first.dataset.stage));
        $$('#spine i').forEach(i =>
          i.classList.toggle('here', i.dataset.stage === first.dataset.stage));
      };
      const io = new IntersectionObserver(es => {
        es.forEach(e => e.isIntersecting
          ? seen.add(e.target.dataset.stage) : seen.delete(e.target.dataset.stage));
        mark();
      }, { rootMargin: '-25% 0px -60% 0px' });
      stages.forEach(s => io.observe(s));
    }

    /* A folded stage is folded on screen, not on paper. */
    const openAll = () => stages.map(d => {
      const was = d.open; d.open = true; return [d, was];
    });
    let snapshot = null;
    window.addEventListener('beforeprint', () => { snapshot = openAll(); });
    window.addEventListener('afterprint', () => {
      if (snapshot) snapshot.forEach(([d, was]) => { d.open = was; });
      snapshot = null;
    });

    wake(paint);
    paint();
  }
})();
