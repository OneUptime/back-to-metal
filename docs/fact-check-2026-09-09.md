# Book fact-check and edition agreement review

Reviewed 9 September 2026. The review covers every section of all twenty Moves, the shared introduction, reference kit, rollback guidance, cloud-equivalence map, economic assumptions, schedule, publication metadata and generated editions.

This is a documentation, source-code, arithmetic and publication review. It is **not an executed production migration**. The changed runbooks require rehearsal against the reader's own estate before use. Version compatibility was checked against official release/support records; a compatible version matrix does not establish that a deployment has passed failure and recovery tests.

## Findings and scope

- Corrected provider-specific extraction, inventory, networking and deletion claims across AWS, Google Cloud and Azure. All twenty Moves received substantiated corrections or qualifications.
- Repaired unsafe state-transfer and rollback guidance, including object overwrites, expiring cache state, queue retries, PostgreSQL roles/replica identities, independent backup recovery and destructive account cleanup. Final cleanup is now labelled irreversible.
- Replaced unsupported precise fleet outcomes (availability, latency, repairs and labour) with measurement criteria. No underlying report was supplied or found in this repository. Those figures should return only with their measurement scope and a traceable source. Cover claims now identify estimated labour and rollback limits; the closing advice count is derived from its actual entries.
- Preserved the illustrative financial model while making its limits explicit: one site with off-site recovery; equal operating hours assumed; VM support and any required second site priced separately; transition labour, overlapping cloud bills, financing and taxes excluded from steady-state totals. Hardware, facility and rental amounts remain quote-dependent allowances.
- Corrected the calendar-wait units and scheduling of independent work. Labour is unchanged; dates remain estimates without a start-date calendar, public holidays or maintenance-window booking.
- Restored the Kindle edition's missing cloud-extraction sections, shared decision/cost material and Move links; derived its rule count. Both the default build and a standalone website build now regenerate the EPUB before the website copies it.
- Added checks for complete Move text and exact risk/cutover/reversibility metadata across print HTML, EPUB and web, and byte-for-byte equality of website PDF/EPUB downloads with their built originals. Added regression checks for the demonstrated omissions, scheduling errors and publishing arithmetic.
- Replaced the non-resolving printed address with `backtometal.oneuptime.com`. The live OneUptime and Firebase URLs both served v6.4.3 during this review. This PR changes the repository artifacts; it does not deploy the live website.

## Shared claims and publishing sources

- [EC2 CPU topology](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html): a vCPU may be an SMT thread or a physical core; it is not universally half a shared core. No fixed latency gain follows from buying hardware.
- [GKE maintenance exclusions](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/maintenance-windows-and-exclusions): upgrade deferral depends on exclusion scope and support policy, not a universal ninety-day maximum. Owning the platform still requires supported software and firmware.
- [EKS pricing](https://aws.amazon.com/eks/pricing/) and [GKE pricing](https://cloud.google.com/kubernetes-engine/pricing): the standard base management fee is $0.10 per cluster-hour, with product-specific credits and extended-support charges. This does not price every managed service or every region.
- [KDP paperback costs](https://kdp.amazon.com/en_US/help/topic/G201834340): confirmed the configured US large-trim colour rates and corrected the premium-colour 24–40-page fixed-price band. [Print royalties](https://kdp.amazon.com/en_US/help/topic/G201834330) use 50% below $9.99 and 60% from $9.99 on Amazon.com; the calculator now handles that threshold.
- [KDP ebook royalties](https://kdp.amazon.com/en_US/help/topic/G200644210): delivery belongs inside the royalty multiplier. [The current US 70% band](https://kdp.amazon.com/en_US/help/topic/G200634560) is $2.99–$12.99 and was already correct. Converted file size, account eligibility and other-marketplace terms still need checking in KDP.
- [KDP print options](https://kdp.amazon.com/en_US/help/topic/G201834180) and [hardcover costs](https://kdp.amazon.com/en_US/help/topic/GHT976ZKSKUXBB6H): the rebuilt 72-page interior meets the standard-colour paperback minimum, but remains below the 75-page hardcover minimum. Hardcover case dimensions, ISBN registration and final print list prices remain deliberate publishing decisions. This review does not create or register them.

## Validation

The structure and content gates report no findings across all twenty Moves. Twenty-one regression tests cover content/metadata agreement, scheduling and publishing arithmetic, including prices immediately below required margins. Final build, print, browser and generated-file checks are recorded in the PR description.

The separate publishing-price gate still fails on existing, intentional publication decisions: no paperback list price is configured, and the 72-page interior is below KDP's 75-page hardcover minimum. Hardcover case dimensions and publication metadata require the stated human steps. These are not covered by the passing build gates.

No deployment, account closure, live database operation or infrastructure purchase was performed. Publication validation cannot certify the operational or financial outcome for a reader's actual workload. The repository's EPUB structural checks are not a substitute for the final EPUBCheck and Kindle Previewer publishing checks.

## Coverage and corrections

| Move | Result |
|---|---|
| 01 · Billing and measurement | Corrected BigQuery backfill: a first export into US/EU multi-regions includes the current and previous month; supported single regions begin when enabled. Separated Cost Explorer's paid hourly history from daily resource detail. Corrected Azure amortised-cost support to include MCA and identified management-group omissions. Changed raw-line ranking into monthly workload aggregation, retained shared costs and cheap dependencies, and required invoice reconciliation. Removed unsupported 80% concentration, 5–15% waste, five-machine scale and fixed monitoring-cost assertions. Sampling now accounts for omitted month-end/seasonal peaks and agent overhead. |
| 02 · Inventory | Changed AWS inventory from capped Search to paginated ListResources, and required complete scopes, supported-type checks and continuation handling. Corrected the assertion that queues/jobs never appear in inventory APIs. Removed unsupported service counts and presumed waste. Resource deletion now checks ownership, dependencies, retention and required recoverable state; an orphaned snapshot is not automatically disposable. |
| 03 · Economic decision | Confirmed separate public/account-aware AWS calculators. Corrected Google Cloud's calculator to acknowledge billing-account pricing and its documented sustained-use/committed-use distinction. Acknowledged Azure EA and MCA negotiated prices. The comparison must match availability/recovery objectives and price VM-specific costs. Equal recurring labour is explicitly a reference assumption to validate; removed an unsupported 10% shortcut guarantee and speculative pay savings. |
| 04 · Retained services | Confirmed Shield Advanced's $3,000 base monthly fee and one-year commitment; clarified that a protected distribution can still front an external rack without protecting direct rack traffic. Confirmed Cloud CDN external internet NEG support and Azure Standard/Premium WAF differences. Kept suitable existing edge/mail providers instead of requiring gratuitous migration. Corrected SPF/DKIM/DMARC wording, dedicated-IP warm-up, domain-versus-IP reputation, contract reversibility and overlap costs. $5,200 is now labelled the reference allowance. |
| 05 · CPU/memory sizing | Confirmed family-specific SMT, T3 baseline and Azure B-series credit behaviour. Corrected the reversed claim about halving Arm counts; some x86 families also expose a vCPU per core. Added Google Cloud extended-memory exception and actual T3 mode checks. Preserved workload benchmarking and failure headroom. Replaced blanket PostgreSQL single-core, fixed over-sizing and drive-IOPS guarantees with measured constraints. |
| 06 · Fleet procurement | Confirmed regional EC2 quota controls and immutable Google instance templates; made existing-instance rollout explicit. Replaced the blanket Azure fault-domain claim with documented zonal Flexible-set behaviour. Corrected 32 cores to total per machine, made memory population vendor-approved and balanced, and qualified the single-host-loss arithmetic: capacity percentage alone proves neither quorum nor service survival. Removed unsupported lease/delivery predictions. |
| 07 · Facility | Corrected AWS AZ-letter mapping to older accounts/some regions and recommended consistent AZ IDs. Replaced the false assertion that Azure non-zonal VMs cannot migrate into zones. Confirmed Google regional quotas do not guarantee zonal availability. Preserved the arithmetic 16 × 450 W = 7.2 kW while making 10 kW provisional against measured fleet/switch/recovery load and feed limits. Explicitly distinguished off-site backups from site availability, priced independent recovery where required, removed the false universal doubling/timing claims, and put contractual liability at binding agreement rather than facility commencement. Procurement can still run alongside Move 06 using provisional quotes. |

## Primary sources

### Move 01

- [AWS Cost Explorer hourly pricing](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/pricing/) and [daily resource-level detail](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-resource-daily.html).
- [AWS CUR 2.0 resource-granularity configuration](https://docs.aws.amazon.com/cur/latest/userguide/table-dictionary-cur2.html).
- [Google Cloud BigQuery billing export, locations and backfill](https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery).
- [Microsoft improved exports: agreement/scope support and exclusions](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-improved-exports) and [cost-data coverage](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data).
- [Google metric billing by bytes or samples](https://docs.cloud.google.com/monitoring/docs/metrics-management), [Azure monitoring cost components](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/cost-usage), [CloudWatch agent metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/metrics-collected-by-CloudWatch-agent.html).

### Move 02

- [AWS ListResources CLI pagination](https://docs.aws.amazon.com/cli/latest/reference/resource-explorer-2/list-resources.html), [Search's 1,000-result ceiling](https://docs.aws.amazon.com/resource-explorer/latest/apireference/API_Search.html), [multi-account setup](https://docs.aws.amazon.com/resource-explorer/latest/userguide/manage-service-multi-account.html).
- [Google Cloud search permission and scope](https://docs.cloud.google.com/asset-inventory/docs/reference/rest/v1/TopLevel/searchAllResources) and [supported asset types, including Cloud Tasks queues](https://docs.cloud.google.com/asset-inventory/docs/asset-types).
- [Azure Resource Graph access scope](https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview) and [REST pagination](https://learn.microsoft.com/en-us/rest/api/azureresourcegraph/resourcegraph/resources/resources?view=rest-azureresourcegraph-resourcegraph-2024-04-01).

### Move 03

- [AWS pricing-calculator experiences and existing commitments](https://docs.aws.amazon.com/cost-management/latest/userguide/pricing-calculator.html).
- [Google Cloud calculator sign-in for account pricing](https://cloud.google.com/products/calculator) and [sustained-use applicability/non-stacking](https://docs.cloud.google.com/compute/docs/sustained-use-discounts).
- [Azure calculator agreement price sheets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/pricing-calculator).

### Move 04

- [Shield Advanced subscription and usage charges](https://aws.amazon.com/shield/pricing/).
- [Cloud CDN external internet NEG origins](https://docs.cloud.google.com/cdn/docs/external-backends-internet-neg-overview).
- [Front Door managed/custom WAF rule tiers](https://learn.microsoft.com/en-us/azure/frontdoor/web-application-firewall).
- [SES DMARC alignment](https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dmarc.html), [shared versus dedicated sending](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip.html), [dedicated-IP warm-up](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip-warming.html), [domain and IP reputation on migration](https://aws.amazon.com/blogs/messaging-and-targeting/guide-to-ip-and-domain-warming-and-migrating-to-amazon-ses/).

### Move 05

- [EC2 CPU topology/options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html), [T3 baseline and Dedicated Host exception](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html).
- [Google custom machine types and extended memory](https://docs.cloud.google.com/compute/docs/instances/creating-instance-with-custom-machine-type).
- [Azure B-series credit model](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/b-series-cpu-credit-model).
- [PostgreSQL parallel-query support and limits](https://www.postgresql.org/docs/17/when-can-parallel-query-be-used.html).

### Move 06

- [EC2 regional quotas](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html), [Auto Scaling quotas](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-quotas.html).
- [Google MIG controlled updates](https://docs.cloud.google.com/compute/docs/instance-groups/rolling-out-updates-to-managed-instance-groups).
- [Azure scale-set fault-domain spreading](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-manage-fault-domains).
- [Dell R6625 memory population rules](https://www.dell.com/support/manuals/en-us/poweredge-r6625/r6625_ism/general-memory-module-installation-guidelines?guid=guid-edec5a2b-f490-44cf-9f59-e4650b8b2071&lang=en-us). Twelve channels per CPU and supported identical DIMMs demonstrate why a universal dual-socket 256 GB/all-channels rule is not valid across modern platforms.

### Move 07

- [AWS AZ IDs and the account/region mapping exceptions](https://docs.aws.amazon.com/global-infrastructure/latest/regions/az-ids.html).
- [Google regional quotas versus zonal availability](https://docs.cloud.google.com/compute/resource-usage).
- [Azure regional-to-zonal VM migration, restrictions and downtime](https://learn.microsoft.com/en-us/azure/virtual-machines/migrate-to-availability-zone). The current direct path is public preview; wording deliberately requires a supported migration path rather than implying universal in-place support.


## 08 — The order and the queues

Fixed the claim that Partner Interconnect means no customer access circuit/cross-connect is needed: the partner owns its connection to Google, while the customer must reach the partner. Scoped the 90-day authorisation expiry to AWS rather than all clouds. Removed unsupported universal delivery/ASN lead times. Corrected the retirement gate: facility transit cannot be removed while it alone routes the facility-assigned addresses; independent upstream failover needs accepted portable space and routing authority, regardless of site count. The four-week wait is now explicitly a planning allowance to replace with carrier promises.

Confirmed AWS LOA-CFA expires at 90 days and can be downloaded again; ExpressRoute begins billing when its service key is issued. Ordering/termination terms remain contract-specific.

Sources: [AWS cross-connects](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Colocation.html), [Partner Interconnect](https://docs.cloud.google.com/network-connectivity/docs/interconnect/concepts/partner-overview), [ExpressRoute provisioning](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-howto-circuit-portal-resource-manager).

## 09 — Racking day

Removed unsupported twenty-minute proof and $150/hour universal remote-hands claims. Clarified serial console is not a physical-controller virtual-media facility; AWS support includes supported bare-metal types rather than only an undifferentiated Nitro class. Scoped Azure boot-diagnostics defaults to portal-created VMs. Added full-load capacity verification for each power feed, unique controller credentials and explicit shared-NIC isolation checks; replaced the inaccurate claim controllers automatically answer on every interface.

Confirmed Google Cloud's serial-port-enable setting can be overridden by organisation policy and Azure serial access has independent permissions/subscription controls. Remote-console, firmware and power drills must still be executed on the actual purchased models, including any virtual-media licences.

Sources: [EC2 prerequisites](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-serial-console-prerequisites.html), [Google Cloud serial console](https://docs.cloud.google.com/compute/docs/troubleshooting/troubleshooting-using-serial-console), [Azure boot diagnostics](https://learn.microsoft.com/en-us/azure/virtual-machines/boot-diagnostics), [Azure console controls](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/serial-console-enable-disable).

## 10 — Network and recovery access

Fixed Google Cloud MTU guidance: stop all attached VMs before changing network MTU, then start them; a guest reboot does not suffice and Windows requires interface configuration. Scoped the AWS 9001-byte MTU to supported paths and retained the internet-gateway 1500 limit. Added Kubernetes pod/service ranges to the non-overlap plan. Distinguished IP MTU from switch frame overhead and tunnel overhead instead of demanding one identical numeric value everywhere. Removed fabricated five-per-cent failure frequency and added path-MTU-discovery ICMP checks.

Confirmed Azure does not support broadcast/multicast; retained the independent out-of-band recovery path and switch failure drill.

Sources: [Google Cloud change MTU](https://docs.cloud.google.com/vpc/docs/change-mtu-vpc-network), [AWS MTU](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-mtu.html), [Azure network FAQ](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-faq), [Cilium system requirements](https://docs.cilium.io/en/stable/operations/system_requirements/).

## 11 — Platform

Confirmed Proxmox VE 9.2-1 is a published current installer. Pinned Talos 1.14.0, Kubernetes 1.35.8 and Cilium 1.20.1 for an overlapping supported baseline with later Moves. Talos 1.14's docs page was unavailable, so its tagged compatibility source was checked directly: Kubernetes >=1.32.0 and <1.37.99 is accepted; the official 1.14 release exists. Corrected the plaintext Git instruction: generated Talos files contain CA/private keys and now stay in an encrypted external credential store, with only non-secret patches in Git. Disabled default CNI before Cilium and used KubePrism localhost:7445 with the documented Talos capability/cgroup settings and Kubernetes IPAM. Added cert-manager v1.21.1/CRDs/readiness before the Barman plugin needs it in Move 16. Corrected rollback's unsupported promise that reversing one kube-proxy flag repairs every network path.

Retained three physical failure domains, separate host/guest patching, compatible migration CPU models, and explicit restart-versus-live-migration distinction. These tests require an actual cluster.

Sources: [Proxmox downloads](https://proxmox.com/en/downloads/proxmox-virtual-environment), [Talos release](https://github.com/siderolabs/talos/releases/tag/v1.14.0), [Talos compatibility constants](https://github.com/siderolabs/talos/blob/v1.14.0/pkg/machinery/compatibility/talos114/talos114.go), [Talos generated secrets](https://docs.siderolabs.com/talos/v1.8/getting-started/prodnotes), [Kubernetes release](https://github.com/kubernetes/kubernetes/releases/tag/v1.35.8), [Cilium Kubernetes requirements](https://docs.cilium.io/en/stable/network/kubernetes/requirements/), [Cilium Talos install](https://docs.cilium.io/en/stable/installation/k8s-install-helm/), [cert-manager Helm install](https://cert-manager.io/docs/installation/helm/).

## 12 — Storage

Fixed Filestore's false never-shrinks claim: basic cannot shrink, while zonal/regional/enterprise tiers can. Distinguished Azure Premium SSD v1 performance tiers from v2's separately provisioned performance. Replaced unsupported Rook 1.16.9 with 1.20.7 and pinned Ceph 20.2.4; Rook's current release notes require current versions for the CephX security fix, and the compatibility matrix includes Kubernetes 1.35. Corrected retirement prose that conflated object buckets with block volumes/file shares.

Confirmed external Rook clients require separately provisioned RBD/CephFS/RGW services and credentials, and their capabilities do not follow merely from having an RBD pool. Retained single device ownership, host failure domains, recovery headroom, no ordinary live migration for passthrough devices, and independent restore testing.

Sources: [Filestore editing](https://docs.cloud.google.com/filestore/docs/editing-instances), [Azure disk billing/performance](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-understand-billing), [Rook maintenance/support](https://rook.io/docs/rook/latest-release/Getting-Started/maintenance-and-support/), [Rook releases/advisory](https://github.com/rook/rook/releases), [external cluster](https://rook.io/docs/rook/v1.14/CRDs/Cluster/external-cluster/external-cluster/), [Ceph storage resource separation](https://www.rook.io/docs/rook/latest-release/Getting-Started/example-configurations/).

## 13 — Registry, secrets, deployment

Fixed Key Vault retention from always 90 days to configured 7–90 days. Clarified AWS scheduled secret deletion default/range. Confirmed Google Cloud enabled and disabled secret versions remain billable until destroyed. Fixed Harbor cache-to-primary instructions: proxy-cache projects cannot accept pushes, so a separate normal project is required. Added upstream adapter/authentication verification, database backup and digest checks; the docs do not list every Artifact Registry configuration as supported.

Updated pinned Harbor to 2.15.2/chart1.19.2; Argo CD to 3.5.2/chart10.8.4; named GitHub Actions Runner Controller and both required charts at0.14.2. Added runner registration/credential/image requirements and isolation from production. Added Argo automated self-healing/namespace recreation configuration so the deletion drill can actually restore desired objects. Kept cloud artifacts current during trial and made platform bootstrap images independent of Harbor to break the boot cycle. Staging data restore remains explicit.

Sources: [Key Vault retention](https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview), [AWS secret deletion](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_delete-secret.html), [Secret Manager pricing](https://cloud.google.com/secret-manager/pricing), [Harbor proxy cache](https://goharbor.io/docs/main/administration/configure-proxy-cache/), [Harbor chart release](https://github.com/goharbor/harbor-helm/releases/tag/v1.19.2), [Argo chart/app mapping](https://github.com/argoproj/argo-helm/blob/argo-cd-10.8.4/charts/argo-cd/Chart.yaml), [ARC deployment](https://docs.github.com/en/actions/how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets), [ARC release](https://github.com/actions/actions-runner-controller/releases/tag/gha-runner-scale-set-0.14.2).

## 14 — First service

Confirmed AWS instance export restrictions for Marketplace/third-party licensed images and encrypted EBS; Google-provided Windows Server licences cannot be exported for external use; Azure direct disk download needs the VM stopped while snapshots of running VMs are crash-consistent. The existing fresh-VM/stateless parallel path and explicit persistent-write rollback caution are appropriate. Added a working TLS endpoint through the existing edge, verified service-port exposure and health checks before the traffic ramp; otherwise this Move silently needed the edge introduced only in Move 17.

The one/ten/fifty/full traffic stages, business-day holds, week soak and eight-week reference allowance are operator planning choices rather than independently established guarantees. DNS-weight accuracy and actual request split must be measured on the deployed service.

Sources: [AWS export restrictions](https://docs.aws.amazon.com/vm-import/latest/userguide/vmexport-limits.html), [Google Cloud image export](https://docs.cloud.google.com/compute/docs/images/export-image), [Azure VHD download](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/download-vhd).


## Move 15 — Buckets, cache and queues

Fixed the unsafe object endpoint switch followed by a blind final source copy; it could overwrite new destination writes or resurrect deleted data. The live route now requires an ordered durable change journal, content verification, a rehearsed writer handoff and reverse replay, with old upload paths fenced. A write-stop window or retaining the service is required where that route is unavailable. This is an engineering consequence of the documented copy and messaging semantics, not a claim that a generic journal implementation already exists in this repository.

Corrected the assumption that an expiring Redis key is disposable cache: sessions, locks and counters can expire too, and PostgreSQL replication in Move 16 does not migrate them. Added durable outbox retries, shared processing deduplication, delayed/in-flight work and independent retention for queue rollback. Removed the false claim that queued copies remain for thirty days; SQS permits at most fourteen. Confirmed SQS's current 1 MiB payload ceiling, Pub/Sub per-subscription copies, and Service Bus Standard/Premium session and duplicate-detection support. Replaced the one-year S3 presigned-link example with its seven-day Signature Version 4 maximum and shorter temporary-credential limit. Made archive retention a cost comparison, not a universal economic conclusion.

Sources:

- [rclone S3 hashes and multipart/encryption limitations](https://rclone.org/s3/)
- [SQS CreateQueue: payload and retention limits](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html)
- [S3 presigned URL lifetime](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)
- [Pub/Sub subscription overview](https://docs.cloud.google.com/pubsub/docs/subscription-overview)
- [Service Bus sessions](https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-sessions)
- [Service Bus duplicate detection](https://learn.microsoft.com/en-us/azure/service-bus-messaging/duplicate-detection)
- [Valkey EXPIRE](https://valkey.io/commands/expire/) and [expiring locks with SET](https://valkey.io/commands/set/)
- [JetStream consumer acknowledgements](https://github.com/nats-io/nats.docs/blob/master/nats-concepts/jetstream/consumers.md) and [delivery/deduplication semantics](https://github.com/nats-io/nats.docs/blob/master/nats-concepts/jetstream/README.md)

## Move 16 — Postgres

Corrected the incompatible CloudNativePG 1.25/Barman plugin requirement. The documented baseline is CloudNativePG 1.30.0, Barman plugin 0.15.0 and cert-manager 1.21.1, coordinated with the platform reviewer. The plugin requires operator 1.26 or later and an installed cert-manager. Added roles/grants, replica identity, an explicit DDL freeze, complete table synchronization and fenced writer handoff. Kept indexes instead of deferring them without ever rebuilding them. Backup restoration now uses an independent copy in isolation, disables outgoing jobs/subscriptions, and compares to the recorded recovery point rather than a changing production database. The final published transaction is verified on the subscriber; no comparison of unrelated local WAL positions is proposed.

Corrected the parallel-copy advice: one subscription already supports parallel initial table copies, while splitting related tables across subscriptions sacrifices their transaction boundary. Corrected slot cleanup: ordinary subscription removal drops its source slot, but disabled, detached or orphaned slots can retain WAL. Removed the circular instruction to wait for billing to disappear before shutting down a still-billing instance. Clarified Cloud SQL restart/growth behaviour and Azure extension preload/restart requirements. Updated the exemplar to teach the same safe procedure.

Sources:

- [CloudNativePG supported versions](https://cloudnative-pg.io/docs/1.30/supported_releases/)
- [CloudNativePG 1.30.0 release](https://cloudnative-pg.io/docs/1.30/release_notes/v1.30/)
- [Barman plugin requirements and installation](https://cloudnative-pg.io/plugin-barman-cloud/docs/installation/)
- [PostgreSQL logical replication](https://www.postgresql.org/docs/current/logical-replication.html)
- [Replication restrictions](https://www.postgresql.org/docs/17/logical-replication-restrictions.html)
- [Parallel copy configuration](https://www.postgresql.org/docs/16/logical-replication-config.html)
- [Replication-slot lifecycle](https://www.postgresql.org/docs/17/logical-replication-subscription.html)
- [RDS replication parameter/reboot](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.Replication.ReadReplicas.LogicalDecoding.html)
- [Cloud SQL logical decoding](https://docs.cloud.google.com/sql/docs/postgres/replication/configure-logical-replication)
- [Azure extension allowlist](https://learn.microsoft.com/en-us/azure/postgresql/extensions/how-to-allow-extensions) and [preloaded libraries](https://learn.microsoft.com/en-us/azure/postgresql/extensions/how-to-load-libraries)

## Move 17 — Front door

Preserved the parallel edge rehearsal and VM/Kubernetes alternatives. Changed expired Envoy Gateway 1.4 and cert-manager 1.17 upstream releases to documented pins compatible with the new Kubernetes baseline. Added multiple data-plane replicas on separate hosts, SNI/hostname certificate verification and observed-behaviour tests for overlapping routes. ACM validation records are needed while certificates require renewal, not forever; Azure Key Vault access loss can disable affected HTTPS listeners rather than necessarily the entire gateway. Removed AWS-specific capacity-unit billing language from the cross-cloud general statement. Confirmed Google reserved static addresses are independent resources that remain reserved until released.

Sources:

- [Envoy Gateway compatibility and EOL matrix](https://gateway.envoyproxy.io/news/releases/matrix/) and [1.8.4 release](https://gateway.envoyproxy.io/news/releases/notes/v1.8.4/)
- [cert-manager support policy](https://cert-manager.io/docs/releases/) and [1.21.1 release](https://github.com/cert-manager/cert-manager/releases/tag/v1.21.1)
- [ACM DNS renewal conditions](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html)
- [Application Gateway/Key Vault certificates](https://learn.microsoft.com/en-us/azure/application-gateway/key-vault-certs)
- [Google static address lifetime](https://docs.cloud.google.com/vpc/docs/reserve-static-external-ip-address)

## Move 18 — Go-live

Corrected Azure's invalid zero-weight instruction: Traffic Manager accepts weights 1–1000, so an endpoint is disabled and re-enabled for removal/return. Route 53 all-zero weights are treated equally, and health checks can revive a zero-weight fallback. DNS weights govern answers rather than an exact request percentage. Added waiting out the prior TTL across the entire DNS chain. Preserved the sound invariant that both edges reach one authoritative writable system. Added explicit pre-production gates for restored off-site backups and an external failure probe reaching on-call; Move 19 completes the full drill rather than delaying basic protection until after cutover. Policy removal now first leaves a working destination DNS record; egress does not vanish if retained cloud workloads still communicate.

Sources:

- [Route 53 weighted routing and health checks](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-weighted.html)
- [Cloud DNS record-set API](https://docs.cloud.google.com/dns/docs/reference/rest/v1/resourceRecordSets)
- [Traffic Manager weighted routing](https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-routing-methods)
- [Traffic Manager TTL and caching](https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-faqs)

## Move 19 — Backups and pager

Corrected Azure's fixed fourteen-day claim to configurable 14–180-day enhanced soft-delete retention and qualified AWS compliance vault lock with its grace period and account-closure exception. Required actual volume-data movement because a CSI snapshot remaining on the primary storage does not survive its loss. Added private repository credentials, full database backup/WAL chains, consistent checkpoints before copying mutable repositories, object-lock/maintenance validation and independent key custody. Removed the dangerous rollback instruction to disable destination backups in favour of old-cloud backups, which lack destination writes. Removed the unsubstantiated claim that automating a restore makes the second run take an afternoon. Distinguished metric series from log-stream cardinality and retained the OneUptime founder disclosure and external alerting recommendation; documented OneUptime heartbeat/escalation features match the recommendation.

Sources:

- [AWS Backup Vault Lock, including account closure](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html)
- [Google Backup and DR retention](https://docs.cloud.google.com/backup-disaster-recovery/docs/concepts/backup-vault)
- [Azure enhanced soft delete](https://learn.microsoft.com/en-us/azure/backup/backup-azure-enhanced-soft-delete-about)
- [Proxmox vzdump semantics](https://github.com/proxmox/pve-docs/blob/master/vzdump.adoc)
- [Velero data movement, repository password and maintenance](https://velero.io/docs/v1.18/csi-snapshot-data-movement/)
- [Velero 1.18.1 release](https://github.com/velero-io/velero/releases/tag/v1.18.1)
- [OneUptime heartbeat monitoring](https://oneuptime.com/docs/en/monitor/incoming-request-monitor) and [incidents/escalation/status pages](https://oneuptime.com/docs/en/incidents/index)

## Move 20 — Closure

Marked final cleanup irreversible instead of promising thirty-day reversibility. Removed the incorrect assertion that all three providers guarantee thirty days of data recovery: Google explicitly says some services can delete resources sooner than its project recovery period. AWS reopening remains conditional; Azure retention is not an unconditional restore promise. Removed premature key destruction and explained that copied ciphertext still depends on its keys. Preserve closure administrators and shared identity/office-service tenants, transfer DNS hosting as well as registrations, and reconcile commitments separately. Corrected the inconsistent $1,240 prose against the $3,200 reference strip by removing the unsupported prose total. Replaced four weeks with one month to match the stated monthly-job observation cycle; actual retention and contractual waits can be longer.

Sources:

- [AWS account closure and continued charges](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-closing.html)
- [Google project deletion and early data loss](https://docs.cloud.google.com/resource-manager/docs/delete-restore-projects)
- [Google deletion liens](https://docs.cloud.google.com/resource-manager/docs/troubleshooting-project-deletion)
- [Azure subscription cancellation](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/cancel-azure-subscription)
- [Entra tenant dependencies](https://learn.microsoft.com/en-us/entra/identity/users/directory-delete-howto)
- [KMS deletion disables cryptographic use](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html)

## Version/source maintenance and shared follow-up

Additional exact documentary pins: [Valkey 8.0.11](https://valkey.io/download/releases/) retains the original minor series; [NATS 2.12.15](https://github.com/nats-io/nats-server/releases/tag/v2.12.15) includes a documented JetStream data-loss fix; [rclone 1.75.1](https://downloads.rclone.org/) is used consistently in Moves 15, 19 and 20. An exact pin is not evidence of a deployment test; compatibility, application behaviour, failure modes and capacity must be rehearsed on the chosen hardware.


## AWS internet egress verification

Fetched the [official regional AWSDataTransfer offer](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSDataTransfer/current/us-east-1/index.json) on 9 September 2026. Published `2026-08-31T12:14:48Z`, version `20260831121448`, effective price date `2026-06-01`. SKU `HQEH3ZWJVT46JHRG`, US East (N. Virginia), `DataTransfer-Out-Bytes`, destination External.

The first dimension's description explicitly says the first 10 TB are **beyond the global free tier**. Its range is 0–10240 GB at $0.09, followed by 10240–51200 at $0.085, 51200–153600 at $0.07 and 153600–infinity at $0.05. Consequently, the existing calculation that subtracts the available shared 100 GB allowance before applying those boundaries is correct. The free allowance must not be independently claimed per service or region. No rate or boundary edit was required.

## AWS M7i verification

Streamed the [official regional AmazonEC2 offer CSV](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/us-east-1/index.csv) on 9 September 2026 and stopped after locating the matching row. Publication `2026-09-09T00:46:05Z`, version `20260909004605`, effective price date `2026-09-01`.

SKU `DFY9W427PBEXH8VY`, rate code `DFY9W427PBEXH8VY.JRTCKXETXF.6YS6EN2CT7`: `m7i.8xlarge`, `us-east-1`, US East (N. Virginia), Linux, Shared tenancy, Used capacity, no preinstalled software, OnDemand, `RunInstances`, 32 vCPUs and 128 GiB. The listed price is **$1.6128000000 per hour**, making **$0.0504 per vCPU-hour** arithmetically correct. No edit to these two reference rates was required. The reviewed result comes from AWS's own offer, without substituting third-party price aggregators.
