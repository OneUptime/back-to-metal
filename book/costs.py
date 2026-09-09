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
# One cloud, one region, about $100,000 a month. Every Move's numbers strip is
# a slice of this bill, and the slices add up to it, which is what makes the
# roadmap page's arithmetic checkable.
#
# THE BOOK GETS EASIER AS THE BILL GETS BIGGER, and this edition is where that
# stops being an assertion. The facility is a fixed cost - space, transit,
# cross-connects, hands - and it is the thing that makes a small repatriation
# marginal:
#
#     quarter rack, 4 machines    $1,400/mo    $350 a machine
#     full rack,   18 machines    $4,500/mo    $250 a machine
#
# At $10,000 a month the room was most of the reason to hesitate and Move 03's
# rule stopped clearing at about $9,000. At $100,000 the room is a rounding
# error against the bill and the rule clears by a mile. The stopping advice in
# why.py is unchanged and still correct: it is about the floor, not this.
BILL_MONTH = 100000


# --- AWS list prices, us-east-1, on-demand, USD ---------------------------
# Observed while writing. On-demand and undiscounted on purpose: a reader with a
# Savings Plan should substitute their own effective rate, and a reader without
# one is genuinely paying this.
AWS = {
    # Verified 2026-09-09 against the official regional AmazonEC2 offer,
    # SKU DFY9W427PBEXH8VY: Linux, shared, on-demand, us-east-1.
    'ec2_m7i_8xl_hour': 1.6128,       # 32 vCPU, 128 GiB
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
    'egress_free_gb': 100,            # shared across eligible services/regions
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
    # likely stale figure here, and it drives the owned infrastructure price.
    'node_capex': 13000,
    'node_life_years': 5,
    'switch_capex': 14000,            # per pair, 25 GbE, enough ports for 18
    'switch_life_years': 7,
    'rack_month': 2600,               # a FULL rack, 10 kW committed, A+B power
    # A FULL RACK, because sixteen racked nodes and two switches are 20U and
    # draw about 7.2 kW, and a facility lets you take only eighty per cent of a
    # commitment continuously: 7.2 / 0.8 is 9, so the next size up is 10. The
    # commitment sizes the breaker; the bill is on draw, which is
    # power_kw_month below. The two spares are on the shelf and unplugged, so
    # they are capital and not power.
    'transit_month': 1200,            # facility blended transit, 5 Gbps commit
    'crossconnect_month': 300,        # two, to two carriers, at this size
    'remote_hands_month': 400,
    'power_kw_month': 190,            # all-in, per kW drawn
    'node_kw': 0.45,
}

# --- people ---------------------------------------------------------------
# Loaded cost includes employer taxes, equipment and benefits. Every option
# carries the same existing operations team in this reference model: cloud ops
# transitions to operating the platform on colocation or rented metal.
#
# This is a steady-state planning assumption for the standardised stack in the
# book, not a promise that every migration keeps the same workload. The cloud
# already needs upgrades, credentials, capacity planning and incident response.
# On metal that attention shifts to the platform; contracted colocation remote
# hands or the dedicated provider carry out the covered physical interventions.
# Their work remains priced in facility charges or the server rental.
#
# On-premises operations roles can cost less than cloud specialist roles, but
# this model takes no salary discount: the same loaded rate applies throughout.
# Any saving from local pay rates must be supported by the actual staffing plan,
# just as any extra recurring hours or support charges must be priced in.
#
# Setup, automation, training and cutover are one-time labour in the Move effort
# figures and roadmap. Do not add that work again as a permanent monthly hire.
# Move 03 asks readers to validate the recurring hours against their own team,
# stack and support contract before relying on this assumption.
STEADY_STATE_OPS_HOURS_MONTH = 160
PEOPLE = {
    'platform_engineer_year': 190000,
    'hours_month': 173,               # a working month, near enough
    'cloud_ops_hours_month': STEADY_STATE_OPS_HOURS_MONTH,
    'owned_ops_hours_month': STEADY_STATE_OPS_HOURS_MONTH,
    'rented_ops_hours_month': STEADY_STATE_OPS_HOURS_MONTH,
}

# Dedicated hosts by the month, for the reader who wants the saving without
# buying the fleet. The rental includes the provider's facility and physical
# hardware support; it does not replace the reader's platform operations team.
# This is an indicative European rate, ex-VAT, retained from the prior edition
# rather than a current quotation. Compare matching CPU, RAM, storage, network
# and support terms against a real quote in Move 07 before deciding.
DEDICATED = {
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


def dedicated_people_month(p=PEOPLE):
    """What running the RENTED platform costs in salary every month."""
    return p['rented_ops_hours_month'] * hourly(p)


def people_month(p=PEOPLE):
    """Owned salary minus cloud salary; zero under the shared-hours assumption."""
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
# backup. All of that is inside the before-state on the left and all of it is still
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


# Physical support is included in the rented infrastructure price, just as
# remote hands is included in colocation's facility line. Both options retain
# the existing team's platform responsibilities and the same recurring hours.


def dedicated_month(nodes, retained=DEFAULT_RETAINED, d=DEDICATED, p=PEOPLE):
    infra = nodes * d['node_month']
    people = dedicated_people_month(p) - cloud_people_month(p)
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
    """Hardware purchase versus the rental payments over its planned life.

    Rental pays for more than the machine: it also includes a facility and
    physical support. This narrow comparison shows the rental premium over purchase in the
    reference quote; five_year() compares the complete operating options.
    Renting keeps hardware capital available and hands procurement and physical
    maintenance to the provider, subject to the quoted capacity and terms.
    """
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
    fifteen per cent of capital. This is an assumption to revisit against the
    expected useful life and resale value, rather than a guaranteed return.
    """
    months = h['node_life_years'] * 12
    people = owned_people_month(p) + retained
    rent_people = dedicated_people_month(p) + retained

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
    # cloud's operational load is real and is not on its invoice. The same
    # salary is counted in every option even when the hours do not change.
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
