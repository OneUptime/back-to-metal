"""What you gain by leaving, what it costs you, and when not to bother.

The book had no such section for three editions, and the omission was on
purpose: the front matter says "a handbook, not an argument — the argument has
been had". That was a fair position when the reader arriving had already
decided. It is not fair to the reader who has not, and it left the one question
everybody actually asks answered nowhere.

So this is the argument, made once, in the book's own voice. Two rules kept it
honest. Every gain that can be measured is measured, from the same model the
cost page computes from or from a published account by somebody who did it.
And the case against is written by the same hand as the case for, at the same
length, at the end, where a reader will still be reading. A page that lists
nine benefits and no costs is an advertisement, and this book has spent three
editions refusing to be one.

Shared by the printed book and the website, like kit and mission, so the two
cannot drift.
"""

KICKER = 'Before the twenty Moves, the question underneath them'
HEADING = 'Why leave at all'

LEDE = ('Nobody moves off a cloud because a book told them to. They move because '
        'one of five things has become true, and usually because the first one '
        'has been true for a while and somebody finally added it up.')

# --- what you gain --------------------------------------------------------
# Each is (heading, body, how it is evidenced). The third field is not printed
# as a citation - it is here so that a claim which loses its evidence loses its
# place, and so the next person can tell an arithmetic claim from a judgement.
GAINS = [
    ('The bill stops being a percentage of your growth',
     'A cloud bill is a toll on activity: more users, more bytes, more bill, for ever, '
     'at a margin somebody else sets. A rack is a fixed cost. It costs the same in the '
     'month you double as in the month you do not, and the only thing that grows is the '
     'power bill, by the watt rather than by the invoice line. Over the life of one '
     'generation of machines the difference on the estate this book is written against '
     'is about {five_year_saved}, and roughly {five_year_pct} per cent.',
     'computed'),

    ('Egress stops being a tax on your own traffic',
     'Moving data out is where the margin lives, and it is the line that ends most of '
     'these arguments: {egress_100tb} a month to send a hundred terabytes of your own '
     'traffic to your own users. Transit at a facility is bought by the megabit and '
     'costs a fraction of it. Nothing you build gets faster, and the line simply stops '
     'being there.',
     'computed'),

    ('The machines are yours, so the performance is yours',
     'A vCPU is half a core somebody else is also using. Local NVMe is not a network '
     'service with a queue in front of it. The company that publishes this book measured '
     'a nineteen per cent latency improvement on the same software after moving, from '
     'local disk and the absence of neighbours alone, and bought no faster code to get '
     'it.',
     'measured, OneUptime, two years on'),

    ('Nobody deprecates your hardware',
     'A managed service is somebody else’s roadmap running inside your product. '
     'Instance families are retired, versions go end-of-life on a date you did not pick, '
     'a control plane upgrades on its own release channel and a maintenance exclusion '
     'holds it for ninety days at most. A machine you own runs the version you chose '
     'until you choose another one.',
     'judgement, sourced in Move 11'),

    ('You can be told no, and it stops mattering',
     'Capacity in your region, a quota nobody will raise, a region-wide outage you can '
     'do nothing about but write a status update. Owning the hardware does not make you '
     'immune to failure - it makes the failure yours to fix, at three in the morning, '
     'without a support tier. Whether that is a gain depends entirely on whether you '
     'would rather be waiting or working.',
     'judgement'),
]

# --- what it costs you ----------------------------------------------------
COSTS_HEADING = 'And what it costs you'
COSTS_LEDE = ('All of that is real and none of it is free. Four things get worse, '
              'and a comparison that leaves them out is the reason repatriations '
              'get approved and then regretted.')

COSTS = [
    ('Capital, on day one',
     'About {capex} leaves the bank before anything serves a request. On eighteen months '
     'of runway that is a fair refusal, and Move 07 tells you what to do instead.'),

    ('Lead time you cannot compress',
     'Hardware is ordered, not provisioned. A cage is signed, a circuit is delivered, and '
     'the calendar for this programme is mostly waiting: of the {weeks} weeks end to end, '
     'only {days} days are anybody working.'),

    ('The pager, and about {ops_hours} more hours a month',
     'Somebody carries it, and it is now a machine rather than a ticket. The measured '
     'figure on a real two-site fleet larger than this one is fourteen engineer-hours a '
     'month; this book books {owned_hours} against the {cloud_hours} the cloud estate was '
     'already taking, because the people who measured it had done it before.'),

    ('Three things that never come home',
     'A content delivery network, outbound mail deliverability and scrubbing at the edge '
     'are businesses other people run better than you will. Move 04 tells you to keep '
     'paying for all three, and they are {retained} a month of the after state for ever.'),
]

# --- when not to ----------------------------------------------------------
# The most important list here, and the reason the rest can be believed.
STAY_HEADING = 'When to stay exactly where you are'
STAY = [
    'Your load is spiky or seasonal and genuinely scales to near nothing between the '
    'spikes. Elasticity is the one thing a rack cannot do, and paying for the peak all '
    'month is how owning becomes the expensive answer.',

    'You lean hard on managed services that have no real equivalent - a serverless '
    'database, a hosted stream, a workflow engine - and replacing them is a rewrite '
    'rather than a migration. Move 02 will tell you this in an afternoon.',

    'Nobody on the team wants to run infrastructure. This is a trade, not a free lunch, '
    'and it is paid for in attention. A team that resents the pager will run the platform '
    'badly and blame the hardware.',

    'The bill is small. Below about ten thousand dollars a month the saving is real and '
    'the distraction is larger; Move 03 gives you permission to do the arithmetic and '
    'stop, and stopping is a perfectly good outcome.',
]

CLOSER = ('If none of those four is true and the arithmetic in Move 03 clears, the rest '
          'of this book is twenty jobs that get you there, each one done on a Tuesday '
          'and undone on a Wednesday.')


def gains(fmt):
    """The gains, with every computed figure filled in by the caller.

    `fmt` is a dict of the values the build has already computed, so a claim
    here cannot drift from the cost page: they are the same numbers.
    """
    return [(h, b.format(**fmt)) for h, b, _ in GAINS]


def costs(fmt):
    return [(h.format(**fmt), b.format(**fmt)) for h, b in COSTS]
