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
     'Bare metal you own, or dedicated hosts by the month', '22'),
    ('EKS',                  'GKE',                   'AKS',
     'Talos Linux, and Kubernetes you run yourself', '43'),
    ('Fargate',              'Cloud Run',             'Container Apps',
     'Deployments and Jobs on your own nodes', '68'),
    ('Auto Scaling groups',  'Managed instance groups', 'Scale sets',
     'Fixed capacity, priority classes, and a spare shelf', '69'),
    ('AMI',                  'Machine images',        'Managed images',
     'A Talos machine config, applied over the network', '42'),

    # --- data
    ('RDS for PostgreSQL',   'Cloud SQL for PostgreSQL', 'Database for PostgreSQL',
     'PostgreSQL under CloudNativePG, on local NVMe', '73'),
    ('Aurora',               'AlloyDB',               'Cosmos DB for PostgreSQL',
     'PostgreSQL - the storage layer does not come with you', '76'),
    ('RDS for MySQL',        'Cloud SQL for MySQL',   'Database for MySQL',
     'MySQL 8.4 LTS or Percona Server, under an operator', '77'),
    ('ElastiCache',          'Memorystore',           'Azure Cache for Redis',
     'Valkey for the half that is really a cache', '79'),
    ('S3',                   'Cloud Storage',         'Blob Storage',
     'Ceph RGW under Rook - archive stays where it is', '84'),
    ('EBS',                  'Persistent Disk',       'Managed Disks',
     'Ceph RBD under Rook, with local NVMe underneath it', '47'),
    ('EFS',                  'Filestore',             'Azure Files',
     'CephFS under Rook, or a filesystem the application stops needing', '49'),
    ('MSK',                  'Managed Service for Apache Kafka', 'Event Hubs',
     'Kafka under Strimzi - after deleting the ones that were never Kafka', '83'),
    ('SQS and SNS',          'Pub/Sub',               'Service Bus',
     'NATS JetStream, or a table in the database you already have', '81'),
    ('OpenSearch Service',   'Elasticsearch on GKE',  'Azure AI Search',
     'OpenSearch you run - the index is rebuildable', '87'),
    ('DynamoDB',             'Bigtable, Firestore',   'Cosmos DB',
     'PostgreSQL, Cassandra, or keep paying below the threshold', '88'),
    ('Redshift',             'BigQuery',              'Synapse',
     'Keep paying - and bring the lake substrate home', '85'),
    ('AWS Backup',           'Backup for GKE',        'Azure Backup for AKS',
     'Velero, CSI snapshots and pgBackRest, to a third site', '115'),

    # --- the edge
    ('ALB and NLB',          'Cloud Load Balancing',  'Load Balancer',
     'Envoy Gateway on addresses advertised over BGP', '96'),
    ('CloudFront',           'Cloud CDN',             'Azure Front Door',
     'Keep paying - change vendor, not model', '105'),
    ('Route 53',             'Cloud DNS',             'Azure DNS',
     'Two independent authoritative providers, never one', '104'),
    ('ACM',                  'Certificate Manager',   'App Service Certificates',
     'cert-manager with ACME, plus an offline internal root', '97'),
    ('AWS WAF and Shield',   'Cloud Armor',           'Azure WAF and DDoS Protection',
     'Keep paying for scrubbing - the capacity is upstream of you', '106'),
    ('Global Accelerator',   'Premium Tier network',  'Front Door',
     'Your own ASN and address space, or the CDN you kept', '91'),
    ('NAT Gateway',          'Cloud NAT',             'NAT Gateway',
     'Node addresses, and one SNAT hop for the few that need it', '94'),
    ('SES',                  'No first-party equivalent', 'Communication Services',
     'Keep paying for outbound - inbound comes home', '107'),

    # --- the platform
    ('ECR',                  'Artifact Registry',     'Container Registry',
     'A pull-through cache, then Harbor as the registry of record', '58'),
    ('CodeBuild and CodePipeline', 'Cloud Build',     'Azure Pipelines',
     'Ephemeral runners on your own nodes, with a warm cache', '64'),
    ('Secrets Manager',      'Secret Manager',        'Key Vault',
     'External Secrets as a dated bridge, then OpenBao or SOPS', '56'),
    ('KMS',                  'Cloud KMS',             'Key Vault',
     'Named custodians, an HSM or TPM-sealed keys - custody is the hard part', '57'),
    ('IAM roles for service accounts', 'Workload Identity', 'Workload Identity',
     'Your own service-account issuer, federated back to each cloud', '55'),
    ('CloudWatch metrics',   'Cloud Monitoring',      'Azure Monitor',
     'Prometheus, with VictoriaMetrics behind it and a cardinality budget', '62'),
    ('CloudWatch Logs',      'Cloud Logging',         'Log Analytics',
     'Alloy or the OpenTelemetry Collector into Loki', '63'),
    ('X-Ray',                'Cloud Trace',           'Application Insights',
     'OpenTelemetry into Tempo, once every service speaks traceparent', '63'),
    ('Lambda',               'Cloud Functions',       'Functions',
     'CronJobs, Deployments and KEDA - in that order of preference', '89'),
    ('Step Functions',       'Workflows',             'Logic Apps',
     'Argo Workflows or Temporal - and a dated exception for the rest', '90'),
    ('Cost Explorer',        'Cloud Billing reports', 'Cost Management',
     'A model built from invoices, counting power, spares and the rota', '120'),

    # --- the things you were paying a second vendor for
    ('CloudWatch alarms and SNS', 'Cloud Monitoring alerting', 'Azure Monitor alerts',
     'OneUptime - alerting, on-call rotas and escalation', '114'),
    ('Systems Manager Incident Manager', 'No first-party equivalent',
     'No first-party equivalent',
     'OneUptime - incidents, timelines and postmortems', '114'),
    ('No first-party equivalent', 'No first-party equivalent', 'No first-party equivalent',
     'OneUptime - a status page your customers can read', '114'),
    ('Synthetic Canaries',   'Uptime checks',         'Standard availability tests',
     'OneUptime - synthetic and uptime monitoring, from outside the cluster', '114'),
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
