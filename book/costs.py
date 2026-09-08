"""The cost model, shared by the book and the site.

Two things this is not. It is not a quotation: every cloud figure is a public
list price observed while writing, before any commitment discount, private
pricing agreement or credit, and your bill will differ. And it is not a
calculator that decides for you - it computes the shape of the comparison and
shows its working, because the whole argument of the book depends on a reader
being able to check the arithmetic against their own invoice.

The one thing it insists on is counting the salary. A comparison that leaves
out the people is the reason repatriations get approved and then regretted.
"""

# --- the estate this edition is written against ---------------------------
# A company of a size, not an enterprise. One cloud, one region, about $24,000 a month.
# Every Move's numbers strip is a slice of this bill, and the slices add up to
# it, which is what makes the roadmap page's arithmetic checkable.
BILL_MONTH = 24000

# --- AWS list prices, us-east-1, on-demand, USD ---------------------------
# Observed while writing. On-demand and undiscounted on purpose: a reader with a
# Savings Plan should substitute their own effective rate, and a reader without
# one is genuinely paying this.
AWS = {
    'ec2_m7i_8xl_hour': 1.6128,       # 32 vCPU, 128 GB
    'ec2_vcpu_hour': 0.0504,          # m7i, per vCPU, derived
    'ebs_gp3_gb_month': 0.08,
    'ebs_io2_gb_month': 0.125,
    's3_standard_gb_month': 0.023,
    's3_glacier_ir_gb_month': 0.004,
    'egress_gb': 0.09,                # first 10 TB; the number that ends arguments
    # Egress is TIERED, and quoting the first tier as though it were a flat
    # rate overstates any volume big enough to be worth arguing about. The
    # bands below are us-east-1 internet egress, read off the published offer
    # file (AWSDataTransfer, us-east-1, DataTransfer-Out-Bytes) rather than
    # off a pricing page: (up-to GB, USD per GB).
    'egress_tiers': ((10 * 1024, 0.09), (50 * 1024, 0.085),
                     (150 * 1024, 0.07), (float('inf'), 0.05)),
    'egress_free_gb': 100,            # every month, every region, since 2021
    'nat_gateway_hour': 0.045,
    'nat_gateway_gb': 0.045,
    'alb_hour': 0.0225,
    'alb_lcu_hour': 0.008,
    # WAS 1.0368 AND LABELLED MULTI-AZ, which was neither: Multi-AZ is 1.913
    # and Single-AZ is 0.956, so the old figure was a Multi-AZ label on
    # something under the Single-AZ price - it understated the managed
    # database by 46 per cent, on the line the book leans on hardest.
    'rds_pg_r7g_2xl_hour': 1.913,     # 8 vCPU, 64 GB, PostgreSQL, Multi-AZ
    'rds_pg_r7g_2xl_hour_single_az': 0.956,
    'rds_storage_gb_month': 0.115,
    'elasticache_r7g_large_hour': 0.219,   # Redis or Memcached; Valkey is 0.1752
    'cloudwatch_ingest_gb': 0.50,
    'cloudwatch_store_gb_month': 0.03,
    'eks_cluster_hour': 0.10,
}

# --- hardware, USD, capital -----------------------------------------------
# A dual-socket 1U with 32 physical cores, 256 GB and 4 x 3.84 TB NVMe, bought
# outright from a tier-two vendor. Amortised straight-line over five years,
# which is conservative: servers of this class are routinely run for seven.
HARDWARE = {
    # ALSO NOT RE-PRICED THIS EDITION. It sits on the same memory and NVMe
    # market that moved the on-ramp node from $420 to $950, so it is the most
    # likely stale figure here, and it drives both the $3,235 and the $87,000.
    'node_capex': 13000,
    'node_life_years': 5,
    'switch_capex': 9000,             # per pair, 25 GbE
    'switch_life_years': 7,
    'rack_month': 650,                # a quarter rack, 4 kW committed, A+B power
    # 4 kW, not 3, which is what this comment used to say while Move 07 said 4:
    # five racked nodes and two switches draw near 2.5 kW, a facility lets you
    # take only eighty per cent of a commitment continuously, and 2.5 / 0.8 is
    # 3.1 - so the next size up is 4. The commitment sizes the breaker; the bill
    # is on draw, which is power_kw_month below. The sixth machine is on the
    # shelf and unplugged, so it is capital and not power.
    'transit_month': 450,             # facility blended transit, 1 Gbps commit
    'crossconnect_month': 150,
    'remote_hands_month': 150,
    'power_kw_month': 190,            # all-in, per kW drawn
    'node_kw': 0.45,
}

# --- people ---------------------------------------------------------------
# The line every comparison omits, and the largest line in the right-hand
# column. Loaded cost, not salary: employer taxes, equipment, benefits and the
# recruiter you paid once.
#
# Half an engineer, not two. Five machines in one cage is not an enterprise
# platform team, and a book that asks a company to hire two people to save
# $3,000 of hardware is asking it to lose money. Move 03 makes the reader write
# this number down before the arithmetic, so the arithmetic cannot be argued
# into the answer somebody wanted.
# THE NUMBER THIS BOOK'S HEADLINE TURNS ON, so it is argued rather than
# asserted, and the argument includes the evidence against it.
#
# It was half an extra engineer - 0.5 FTE, $7,917 a month, fifty-nine per cent
# of the whole owned column. That is about eighty-seven engineer-hours a month
# of incremental work on six machines: fourteen hours per machine per month,
# for ever. Nothing published supports it at this fleet size, and it was a
# guess sitting in the load-bearing position.
#
# THE OUTSIDE ANCHOR, and the one the number actually rests on - the only
# estimate of the DELTA we could find that is not selling something adjacent: ten to twenty additional operations hours a month
# for a production stack self-hosting its database, cluster and cache instead
# of renting them managed. This book takes TWENTY - the top of that range.
#
# CORROBORATION, at a hundred times the scale: 37signals moved off the cloud
# and reported no change in the size of the ops team - "the same people who
# were operating HEY and Basecamp and the other apps in the cloud are now
# operating them on our own hardware" - across four thousand vCPUs and 384 TB
# of NVMe. Ahrefs reports the same at eight hundred and fifty machines. A delta
# of zero at that size does not prove a delta of zero at this one; it does make
# half an engineer for six machines very hard to believe.
#
# OUR OWN NUMBER, SAID PLAINLY. We make OneUptime, we made this move, and we
# measured our own fleet: about fourteen engineer-hours a month across two
# sites, dual EPYC with a terabyte a node, over two years. That is a bigger
# fleet than the one this book is written against.
#
# It is not an independent source and it is not offered as one. A book that
# quietly used its own authors' experience to move its own headline in its own
# favour would deserve everything it got, so: it is named here, it is named in
# the prose on the cost page, and the twenty hours below would stand on the
# outside estimate without it. We are showing our working, not citing a
# stranger.
#
# THE EVIDENCE AGAINST, which is real: vendors selling managed Kubernetes put
# self-hosting at anywhere from half an engineer to two. The rebuttal is not
# that they are biased - so is everybody here - it is that their itemised
# effort is SETUP. A fortnight for etcd backup automation, a week for the
# network layer, a fortnight for logging: this book already prices all of that,
# once, as the eighty person-days in the roadmap. Counting it again as a
# monthly line charges the reader twice for the same work.
#
# So: twenty hours, at the top of the independent range, against the sixty the
# cloud estate was already taking. If your own number is different, Move 03
# asks you to write it down before the arithmetic rather than after.
PEOPLE = {
    'platform_engineer_year': 190000,
    'hours_month': 173,               # a working month, near enough
    # What the cloud estate costs in engineer time. NOT ZERO, which is what a
    # comparison that puts "already in the bill" in this cell is claiming: an
    # AWS invoice contains no salary. Somebody upgrades the managed cluster,
    # rotates the credentials, chases the bill and carries the pager.
    'cloud_ops_hours_month': 60,
    # What the owned platform costs on top of that. See above.
    'owned_ops_hours_month': 80,
}

# Dedicated hosts by the month, for the reader who wants the saving without the
# cage. Roughly a comparable machine at a European provider, list, ex-VAT.
#
# At six machines - which is what every caller passes, the five racked and the
# one on the shelf - this comes out BELOW owning rather than close to it,
# because a quarter rack's fixed costs (space, transit, cross-connect, hands)
# do not amortise over a fleet this small. Move 07 says so rather than hiding
# it: you own hardware when the fleet is big enough to carry the room, and
# before that you rent it.
#
# NOT RE-VERIFIED THIS EDITION, AND THE ONLY NUMBER IN THIS FILE THAT CHANGES A
# CONCLUSION. The fact-check could not settle it: the cheapest European provider
# lists a 48-core / 128 GB / 2 x 3.84 TB machine around $371, and the reference
# spec is double that RAM and double that disk; a survey of three providers put
# the class nearer $1,100, but its cheapest citation was a desktop part with a
# server's name. At $420 renting is well under owning. Near $1,100 it is level.
# The book will not pick between those on a number nobody could source, so the
# figure stands as last observed, it is labelled here, and the prose around it
# no longer draws a conclusion that needs it to be exact. Price it against a
# real quote before you decide anything; that is what Move 07 step 6 is for.
DEDICATED = {
    # WAS 420, WHICH MADE RENTING LOOK CHEAPER THAN OWNING AND SHOULD HAVE BEEN
    # THE GIVEAWAY. Renting a machine for five years cannot beat buying the same
    # machine unless the landlord is losing money: at $420 a month you hand over
    # $25,200 over sixty months for a box that costs $13,000 to buy, and the
    # model still came out ahead because the rented column also drops the cage.
    # Two errors cancelling into a plausible-looking answer.
    #
    # $650 is the cheapest European provider's list for a machine that actually
    # meets the reference specification. Their published 48-core / 128 GB /
    # 2 x 3.84 TB box is about $371; this one carries twice the memory and twice
    # the disk. A US provider is two to three times that again. See
    # rent_vs_own_5yr() for what either does over the life of the machine.
    'node_month': 650,                # 32 core / 256 GB / 4 x 3.84 TB NVMe class
    'traffic_included_tb': 20,
    'extra_traffic_gb': 0.0011,
}

# --- the on-ramp, USD -----------------------------------------------------
# Second-hand small-form-factor machines and a managed switch. The point of this
# figure is not the saving - there is none, because it replaces nothing - but
# the size of the bet you have to place before you know whether any of the rest
# of the book will work for you. It used to be three weekends and the price of a
# laptop; since memory doubled it is three weekends and the price of two.
HOMELAB = {
    # WAS 420, WHICH HAS NOT BEEN BUYABLE SINCE THE 2026 MEMORY SQUEEZE. At list
    # today the chassis with a 12-core part is $200-300, the 64 GB kit is
    # $340-450 - more than the machine it goes in - and two 1 TB NVMe is
    # $200-315. Memory is most of this now, which is worth knowing before you
    # price a homelab off a two-year-old blog post.
    'node_capex': 950,          # refurbished, 12 core / 64 GB / 2 x 1 TB NVMe
    'nodes': 3,
    'switch_capex': 260,        # managed, VLANs, 2.5 GbE
    'ups_capex': 180,
    'sundries_capex': 140,      # cables, a label printer, a spare drive
    'power_w': 145,             # all three nodes, measured at idle-to-light load
    'kwh_price': 0.28,          # domestic, USD
}


def homelab_capex(h=HOMELAB):
    """What it costs to own the on-ramp outright."""
    return (h['nodes'] * h['node_capex'] + h['switch_capex']
            + h['ups_capex'] + h['sundries_capex'])


def homelab_month(h=HOMELAB):
    """What it costs to run: electricity, and nothing else."""
    return h['power_w'] / 1000 * 24 * 30.4 * h['kwh_price']


def node_month(h=HARDWARE):
    """One racked node's true monthly cost: metal, power, and nothing else."""
    metal = h['node_capex'] / (h['node_life_years'] * 12)
    power = h['node_kw'] * h['power_kw_month']
    return metal + power


def spare_month(h=HARDWARE):
    """The machine on the shelf. It is capital and it draws no power, and it is
    the cheapest insurance in the book - see Move 06."""
    return h['node_capex'] / (h['node_life_years'] * 12)


def site_month(nodes, spares=1, h=HARDWARE):
    """One site: the nodes, the spare, the switches, the space and the link."""
    switches = h['switch_capex'] / (h['switch_life_years'] * 12)
    return (nodes * node_month(h) + spares * spare_month(h) + switches
            + h['rack_month'] + h['transit_month'] + h['crossconnect_month']
            + h['remote_hands_month'])


def hourly(p=PEOPLE):
    """One loaded engineer-hour."""
    return p['platform_engineer_year'] / 12 / p['hours_month']


def cloud_people_month(p=PEOPLE):
    """What running the CLOUD estate costs in salary every month.

    It is not nought, and a table that writes "already in the bill" in this cell
    is claiming that it is: a cloud invoice bills for machines, not for the
    person who upgrades the managed cluster, rotates the credentials, argues
    with the bill and carries the pager. Leaving it off the left-hand column
    while charging the right-hand column for its own people is the mirror image
    of the error this book was written to argue against."""
    return p['cloud_ops_hours_month'] * hourly(p)


def owned_people_month(p=PEOPLE):
    """What running the OWNED platform costs in salary every month."""
    return p['owned_ops_hours_month'] * hourly(p)


def people_month(p=PEOPLE):
    """The difference between the two - the extra salaried time owning costs."""
    return owned_people_month(p) - cloud_people_month(p)


# --- what you go on paying, USD -------------------------------------------
# THE LINE THE FIRST EDITION OF THIS MODEL LEFT OUT, and the reason its headline
# was wrong by $2,310 a month.
#
# Move 04 concludes that three things do not come home - the content delivery
# network, outbound mail deliverability and volumetric scrubbing at the edge -
# and tells the reader to write them into the comparison as a PERMANENT line.
# Five more Moves retire most of a service and keep a residue: object storage
# that stays archived, a registry, a queue, a certificate authority, off-site
# backup. All of that is inside the $24,000 before-state and all of it is still
# there afterwards, and a model that counts it on the left and not on the right
# is the exact error this book was written to argue against.
#
# It is not a constant here, because it is not a judgement: it is the sum of
# the Now column of the Move files, and the build passes it in. See
# site.totals() for how it is derived and why Move 07's cage is not in it.
DEFAULT_RETAINED = 0.0


def owned_month(nodes, spares=1, retained=DEFAULT_RETAINED):
    infra = site_month(nodes, spares)
    people = people_month()
    return {'infrastructure': infra, 'people': people, 'retained': retained,
            'total': infra + people + retained}


# Renting the metal removes the hardware-specific work: firmware, disk swaps,
# capacity planning against a rack, and the coordination with remote hands. It
# removes none of the platform work - the cluster, the storage, the upgrades
# and the pager are identical whoever owns the box.
#
# Ten hours, not twenty. Racking is a one-off (Move 09), not a monthly cost,
# and the measured hardware intervention rate on a fleet this size is two
# call-outs in twenty-four months. Ten hours a month is already generous.
RENT_SAVES_HOURS = 10


def dedicated_month(nodes, retained=DEFAULT_RETAINED, d=DEDICATED, p=PEOPLE):
    infra = nodes * d['node_month']
    people = ((p['owned_ops_hours_month'] - RENT_SAVES_HOURS)
              - p['cloud_ops_hours_month']) * hourly(p)
    # The retained line is the same either way: a content delivery network does
    # not care whose rack the origin is in.
    return {'infrastructure': infra, 'people': people, 'retained': retained,
            'total': infra + people + retained}


def control_plane_month(a=AWS):
    """What a managed Kubernetes control plane costs to be handed to you.

    The same list rate at all three - EKS on standard support, GKE in either
    mode past the free one, AKS on the Standard tier - which is why one number
    serves the whole book. It is here rather than typed into Move 11 because
    Move 11 used to say $220 while this file said $0.10 an hour, and one of
    them had to be reading the other."""
    return a['eks_cluster_hour'] * 730


def rent_vs_own_5yr(nodes, h=HARDWARE, d=DEDICATED):
    """The question everybody asks, answered on the hardware alone.

    "How is renting cheaper than owning over five years?" It is not, and any
    model that says otherwise has a number wrong somewhere. A landlord buys the
    same machine you would, finances it, racks it, powers it, insures it and
    takes a margin - so the rent has to exceed the amortised purchase or there
    is no business. This function exists so the book can show that rather than
    assert it, and so a rent figure that has drifted low fails a sanity check
    instead of quietly flattering the wrong column.

    What renting genuinely buys is not a lower hardware cost. It is no capital
    outlay, no lead time, no cage, no contract and no racking day - which is a
    real answer for a company with eighteen months of runway, and a different
    answer from "it is cheaper"."""
    months = h['node_life_years'] * 12
    own = nodes * h['node_capex']
    rent = nodes * d['node_month'] * months
    return {'months': months, 'nodes': nodes, 'own_capex': own, 'rent_total': rent,
            'multiple': rent / own if own else 0,
            'own_per_node_month': h['node_capex'] / months,
            'rent_per_node_month': d['node_month']}


def five_year(nodes, spares=1, retained=DEFAULT_RETAINED,
              h=HARDWARE, d=DEDICATED, p=PEOPLE):
    """The three ways of buying the same computers, over the life of a machine.

    A month is the wrong window for this decision and it always was. Owning is
    capital on day one and cheap running afterwards; renting is no capital and
    dearer running; the cloud is no capital and dearest running. Compared a
    month at a time the capital either disappears into an amortisation line or
    sits there looking like the whole story, and neither is what a founder
    signing the cheque is actually choosing between.

    So this compares five years, which is the amortisation life the rest of the
    file uses, and it keeps the capital OUT of the monthly figure and puts it
    on the line where it happens. The monthly running cost here therefore
    excludes amortisation - it is power, space, transit, the cross-connect,
    hands, the people and the lines that never come home.

    The residual is the part every rent-versus-buy comparison forgets. After
    sixty months the owned machines are five years old and still working:
    hardware of this class is routinely run for seven or eight, so what you
    hold is a fleet with years left, not scrap. It is counted conservatively at
    fifteen per cent of capital, and it is the whole of the difference between
    owning and renting at this size.
    """
    months = h['node_life_years'] * 12
    people = owned_people_month(p) + retained
    rent_people = ((p['owned_ops_hours_month'] - RENT_SAVES_HOURS) * hourly(p)) + retained

    # --- the cloud: no capital, and the largest running cost -------------
    cloud_m = BILL_MONTH + cloud_people_month(p)

    # --- rented metal: no capital, the facility is somebody else's -------
    rent_m = (nodes + spares) * d['node_month'] + rent_people

    # --- owned metal: capital on day one, then power and the room --------
    capex = (nodes + spares) * h['node_capex'] + h['switch_capex']
    own_m = (nodes * h['node_kw'] * h['power_kw_month']
             + h['rack_month'] + h['transit_month'] + h['crossconnect_month']
             + h['remote_hands_month'] + people)
    residual = capex * 0.15

    rows = [
        {'key': 'cloud', 'label': 'Cloud',
         'capex': 0, 'month': cloud_m, 'total': cloud_m * months, 'residual': 0},
        {'key': 'rented', 'label': 'Rented metal',
         'capex': 0, 'month': rent_m, 'total': rent_m * months, 'residual': 0},
        {'key': 'owned', 'label': 'Colocation',
         'capex': capex, 'month': own_m,
         'total': capex + own_m * months - residual, 'residual': residual},
    ]
    for r in rows:
        r['saved'] = rows[0]['total'] - r['total']
        r['pct'] = r['saved'] / rows[0]['total'] * 100 if rows[0]['total'] else 0
    return {'months': months, 'rows': rows}


def egress_month(tb, a=AWS):
    """What moving `tb` terabytes out of AWS costs every month. The single line
    that decides more repatriations than any other.

    Tiered, and it has to be. This used to multiply the whole volume by the
    first band's rate, which is right up to 10 TB and increasingly wrong above
    it: at 100 TB a month the flat sum came to $9,216 against a real $7,987,
    an overstatement of $1,229 and fifteen per cent. A book that invites the
    reader to check its arithmetic against their own invoice cannot afford to
    be the one quoting the higher number.

    The free allowance is in here too. It is 100 GB a month and it changes
    nothing at this size - nine dollars - but leaving it out is the same class
    of error in the other direction, and the point is to be checkable."""
    gb = max(0.0, tb * 1024 - a['egress_free_gb'])
    total, lower = 0.0, 0.0
    for upper, rate in a['egress_tiers']:
        if gb <= lower:
            break
        total += (min(gb, upper) - lower) * rate
        lower = upper
    return total


if __name__ == '__main__':
    import sys
    sys.path.insert(0, __file__.rsplit('/', 1)[0])
    from kit import REFERENCE as R
    n, sp = R['nodes'], R['spares']
    # The retained line is the Now column of the Move files and the build
    # passes it in; this self-test has no Move files, so it prints the shape
    # with nothing retained and says so.
    o = owned_month(n, sp)
    d = dedicated_month(n + sp)
    print(f'Reference build: {n} nodes + {sp} spare, '
          f'{n * R["cores_per_node"]} cores, {n * R["ram_gb_per_node"] / 1024:.1f} TB RAM')
    print(f'  cloud now                                        '
          f'    ${BILL_MONTH:>9,.0f} /month')
    print(f'  owned      infra ${o["infrastructure"]:>9,.0f}  people ${o["people"]:>9,.0f}'
          f'  total ${o["total"]:>9,.0f} /month')
    print(f'  dedicated  infra ${d["infrastructure"]:>9,.0f}  people ${d["people"]:>9,.0f}'
          f'  total ${d["total"]:>9,.0f} /month')
    # THE SAME FRAMING THE SITE AND THE BOOK USE, or this self-test prints a
    # headline that contradicts them. Both columns carry their own people: the
    # cloud's operational load is real and is not on its invoice, so leaving it
    # off the left while charging the right is what makes 79 per cent out of
    # what is honestly 56.
    cp = cloud_people_month()
    cloud_total = BILL_MONTH + cp
    save = cloud_total - (o['total'] + cp)
    print(f'  ...with the cloud\'s own {PEOPLE["cloud_ops_hours_month"]} ops hours '
          f'counted on its side too: ${cloud_total:,.0f} against '
          f'${o["total"] + cp:,.0f}')
    print(f'  saving ${save:,.0f} /month, ${save * 12:,.0f} /year, '
          f'{save / cloud_total * 100:.0f} per cent of the loaded bill '
          f'({(BILL_MONTH - o["infrastructure"]) / BILL_MONTH * 100:.0f} per cent '
          f'of the infrastructure line)')
    print(f'  (retained third-party lines are passed in by the build, and are '
          f'${0:,.0f} here)')
    print(f'  a managed control plane: ${control_plane_month():,.0f} /month')
    print(f'  100 TB/month of egress on AWS: ${egress_month(100):,.0f}')
    print(f'  the on-ramp: ${homelab_capex():,.0f} once and '
          f'${homelab_month():.0f}/month of electricity for '
          f'{HOMELAB["nodes"]} nodes - which proves the stack and saves nothing')
