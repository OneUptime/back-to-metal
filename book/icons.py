"""The book's marks: one glyph per stage, the cutover dial, the risk bars, and the
page-anatomy diagram printed in the foreword.

Drawn rather than fetched. Every one is a stroked 24x24 path so it inherits
colour and scales to any size in print and on screen, and none of them needs a
font, a sprite sheet or a request.
"""
import math
from flatten import mix

ICONS = {
    # Decide: an invoice with a total ruled off at the foot of it. The whole of
    # Stage 1 is reading a number somebody else wrote down.
    'decide': '<path d="M4.6 2.6h14.8v18.8l-2.5-1.6-2.4 1.6-2.5-1.6-2.5 1.6-2.4-1.6-2.5 1.6z"/>'
              '<path d="M8 7.6h8M8 11.2h8M8 14.8h4.4"/>',
    # Buy: a chassis, front on - drive bays and a vent. The machine itself.
    'buy':    '<rect x="2.2" y="6.6" width="19.6" height="10.8" rx="1"/>'
              '<path d="M5.2 9.6h5.6M5.2 12h5.6M5.2 14.4h5.6"/>'
              '<path d="M14.6 10.4h4.6M14.6 13.6h4.6"/>'
              '<path d="M4.6 17.4v2M19.4 17.4v2"/>',
    # Build: nodes that know about each other. Not a rack - the rack is Buy.
    'build':  '<circle cx="12" cy="4.8" r="2.6"/><circle cx="5" cy="17.6" r="2.6"/>'
              '<circle cx="19" cy="17.6" r="2.6"/>'
              '<path d="M10.7 7.2 6.3 15.2M13.3 7.2l4.4 8M7.6 17.6h8.8"/>',
    # Move: the database cylinder everyone draws, with an arrow leaving it,
    # because everyone recognises both.
    'move':   '<ellipse cx="9.4" cy="5.6" rx="6.6" ry="2.6"/>'
              '<path d="M2.8 5.6v12.8c0 1.4 3 2.6 6.6 2.6 1.1 0 2.2-.1 3.1-.3"/>'
              '<path d="M2.8 12c0 1.4 3 2.6 6.6 2.6"/>'
              '<path d="M15 12.6h6.2M18.4 9.8l2.8 2.8-2.8 2.8"/>',
    # Run: a trace on a screen, with the spike somebody has to answer.
    'run':    '<rect x="2.4" y="4.2" width="19.2" height="15.6" rx="1"/>'
              '<path d="M5.4 14.4h2.6l1.8-4.6 2.4 6.4 2-3.4h4.4"/>',
}


def _dim(color, bg, alpha):
    """The faded twin of `color`, as an opaque hex where both inputs are hex.

    Print must never carry an alpha - KDP requires a flattened interior, and
    kdpcheck.py fails the build on one - so wherever both colours are known the
    tint is pre-composited here. The web passes `currentColor` and a transparent
    backdrop so a mark can inherit the theme, and neither can be mixed; there the
    caller gets an opacity instead, which is fine in a browser and never reaches
    the PDF.
    """
    if color.startswith('#') and bg.startswith('#'):
        return mix(color, bg, alpha), None
    return color, round(alpha, 3)


def icon(key, size='4.6mm', sw=1.5):
    return (f'<svg class="ico" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
            f'stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round">{ICONS[key]}</svg>')


def meter(minutes, color, cap=60, w='100%', ink4='#9DA4A8', rule='#B9BFC3'):
    """The cutover, read against an hour, as a gauge rather than a dial.

    A scale with ticks at the quarter hours and a solid span from zero. A
    zero-downtime Move gets a single stop mark at the origin rather than an
    empty ring: it is the most common value in the book and it should read as
    "none" at a glance, not as "not measured".
    """
    W, y = 200.0, 9.0
    span = min(max(minutes, 0) / cap, 1.0) * W
    ticks = ''.join(
        f'<line x1="{W * f:.1f}" y1="{y + 3}" x2="{W * f:.1f}" y2="{y + 7}" '
        f'stroke="{rule}" stroke-width="1"/>' for f in (0.25, 0.5, 0.75))
    bar = (f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{rule}" stroke-width="1.6"/>'
           + ticks
           + f'<line x1="0" y1="{y + 3}" x2="0" y2="{y + 7}" stroke="{color}" stroke-width="1.6"/>'
           + f'<line x1="{W}" y1="{y + 3}" x2="{W}" y2="{y + 7}" stroke="{rule}" '
             f'stroke-width="1"/>')
    if span > 0.5:
        bar += (f'<line x1="0" y1="{y}" x2="{span:.1f}" y2="{y}" stroke="{color}" '
                f'stroke-width="4.4"/>')
    labels = (f'<text x="0" y="{y + 15}" font-size="7" fill="{ink4}" '
              f'font-family="JetBrains Mono">0</text>'
              f'<text x="{W}" y="{y + 15}" font-size="7" fill="{ink4}" text-anchor="end" '
              f'font-family="JetBrains Mono">{cap}</text>')
    return (f'<svg viewBox="-1 0 {W + 2} 26" width="{w}" style="display:block;height:auto" '
            f'aria-hidden="true">{bar}{labels}</svg>')


RISK_LEVEL = {'Low': 1, 'Medium': 2, 'High': 3}


def risk_bars(level, color, h='3.2mm', bg='#FBFAF7'):
    """Three bars, filled to the risk. Reads without the label, and prints in one ink."""
    n = RISK_LEVEL[level]
    dimc, dimo = _dim(color, bg, .22)
    op = f' fill-opacity="{dimo}"' if dimo is not None else ''
    bars = ''.join(
        f'<rect x="{i * 5}" y="{(2 - i) * 2}" width="3.4" height="{(i + 1) * 4 + 2}" '
        + (f'fill="{color}"/>' if i < n else f'fill="{dimc}"{op}/>') for i in range(3))
    return (f'<svg class="ico" viewBox="0 0 13.4 14" height="{h}" width="{h}" '
            f'style="width:auto" aria-hidden="true">{bars}</svg>')


def anatomy(c='#1F4E79', tint='#E6ECF3', w='64mm', bg='#FBFAF7'):
    """The diagram in the foreword: what every Move page contains, and where.

    Drawn to the same proportions as a real page so a reader can match the shape
    rather than read the caption.
    """
    def bars(x, y, widths, gap=6.2, h=2.6, fill='#6B7280', op=.42, rx=1.3, on=None):
        return ''.join(
            f'<rect x="{x}" y="{y + i * gap}" width="{ww}" height="{h}" rx="{rx}" '
            f'fill="{mix(fill, on or bg, op)}"/>' for i, ww in enumerate(widths))

    r = 14
    C = 2 * math.pi * r
    mk = lambda x, y, n: (
        f'<circle cx="{x}" cy="{y}" r="7.6" fill="{c}"/>'
        f'<text x="{x}" y="{y + 3.4}" font-size="9.4" font-weight="700" fill="#fff" '
        f'text-anchor="middle" font-family="Inter">{n}</text>')

    steps = ''
    for i in range(4):
        yy = 138 + i * 21
        steps += (f'<rect x="91" y="{yy - 6}" width="9" height="9" rx="4.5" fill="{c}"/>'
                  f'<text x="95.5" y="{yy + .8}" font-size="6.4" font-weight="700" fill="#fff" '
                  f'text-anchor="middle" font-family="Inter">{i + 1}</text>'
                  + bars(105, yy - 4, [88, 74, 52][:2 + (i % 2)], 6.4))

    cells = ''.join(
        f'<line x1="{17 + 35.2 * (i + 1)}" y1="258" x2="{17 + 35.2 * (i + 1)}" y2="278" '
        f'stroke="#fff" stroke-width="1"/>' for i in range(4))
    vals = ''.join(
        f'<rect x="{24 + 35.2 * i}" y="263" width="21" height="5" rx="2" '
        f'fill="{mix(c, tint, .55)}"/>'
        f'<rect x="{27 + 35.2 * i}" y="271" width="15" height="2.6" rx="1.3" '
        f'fill="{mix("#6B7280", tint, .45)}"/>' for i in range(5))

    return f'''<svg viewBox="0 0 210 297" width="{w}" style="height:auto;display:block">
<rect x=".5" y=".5" width="209" height="296" fill="{bg}" stroke="#DEDCD4"/>
<rect width="210" height="7" fill="{c}"/>
<text x="17" y="45" font-size="24" font-weight="700" fill="{c}" font-family="Georgia">01</text>
<rect x="52" y="26" width="100" height="9" rx="3" fill="{mix('#14171C', bg, .85)}"/>
<rect x="52" y="41" width="27" height="7" rx="3.5" fill="{c}"/>
<rect x="84" y="42.5" width="30" height="3" rx="1.5" fill="{mix('#6B7280', bg, .42)}"/>
<rect x="119" y="42.5" width="22" height="3" rx="1.5" fill="{mix('#6B7280', bg, .42)}"/>
<circle cx="180" cy="38" r="{r}" fill="none" stroke="{mix(c, bg, .18)}" stroke-width="3"/>
<circle cx="180" cy="38" r="{r}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round"
  stroke-dasharray="{C * 0.28:.1f} {C:.1f}" transform="rotate(-90 180 38)"/>
<rect x="17" y="70" width="2.2" height="18" fill="{c}"/>
<rect x="26" y="72" width="150" height="4" rx="2" fill="{mix(c, bg, .5)}"/>
<rect x="26" y="81" width="96" height="4" rx="2" fill="{mix(c, bg, .5)}"/>
<rect x="17" y="94" width="24" height="3.2" rx="1.6" fill="{mix(c, bg, .75)}"/>
<line x1="17" y1="102" x2="81" y2="102" stroke="#DEDCD4" stroke-width="1"/>
<rect x="17" y="108" width="64" height="112" rx="4" fill="{tint}"/>
{bars(23, 116, [40, 50, 44, 52, 36, 48, 42, 51, 38, 46, 44, 39, 47, 35], 7.1, 2.7, '#4B5563', .38, 1.3, tint)}
<rect x="93" y="94" width="24" height="3.2" rx="1.6" fill="{mix(c, bg, .75)}"/>
<line x1="93" y1="102" x2="193" y2="102" stroke="#DEDCD4" stroke-width="1"/>
{bars(93, 108, [100, 96, 62], 6.6)}
<rect x="93" y="128" width="20" height="3.2" rx="1.6" fill="{mix(c, bg, .75)}"/>
<line x1="93" y1="133.5" x2="193" y2="133.5" stroke="#DEDCD4" stroke-width="1"/>
{steps}
<line x1="17" y1="230" x2="193" y2="230" stroke="#DEDCD4" stroke-width="1"/>
<rect x="17" y="236" width="18" height="3" rx="1.5" fill="{mix(c, bg, .7)}"/>
<rect x="110" y="236" width="24" height="3" rx="1.5" fill="{mix(c, bg, .7)}"/>
{bars(17, 243, [76, 62], 6.2)}{bars(110, 243, [80, 58], 6.2)}
<rect x="17" y="258" width="176" height="20" rx="3" fill="{tint}"/>{cells}{vals}
<rect x="17" y="286" width="22" height="3" rx="1.5" fill="{mix(c, bg, .7)}"/>
<rect x="45" y="286" width="96" height="3" rx="1.5" fill="{mix('#6B7280', bg, .42)}"/>
{mk(180, 38, 1)}{mk(26, 57, 2)}{mk(49, 164, 3)}{mk(160, 110, 4)}{mk(105, 268, 5)}{mk(37, 286, 6)}
</svg>'''


def cost_chart(rows, w='100%', color='#1F4E79', bg='#FBFAF7', line='#DEDCD4'):
    """A stacked bar per option: infrastructure, the salaried time, and what
    stays on somebody else's invoice however it goes.

    Drawn rather than charted, because the point is a comparison a reader can
    check in their head, not a dashboard. Three segments, one scale, no
    gridlines and no legend beyond the labels already on the bars.

    `rows` is a list of (label, infrastructure, people) or, with the third
    segment, (label, infrastructure, people, retained). The four-cell form is
    the honest one: the content network, the outbound mail and the edge
    scrubbing that Move 04 tells you to keep renting are inside the bill on the
    left and inside the bar on the right, and a chart that drops them from the
    second draws a saving nobody gets.

    Colours are pre-composited against the paper with flatten.mix - the printed
    interior carries no alpha, so a lighter segment has to be a lighter colour
    rather than a faded one.
    """
    pad_l, top, bar_h, gap, right = 116, 20, 26, 20, 74
    width, height = 700, top + len(rows) * (bar_h + gap)
    kept_of = lambda r: r[3] if len(r) > 3 else 0
    total = max(r[1] + r[2] + kept_of(r) for r in rows)
    scale = (width - pad_l - right) / total if total else 0
    light = mix(color, bg, .34)
    ink3, ink4 = '#767E8A', '#A2A9B3'

    out = [f'<line x1="{pad_l}" y1="{top - 8}" x2="{width - right + 8}" y2="{top - 8}" '
           f'stroke="{line}" stroke-width="1"/>']
    for k, row in enumerate(rows):
        label, infra, people, kept = row[0], row[1], row[2], kept_of(row)
        y = top + k * (bar_h + gap)
        wi, wp, wk = infra * scale, people * scale, kept * scale
        out.append(
            f'<text x="{pad_l - 12}" y="{y + bar_h * 0.68}" font-size="13" fill="{ink3}" '
            f'text-anchor="end" font-family="Inter" font-weight="600">{label}</text>')
        out.append(f'<rect x="{pad_l}" y="{y}" width="{wi:.1f}" height="{bar_h}" '
                   f'fill="{color}" rx="2"/>')
        if wp > 0:
            out.append(f'<rect x="{pad_l + wi:.1f}" y="{y}" width="{wp:.1f}" height="{bar_h}" '
                       f'fill="{light}" rx="2"/>')
        if wk > 0:
            out.append(f'<rect x="{pad_l + wi + wp:.1f}" y="{y}" width="{wk:.1f}" '
                       f'height="{bar_h}" fill="{ink4}" rx="2"/>')
        out.append(
            f'<text x="{pad_l + wi + wp + wk + 10:.1f}" y="{y + bar_h * 0.7}" font-size="14" '
            f'fill="{color}" font-family="Inter" font-weight="700">'
            f'${(infra + people + kept) / 1000:,.1f}k</text>')
    # The legend goes under the last bar, where there is room for it.
    yk = top + (len(rows) - 1) * (bar_h + gap) + bar_h + 15
    # A LEGEND ROW, NOT LABELS ON THE BAR. The labels used to sit under the
    # start of the segments they named, which reads beautifully at two
    # segments and broke at three: "INFRASTRUCTURE" is 122px of Inter and the
    # salaried segment starts 78px along, so the first two overprinted into
    # "INFRASTRUC(X)RRIED TIME" and the key under the only chart in the cost
    # argument became unreadable. Dropping the colliding label is worse than
    # the collision - the one it drops is the salary, which is the argument.
    # So: a swatch and a word each, laid out left to right on a line of their
    # own, measured (Inter at 11px with 1.4 of tracking runs about 8.7px a
    # character) so they cannot touch whatever the segment widths do.
    keys = [(color, 'INFRASTRUCTURE'), (light, 'SALARIED TIME')]
    if any(kept_of(r) for r in rows):
        keys.append((ink4, 'STILL RENTED'))
    xk = pad_l
    for swatch, label in keys:
        out.append(f'<rect x="{xk:.1f}" y="{yk - 8}" width="12" height="8" '
                   f'fill="{swatch}" rx="1"/>')
        out.append(f'<text x="{xk + 17:.1f}" y="{yk}" font-size="11" '
                   f'fill="{ink4}" font-family="Inter" letter-spacing="1.4">'
                   f'{label}</text>')
        xk += 17 + len(label) * 8.7 + 26
    return (f'<svg viewBox="0 0 {width} {height + 22}" width="{w}" '
            f'style="height:auto;display:block" aria-hidden="true">{"".join(out)}</svg>')
