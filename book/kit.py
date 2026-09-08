"""The reference build: what you are buying, what you are installing, and the
rules the whole book rests on.

Shared by the printed book's front matter and the website, so a change here
lands in both. The specification is a worked reference point sized for a
company - roughly what one spending $24,000 a month on a single cloud actually
needs - and not a shopping list to copy blindly.
"""

# The reference cluster the Moves are written against. One site, five nodes and
# a spare on the shelf.
#
# Five, because three is the smallest control plane with a quorum and losing one
# of three leaves two machines carrying a load they were never sized for. Six,
# because the sixth is not in the rack: it is burned in, configured and
# unplugged, and it costs less than three weeks of degraded capacity during your
# first quarter on your own hardware.
#
# One site. An earlier edition of this book specified two, and two sites is the
# single most common reason a repatriation runs out of energy: double the
# hardware, double the operational surface, and a failover nobody has tested.
# One site with proven off-site backups is the honest answer at this size.
REFERENCE = {
    'sites': 1,
    'nodes': 5,
    'spares': 1,
    'cores_per_node': 32,
    'ram_gb_per_node': 256,
    'nvme_tb_per_node': 15.36,
    'uplink_gbps': 25,
}

# The on-ramp. Before anybody signs a contract, prove the whole stack on cheap
# second-hand hardware. Three nodes because a control plane needs three, and
# refurbished because a machine two generations old runs Kubernetes exactly as
# well as a new one and costs a tenth as much.
HOMELAB = {
    'nodes': 3,
    'cores_per_node': 12,
    'ram_gb_per_node': 64,
    'nvme_tb_per_node': 1.0,
    'uplink_gbps': 2.5,
}

HOMELAB_KIT = [
    'Three refurbished mini PCs or small-form-factor desktops',
    '64 GB in each - memory is what runs out first, not cores',
    'Two NVMe drives a node: one to boot, one for data',
    'A managed switch with VLANs and a spare port for out-of-band',
    'A small uninterruptible power supply, mostly to survive the brownouts '
    'that corrupt etcd',
    'A domain you own, for real certificates rather than self-signed ones',
]

SHELVES = [
    ('Compute', [
        'Five 1U dual-socket servers, and a sixth on the shelf',
        '32 physical cores a node, current-generation EPYC or Xeon',
        '256 GB ECC memory a node, all channels populated',
        'Redundant hot-swap power supplies, each fed from a different strip',
        'A management controller on every node - Redfish, not just a web console',
    ]),
    ('Storage', [
        'Four NVMe drives a node, mixed-use endurance, 3.84 TB each',
        'Enterprise drives with power-loss protection - not consumer SSDs',
        'A separate boot pair, mirrored',
        'One spare drive of each size, on site, unopened',
        'A backup target at a provider you are not otherwise using',
    ]),
    ('Network and space', [
        'Two 25 GbE switches, stacked or in a link-aggregation pair',
        'Two uplinks a node, one to each switch',
        'A separate 1 GbE management switch, not reachable from the internet',
        'A quarter rack in a carrier-neutral facility, A and B power',
        'Facility transit for go-live, and a second upstream ordered alongside it',
        'An out-of-band line that works when the main path does not',
    ]),
    ('The software stack', [
        'Talos Linux on every node - no shell, no package manager, no drift',
        'Kubernetes, on a version at least one minor behind the newest',
        'Cilium for the cluster network, with kube-proxy replaced',
        'Rook, and the Ceph cluster it manages',
        'CloudNativePG, on local NVMe rather than on Ceph',
        'cert-manager and Envoy Gateway',
        'Argo CD, with the cluster state in Git',
        'Prometheus and Loki for the stores, OneUptime for what wakes somebody',
        'Velero, and a restore you have actually performed',
    ]),
    ('Access', [
        'An identity provider that is not the cluster',
        'Break-glass credentials in a safe, on paper',
        'A jump host or a mesh - never a public API server',
        'Hardware tokens for anyone who can delete a cluster',
        'A status page that is not hosted on the thing it reports on',
        'The domain registrar account locked, with recovery codes printed',
    ]),
]

# What has to be on the laptop of whoever is running a Move.
KIT = [
    'kubectl', 'helm', 'talosctl', 'k9s', 'argocd', 'velero',
    'psql and pg_dump', 'barman-cloud', 'redis-cli', 'rclone',
    'the cloud CLI, still logged in', 'dig and mtr', 'openssl',
    'ipmitool', 'the runbook, printed',
]

# The rules. Printed as a page of their own, and the spine of the argument.
# There were ten in the previous edition. Seven is what survived being written
# for a company with two engineers rather than twenty.
RULES = [
    ('Move the cheapest thing first.',
     'Not the most expensive. The first Move exists to prove the platform and the '
     'team, and it should be something whose failure is a shrug. You are buying '
     'evidence, and evidence is worth more early than savings are.'),
    ('Data moves last and leaves last.',
     'Every stateless thing can be cut over and cut back in minutes. State cannot. '
     'Move compute first, run it against the cloud database across the link, and '
     'only then move the database - by which point you have already learned the '
     'things you would otherwise learn during a data migration.'),
    ('Never run two platforms longer than you planned to.',
     'The cost of leaving is not the hardware. It is the months in which both '
     'estates are live, both are on call, and every change has to be made twice. '
     'Pick the overlap window before you start, write it down, and treat '
     'overrunning it as the incident it is.'),
    ('Keep the bill until the invoice proves you can stop.',
     'A resource is not decommissioned when nothing points at it. It is '
     'decommissioned when a full month has passed, the line has gone from the bill, '
     'and nobody has filed a ticket. Turning things off too early is how a '
     'migration becomes an outage a fortnight later.'),
    ('Buy the second of everything, and one spare.',
     'Two switches, two power feeds, two people who can get into the building, and '
     'a sixth machine that is already burned in. Every single point of failure you '
     'accept at the start becomes an incident you attend in person, at night, in a '
     'year.'),
    ('Count the salary.',
     'A saving that costs engineer-hours is a real saving only if you write the '
     'hours into the comparison - on both sides, because the cloud takes them '
     'too. Most of these still win by a wide '
     'margin once you do. The ones that do not, you want to know about in week one '
     'rather than month ten.'),
    ('Keep paying for the three things you will not beat.',
     'A content delivery network, denial-of-service scrubbing at the edge, and '
     'outbound email deliverability. Each is a business somebody else already runs '
     'better than you will, and each is cheap next to what it replaces. Ownership '
     'is a means, not a principle.'),
]
