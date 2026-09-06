# Back to Metal

**Leaving the cloud with Kubernetes**, by the makers of
[OneUptime](https://oneuptime.com), published three ways: a printable
book, a reflowable EPUB, and a static website you can host anywhere.

The reason cloud repatriations fail is rarely the technology. It is that they are attempted as
one decision, executed as one project, and abandoned somewhere in the middle with two platforms
running and nobody able to say whether it is going well.

This book is the opposite shape. It is a sequence of **Moves**. Each is one job with a stated
cutover in minutes of user-visible downtime, a stated risk, and a rollback that names its point
of no return. Each can be done on a Tuesday and undone on a Wednesday, and you can stop after
any of them and still be somewhere coherent.

📕 **[dist/Back-to-Metal.pdf](dist/Back-to-Metal.pdf)** &nbsp;·&nbsp;
📖 **[dist/Back-to-Metal.epub](dist/Back-to-Metal.epub)** &nbsp;·&nbsp;
🌐 **[site/](site/)** — open `site/index.html`

## Three clouds, one runbook

Every Move covers **AWS, Google Cloud and Azure**. The job is the same whichever you are
leaving; only the extraction differs, so only the extraction is written three times. Each Move
opens with three lines naming the real product on each provider and the one thing that is
genuinely different there — a flag that needs a reboot, a tier that cannot do it at all, a
resource that outlives its parent. The runbook itself is written once.

## It is honest about what not to move

Several Moves conclude that you should keep paying somebody else. A global content network,
scrubbing capacity at the edge and outbound mail deliverability are businesses other people run
better than you will, and each is cheap next to what it replaces. A book that claims everything
can be repatriated is selling something.

## The dependency invariant

Every Move's prerequisites are **lower-numbered Moves**. A reader who has reached Move 40 has,
by construction, met every prerequisite of Move 40. That is not a stylistic choice — the build
refuses to compile a book where it does not hold, and it is what lets the website's planner
order a migration by sorting rather than searching.

## Layout

```
moves/       the Move files, numbered from 01 — the source of truth
book/        the typesetter and the site generator
  parse.py       markdown -> structured Move data
  verify.py      structure: the contract, the arithmetic, the house style
  audit.py       content: undeclared tools, unguarded destructive steps,
                 unpinned installs, drifted service names, repeated prose
  build.py       Move data -> a self-contained book.html
  render.py      html -> PDF via headless Chromium, vertically justified
  site.py        Move data -> a static website in site/
  epub.py        Move data -> a reflowable EPUB3
  cover.py       the paperback wrap, the Kindle cover, the hardback case
  deps.py        which Moves must be finished before which
  kit.py         the reference build, the laptop kit, the ten rules
  costs.py       the cost model, with the salary line in it
  equivalents.py AWS to Google Cloud to Azure to what you run instead
  rollback_data.py  the safety page every Move's rollback derives from
  symptoms.py    the symptom index — "which Move do I need"
  icons.py       Part glyphs, the cutover gauge, the risk bars, the page anatomy
  style.css      the print stylesheet
  web/           the site's stylesheet and scripts
dist/        the built PDF, EPUB and covers
site/        the built website
build/       intermediate HTML (gitignored)
```

## Building

```bash
make deps       # fonts, playwright, chromium
make verify     # structure — must be clean
make audit      # content — must be clean
make book       # markdown -> HTML -> PDF -> KDP compliance check
make site       # markdown -> static website
make            # all of it, and the tables in this README
```

Python 3.9 or newer with `playwright` and a Chromium build available to it. The Makefile prefers
`.venv/bin/python3` when it exists, so `python3 -m venv .venv && make deps` works without
activating anything.

`verify.py` and `audit.py` are the gate and both must come back clean. `verify.py` checks the
shape of every Move: the sections, the three-cloud block, the cost arithmetic, and that no Move
moving persistent state ships without saying how the state comes back. `audit.py` goes after the
things that are actually wrong in infrastructure writing — a runbook calling a tool the
prerequisites never mentioned, a destructive command with nothing standing behind it, software
installed without a version, a service spelled four ways, prose copy-pasted between Moves.

## The website

`site/` is self-contained — the fonts are embedded in the stylesheet and nothing is fetched at
runtime — so it drops onto any static host unchanged. It carries a **migration planner**: tick
the Moves you need and it closes the dependency set, orders it, and totals the downtime, the
effort and the saving. The plan lives in the address bar, so it is a link you can send to
whoever has to approve it.

## Contributing

The most valuable contribution is a **correction**. If you ran a runbook and it did not work as
written, that is worth an issue on its own. [CONTRIBUTING.md](CONTRIBUTING.md) covers the
workflow; [AGENTS.md](AGENTS.md) documents the Move contract, the house style the build
enforces, and what not to hand-edit.

## Licence

Two licences, because this repository is two things:

- **The software** — the toolchain in `book/`, the print stylesheet, the site's stylesheet and
  scripts — is [MIT](LICENSE).
- **The content** — the Moves, the written text of the book — is
  [CC BY 4.0](LICENSE-CONTENT).

So you may share and adapt any of it, for any purpose including commercially, as long as you
give credit.

<!-- generated: everything below this line is written by book/readme.py -->

## The book at a glance

| | |
|---|---|
| Moves | 122 |
| Part I · Iron | 20, 01–20 |
| Part II · Site | 18, 21–38 |
| Part III · Cluster | 16, 39–54 |
| Part IV · Platform | 16, 55–70 |
| Part V · Data | 20, 71–90 |
| Part VI · Edge | 17, 91–107 |
| Part VII · Watch | 15, 108–122 |
| At zero downtime | 110 of 122 |
| Whole book, end to end | 202 minutes of user-visible outage |
| Cannot be undone | 13 |
| Risk | 17 low, 38 medium, 67 high |
| Dependencies | 362, every one pointing backwards |
| Illustrative monthly saving | $212,364 across every Move |

Every Move names the real service on AWS, Google Cloud and Azure, and the one thing that differs on each.

## Part I · Iron

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 01 | [The month of numbers you do not have](moves/01-the-month-of-numbers-you-do-not-have.md) | — | Low | 0 min | Immediately |
| 02 | [What a vCPU is actually worth](moves/02-what-a-vcpu-is-actually-worth.md) | The vCPU as a unit of purchase | High | 0 min | Until the order is signed |
| 03 | [The estate nobody sizes](moves/03-the-estate-nobody-sizes.md) | Non-production capacity that costs nothing when it is switched off, and hosted CI runners | Medium | 0 min | Until the order is signed |
| 04 | [Cores against clock, and the licence that decides it](moves/04-cores-against-clock-and-the-licence-that-decides-it.md) | — | High | 0 min | Until the order is signed |
| 05 | [SMT, NUMA, and the workload that notices](moves/05-smt-numa-and-the-workload-that-notices.md) | — | Medium | 0 min | Immediately, by reboot |
| 06 | [Memory is what runs out first](moves/06-memory-is-what-runs-out-first.md) | — | High | 0 min | Until the order is signed |
| 07 | [One rack unit or two, and the watts it draws](moves/07-one-rack-unit-or-two-and-the-watts-it-draws.md) | — | Medium | 0 min | Until the order is signed |
| 08 | [The way in when the machine will not boot](moves/08-the-way-in-when-the-machine-will-not-boot.md) | The provider's serial console and boot diagnostics | High | 0 min | Until the order is signed |
| 09 | [The drive you are allowed to put etcd on](moves/09-the-drive-you-are-allowed-to-put-etcd-on.md) | — | High | 0 min | Per drive, at the cost of a Ceph rebuild |
| 10 | [How much flash, and where it sits](moves/10-how-much-flash-and-where-it-sits.md) | Block volumes that grow with an API call | High | 0 min | Until the bays are full |
| 11 | [Headroom, and the number of machines you order](moves/11-headroom-and-the-number-of-machines-you-order.md) | Elastic node capacity: cluster autoscaling and node auto-provisioning | High | 0 min | Until the order is signed |
| 12 | [Two switches, and the spine you do not need yet](moves/12-two-switches-and-the-spine-you-do-not-need-yet.md) | — | High | 0 min | Until the second rack is cabled |
| 13 | [The switch, and the software running on it](moves/13-the-switch-and-the-software-running-on-it.md) | — | High | 0 min | Until the order is signed |
| 14 | [The card, the driver, and the kernel you will run](moves/14-the-card-the-driver-and-the-kernel-you-will-run.md) | The provider's paravirtual network interface and its single driver | Medium | 0 min | Per node, at the cost of a card swap and a reboot |
| 15 | [Copper inside the rack, glass between them](moves/15-copper-inside-the-rack-glass-between-them.md) | — | Low | 0 min | Immediately, at the cost of re-coding or re-ordering |
| 16 | [The network that works when the network is down](moves/16-the-network-that-works-when-the-network-is-down.md) | — | High | 0 min | Immediately |
| 17 | [Who you buy from, and what is safe to buy used](moves/17-who-you-buy-from-and-what-is-safe-to-buy-used.md) | The hardware refresh someone else did for you | Medium | 0 min | 14 to 30 days, per the vendor's return window |
| 18 | [Nothing carries production until it has been made to fail](moves/18-nothing-carries-production-until-it-has-been-made-to-fail.md) | — | High | 0 min | Immediately; this is the last cheap moment |
| 19 | [The shelf, and the failure rates you stock against](moves/19-the-shelf-and-the-failure-rates-you-stock-against.md) | — | Medium | 0 min | Immediately |
| 20 | [The bill of materials](moves/20-the-bill-of-materials.md) | Committed-spend discounts on rented compute | High | 0 min | No |

## Part II · Site

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 21 | [What the three machines under the desk cannot tell you](moves/21-what-the-three-machines-under-the-desk-cannot-tell-you.md) | — | Low | 0 min | Immediately |
| 22 | [The four places the machines could live](moves/22-the-four-places-the-machines-could-live.md) | The region-and-zone abstraction | High | 0 min | Immediately |
| 23 | [The room in your own building](moves/23-the-room-in-your-own-building.md) | — | High | 0 min | Immediately |
| 24 | [The second site you are not building this year](moves/24-the-second-site-you-are-not-building-this-year.md) | — | High | 0 min | Immediately |
| 25 | [The flood plain, the fault line and the grid](moves/25-the-flood-plain-the-fault-line-and-the-grid.md) | — | High | 0 min | Immediately |
| 26 | [Carrier neutrality and the cross-connect price list](moves/26-carrier-neutrality-and-the-cross-connect-price-list.md) | — | Medium | 0 min | Immediately |
| 27 | [What a tier rating promises, and what it does not](moves/27-what-a-tier-rating-promises-and-what-it-does-not.md) | — | Medium | 0 min | Immediately |
| 28 | [Committed kilowatts, metered kilowatts and the derate](moves/28-committed-kilowatts-metered-kilowatts-and-the-derate.md) | — | High | 0 min | No |
| 29 | [What the service credit is actually worth](moves/29-what-the-service-credit-is-actually-worth.md) | Cloud service-level agreements and their credits | Low | 0 min | Until the schedule is signed |
| 30 | [The notice period and the door out](moves/30-the-notice-period-and-the-door-out.md) | — | Medium | 0 min | Until the term commences |
| 31 | [The 80 per cent you are allowed to draw](moves/31-the-80-per-cent-you-are-allowed-to-draw.md) | — | High | 0 min | Immediately |
| 32 | [Two feeds, one of which you have tested](moves/32-two-feeds-one-of-which-you-have-tested.md) | — | High | 0 min | Immediately |
| 33 | [The inlet temperature you are allowed](moves/33-the-inlet-temperature-you-are-allowed.md) | — | High | 0 min | Immediately |
| 34 | [The importer of record and the loading dock](moves/34-the-importer-of-record-and-the-loading-dock.md) | — | Medium | 0 min | Until the shipment is booked |
| 35 | [Who can get in at 03:00](moves/35-who-can-get-in-at-0300.md) | The shared-responsibility split for physical security | High | 0 min | Immediately |
| 36 | [The first rack](moves/36-the-first-rack.md) | — | Medium | 0 min | Immediately |
| 37 | [Labels, port maps and the as-built](moves/37-labels-port-maps-and-the-as-built.md) | — | Low | 0 min | Immediately |
| 38 | [The drives that leave, and the snapshots that stay](moves/38-the-drives-that-leave-and-the-snapshots-that-stay.md) | Provider-managed snapshot, image and backup retention | High | 0 min | No |

## Part III · Cluster

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 39 | [The address plan, and the three clocks you start today](moves/39-the-address-plan-and-the-three-clocks-you-start-today.md) | Cloud-managed private addressing and inter-network transit | High | 0 min | Immediately |
| 40 | [The management VLAN, and the way in at 03:00](moves/40-the-management-vlan-and-the-way-in-at-03-00.md) | Cloud serial console and agent-based remote shell | High | 0 min | Immediately |
| 41 | [Talos as the host OS, and where it cannot go](moves/41-talos-as-the-host-os-and-where-it-cannot-go.md) | Managed node images and their patch and time-sync agents | Medium | 0 min | Immediately |
| 42 | [Netboot, node identity and failure-domain labels](moves/42-netboot-node-identity-and-failure-domain-labels.md) | Golden machine images, launch templates and the instance metadata service | Medium | 0 min | Immediately |
| 43 | [Three control-plane nodes, the API VIP and the cluster CA](moves/43-three-control-plane-nodes-the-api-vip-and-the-cluster-ca.md) | The managed Kubernetes control plane and its cluster-creation tooling | High | 0 min | Immediately |
| 44 | [Cilium, with kube-proxy off](moves/44-cilium-with-kube-proxy-off.md) | The cloud-provider CNI plug-in and kube-proxy | High | 0 min | Immediately |
| 45 | [BGP to the top-of-rack, and the MTU that breaks five per cent](moves/45-bgp-to-the-top-of-rack-and-the-mtu-that-breaks-five-per-cent.md) | Cloud network routing and managed transit hubs | High | 0 min | Immediately |
| 46 | [Cluster DNS, and the resolver the network used to be](moves/46-cluster-dns-and-the-resolver-the-network-used-to-be.md) | The managed cluster DNS add-on and the provider's private resolver | Medium | 0 min | Immediately |
| 47 | [Local NVMe, and the default StorageClass nobody gave you](moves/47-local-nvme-and-the-default-storageclass-nobody-gave-you.md) | Managed network block storage and its default StorageClass | High | 0 min | No |
| 48 | [Encryption at rest, and who holds the key](moves/48-encryption-at-rest-and-who-holds-the-key.md) | Default encryption at rest on managed volumes | High | 0 min | No |
| 49 | [Ceph under Rook: block, shared filesystem and the object store](moves/49-ceph-under-rook-block-shared-filesystem-and-the-object-store.md) | Managed network block storage, managed shared filesystems and managed object storage | High | 0 min | No |
| 50 | [Humans on the API server: OIDC, after break-glass](moves/50-humans-on-the-api-server-oidc-after-break-glass.md) | Cloud IAM authentication to the managed cluster | High | 0 min | Immediately |
| 51 | [The second cluster, and what it shares](moves/51-the-second-cluster-and-what-it-shares.md) | The second managed cluster and its per-branch ephemeral variants | Low | 0 min | Immediately |
| 52 | [The etcd restore drill](moves/52-the-etcd-restore-drill.md) | Managed control-plane backup and restore | Low | 0 min | Immediately |
| 53 | [The links you build first: to the cloud, to the office](moves/53-the-links-you-build-first-to-the-cloud-to-the-office.md) | Physical data-transfer appliances and managed bulk-copy services | Medium | 0 min | Immediately |
| 54 | [The object store you now own, and how it loses data](moves/54-the-object-store-you-now-own-and-how-it-loses-data.md) | Managed object-storage durability, versioning and object lock | High | 0 min | No |

## Part IV · Platform

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 55 | [Workload identity without the cloud's](moves/55-workload-identity-without-the-clouds.md) | Cloud IAM workload identity: cluster OIDC federation, pod-identity agents and instance metadata credentials | Medium | 0 min | Immediately |
| 56 | [Secrets: External Secrets as the dated bridge](moves/56-secrets-external-secrets-as-the-dated-bridge.md) | — | Low | 0 min | Immediately |
| 57 | [The root of trust after managed key management](moves/57-the-root-of-trust-after-managed-key-management.md) | Managed key management and cloud HSM services, cloud-backed auto-unseal, envelope encryption in CI, and the cloud secret store as the record | High | 0 min | 30 days |
| 58 | [The mirror, then Harbor as the registry of record](moves/58-the-mirror-then-harbor-as-the-registry-of-record.md) | Managed container registries: private and public repositories, geo-replication, lifecycle rules and pull-through cache rules | High | 0 min | 30 days |
| 59 | [cosign, Trivy and an admission policy](moves/59-cosign-trivy-and-an-admission-policy.md) | Managed image scanning, managed code signing, tag immutability, scan-on-push gates and cluster-level binary authorisation | High | 0 min | Immediately |
| 60 | [East-west: security groups into NetworkPolicy](moves/60-east-west-security-groups-into-networkpolicy.md) | Instance-level firewalls: security groups and their group-to-group references, VPC firewall rules and network ACLs | High | 0 min | Immediately |
| 61 | [East-west encryption, and an identity per workload](moves/61-east-west-encryption-and-an-identity-per-workload.md) | Managed service mesh add-ons and the in-mesh mTLS they provided by default | Medium | 0 min | Immediately |
| 62 | [Metrics off the managed monitor, and the cardinality budget](moves/62-metrics-off-the-managed-monitor-and-the-cardinality-budget.md) | Managed metric stores, container insight agents, custom metrics and the provider's metric query language | Medium | 0 min | 14 days |
| 63 | [Logs and traces, brought home](moves/63-logs-and-traces-brought-home.md) | Managed log ingestion and query, managed distributed tracing, the provider's trace agent and its propagation header | Medium | 0 min | 30 days |
| 64 | [Builds onto your own metal](moves/64-builds-onto-your-own-metal.md) | Managed CI build services, their hosted runner pools and self-managed runner autoscaling groups | Medium | 0 min | Immediately |
| 65 | [Argo CD, and the two infrastructure-as-code estates](moves/65-argo-cd-and-the-two-infrastructure-as-code-estates.md) | Managed deployment services, pipeline deploy stages, source-repository connections and cloud-hosted remote state backends | High | 0 min | 30 days |
| 66 | [Infrastructure code that only compiles for one cloud](moves/66-infrastructure-code-that-only-compiles-for-one-cloud.md) | Provider-native stack templates, their programming-language synthesisers and the serverless application frameworks built on them | Medium | 0 min | Immediately |
| 67 | [The first stateless service, end to end](moves/67-the-first-stateless-service-end-to-end.md) | One stateless service: its workload identity role, its load-balancer target group and its managed log group | Medium | 0 min | Immediately |
| 68 | [The container service that was not Kubernetes](moves/68-the-container-service-that-was-not-kubernetes.md) | Managed container runtimes that are not Kubernetes: task-definition services, request-billed serverless containers and their built-in service discovery | Medium | 0 min | Immediately |
| 69 | [The fixed fleet: priority, preemption, NUMA and the GPUs](moves/69-the-fixed-fleet-priority-preemption-numa-and-the-gpus.md) | Node autoscaling groups, cluster autoscalers, just-in-time node provisioners, managed node pools and serverless pod runtimes | High | 0 min | Immediately |
| 70 | [The workloads that must stay virtual machines](moves/70-the-workloads-that-must-stay-virtual-machines.md) | Rented virtual machines outside the cluster, managed hypervisor estates and the appliance images sold through cloud marketplaces | Medium | 30 min | 14 days |

## Part V · Data

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 71 | [The Postgres pre-flight](moves/71-the-postgres-pre-flight.md) | Managed PostgreSQL | Medium | 15 min | Immediately |
| 72 | [The verification gate](moves/72-the-verification-gate.md) | Managed database-migration validation | Low | 0 min | Immediately |
| 73 | [Postgres onto your own disks](moves/73-postgres-onto-your-own-disks.md) | Managed PostgreSQL | High | 20 min | 7 days |
| 74 | [Point-in-time recovery with pgBackRest](moves/74-point-in-time-recovery-with-pgbackrest.md) | Managed automated backups and snapshots | High | 0 min | Immediately |
| 75 | [Quorum commit and fencing, after the restore was proven](moves/75-quorum-commit-and-fencing-after-the-restore-was-proven.md) | Managed multi-zone database failover | High | 2 min | Immediately |
| 76 | [The proprietary Postgres engines: the exit is a stream](moves/76-the-proprietary-postgres-engines-the-exit-is-a-stream.md) | Proprietary managed PostgreSQL-compatible engines | High | 20 min | 7 days |
| 77 | [MySQL, wherever it is managed](moves/77-mysql-wherever-it-is-managed.md) | Managed MySQL | High | 20 min | 7 days |
| 78 | [The licensed databases, and the contract that can veto it](moves/78-the-licensed-databases-and-the-contract-that-can-veto-it.md) | Managed licensed database engines | High | 30 min | No |
| 79 | [Redis: which half of it is actually a cache](moves/79-redis-which-half-of-it-is-actually-a-cache.md) | Managed Redis, Valkey and Memcached | Medium | 0 min | Immediately |
| 80 | [Brokered messaging: JMS, durable subscriptions, your broker](moves/80-brokered-messaging-jms-durable-subscriptions-your-broker.md) | Managed message brokers | High | 10 min | 7 days |
| 81 | [The queues come home, the fan-out does not](moves/81-the-queues-come-home-the-fan-out-does-not.md) | Managed queues and topic fan-out | High | 0 min | 14 days |
| 82 | [The event bus, and the control-plane events that stop arriving](moves/82-the-event-bus-and-the-control-plane-events-that-stop-arriving.md) | Managed event buses and provider control-plane events | Medium | 0 min | 7 days |
| 83 | [Kafka off the managed broker](moves/83-kafka-off-the-managed-broker.md) | Managed Kafka | High | 0 min | 7 days |
| 84 | [Application buckets, and the object API your code assumes](moves/84-application-buckets-and-the-object-api-your-code-assumes.md) | Managed object storage (application buckets) | High | 0 min | 30 days |
| 85 | [The data that stays: deep archive and the warehouse](moves/85-the-data-that-stays-deep-archive-and-the-warehouse.md) | — | Low | 0 min | Immediately |
| 86 | [The batch estate: who schedules the jobs](moves/86-the-batch-estate-who-schedules-the-jobs.md) | Managed workflow orchestration and managed Spark | Medium | 0 min | 30 days |
| 87 | [Search off the managed cluster](moves/87-search-off-the-managed-cluster.md) | Managed search clusters | Medium | 0 min | 7 days |
| 88 | [Document and wide-column stores: the hardest exit](moves/88-document-and-wide-column-stores-the-hardest-exit.md) | Managed document, key-value and wide-column stores | High | 30 min | 30 days |
| 89 | [The serverless estate in four piles](moves/89-the-serverless-estate-in-four-piles.md) | Managed function-as-a-service and its schedulers | High | 0 min | 30 days |
| 90 | [Orchestrated workflows: the dated exception](moves/90-orchestrated-workflows-the-dated-exception.md) | — | Low | 0 min | Immediately |

## Part VI · Edge

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 91 | [Your own ASN, a /24 and the address space you already have](moves/91-your-own-asn-a-24-and-the-address-space-you-already-have.md) | Provider-assigned public IP addresses and bring-your-own-IP programmes | Medium | 0 min | Immediately |
| 92 | [Turning on dual-stack, and the code that parses an address](moves/92-turning-on-dual-stack-and-the-code-that-parses-an-address.md) | Provider-managed IPv6 subnets and translation gateways | High | 0 min | No |
| 93 | [Transit: two upstreams and the 95th percentile](moves/93-transit-two-upstreams-and-the-95th-percentile.md) | Metered data transfer out and dedicated interconnect | Medium | 0 min | 30 days |
| 94 | [Egress off the managed NAT, and the allowlists you renegotiate](moves/94-egress-off-the-managed-nat-and-the-allowlists-you-renegotiate.md) | Managed NAT gateways and provider-assigned egress addresses | High | 0 min | 30 days |
| 95 | [The first VIP: L2, and failover when nobody will peer](moves/95-the-first-vip-l2-and-failover-when-nobody-will-peer.md) | Managed layer-4 load balancers | Medium | 0 min | Immediately |
| 96 | [VIPs over BGP: ECMP, BFD and the rehash](moves/96-vips-over-bgp-ecmp-bfd-and-the-rehash.md) | Managed cross-zone load balancing and anycast front ends | Medium | 0 min | Immediately |
| 97 | [TLS off the managed certificate service](moves/97-tls-off-the-managed-certificate-service.md) | Managed certificate services and managed private certificate authorities | High | 0 min | 30 days |
| 98 | [Envoy Gateway, after ingress-nginx](moves/98-envoy-gateway-after-ingress-nginx.md) | Managed layer-7 load balancers and in-cluster ingress controllers | Low | 0 min | Immediately |
| 99 | [Balancer rules and proxy annotations into HTTPRoute](moves/99-balancer-rules-and-proxy-annotations-into-httproute.md) | Managed balancer listener rules and ingress-controller annotations | Low | 0 min | Immediately |
| 100 | [The managed API front door: keys, quotas and WebSockets](moves/100-the-managed-api-front-door-keys-quotas-and-websockets.md) | Managed API gateways | High | 0 min | 30 days |
| 101 | [Edge authentication after the balancer did it](moves/101-edge-authentication-after-the-balancer-did-it.md) | Load-balancer authentication, managed user directories and client VPN | High | 5 min | 7 days |
| 102 | [The shadow edge: two gateways and a weighted record](moves/102-the-shadow-edge-two-gateways-and-a-weighted-record.md) | — | Low | 0 min | Immediately |
| 103 | [Go-live: the soak, the freeze, and how you abort](moves/103-go-live-the-soak-the-freeze-and-how-you-abort.md) | The parallel managed edge: layer-7 balancers and weighted DNS records | High | 10 min | 7 days |
| 104 | [Authoritative DNS, and the registrar you forgot](moves/104-authoritative-dns-and-the-registrar-you-forgot.md) | Managed authoritative DNS and provider-integrated registrars | High | 0 min | 7 days |
| 105 | [CDN: change vendor, not model](moves/105-cdn-change-vendor-not-model.md) | Provider-bundled CDN, edge functions and managed web application firewall | High | 0 min | 7 days |
| 106 | [DDoS: the capacity you rent forever](moves/106-ddos-the-capacity-you-rent-forever.md) | Managed DDoS protection subscriptions | High | 0 min | No |
| 107 | [Email: inbound comes home, outbound does not](moves/107-email-inbound-comes-home-outbound-does-not.md) | Managed inbound email receiving and its object-store pipelines | Medium | 0 min | 7 days |

## Part VII · Watch

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 108 | [The upgrade calendar and the control-plane upgrade](moves/108-the-upgrade-calendar-and-the-control-plane-upgrade.md) | Managed control-plane upgrades, purchasable extended support for end-of-life Kubernetes minors, and a managed add-on lifecycle | High | 0 min | No |
| 109 | [The fleet roll with no thirteenth machine](moves/109-the-fleet-roll-with-no-thirteenth-machine.md) | Managed node groups, image-based node rollouts, autoscaler surge capacity and managed node auto-repair | High | 10 min | Immediately |
| 110 | [The inventory, the RMA loop and which rack unit](moves/110-the-inventory-the-rma-loop-and-which-rack-unit.md) | The provider's capacity pool and its hardware-retirement notices | Low | 0 min | Immediately |
| 111 | [The 03:00 disk](moves/111-the-0300-disk.md) | Transparent block-device replacement and degraded-hardware notices | High | 0 min | Immediately |
| 112 | [The support contracts you buy for open source](moves/112-the-support-contracts-you-buy-for-open-source.md) | Paid cloud support plans priced against spend | Low | 0 min | 365 days |
| 113 | [The rota](moves/113-the-rota.md) | — | Medium | 0 min | Immediately |
| 114 | [Alerts that survive the cluster, and the pager you drop](moves/114-alerts-that-survive-the-cluster-and-the-pager-you-drop.md) | Managed alarms, managed synthetic checks, a rented paging and incident service and a hosted status page | High | 0 min | Immediately |
| 115 | [Velero, the off-site copy and the rebuild drill](moves/115-velero-the-off-site-copy-and-the-rebuild-drill.md) | Managed backup, snapshot lifecycle policies, cross-region copy and managed fault injection | High | 0 min | Immediately |
| 116 | [Capacity planning, and the cloud footprint you keep](moves/116-capacity-planning-and-the-cloud-footprint-you-keep.md) | On-demand elasticity and managed cluster autoscaling (keeping a minimal tested overflow) | Medium | 0 min | Immediately |
| 117 | [The patch SLA after the vulnerability feed stopped](moves/117-the-patch-sla-after-the-vulnerability-feed-stopped.md) | Managed vulnerability scanning, registry image scanning and managed patch-compliance reporting | Medium | 0 min | Immediately |
| 118 | [Audit logs after the provider's](moves/118-audit-logs-after-the-providers.md) | The provider's control-plane audit trail, its configuration-compliance rules and its posture-management service | Medium | 0 min | Immediately |
| 119 | [The auditor's checklist, and the contracts nobody read](moves/119-the-auditors-checklist-and-the-contracts-nobody-read.md) | Inherited compliance attestations, the provider's audit-evidence portal and its committed-spend agreement | High | 0 min | No |
| 120 | [What it actually costs](moves/120-what-it-actually-costs.md) | The provider's cost explorer, billing exports, budgets and cost-advisory service | Low | 0 min | Immediately |
| 121 | [Going back: how the programme is aborted](moves/121-going-back-how-the-programme-is-aborted.md) | — | High | 0 min | No |
| 122 | [The last account](moves/122-the-last-account.md) | The provider's organisation and identity centre, audit trail, key management, registry, marketplace subscriptions and support plan | High | 0 min | 30 days |
