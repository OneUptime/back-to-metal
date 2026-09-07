"""Check that every edition clears its target margin, and say what it would take.

Margin here is the share of the list price left after Amazon's cut and the cost of
making the copy — royalty minus printing for the print editions, royalty minus the
delivery fee for Kindle. It is the number that decides whether the book is worth
selling, and on a long colour book it is set almost entirely by the page count.

Every figure this uses is marked UNVERIFIED in book/imprint.py. Confirm them in
KDP's own printing-cost calculator before pricing anything: the conclusions here
are only as good as those inputs.
"""
import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import imprint as IMP

PDF = ROOT / 'dist' / IMP.PDF_NAME
EPUB = ROOT / 'dist' / IMP.EPUB_NAME


def pages():
    if not PDF.exists():
        sys.exit('pricing: build the interior first (make book)')
    return len(re.findall(rb'/Type\s*/Page[^s]', PDF.read_bytes()))


def print_cost(n, ink):
    fixed, per_page = IMP.INK[ink]
    return fixed + per_page * n


def min_list(unit_cost, rate, margin):
    """Cheapest list price at which royalty - unit_cost is `margin` of list.

    rate*L - cost >= margin*L  =>  L >= cost / (rate - margin)
    """
    denom = rate - margin
    if denom <= 0:
        return None
    return unit_cost / denom


def margin_at(list_price, unit_cost, rate):
    return (rate * list_price - unit_cost) / list_price


def row(label, unit_cost, rate, target, listed):
    need = min_list(unit_cost, rate, target)
    got = margin_at(listed, unit_cost, rate) if listed else None
    return {'label': label, 'cost': unit_cost, 'rate': rate, 'need': need,
            'listed': listed, 'margin': got}


def main():
    n = pages()
    target = IMP.MIN_PRINT_MARGIN
    rows, problems, notes = [], [], []

    # ---- can it be printed at all? ------------------------------------------
    # BEFORE ANY MARGIN. KDP will not manufacture outside these bands whatever
    # the arithmetic says, and a margin computed for an edition that cannot be
    # made is a submission rejected after the covers have been drawn. The bands
    # were a comment beside INK for three editions and nothing read them.
    lo, hi = IMP.INK_PAGES[IMP.INK_CHOICE]
    if not (lo <= n <= hi):
        short = lo - n if n < lo else 0
        problems.append(
            f'Paperback ({IMP.INK_CHOICE}): {n} pages is outside KDP\'s {lo}-{hi} band '
            + (f'for this ink - the interior is {short} page{"" if short == 1 else "s"} '
               f'short and CANNOT be printed this way. Either grow it past {lo}, or '
               f'switch INK_CHOICE to premium colour, which prints from '
               f'{IMP.INK_PAGES["premium colour"][0]} pages and costs '
               f'${print_cost(n, "premium colour"):.2f} a copy against '
               f'${print_cost(n, IMP.INK_CHOICE):.2f}. Ink is locked permanently once a '
               f'title is published, so this is not a decision to take twice.'
               if short else 'and cannot be printed this way.'))

    hlo, hhi = IMP.HARDBACK_PAGES
    hardback_printable = hlo <= n <= hhi
    if not hardback_printable:
        problems.append(
            f'Hardback ({IMP.HARDBACK_INK}): {n} pages is outside KDP\'s {hlo}-{hhi} band, '
            f'so there is no hardcover edition to price. It needs {hlo - n} more page'
            f'{"" if hlo - n == 1 else "s"}. This is also why cover.py has no jacket to '
            f'draw: there is no book to wrap.')

    # ---- print editions ----------------------------------------------------
    pb_cost = print_cost(n, IMP.INK_CHOICE)
    rows.append(row(f'Paperback ({IMP.INK_CHOICE})', pb_cost,
                    IMP.PRINT_ROYALTY_RATE, target, IMP.LIST_USD.get('paperback')))

    # The hardcover rate is a property of the trim and the ink, so it can be
    # computed - but only for a page count KDP will actually print.
    hb_cost = (IMP.HARDBACK_PRINT_COST_USD if IMP.HARDBACK_PRINT_COST_USD is not None
               else IMP.HARDBACK_FIXED_USD + IMP.HARDBACK_PER_PAGE_USD * n)
    if hardback_printable:
        rows.append(row(f'Hardback ({IMP.HARDBACK_INK})', hb_cost,
                        IMP.PRINT_ROYALTY_RATE, target, IMP.LIST_USD.get('hardback')))
        notes.append('Hardcover is premium colour only — KDP does not offer standard colour '
                     'for it, so the hardback cannot be made cheaper the way the paperback can.')
    else:
        notes.append(f'Hardback not priced: {n} pages is under the {hlo}-page minimum. At '
                     f'{hlo} pages it would cost ${IMP.HARDBACK_FIXED_USD + IMP.HARDBACK_PER_PAGE_USD * hlo:.2f} '
                     f'a copy.')

    # ---- kindle ------------------------------------------------------------
    if EPUB.exists():
        mb = EPUB.stat().st_size / 1e6
        delivery = mb * IMP.KDP_DELIVERY_PER_MB
        k = row(f'Kindle ({mb:.2f} MB)', delivery, IMP.KINDLE_ROYALTY_RATE,
                IMP.MIN_KINDLE_MARGIN, IMP.KINDLE_LIST_USD)
        rows.append(k)
        lo, hi = IMP.KDP_70_BAND
        if not (lo <= IMP.KINDLE_LIST_USD <= hi):
            problems.append(f'Kindle list ${IMP.KINDLE_LIST_USD:.2f} is outside the '
                            f'{IMP.KINDLE_ROYALTY_RATE:.0%} band ${lo:.2f}-${hi:.2f}; '
                            f'it would earn 35%, not 70%')
        notes.append('KDP charges delivery on the CONVERTED file size, not the EPUB. '
                     'Measured once, on the illustrated 1.0.0 edition: a 4.23 MB EPUB '
                     'converted to 4.56 MB, so this estimate runs slightly optimistic.')
    else:
        notes.append('No EPUB built, so the Kindle edition was not checked (make epub).')

    # ---- report ------------------------------------------------------------
    print(f'pricing: {n} pages, ink "{IMP.INK_CHOICE}", '
          f'target margin {target:.0%} print / {IMP.MIN_KINDLE_MARGIN:.0%} Kindle\n')
    w = max(len(r['label']) for r in rows)
    print(f'  {"edition".ljust(w)}  {"unit cost":>9}  {"KDP min":>8}  '
          f'{"25% at":>8}  {"your list":>9}  {"margin":>7}')
    for r in rows:
        need = f"${r['need']:.2f}" if r['need'] else 'impossible'
        listed = f"${r['listed']:.2f}" if r['listed'] else '—'
        marg = f"{r['margin']:.0%}" if r['margin'] is not None else '—'
        # KDP will not accept a list price below printing cost / royalty rate
        floor = f"${r['cost'] / r['rate']:.2f}"
        print(f"  {r['label'].ljust(w)}  {'$%.2f' % r['cost']:>9}  {floor:>8}  "
              f"{need:>8}  {listed:>9}  {marg:>7}")
    print()

    for r in rows:
        tgt = IMP.MIN_KINDLE_MARGIN if r['label'].startswith('Kindle') else target
        if r['listed'] is None:
            problems.append(f"{r['label']}: no list price set — it needs at least "
                            f"${r['need']:.2f} to clear {tgt:.0%}")
        elif r['rate'] * r['listed'] < r['cost']:
            loss = r['cost'] - r['rate'] * r['listed']
            problems.append(f"{r['label']}: ${r['listed']:.2f} does not cover the ${r['cost']:.2f} "
                            f"it costs to make. Every copy sold LOSES ${loss:.2f}; KDP will not "
                            f"accept the price. It needs ${r['need']:.2f} to clear {tgt:.0%}")
        elif r['margin'] < tgt:
            problems.append(f"{r['label']}: {r['margin']:.0%} margin at ${r['listed']:.2f}, "
                            f"below the {tgt:.0%} target — needs ${r['need']:.2f}")

    # The useful question is not "what is the minimum price" but "can I sell at the
    # price I want", so answer that for each ink the book could be printed on.
    pb_list = IMP.LIST_USD.get('paperback')
    if pb_list:
        print(f'  paperback at ${pb_list:.2f}, by ink:')
        for ink in IMP.INK:
            cost = print_cost(n, ink)
            m = margin_at(pb_list, cost, IMP.PRINT_ROYALTY_RATE)
            per_copy = IMP.PRINT_ROYALTY_RATE * pb_list - cost
            verdict = ('below cost' if per_copy < 0
                       else 'clears target' if m >= target else 'under target')
            mark = '<-- selected' if ink == IMP.INK_CHOICE else ''
            print(f'    {ink:16s} cost ${cost:5.2f}   you keep ${per_copy:6.2f}   '
                  f'{m:>5.0%}   {verdict:14s} {mark}')
        print()

    per_page = IMP.INK[IMP.INK_CHOICE][1]
    notes.append(f'Each page costs ${per_page:.4f} in {IMP.INK_CHOICE}, so every 10 pages '
                 f'cut lowers the minimum list price by about '
                 f'${10 * per_page / (IMP.PRINT_ROYALTY_RATE - target):.2f}.')

    for x in notes:
        print(f'  note: {x}')
    if problems:
        print('\npricing: TARGET NOT MET')
        for x in problems:
            print('  -', x)
        print('\n  Every figure here is unverified — check KDP\'s printing-cost calculator '
              'before treating this as final.')
        sys.exit(1)
    print('\npricing: all editions clear their target margin')


if __name__ == '__main__':
    main()
