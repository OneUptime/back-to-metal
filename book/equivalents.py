"""What each managed service is called on the three clouds, and what replaces it.

Every Move in the book already names the real service on AWS, Google Cloud and
Azure in its own "Leaving from" block, so this is the map rather than the
content: a reader finds the row they are paying for and it points at the Move.

The right-hand column is the point of the book. Where it says "keep paying",
that is a conclusion, not a gap.

Kept to the services a company of this size actually pays for. If your estate has a row that
is not here, it is either something you can delete or something the book would
have to be longer to cover honestly, and the second is rarer than it looks.
"""

# (AWS, GCP, Azure, what you run instead, move number or None)
ROWS = [
    # --- the machines and the cluster
    ('EC2',                  'Compute Engine',        'Virtual Machines',
     'KVM virtual machines on Proxmox VE hosts', '11'),
    ('EC2 Auto Scaling',     'Managed instance groups', 'Virtual Machine Scale Sets',
     'Fixed capacity, a priority class, and a spare on the shelf', '06'),
    ('EKS',                  'GKE',                   'AKS',
     'Talos and Kubernetes, on hardware or in Proxmox VE guests', '11'),
    ('ECS on Fargate',       'Cloud Run',             'Container Apps',
     'Deployments and Jobs on your own nodes', '14'),
    ('AMI',                  'Machine images',        'Managed images',
     'KVM guest templates; rebuild or rehearse a supported disk import', '14'),
    ('VPC',                  'VPC networks',          'Virtual Network',
     'Two switches, separate address ranges, and a documented routing plan', '10'),

    # --- storage and data
    ('EBS',                  'Persistent Disk',       'Managed Disks',
     'Proxmox VM disks on Ceph RBD; Rook volumes for Kubernetes', '12'),
    ('EFS',                  'Filestore',             'Azure Files',
     'CephFS under Rook, or a filesystem the application stops needing', '12'),
    ('S3',                   'Cloud Storage',         'Blob Storage',
     "Ceph's S3 gateway - deep archive stays where it is", '15'),
    ('RDS for PostgreSQL',   'Cloud SQL for PostgreSQL', 'Database for PostgreSQL',
     'PostgreSQL under CloudNativePG, on local NVMe', '16'),
    ('ElastiCache',          'Memorystore',           'Azure Cache for Redis',
     'Valkey for the half that is really a cache', '15'),
    ('SQS and SNS',          'Pub/Sub',               'Service Bus',
     'NATS JetStream, or a table in the database you already have', '15'),
    ('Glacier Deep Archive', 'Archive storage class', 'Archive tier',
     'Keep paying where retrieval, retention and migration costs justify it', '15'),
    ('AWS Backup',           'Backup and DR Service', 'Azure Backup',
     'Whole-VM backups, Velero and database archives, held off-site', '19'),

    # --- the edge
    ('Application Load Balancer', 'Cloud Load Balancing', 'Application Gateway',
     'Envoy Gateway behind a virtual IP that fails over', '17'),
    ('ACM',                  'Certificate Manager',   'Key Vault certificates',
     'cert-manager, with renewal failures and expiry monitored', '17'),
    ('Route 53',             'Cloud DNS',             'Azure DNS',
     'Managed authoritative DNS; rehearse changes separately from cutover', '18'),
    ('NAT Gateway',          'Cloud NAT',             'NAT Gateway',
     'Node addresses, and one translation hop for the few that need it', '18'),
    ('CloudFront',           'Cloud CDN',             'Azure Front Door',
     'Keep paying - change vendor, not model', '04'),
    ('AWS Shield and WAF',   'Cloud Armor',           'Azure DDoS Protection and WAF',
     'Keep paying for scrubbing - the capacity is upstream of you', '04'),
    ('SES',                  'No first-party equivalent', 'Communication Services',
     'Keep paying for outbound - inbound can come home', '04'),

    # --- the platform
    ('ECR',                  'Artifact Registry',     'Container Registry',
     'A pull-through cache, then your own registry of record', '13'),
    ('Secrets Manager',      'Secret Manager',        'Key Vault',
     'Encrypted in the repository, with the key held outside the cluster', '13'),
    ('CodeBuild',            'Cloud Build',           'Azure Pipelines',
     'Isolated build runners, or the existing hosted CI service', '13'),
    ('CloudWatch metrics',   'Cloud Monitoring',      'Azure Monitor',
     'Prometheus, with a cardinality budget agreed in advance', '19'),
    ('CloudWatch Logs',      'Cloud Logging',         'Log Analytics',
     'Loki, sized against retention somebody actually chose', '19'),
    ('CloudWatch alarms',    'Cloud Monitoring alerting', 'Azure Monitor alerts',
     'OneUptime - alerting, on-call rotas, incidents and a status page', '19'),
    ('Cost Explorer',        'Cloud Billing reports', 'Cost Management',
     'A model built from invoices, counting power, spares and the rota', '03'),
    ('Organizations',        'Organisation and projects', 'Subscriptions and Entra',
     'Retire empty accounts; keep those that own retained services or records', '20'),
]

CLOUDS = ['AWS', 'Google Cloud', 'Azure']


def keep_paying():
    """The rows whose honest answer is that somebody else should keep running it."""
    return [r for r in ROWS if r[3].lower().startswith('keep paying')]


def check(moves):
    """Every move number referenced here must exist. Called by verify.py."""
    have = {m['num'] for m in moves}
    return [f'equivalents.py references move {r[4]}, which does not exist'
            for r in ROWS if r[4] and r[4] not in have]
