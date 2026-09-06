"""The reference build: what you are buying, what you are installing, and the
ten rules the whole book rests on.

Shared by the printed book's front matter and the website's Kit page, so a change
here lands in both. The specifications are a worked reference point sized for a
mid-size estate - roughly what a company spending $30k-$60k a month on AWS
compute and data actually needs - not a shopping list to copy blindly.
"""

# The reference cluster the Moves are written against. Two sites, six nodes each,
# because one site is not a platform and seven nodes is where the arithmetic of
# losing one stops hurting.
REFERENCE = {
    'sites': 2,
    'nodes_per_site': 6,
    'cores_per_node': 64,
    'ram_gb_per_node': 512,
    'nvme_tb_per_node': 15.36,
    'uplink_gbps': 25,
}

# The on-ramp. Part I argues that most readers should prove the whole stack on
# cheap second-hand hardware before anybody signs a contract, and this is what
# that costs and what it consists of. Three nodes because a control plane needs
# three, and refurbished because a machine two generations old runs Kubernetes
# exactly as well as a new one and costs a tenth as much.
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
    'A small UPS, mostly to survive the brownouts that corrupt etcd',
    'A label printer, because you will regret not having one',
    'A separate router or firewall you are willing to break',
    'A domain you own, for real certificates rather than self-signed ones',
]

SHELVES = [
    ('Compute', [
        'Six 1U or 2U dual-socket servers per site',
        '64 physical cores a node, current-generation EPYC or Xeon',
        '512 GB ECC RAM a node, all channels populated',
        'Redundant hot-swap power supplies, both fed',
        'BMC on every node - Redfish, not just a web console',
        'Two spare nodes on the shelf, racked and burned in',
    ]),
    ('Storage', [
        'Four NVMe drives a node, mixed-use endurance, 3.84 TB each',
        'Enterprise drives with power-loss protection - not consumer SSDs',
        'A separate boot pair, mirrored',
        'One spare drive of each size, on site, unopened',
        'A backup target in a third location you do not control',
    ]),
    ('Network', [
        'Two 25 GbE ToR switches a site, MLAG or stacked',
        'Two uplinks a node, LACP to separate switches',
        'A separate 1 GbE out-of-band management switch',
        'Your own address space, or a /24 from the facility',
        'Two transit providers, or one transit and one IX',
        'A serial console server, reachable when the cluster is not',
    ]),
    ('Site and power', [
        'Two facilities far enough apart to fail separately',
        'A- and B-side power, on separate PDUs',
        'Remote hands with a response time in the contract',
        'Cross-connects ordered and tested before you need them',
        'Physical access for at least two named people',
        'A written escalation path with a phone number on it',
    ]),
    ('The software stack', [
        'Talos Linux on every node - no shell, no package manager, no drift',
        'Kubernetes, on a version at least one minor behind the newest',
        'Cilium for CNI, with kube-proxy replacement',
        'Rook, and the Ceph cluster it manages',
        'cert-manager, external-dns, and Envoy Gateway',
        'Argo CD, with the cluster state in Git',
        'Prometheus and Loki for the stores, OneUptime for what wakes someone',
        'Velero, and a restore you have actually performed',
    ]),
    ('Access and identity', [
        'An OIDC provider that is not the cluster',
        'Break-glass credentials in a safe, on paper',
        'A bastion or a mesh - not a public API server',
        'Hardware tokens for anyone who can delete a cluster',
        'An audit log shipped somewhere the cluster cannot reach',
        'A status page that is not hosted on the thing it reports on',
        'The domain registrar account locked, with recovery codes printed',
    ]),
]

# What has to be on the laptop of whoever is running a Move.
KIT = [
    'kubectl', 'helm', 'talosctl', 'k9s', 'argocd', 'velero',
    'psql and pg_dump', 'mysql client', 'redis-cli', 'rclone',
    'aws CLI, still logged in', 'dig and mtr', 'openssl',
    'ipmitool', 'a serial cable', 'the runbook, printed',
]

# The ten rules. Printed as a page of their own, and the spine of the argument.
RULES = [
    ('Move the cheapest thing first.',
     'Not the most expensive. The first Move exists to prove the platform and the '
     'team, and it should be something whose failure is a shrug. You are buying '
     'evidence, and evidence is worth more early than savings are.'),
    ('Never run two platforms longer than you planned to.',
     'The cost of a repatriation is not the hardware. It is the months in which both '
     'estates are live, both are on call, and every change has to be made twice. Pick '
     'the overlap window before you start, write it down, and treat overrunning it as '
     'the incident it is.'),
    ('Data moves last and leaves last.',
     'Every stateless thing can be cut over and cut back in minutes. State cannot. '
     'Move compute first, prove it against the cloud database across the link, and '
     'only then move the database - by which point you will have learned the things '
     'you would otherwise have learned during a data migration.'),
    ('Keep the bill until the invoice proves you can stop.',
     'A resource is not decommissioned when nothing points at it. It is '
     'decommissioned when a full month has passed, the line has gone from the bill, '
     'and nobody has filed a ticket. Turning things off too early is how a migration '
     'becomes an outage a fortnight later.'),
    ('Buy the second of everything before you need the first.',
     'Two switches, two power feeds, two transit providers, two people who can get '
     'into the building. Every single point of failure you accept at the start '
     'becomes an incident you will attend in person, at night, in a year.'),
    ('Own your addresses.',
     "An IP range you rent from a provider is a migration you have to do again. Your "
     "own address space and your own ASN cost a few hundred pounds and take a few "
     "weeks, and they are the difference between changing suppliers and changing "
     "everything."),
    ('Automate the rebuild, not the build.',
     'Anyone can install a cluster once. What matters is whether you can lose a site '
     'and rebuild it from a repository and a backup, with no hands on the original. '
     'If the answer involves remembering something, you do not have a platform yet.'),
    ('Count the salary.',
     'A saving that costs one and a half engineers is a real saving only if you write '
     'the one and a half engineers into the comparison. Most repatriations still win '
     'by a wide margin once you do. The ones that do not, you want to know about in '
     'month one rather than month ten.'),
    ('Keep paying for the three things you will not beat.',
     'A global CDN, DDoS scrubbing at the edge, and outbound email deliverability. '
     'Each is a business somebody else is already running better than you will, and '
     'each is cheap next to what it replaces. Ownership is a means, not a principle.'),
    ('The migration is finished when the account is closed.',
     'Not when the traffic moves. An estate with a dormant cloud account still has '
     'the cost, the credentials, the compliance surface and the temptation. The last '
     'Move in this book is closing the account, and until it is done the project is '
     'still open.'),
]
