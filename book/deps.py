"""Which Moves must be finished before which.

One hand-maintained map that every output renders. The printed book prints
"Needs" at the foot of a Move's setup page and "Unlocks" on the Stage divider;
the website draws the graph and the checklist uses it to order a migration.

Two rules the build enforces:

  * every dependency must be a LOWER-numbered Move. That makes the book readable
    front to back - a reader who has reached Move 14 has, by construction, met
    every prerequisite of Move 14 - and it makes a cycle impossible to express.
  * a dependency must be a real prerequisite, not a thematic neighbour. If Move B
    would work without Move A, they are not related, however much they rhyme.

Keep it minimal: most Moves need one or two. Twenty Moves and twenty-eight
edges is a graph somebody can hold in their head, which is the point.
"""

# move number -> the moves that must be done first
DEPS = {
    # Stage 1 - Decide. A straight line: you cannot inventory a bill you have
    # not read, or price a comparison against an inventory you do not have.
    '02': ['01'],
    '03': ['01', '02'],
    '04': ['02', '03'],

    # Stage 2 - Buy. Deliberately NOT a straight line. The cage and the machines
    # are ordered in parallel, because both have lead times and running them in
    # series adds a month to the programme for no reason.
    '05': ['01', '03'],
    '06': ['02', '05'],
    '07': ['03'],
    '08': ['07'],

    # Stage 3 - Build. Serial, and unavoidably so: nothing here can start before
    # the thing under it exists.
    '09': ['06', '08'],
    '10': ['09'],
    '11': ['10'],
    '12': ['11'],

    # Stage 4 - Move. Postgres needs an object store to back up into, which is
    # why 16 waits on 15 and not just on the cluster.
    '13': ['11', '12'],
    '14': ['13'],
    '15': ['12', '14'],
    '16': ['12', '13', '15'],

    # Stage 5 - Run. The edge is built beside the cloud edge before anything is
    # cut over, and the account is closed only once the pager has been proved.
    '17': ['14', '16'],
    '18': ['17'],
    '19': ['16', '18'],
    '20': ['18', '19'],
}


def needs(num, by_num):
    """The Moves this one depends on, as records, in book order."""
    return [by_num[d] for d in sorted(DEPS.get(num, []), key=int) if d in by_num]


def unlocks(num, by_num):
    """The Moves that name this one as a prerequisite."""
    return [by_num[k] for k, v in sorted(DEPS.items(), key=lambda kv: int(kv[0]))
            if num in v and k in by_num]


def roots(moves):
    """Moves with no prerequisites - the places a reader can start."""
    return [m for m in moves if not DEPS.get(m['num'])]


def plan(selected, by_num):
    """`selected` move numbers plus everything they need, in a valid order.

    Because every dependency is a lower number, book order is already a
    topological order, so this closes the set and sorts it. The checklist on the
    website runs the same function in JavaScript against the same data.
    """
    want, queue = set(), list(selected)
    while queue:
        n = queue.pop()
        if n in want or n not in by_num:
            continue
        want.add(n)
        queue.extend(DEPS.get(n, []))
    return sorted(want, key=int)


def check(moves):
    """Called through the audit: every edge must exist and point backwards."""
    have = {m['num'] for m in moves}
    out = []
    for n, ds in DEPS.items():
        if n not in have:
            out.append(f'deps.py: move {n} does not exist')
            continue
        for d in ds:
            if d not in have:
                out.append(f'deps.py: move {n} needs {d}, which does not exist')
            elif int(d) >= int(n):
                out.append(f'deps.py: move {n} needs {d}, which is not a lower '
                           f'number - the book would not read front to back')
    return out


if __name__ == '__main__':
    edges = sum(len(v) for v in DEPS.values())
    print(f'{len(DEPS)} moves with prerequisites, {edges} edges')
