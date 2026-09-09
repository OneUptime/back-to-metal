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

LEDE = ('Colocation and rented dedicated servers put more of your infrastructure '
        'budget into capacity you can use. Rent the machines to preserve cash, or '
        'own them in a colocation facility for lower running costs and control over '
        'the hardware. In this reference model, colocation saves {five_year_saved} '
        'over five years, with the same operations hours as the cloud. Your team '
        'brings its skills; the provider supplies the building and physical support.')

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
     'somebody else sets and can change. A rack or a dedicated-server contract buys '
     'capacity at a predictable price. While your workload fits that capacity and '
     'your power and traffic allowances, more users need not mean more infrastructure '
     'rent. Add machines when demand calls for them. Over five years '
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

    ('Your team runs the platform; remote hands look after the rack',
     'Your cloud-ops engineers already deploy, monitor, patch and recover services. '
     'Those skills move with the workload. Colocation remote hands carry out disk '
     'swaps, cabling and power cycles under your runbooks; a rented-metal provider '
     'maintains its hardware under the support agreement. The reference model keeps '
     'the same team and monthly operations hours across all three options.',
     'judgement',
     'Agree the physical tasks, coverage and response times with the provider, then '
     'rehearse an incident together. Measure your team\u2019s hours before and after '
     'the move \u2014 Moves 07 and 19.'),
]

# --- what it costs you ----------------------------------------------------
COSTS_HEADING = 'Choose how you move'
COSTS_LEDE = ('Both routes can lower the bill. Choose the purchasing and support '
              'arrangements that fit your cash flow and the team you already have.')

COSTS = [
    ('Rent first, or own in colocation',
     'Rented metal lets you move without buying the servers upfront. Colocation lets '
     'you own the hardware and spread its purchase cost over years of use. Compare '
     'both cash flows in Move 03 and choose the route in Move 07.'),

    ('A timetable that fits the route',
     'Available rented servers can avoid the hardware purchase and facility setup '
     'lead times. The colocation plan includes ordering machines, signing space and '
     'waiting for circuits: {days} person-days of work across {weeks} weeks. Both '
     'routes keep the migration rehearsals and rollback windows.'),

    ('The same team, the same operations hours',
     'Cloud ops transitions into on-prem ops. Remote hands handles the physical '
     'interventions; your engineers keep responsibility for the platform and '
     'application. The model budgets {cloud_hours} hours a month in every option, '
     'with remote hands in the facility bill. Migration work is counted separately.'),

    ('Three things that never come home',
     'A content delivery network, outbound mail deliverability and scrubbing at the edge '
     'are businesses other people run better than you will. Move 04 tells you to keep '
     'paying for all three. These and the services retained in later Moves total '
     '{retained} a month in the reference model.'),
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

    'You have no team to own the platform and no managed operations partner. Remote '
    'hands covers physical work; application recovery and platform decisions still '
    'need an owner. An existing cloud-ops team can transition into that role.',

    'Your effective cloud bill is too small to cover migration and the capacity you '
    'need. Price rented metal as well as a colocation rack: renting can suit a smaller '
    'estate. Move 03 compares your own quotes and hours, so the decision rests on your '
    'workload rather than a spending threshold borrowed from another company.',
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
