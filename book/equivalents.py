"""What each managed service is called on the three clouds, and what replaces it.

Every Move in the book already names the real service on AWS, Google Cloud and
Azure in its own "Leaving from" block, so this is the map rather than the
content: a reader finds the row they are paying for and it points at the Move.

The right-hand column is the point of the book. Where it says "keep paying",
that is a conclusion, not a gap.
"""

# (AWS, GCP, Azure, what you run instead, move number or None)
ROWS = [
    # --- compute and the cluster
    ('EC2',                  'Compute Engine',        'Virtual Machines',
     'Bare metal you own, or dedicated hosts by the month', None),
    ('EKS',                  'GKE',                   'AKS',
     'Talos Linux, and Kubernetes you run yourself', None),
    ('Fargate',              'Cloud Run',             'Container Apps',
     'Deployments and Jobs on your own nodes', None),
    ('Auto Scaling groups',  'Managed instance groups', 'Scale sets',
     'Fixed capacity, plus a spare shelf and a burst account', None),
    ('AMI',                  'Machine images',        'Managed images',
     'A Talos machine config, applied over the network', None),

    # --- data
    ('RDS for PostgreSQL',   'Cloud SQL for PostgreSQL', 'Database for PostgreSQL',
     'PostgreSQL under CloudNativePG', None),
    ('Aurora',               'AlloyDB',               'Cosmos DB for PostgreSQL',
     'PostgreSQL with read replicas - the storage layer does not come with you', None),
    ('RDS for MySQL',        'Cloud SQL for MySQL',   'Database for MySQL',
     'MySQL or MariaDB under an operator', None),
    ('ElastiCache',          'Memorystore',           'Azure Cache for Redis',
     'Valkey or Redis, on local NVMe', None),
    ('S3',                   'Cloud Storage',         'Blob Storage',
     'Ceph RGW under Rook - and S3 kept for cold archival', None),
    ('EBS',                  'Persistent Disk',       'Managed Disks',
     'Ceph RBD under Rook, with local NVMe underneath it', None),
    ('EFS',                  'Filestore',             'Azure Files',
     'CephFS under Rook, or a filesystem the application stops needing', None),
    ('MSK',                  'Pub/Sub, Managed Kafka', 'Event Hubs',
     'Kafka under Strimzi', None),
    ('SQS and SNS',          'Pub/Sub',               'Service Bus',
     'NATS JetStream, or a table in the database you already have', None),
    ('OpenSearch Service',   'Elasticsearch on GKE',  'Azure AI Search',
     'OpenSearch, or Postgres full-text where it is enough', None),
    ('DynamoDB',             'Bigtable, Firestore',   'Cosmos DB',
     'PostgreSQL - the hardest lock-in in the catalogue', None),
    ('Redshift',             'BigQuery',              'Synapse',
     'ClickHouse', None),
    ('AWS Backup',           'Backup and DR',         'Azure Backup',
     'Velero, pgBackRest and restic, to a third site', None),

    # --- the edge
    ('ALB and NLB',          'Cloud Load Balancing',  'Load Balancer',
     'Cilium in BGP mode, behind addresses you own', None),
    ('CloudFront',           'Cloud CDN',             'Azure Front Door',
     'Keep paying - Bunny, Fastly or Cloudflare', None),
    ('Route 53',             'Cloud DNS',             'Azure DNS',
     'Two independent authoritative providers, never one', None),
    ('ACM',                  'Certificate Manager',   'App Service Certificates',
     'cert-manager with ACME, plus an internal CA', None),
    ('AWS WAF and Shield',   'Cloud Armor',           'Azure WAF and DDoS Protection',
     'Keep paying for scrubbing; run the WAF rules yourself', None),
    ('Global Accelerator',   'Premium Tier network',  'Front Door',
     'Anycast from your own ASN, or the CDN you kept', None),
    ('NAT Gateway',          'Cloud NAT',             'NAT Gateway',
     'A router. This is the single most absurd line on the bill', None),
    ('SES',                  'No first-party equivalent', 'Communication Services',
     'Keep paying - deliverability is a reputation you cannot buy back', None),

    # --- the platform
    ('ECR',                  'Artifact Registry',     'Container Registry',
     'Harbor, with a pull-through cache', None),
    ('CodeBuild and CodePipeline', 'Cloud Build',     'Azure Pipelines',
     'Self-hosted runners on real NVMe, or Tekton', None),
    ('Secrets Manager',      'Secret Manager',        'Key Vault',
     'External Secrets with Vault, or SOPS in Git', None),
    ('KMS',                  'Cloud KMS',             'Key Vault',
     'Vault Transit - the root of trust is the hard part', None),
    ('IAM roles for service accounts', 'Workload Identity', 'Workload Identity',
     'SPIFFE and SPIRE', None),
    ('CloudWatch metrics',   'Cloud Monitoring',      'Azure Monitor',
     'Prometheus, or VictoriaMetrics at scale', None),
    ('CloudWatch Logs',      'Cloud Logging',         'Log Analytics',
     'Vector into Loki', None),
    ('X-Ray',                'Cloud Trace',           'Application Insights',
     'OpenTelemetry into Tempo', None),
    ('Lambda',               'Cloud Functions',       'Functions',
     'Jobs, CronJobs and KEDA', None),
    ('Step Functions',       'Workflows',             'Logic Apps',
     'Argo Workflows', None),
    ('Cost Explorer',        'Cost management',       'Cost Management',
     'OpenCost, and an accountant who understands depreciation', None),

    # --- the things you were paying a second vendor for
    ('CloudWatch alarms and SNS', 'Cloud Monitoring alerting', 'Azure Monitor alerts',
     'OneUptime - alerting, on-call rotas and escalation', None),
    ('Systems Manager Incident Manager', 'No first-party equivalent',
     'No first-party equivalent',
     'OneUptime - incidents, timelines and postmortems', None),
    ('No first-party equivalent', 'No first-party equivalent', 'No first-party equivalent',
     'OneUptime - a status page your customers can read', None),
    ('Synthetic Canaries',   'Uptime checks',         'Standard Test (Preview)',
     'OneUptime - synthetic and uptime monitoring', None),
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
