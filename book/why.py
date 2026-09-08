"""What you gain by leaving, what it costs you, and when not to bother.

The book had no such section for three editions, and the omission was on
purpose: the front matter says "a handbook, not an argument — the argument has
been had". That was a fair position when the reader arriving had already
decided. It is not fair to the reader who has not, and it left the one question
everybody actually asks answered nowhere.

So this is the argument, made once, in the book's own voice. Two rules kept it
honest. Every gain that can be measured is measured - from the same model the
cost page computes from, or from our own fleet, and where it is ours it says
so in the first person rather than hiding behind a citation.
And the case against is written by the same hand as the case for, at the same
length, at the end, where a reader will still be reading. A page that lists
nine benefits and no costs is an advertisement, and this book has spent three
editions refusing to be one.

Shared by the printed book and the website, like kit and mission, so the two
cannot drift.
"""

KICKER = 'Before the twenty Moves, the question underneath them'
HEADING = 'Why leave at all'

LEDE = ('A cloud bill is rent on somebody else\u2019s margin, charged by the byte, '
        'for as long as you exist. On the estate this book is written against it '
        'comes to {five_year_saved} over the life of one generation of machines \u2014 '
        'which is two engineers, or a year of runway, or the difference between '
        'raising again and not. That is the whole argument. Everything below is '
        'either a way of checking it or a reason it might not apply to you.')

# We did this. That is worth more than any argument, and it is the one thing
# here nobody else can say - so it is said in the first person and it is put
# where a sceptic will hit it early.
OURS_HEADING = 'We did this, and here is what actually happened'
OURS = [
    ('730 days', 'at 99.993 per cent measured availability, through a period that '
                 'included a region-wide outage at the cloud we had left'),
    ('19%', 'lower latency on the same software, from local NVMe and the absence of '
            'neighbours. We bought no faster code to get it'),
    ('2', 'hardware interventions in twenty-four months, both disks, both handled by '
          'remote hands with a mean response of twenty-seven minutes'),
    ('0', 'people hired. The toil moved; it did not multiply. We measured it at about '
          'fourteen engineer-hours a month across two sites'),
]
OURS_NOTE = ('Our own fleet and our own measurement, not an independent audit, and a '
             'bigger estate than this book is sized for. The rest of the figures here '
             'stand on outside sources and on arithmetic you can repeat.')

# --- what you gain --------------------------------------------------------
# Each is (heading, body, how it is evidenced, the test that would disprove it).
#
# THE FOURTH FIELD IS WHAT KEEPS THIS FROM BEING MARKETING. Every claim ships
# with a test the reader runs against their own invoice, and most of them point
# at a Move. A claim with a disproof attached is an engineering claim; a page
# that tells you how to prove it wrong is not trying to sell you anything.
GAINS = [
    ('The bill stops being a percentage of your growth',
     'This is the one that matters and the rest are consequences of it. A cloud bill '
     'is a toll on activity: more users, more bytes, more bill, for ever, at a margin '
     'somebody else sets and can change. A rack is a fixed cost. It costs the same in '
     'the month you double as in the month you do not, and the only thing that grows '
     'is the power draw, by the watt rather than by the invoice line. Over five years '
     'the difference here is {five_year_saved}, and the machines are still working at '
     'the end of it.',
     'computed',
     'Take last quarter\u2019s invoices and plot the total against your own usage '
     'metric. If the line is flat you have nothing to gain here. If it tracks your '
     'growth, that slope is what you are buying out of \u2014 Move 01.'),

    ('Egress stops being a tax on your own traffic',
     'Moving your own data to your own users is where the margin lives, and it is the '
     'line that ends most of these arguments: {egress_100tb} a month to send a hundred '
     'terabytes out. Transit at a facility is bought by the megabit and costs a small '
     'fraction of that. Nothing you build gets faster and no code changes; the line '
     'simply stops being there.',
     'computed',
     'Find the data-transfer line on last month\u2019s bill. Divide it by your egress '
     'in terabytes. If it is anywhere near ninety dollars a terabyte, that line is '
     'nearly pure margin \u2014 Move 01, then Move 18.'),

    ('The machines are yours, so the performance is yours',
     'A vCPU is half a core somebody else is also using. Local NVMe is not a network '
     'service with a queue in front of it and a token bucket on top. The gain is not '
     'theoretical and it is not small: on identical software we measured nineteen per '
     'cent, and the noisy-neighbour tail \u2014 the ninety-ninth percentile that '
     'wakes people \u2014 improves more than the mean does.',
     'measured, our own fleet',
     'Compare your ninety-ninth percentile against your median for a week. If the gap '
     'is wide and unexplained by your own code, some of it is not yours \u2014 '
     'Move 14 measures it on real hardware before anything moves.'),

    ('Nobody deprecates your hardware',
     'A managed service is somebody else\u2019s roadmap running inside your product. '
     'Instance families are retired, versions go end-of-life on a date you did not '
     'pick, a control plane upgrades on its own release channel, and the longest you '
     'can hold it is ninety days. A machine you own runs the version you chose until '
     'you choose another one, and the migration happens when you have time rather '
     'than when the notice arrives.',
     'judgement, sourced in Move 11',
     'Count the forced upgrades and deprecation notices you have absorbed in the last '
     'two years, and what each cost in engineer-days. That is a recurring bill nobody '
     'invoices you for.'),

    ('You can be told no, and it stops mattering',
     'Capacity in your region, a quota nobody will raise, a region-wide outage you can '
     'do nothing about except write a status update. Owning hardware does not make you '
     'immune to failure \u2014 it makes the failure yours to fix, at three in the '
     'morning, without a support tier and without waiting. Whether that reads as a '
     'gain or a cost depends entirely on whether you would rather be working or '
     'waiting, and you already know which you are.',
     'judgement',
     'Look up the last provider incident that hurt you. Ask what you could have done '
     'differently with root on the machines. If the answer is nothing, this one is '
     'worth real money to you.'),
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
     'Somebody carries it, and it is now a machine rather than a ticket. We measured our '
     'own two-site fleet, which is larger than the one this book is written against, at '
     'fourteen engineer-hours a month; the book books {owned_hours} against the '
     '{cloud_hours} the cloud estate was already taking, because we had done it once '
     'before and you will not have.'),

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

    'The bill is small. This edition is written against ten thousand dollars a month, '
    'which is close to the floor: the quarter rack costs $1,400 whether it holds three '
    'machines or thirty, so the saving falls faster than the bill does and Move 03\u2019s '
    'rule stops clearing at about nine thousand. Below that the saving is real and the '
    'distraction is larger; Move 03 gives you permission to do the arithmetic and stop, '
    'and stopping is a perfectly good outcome.',
]

CLOSER = ('If none of those four is true and the arithmetic in Move 03 clears, the rest '
          'of this book is twenty jobs that get you there, each one done on a Tuesday '
          'and undone on a Wednesday.')


def lede(fmt):
    return LEDE.format(**fmt)


def gains(fmt):
    """The gains, each with the test that would disprove it.

    `fmt` is a dict of the values the build has already computed, so a claim
    here cannot drift from the cost page: they are the same numbers.
    """
    return [(h, b.format(**fmt), c.format(**fmt)) for h, b, _, c in GAINS]


def costs(fmt):
    return [(h.format(**fmt), b.format(**fmt)) for h, b in COSTS]
