(() => {
  'use strict';

  /* A Move page: tick steps off as you run them. This is above the guard below
     because it is the only thing on this page that needs a script, and it needs
     nothing else - a Move page does not load next.js and never should. */
  document.querySelectorAll('.sdone').forEach(b => b.addEventListener('click', () => {
    b.closest('.step').classList.toggle('done');
  }));

  const B = window.BTM;
  if (!B) return;
  const { $, $$ } = B;

  /* ------------------------------------------------------------------ *
   * Progress lives in localStorage, which means it is per-browser and never
   * leaves the machine. That is the right trade for a book: no account, no
   * server, nothing to lose, and it works on a laptop in a datacentre with
   * no signal. next.js owns the reads, the writes and the rule that decides
   * which Move is next; this file is the hands.
   * ------------------------------------------------------------------ */
  let done = B.done();
  let floor = B.floor();

  /* The reader now has two pages that write ticks and each links to the other,
     so having both open is the ordinary way to use the site. Every write is a
     read-modify-write against storage rather than a blind replacement of the
     whole set, and each page re-reads when it is woken or written to from
     another tab - otherwise the older tab's snapshot silently undoes the
     newer tab's ticks. */
  const tick = (n, on) => { done = B.tick(n, on); };
  const wake = repaint => {
    const reread = () => { done = B.done(); floor = B.floor(); repaint(); };
    window.addEventListener('storage', e => {
      if (e.key === B.KEY || e.key === B.FROM || e.key === null) reread();
    });
    window.addEventListener('pageshow', e => { if (e.persisted) reread(); });
  };

  /* ---------------------------- the front page ---------------------------- */
  const answer = $('#answer');
  if (answer) {
    const records = B.records() || [];
    let undoable = null;   /* this page-load only, so "undo" is never ambiguous */

    const paint = () => {
      B.answer(records, done, floor);
      B.progress(records, done, floor);
      const undo = $('#ans-undo');
      undo.hidden = !undoable;
      if (undoable) undo.textContent = `Undo ${undoable}`;
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
       anything: the Moves below it are somebody else's work or already true,
       not work this reader did, and the count should not claim otherwise. */
    $$('.route').forEach(a => a.addEventListener('click', e => {
      e.preventDefault();
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

  /* ---------------------------- the checklist ----------------------------- */
  const list = $('.stg ol.ck');
  if (list) {
    const rows = B.rowRecords();

    function paint() {
      for (const r of rows) {
        const on = done.has(r.n);
        r.li.classList.toggle('done', on);
        const box = $('input', r.li);
        if (box) box.checked = on;
        /* A Move whose prerequisites are not ticked is marked, not disabled -
           the reader may well know better than the graph does - and it is
           marked only inside the figures strip, which is hidden until asked
           for, and only once something has been ticked. On a fresh checklist
           all but the first Move is waiting on something, and a mark on every
           row is wallpaper rather than a warning. */
        const need = $('.ck-need', r.li);
        if (need) {
          const blocked = done.size > 0 && r.deps.some(
            d => !done.has(d) && !(floor != null && (+d) < (+floor)));
          need.classList.toggle('ck-blocked', blocked && !on);
        }
        r.li.classList.remove('ck-next');
      }
      for (const stg of $$('.stg[data-stage]')) {
        const li = $$('ol.ck > li', stg);
        if (!li.length) continue;
        const n = li.filter(x => done.has(x.dataset.n)).length;
        const bar = $('.stg-prog .track i', stg);
        const cnt = $('.stg-prog .cnt', stg);
        if (bar) bar.style.width = (100 * n / li.length) + '%';
        if (cnt) cnt.textContent = `${n}/${li.length}`;
        stg.classList.toggle('done', n === li.length);
        const rail = $(`.rail .r-w[data-stage="${stg.dataset.stage}"]`);
        if (rail) rail.textContent = `${n} of ${li.length} done`;
      }
      const r = B.sentence(rows, done, floor);
      B.progress(rows, done, floor);
      if (r && r.m) {
        const row = rows.find(x => x.n === r.m.n);
        if (row) {
          row.li.classList.add('ck-next');
          const stg = row.li.closest('.stg');
          if (stg && !stg.open) stg.open = true;
        }
      }
    }

    list.closest('.main').addEventListener('change', e => {
      const box = e.target.closest('input[data-move]');
      if (!box) return;
      tick(box.dataset.move, box.checked);
      paint();
    });

    $('#ck-reset').addEventListener('click', () => {
      done = new Set(); B.saveDone(done);
      floor = null; B.drop(B.FROM);
      paint();
    });
    $('#ck-restart').addEventListener('click', () => {
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

    /* A folded stage is folded on screen, not on paper. */
    const openAll = () => $$('details.stg').map(d => {
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
