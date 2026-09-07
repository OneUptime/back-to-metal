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
# A startup, not an enterprise. One cloud, one region, about $24,000 a month.
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
# platform team, and a book that asks a startup to hire two people to save
# $3,000 of hardware is asking it to lose money. Move 03 makes the reader write
# this number down before the arithmetic, so the arithmetic cannot be argued
# into the answer somebody wanted.
PEOPLE = {
    'platform_engineer_year': 190000,
    'engineers_before': 0.5,          # somebody already runs the cloud part-time
    'engineers_after': 1.0,           # what the reference build honestly needs
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
    'node_month': 420,                # 32 core / 256 GB / 4 x 3.84 TB NVMe class
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


def people_month(p=PEOPLE):
    """The extra salaried time the platform costs, over what the cloud cost."""
    delta = p['engineers_after'] - p['engineers_before']
    return delta * p['platform_engineer_year'] / 12


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


def dedicated_month(nodes, retained=DEFAULT_RETAINED, d=DEDICATED, p=PEOPLE):
    infra = nodes * d['node_month']
    # Renting the metal removes the racking and the hands, not the platform work.
    people = (p['engineers_after'] - 0.25 - p['engineers_before']) \
        * p['platform_engineer_year'] / 12
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
    save = BILL_MONTH - o['total']
    print(f'  saving ${save:,.0f} /month, ${save * 12:,.0f} /year, '
          f'{save / BILL_MONTH * 100:.0f} per cent')
    print(f'  (retained third-party lines are passed in by the build, and are '
          f'${0:,.0f} here)')
    print(f'  a managed control plane: ${control_plane_month():,.0f} /month')
    print(f'  100 TB/month of egress on AWS: ${egress_month(100):,.0f}')
    print(f'  the on-ramp: ${homelab_capex():,.0f} once and '
          f'${homelab_month():.0f}/month of electricity for '
          f'{HOMELAB["nodes"]} nodes - which proves the stack and saves nothing')
