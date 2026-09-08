"""The book as a schedule: what to do, in what order, and roughly when.

The book is already a sequence - Moves are numbered, and every dependency points
at a lower number - so an order exists by construction. What this adds is TIME.
Each Move states its effort in person-days in its own numbers strip; the
dependency graph says what can run alongside what; and from those two facts a
roadmap can be COMPUTED rather than asserted.

That distinction matters. A roadmap somebody typed is a guess that goes stale the
moment a Move is added. This one is derived from the Move files like every other
number in the book, so it cannot drift from them.

Two questions it answers:

  critical_path()   the shortest the migration could possibly take, with unlimited
                    people - the chain of Moves that must happen one after another.
  schedule(n)       when each Move actually lands with `n` people working, using
                    the same greedy list scheduling a delivery manager would do on
                    a whiteboard: at every moment, start the lowest-numbered Move
                    whose prerequisites are finished and for whom somebody is free.

Neither is a promise. Effort figures are estimates and the calendar is not the
constraint anyway - the overlap window, the maintenance windows and the people who
also have day jobs are. The number is here so a reader can argue with it.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse import LAYERS, ORDER
from deps import DEPS

# A five-day week: the schedule is quoted in working weeks because that is how the
# question is asked ("how long will this take?"), not in elapsed days.
WEEK = 5.0


def _days(s):
    """'3 days', '2 weeks', '6 months', '< 1 day' -> a number of working days."""
    if not s or s.strip() in ('—', '-', ''):
        return 0.0
    s = s.strip()
    if s.startswith('<'):
        return 0.5
    # "6 to 12 weeks" is a real answer; take the pessimistic end, because a
    # schedule that quotes the optimistic one is the failure this field exists
    # to prevent.
    mm = re.match(r'(?:[\d.]+\s*(?:to|-|\u2013)\s*)?([\d.]+)\s*(day|week|month)', s)
    if not mm:
        return 0.0
    n = float(mm.group(1))
    return n * {'day': 1, 'week': 5, 'month': 21}[mm.group(2)]


def effort_days(m):
    """Person-days of labour, from the Move's own numbers strip."""
    return _days(m['figures'][4])


def wait_days(m):
    """Calendar days that must pass before a dependent Move can start, over and
    above the labour: a sampling window, a circuit order, an RIR queue, a
    procurement cycle. Nobody is working during it, so it lengthens the
    programme without consuming anybody's time - which is precisely why a
    schedule built from effort alone under-forecasts, and why this is a field
    rather than a footnote."""
    return _days(m['figures'][5]) if len(m['figures']) > 5 else 0.0


def _graph(moves):
    by = {m['num']: m for m in moves}
    days = {m['num']: effort_days(m) for m in moves}
    deps = {m['num']: [d for d in DEPS.get(m['num'], []) if d in by] for m in moves}
    return by, days, deps


def critical_path(moves):
    """Earliest finish for every Move with unlimited people, and the chain that
    sets the total. Book order is a topological order, so one pass suffices."""
    by, days, deps = _graph(moves)
    finish, start, prev = {}, {}, {}
    wait = {m['num']: wait_days(m) for m in moves}
    for m in moves:
        n = m['num']
        s_, p = 0.0, None
        for d in deps[n]:
            if finish[d] > s_:
                s_, p = finish[d], d
        # `finish` is when DEPENDENTS may start, so it carries the wait too
        start[n], finish[n], prev[n] = s_, s_ + days[n] + wait[n], p
    if not finish:
        return {'start': {}, 'finish': {}, 'days': 0.0, 'chain': []}
    end = max(finish, key=lambda n: finish[n])
    chain, cur = [], end
    while cur:
        chain.append(cur)
        cur = prev[cur]
    return {'start': start, 'finish': finish, 'days': finish[end],
            'chain': list(reversed(chain))}


def schedule(moves, workers=2):
    """When each Move lands with `workers` people. Greedy list scheduling: at each
    moment take the lowest-numbered Move whose prerequisites are done and whose
    turn it is. Lowest-numbered rather than longest-first on purpose - the book's
    order is editorial, and a roadmap that reorders it to look efficient is
    answering a question nobody asked."""
    by, days, deps = _graph(moves)
    free = [0.0] * max(1, workers)
    wait = {m['num']: wait_days(m) for m in moves}
    start, finish, busy_until = {}, {}, {}
    for m in moves:                      # book order is already topological
        n = m['num']
        ready = max([finish[d] for d in deps[n]], default=0.0)
        w = min(range(len(free)), key=lambda i: free[i])
        s_ = max(ready, free[w])
        start[n] = s_
        busy_until[n] = s_ + days[n]          # the engineer is free again here
        finish[n] = busy_until[n] + wait[n]   # dependents may start here
        free[w] = busy_until[n]
    total = max(finish.values(), default=0.0)
    busy = sum(days.values())
    labour = max(busy_until.values(), default=0.0)
    return {'start': start, 'finish': finish, 'busy_until': busy_until,
            'days': total, 'weeks': total / WEEK, 'person_days': busy,
            'wait_days': sum(wait.values()),
            # Utilisation is measured against the time people are actually
            # available, not against the calendar, or every week of waiting for
            # a circuit would read as somebody idling.
            'utilisation': (busy / (labour * max(1, workers))) if labour else 0.0}


def stages(moves, sched):
    """The roadmap grouped the way a reader will actually read it: one row per
    Stage, with the window it occupies and what it delivers."""
    out = []
    for k in ORDER:
        rs = [m for m in moves if m['layer'] == k]
        if not rs:
            continue
        s = min(sched['start'][m['num']] for m in rs)
        f = max(sched['finish'][m['num']] for m in rs)
        out.append({
            'layer': k, 'roman': LAYERS[k]['roman'], 'color': LAYERS[k]['color'],
            'first': rs[0]['num'], 'last': rs[-1]['num'], 'count': len(rs),
            'start_day': s, 'end_day': f,
            'start_week': int(s // WEEK) + 1, 'end_week': int((f - 0.01) // WEEK) + 1,
            'person_days': sum(effort_days(m) for m in rs),
            'cutover': sum(m['cutover'] for m in rs),
        })
    return out


def payload(moves, workers=2):
    """Everything the website's roadmap needs, in one object."""
    sc = schedule(moves, workers)
    cp = critical_path(moves)
    return {
        'workers': workers,
        'weeks': sc['weeks'],
        'person_days': sc['person_days'],
        'utilisation': sc['utilisation'],
        'critical_weeks': cp['days'] / WEEK,
        'critical_chain': cp['chain'],
        'stages': stages(moves, sc),
        'moves': {m['num']: {'s': round(sc['start'][m['num']], 2),
                             'f': round(sc['finish'][m['num']], 2),
                             'd': effort_days(m)} for m in moves},
    }


if __name__ == '__main__':
    from parse import load_all
    ms = load_all()
    if not ms:
        sys.exit('roadmap: no Move files yet')
    cp = critical_path(ms)
    print(f'{len(ms)} Moves, {sum(effort_days(m) for m in ms):.0f} person-days of effort')
    print(f'critical path: {cp["days"] / WEEK:.0f} weeks over {len(cp["chain"])} Moves '
          f'({" -> ".join(cp["chain"][:6])}{" -> ..." if len(cp["chain"]) > 6 else ""})')
    print()
    for w in (1, 2, 3):
        s = schedule(ms, w)
        print(f'  {w} engineer{"s" if w > 1 else " "}: {s["weeks"]:5.0f} weeks   '
              f'utilisation {s["utilisation"]:.0%}')
    print()
    for st in stages(ms, schedule(ms, 2)):
        print(f'  {st["roman"]:8s} {st["layer"]:9s} {st["first"]}-{st["last"]}  '
              f'weeks {st["start_week"]:3d}-{st["end_week"]:<3d} '
              f'{st["person_days"]:5.0f} person-days')


# ---------------------------------------------------------------- the drawing
def _lanes(items):
    """Pack blocks into the fewest non-overlapping rows. A Stage's Moves can run
    alongside each other once there is more than one person, so a Stage needs a
    band rather than a line."""
    lanes = []
    for it in items:
        for row in lanes:
            if row[-1]['f'] <= it['s'] + 1e-9:
                row.append(it)
                break
        else:
            lanes.append([it])
    return lanes


def svg(moves, workers=2, w=1180, week=WEEK, href=None):
    """The roadmap as a schedule drawing: weeks across, Stages down.

    Rendered on the server rather than in the browser, so it is in the HTML, it
    prints, it needs no JavaScript, and there is no second implementation of the
    scheduling to disagree with the first. `href` maps a Move to a link, or None
    for a static drawing (the printed book has nowhere to click).
    """
    sc = schedule(moves, workers)
    cp = set(critical_path(moves)['chain'])
    st = stages(moves, sc)
    if not st:
        return ''
    by = {m['num']: m for m in moves}

    total = max(sc['finish'].values(), default=1.0) or 1.0
    weeks = int(total // week) + 1
    L, R, TOP = 104, 16, 30            # left gutter for Stage labels, top for the ruler
    plot = w - L - R
    px = plot / total
    ROW, LANE, GAP = 13.0, 2.0, 11.0

    bands, y = [], TOP
    for s_ in st:
        items = sorted(({'n': m['num'], 's': sc['start'][m['num']],
                         'f': sc['finish'][m['num']], 't': m['title']}
                        for m in moves if m['layer'] == s_['layer']),
                       key=lambda i: (i['s'], int(i['n'])))
        lanes = _lanes(items)
        h = len(lanes) * (ROW + LANE) - LANE
        bands.append((s_, y, h, lanes))
        y += h + GAP
    height = y + 6

    ruler = [f'<line x1="{L}" y1="{TOP - 9}" x2="{w - R}" y2="{TOP - 9}" '
             f'stroke="var(--rule)" stroke-width="1"/>',
             f'<text x="{L - 12}" y="{TOP - 18}" class="rm-axis" '
             f'text-anchor="end">WEEK</text>']
    # The ruler is spaced from the room it has, not from a guess. The previous
    # edition ran to 242 weeks at three engineers, and a fixed step of 4 put 61
    # three-digit labels into 1,060 units of drawing - they overprinted into a
    # grey smear and the axis stopped being readable at all. Twenty Moves does
    # not need the defence, but the drawing should not depend on that.
    LAB = 32.0
    step = next((c for c in (1, 2, 4, 5, 10, 20, 25, 50, 100)
                 if (weeks / c) * LAB <= plot), 100)
    for wk in range(0, weeks + 1, step):
        x = L + wk * week * px
        if x > w - R:
            break
        ruler.append(f'<line x1="{x:.1f}" y1="{TOP - 13}" x2="{x:.1f}" y2="{height - 6}" '
                     f'stroke="var(--rule2)" stroke-width="1"/>')
        ruler.append(f'<text x="{x:.1f}" y="{TOP - 18}" class="rm-wk">{wk}</text>')

    fill = 'var(--c)' if href else None
    body = []
    for s_, top, h, lanes in bands:
        key = LAYERS[s_['layer']]['key']
        body.append(f'<g data-part="{key}">')
        body.append(f'<text x="{L - 12}" y="{top + 10}" class="rm-part" '
                    f'text-anchor="end" fill="{fill or s_["color"]}">{s_["roman"]}</text>')
        body.append(f'<text x="{L - 12}" y="{top + 22}" class="rm-partn" '
                    f'text-anchor="end">{s_["layer"]}</text>')
        for li, lane in enumerate(lanes):
            ly = top + li * (ROW + LANE)
            for it in lane:
                x0 = L + it['s'] * px
                bw = max(it['f'] - it['s'], 0.35) * px
                # The critical path is outlined rather than recoloured: it is a
                # property of a Move, not a different kind of Move.
                #
                # --on-c, not --ink: the token that already means "what reads on
                # top of a Stage fill", so the outline moves with the Stage
                # palette instead of being right for one ground. Against the
                # website's light Stage set an --ink outline measured 2.08:1 on
                # four of the five, and it is an SVG stroke, so nothing checks it.
                edge = ' stroke="var(--on-c)" stroke-width="1.4"' if it['n'] in cp else ''
                label = ''
                if bw > 17:
                    label = (f'<text x="{x0 + 3.5:.1f}" y="{ly + 9.4:.1f}" '
                             f'class="rm-n">{it["n"]}</text>')
                block = (f'<title>{it["n"]} · {it["t"]}</title>'
                         f'<rect x="{x0:.1f}" y="{ly:.1f}" width="{bw:.1f}" '
                         f'height="{ROW}" fill="{fill or s_["color"]}"{edge}/>{label}')
                if href:
                    body.append(f'<a href="{href(by[it["n"]])}">{block}</a>')
                else:
                    body.append(f'<g>{block}</g>')
        body.append('</g>')
    # role="img" is children-presentational: on the web the bars are real
    # links, and declaring the drawing an image prunes every one of them from
    # the accessibility tree while leaving them in the tab order as silent
    # stops. The printed drawing has nothing to click, so there it is an image.
    role = 'img' if href is None else 'group'
    # EVERYTHING IS INSIDE ONE GROUP, and the group exists so the website can
    # wipe the drawing in without clipping the <svg> itself. It matters more
    # than it looks: an IntersectionObserver measures the target's box AFTER
    # its own clip-path, so an element hidden by being clipped to zero width
    # reports an intersection of nothing, is never seen to arrive, and is
    # never revealed. That shipped once. The observer watches the <svg>; the
    # clip belongs to the <g>.
    return (f'<svg class="rm" viewBox="0 0 {w} {height:.0f}" width="100%" '
            f'style="height:auto;display:block" role="{role}" '
            f'aria-label="The roadmap: {len(moves)} Moves across {len(st)} Stages, '
            f'{sc["weeks"]:.0f} weeks with {workers} engineers">'
            f'<g class="rm-in">'
            + ''.join(ruler) + ''.join(body) + '</g></svg>')
