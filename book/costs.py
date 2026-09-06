"""The cost model, shared by the book and the site.

Two things this is not. It is not a quotation: every AWS figure is a public
list price observed while writing, before any commitment discount, private
pricing agreement or credit, and your bill will differ. And it is not a
calculator that decides for you - it computes the shape of the comparison and
shows its working, because the whole argument of the book depends on a reader
being able to check the arithmetic against their own invoice.

The one thing it insists on is counting the salary. A comparison that leaves
out the people is the reason repatriations get approved and then regretted.
"""

# --- AWS list prices, us-east-1, on-demand, USD ---------------------------
# Observed while writing. On-demand and undiscounted on purpose: a reader with a
# Savings Plan should substitute their own effective rate, and a reader without
# one is genuinely paying this.
AWS = {
    'ec2_m7i_48xl_hour': 9.6768,      # 192 vCPU, 768 GB
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
    'rds_pg_r7g_4xl_hour': 2.0736,    # 16 vCPU, 128 GB, Multi-AZ
    'rds_storage_gb_month': 0.115,
    'elasticache_r7g_xl_hour': 0.4032,
    'msk_m7g_large_hour': 0.189,
    'cloudwatch_ingest_gb': 0.50,
    'cloudwatch_store_gb_month': 0.03,
    'eks_cluster_hour': 0.10,
}

# --- hardware, USD, capital -----------------------------------------------
# A dual-socket 1U with 64 cores, 512 GB and 4 x 3.84 TB NVMe, bought outright
# from a tier-two vendor. Amortised straight-line over five years, which is
# conservative: servers of this class are routinely run for seven.
HARDWARE = {
    'node_capex': 24000,
    'node_life_years': 5,
    'switch_capex': 14000,            # per pair, 25 GbE
    'switch_life_years': 7,
    'rack_month': 1400,               # a full rack, 5 kW, A+B power, one site
    'transit_month': 900,             # per site, 10 Gbps commit, blended
    'crossconnect_month': 300,
    'remote_hands_month': 250,
    'power_kw_month': 190,            # all-in, per kW drawn
    'node_kw': 0.55,
}

# --- people ---------------------------------------------------------------
# The line every comparison omits. Loaded cost, not salary: employer taxes,
# equipment, benefits and the recruiter you paid once.
PEOPLE = {
    'platform_engineer_year': 210000,
    'engineers_before': 1.0,          # you were already paying somebody to run the cloud
    'engineers_after': 2.5,           # what the reference build honestly needs
}

# Dedicated hosts by the month, for the reader who wants the saving without the
# rack. Roughly a comparable machine at a European provider, list, ex-VAT.
DEDICATED = {
    'node_month': 480,                # 64 core / 512 GB / 4 x 3.84 TB NVMe class
    'traffic_included_tb': 20,
    'extra_traffic_gb': 0.0011,
}


# --- the homelab on-ramp, USD -------------------------------------------
# Second-hand small-form-factor machines and a managed switch. The point of this
# figure is not the saving - there is none, because it replaces nothing - but
# the size of the bet you have to place before you know whether any of the rest
# of the book will work for you.
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
    """One owned node's true monthly cost: metal, power, and its share of the room."""
    metal = h['node_capex'] / (h['node_life_years'] * 12)
    power = h['node_kw'] * h['power_kw_month']
    return metal + power


def site_month(nodes, h=HARDWARE):
    """One site: the nodes, the switches, the rack, transit and hands."""
    switches = h['switch_capex'] / (h['switch_life_years'] * 12)
    return (nodes * node_month(h) + switches + h['rack_month']
            + h['transit_month'] + h['crossconnect_month'] + h['remote_hands_month'])


def people_month(p=PEOPLE):
    """The extra salaried time the platform costs, over what the cloud cost."""
    delta = p['engineers_after'] - p['engineers_before']
    return delta * p['platform_engineer_year'] / 12


def owned_month(sites, nodes_per_site):
    infra = sites * site_month(nodes_per_site)
    return {'infrastructure': infra, 'people': people_month(),
            'total': infra + people_month()}


def dedicated_month(nodes, d=DEDICATED, p=PEOPLE):
    infra = nodes * d['node_month']
    # Renting the metal removes the racking and the hands, not the platform work.
    people = (p['engineers_after'] - 0.5 - p['engineers_before']) \
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
    o = owned_month(R['sites'], R['nodes_per_site'])
    d = dedicated_month(R['sites'] * R['nodes_per_site'])
    n = R['sites'] * R['nodes_per_site']
    print(f'Reference build: {R["sites"]} sites x {R["nodes_per_site"]} nodes = {n} nodes, '
          f'{n * R["cores_per_node"]} cores, {n * R["ram_gb_per_node"] / 1024:.0f} TB RAM')
    print(f'  owned      infra ${o["infrastructure"]:>10,.0f}  people ${o["people"]:>9,.0f}'
          f'  total ${o["total"]:>10,.0f} /month')
    print(f'  dedicated  infra ${d["infrastructure"]:>10,.0f}  people ${d["people"]:>9,.0f}'
          f'  total ${d["total"]:>10,.0f} /month')
    vcpu = n * R['cores_per_node'] * 2
    aws_compute = vcpu * AWS['ec2_vcpu_hour'] * 730
    print(f'  the same {vcpu} vCPU on EC2 on-demand: ${aws_compute:,.0f} /month, '
          f'compute alone, before storage or egress')
    print(f'  100 TB/month of egress on AWS: ${egress_month(100):,.0f}')
    print(f'  the on-ramp: ${homelab_capex():,.0f} once and '
          f'${homelab_month():.0f}/month of electricity for '
          f'{HOMELAB["nodes"]} nodes - which proves the stack and saves nothing')
