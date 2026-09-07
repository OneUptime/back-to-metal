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
    'nat_gateway_hour': 0.045,
    'nat_gateway_gb': 0.045,
    'alb_hour': 0.0225,
    'alb_lcu_hour': 0.008,
    'rds_pg_r7g_2xl_hour': 1.0368,    # 8 vCPU, 64 GB, Multi-AZ
    'rds_storage_gb_month': 0.115,
    'elasticache_r7g_large_hour': 0.2016,
    'cloudwatch_ingest_gb': 0.50,
    'cloudwatch_store_gb_month': 0.03,
    'eks_cluster_hour': 0.10,
}

# --- hardware, USD, capital -----------------------------------------------
# A dual-socket 1U with 32 physical cores, 256 GB and 4 x 3.84 TB NVMe, bought
# outright from a tier-two vendor. Amortised straight-line over five years,
# which is conservative: servers of this class are routinely run for seven.
HARDWARE = {
    'node_capex': 13000,
    'node_life_years': 5,
    'switch_capex': 9000,             # per pair, 25 GbE
    'switch_life_years': 7,
    'rack_month': 650,                # a quarter rack, 3 kW committed, A+B power
    # 3 kW because five racked nodes and two switches draw near 2.5 kW, and a
    # facility lets you take eighty per cent of a commitment continuously. The
    # sixth machine is on the shelf and unplugged, so it is capital and not power.
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
# At five machines this comes out close to owning, because a quarter rack's
# fixed costs - space, transit, cross-connect, hands - do not amortise over a
# small fleet. Move 07 says so rather than hiding it: you own hardware when the
# fleet is big enough to carry the room, and before that you rent it.
DEDICATED = {
    'node_month': 420,                # 32 core / 256 GB / 4 x 3.84 TB NVMe class
    'traffic_included_tb': 20,
    'extra_traffic_gb': 0.0011,
}

# --- the on-ramp, USD -----------------------------------------------------
# Second-hand small-form-factor machines and a managed switch. The point of this
# figure is not the saving - there is none, because it replaces nothing - but
# the size of the bet you have to place before you know whether any of the rest
# of the book will work for you. It is three weekends and the price of a laptop.
HOMELAB = {
    'node_capex': 420,          # refurbished, 12 core / 64 GB / 2 x 1 TB NVMe
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


def owned_month(nodes, spares=1):
    infra = site_month(nodes, spares)
    return {'infrastructure': infra, 'people': people_month(),
            'total': infra + people_month()}


def dedicated_month(nodes, d=DEDICATED, p=PEOPLE):
    infra = nodes * d['node_month']
    # Renting the metal removes the racking and the hands, not the platform work.
    people = (p['engineers_after'] - 0.25 - p['engineers_before']) \
        * p['platform_engineer_year'] / 12
    return {'infrastructure': infra, 'people': people, 'total': infra + people}


def egress_month(tb):
    """What moving `tb` terabytes out of AWS costs every month. The single line
    that decides more repatriations than any other."""
    return tb * 1024 * AWS['egress_gb']


if __name__ == '__main__':
    import sys
    sys.path.insert(0, __file__.rsplit('/', 1)[0])
    from kit import REFERENCE as R
    n, sp = R['nodes'], R['spares']
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
    print(f'  100 TB/month of egress on AWS: ${egress_month(100):,.0f}')
    print(f'  the on-ramp: ${homelab_capex():,.0f} once and '
          f'${homelab_month():.0f}/month of electricity for '
          f'{HOMELAB["nodes"]} nodes - which proves the stack and saves nothing')
