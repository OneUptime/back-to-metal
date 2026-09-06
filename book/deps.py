"""Which Moves must be finished before which.

The book's analogue of a recipe book's side-to-main pairings: one hand-maintained
map that both outputs render. The printed book prints "Needs" at the foot of a
Move's setup page and "Unlocks" on the Part divider; the website draws the graph
and the planner uses it to order a migration.

Two rules the build enforces:

  * every dependency must be a LOWER-numbered Move. That makes the book readable
    front to back - a reader who has reached Move 40 has, by construction, met
    every prerequisite of Move 40 - and it makes a cycle impossible to express.
  * a dependency must be a real prerequisite, not a thematic neighbour. If Move B
    would work without Move A, they are not related, however much they rhyme.

Populated from the manifest. Keep it minimal: most Moves need one or two.
"""

# move number -> the moves that must be done first
DEPS = {
    '02': ['01'],
    '03': ['02'],
    '04': ['02'],
    '05': ['04'],
    '06': ['02', '04'],
    '07': ['04', '06'],
    '08': ['07'],
    '09': ['07'],
    '10': ['02', '09'],
    '11': ['03', '05', '06', '07', '10'],
    '12': ['11'],
    '13': ['12'],
    '14': ['07', '13'],
    '15': ['13', '14'],
    '16': ['08', '13'],
    '17': ['11', '13'],
    '18': ['17'],
    '19': ['11', '17'],
    '20': ['14', '15', '16', '18', '19'],
    '22': ['20', '21'],
    '23': ['22'],
    '24': ['22'],
    '25': ['22'],
    '26': ['22'],
    '27': ['22'],
    '28': ['20', '26'],
    '29': ['28'],
    '30': ['28', '29'],
    '31': ['20', '28'],
    '32': ['31'],
    '33': ['31'],
    '34': ['20', '28'],
    '35': ['28', '29'],
    '36': ['31', '32', '33', '34', '35'],
    '37': ['36'],
    '38': ['37'],
    '39': ['11', '24'],
    '40': ['08', '35', '39'],
    '41': ['14', '40'],
    '42': ['37', '39', '41'],
    '43': ['09', '32', '42'],
    '44': ['43'],
    '45': ['12', '13', '44'],
    '46': ['42', '44'],
    '47': ['09', '10', '43'],
    '48': ['09', '35', '43', '47'],
    '49': ['10', '42', '47', '48'],
    '50': ['40', '43'],
    '51': ['03', '42', '43', '47', '50'],
    '52': ['43', '49', '51'],
    '53': ['26', '39', '45'],
    '54': ['49', '53'],
    '55': ['43', '53'],
    '56': ['55'],
    '57': ['48', '56'],
    '58': ['47', '49', '54', '55'],
    '59': ['57', '58'],
    '60': ['44', '46'],
    '61': ['55', '60'],
    '62': ['49', '54'],
    '63': ['49', '54', '62'],
    '64': ['56', '58', '59'],
    '65': ['56', '58', '64'],
    '66': ['65'],
    '67': ['53', '55', '56', '58', '59', '60', '62', '63', '65'],
    '68': ['60', '67'],
    '69': ['05', '47', '67'],
    '70': ['47', '49', '55', '60', '69'],
    '71': ['51', '53'],
    '72': ['51', '53', '71'],
    '73': ['47', '48', '53', '56', '58', '60', '62', '63', '71', '72'],
    '74': ['49', '54', '55', '72', '73'],
    '75': ['42', '73', '74'],
    '76': ['71', '72', '73', '74'],
    '77': ['47', '48', '53', '58', '60', '62', '72'],
    '78': ['47', '48', '53', '70', '72'],
    '79': ['47', '58', '60', '62'],
    '80': ['47', '53', '58', '60', '62'],
    '81': ['58', '60', '62', '73', '79', '80'],
    '82': ['49', '58', '60', '62', '81'],
    '83': ['47', '49', '58', '60', '62', '81', '82'],
    '84': ['49', '54', '55', '60', '62'],
    '85': ['84'],
    '86': ['56', '58', '60', '62', '65', '69', '73', '84', '85'],
    '87': ['49', '54', '58', '60', '62', '84'],
    '88': ['72', '73', '84'],
    '89': ['65', '66', '67', '69', '81', '82', '84', '88'],
    '90': ['86', '89'],
    '91': ['39'],
    '92': ['44', '45', '91'],
    '93': ['26', '53', '91'],
    '94': ['39', '44', '93'],
    '95': ['44', '91'],
    '96': ['12', '45', '95'],
    '97': ['43', '57'],
    '98': ['95', '97'],
    '99': ['98'],
    '100': ['79', '89', '99'],
    '101': ['50', '98'],
    '102': ['62', '99', '100', '101'],
    '103': ['94', '96', '102'],
    '104': ['97', '103'],
    '105': ['103', '104'],
    '106': ['91', '93', '105'],
    '107': ['49', '104'],
    '108': ['43', '51', '52', '62', '65'],
    '109': ['42', '47', '108'],
    '110': ['19', '20', '37'],
    '111': ['49', '62', '110'],
    '112': ['13', '41', '49', '73'],
    '113': ['22', '62', '111'],
    '114': ['49', '50', '62', '63', '113'],
    '115': ['49', '54', '65', '74', '114'],
    '116': ['11', '20', '62', '69', '70', '103'],
    '117': ['59', '109', '110'],
    '118': ['50', '54', '59', '63', '65'],
    '119': ['30', '38', '110', '118'],
    '120': ['19', '20', '28', '93', '112', '113', '116'],
    '121': ['53', '103', '116', '120'],
    '122': ['55', '57', '85', '88', '90', '116', '119', '121'],
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
    topological order, so this closes the set and sorts it. The planner on the
    website runs the same function in JavaScript against the same data.
    """
    want, queue = set(), list(selected)
    while queue:
        n = queue.pop()
        if n in want or n not in by_num:
            continue
        want.add(n)
        queue.extend(DEPS.get(n, []))
    return sorted(want)


def check(moves):
    """Called by audit.py. Returns a list of problems, empty when clean."""
    have = {m['num'] for m in moves}
    out = []
    for n, ds in sorted(DEPS.items()):
        if n not in have:
            out.append(f'deps.py has an entry for move {n}, which does not exist')
            continue
        for d in ds:
            if d not in have:
                out.append(f'move {n} depends on {d}, which does not exist')
            elif int(d) >= int(n):
                out.append(f'move {n} depends on {d}, which is not an earlier Move')
        if len(set(ds)) != len(ds):
            out.append(f'move {n} lists a dependency twice')
    return out


if __name__ == '__main__':
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from parse import load_all
    ms = load_all()
    by = {m['num']: m for m in ms}
    print(f'{len(ms)} moves, {sum(len(v) for v in DEPS.values())} dependencies')
    probs = check(ms)
    print('problems:', probs or 'none')
    if ms:
        print(f'{len(roots(ms))} moves need nothing first')
        deep = max(ms, key=lambda m: len(plan([m['num']], by)))
        print(f'deepest: {deep["num"]} {deep["title"]} needs '
              f'{len(plan([deep["num"]], by)) - 1} earlier moves')
