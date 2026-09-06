# The manifest critique

An adversarial review of the 122-Move manifest, run before any Move was written.
Its verdict is that the manifest is safe to write a book from; what follows is the
fix list to apply while writing. Kept in the repository because a reader who finds
an error in the finished book deserves to see what was already known about.

**Verdict.** Yes — this is safe to write a book from, which is not what I said last time and is not a close call now. The three failures that made the previous manifest unsafe are genuinely repaired rather than papered over. The Part order does the work it was rebuilt to do: identity, secrets, the root of trust, the registry, supply chain, east-west policy, metrics, logs, CI, delivery and a first stateless service all land before Move 71, and Move 73 deps six of them by number, so the reader who follows the sequence literally can no longer migrate production Postgres onto a cluster with static keys, Docker Hub pulls, no dashboards and a flat network. All four broken runbooks are fixed at the mechanism rather than the wording — XtraBackup is refused against all three managed MySQL services, Backtrack is relocated to the MySQL Move where it belongs, Calico's iptables dataplane is named as the old-kernel path with the correct 5.3 and 5.8 floors, and OpenSearch Serverless and Azure AI Search are both correctly excluded from the snapshot runbook and given reindex-from-source instead. All fifteen missing Moves exist and several are better than what I asked for: Move 68 refuses to treat three unlike container runtimes as one job, Move 66 identifies the language synthesisers as the half that cannot be translated, Move 78 gets the Oracle core-factor inversion right in the direction that surprises people, and Move 121 correctly names the point of no return as the facility notice rather than any technical step. Every one of my nineteen ordering complaints is addressed, the graph is still acyclic across all 122 Moves, and the coverage boundary now spans three clouds properly rather than one — the per-provider differences I spot-checked are right far more often than they are wrong, including the ones that are easy to get wrong (Google's uploadable JWKS, Azure's twenty federated credentials per identity, the AWS pod-identity agent that cannot follow you off EKS, Cumulus 5 on Spectrum only, Citus being AGPL and therefore self-hostable, Event Hubs' partition-key compaction model, the three registrar stories). What is left is a fix list, not a rework, and it is short enough to name: correct the 12-channel DIMM claim in Move 06 before anyone drafts a purchase order; settle whether the node network is stretched layer 2 or routed, because Talos's VIP is gratuitous ARP and Moves 43 and 45 currently assume opposite answers; give Move 58 a certificate by splitting the internal CA out of Move 97 into Part IV; fix VictoriaMetrics in 62, Azure disk encryption in 48, Azure Backup for AKS in 52 and Event Hubs compaction in 83; split Move 32 so the load test follows the racking; rewrite the Move 75 hook. Only two of those are more than an afternoon. The one thing I would fix before anything else is not on that list and is not a factual error: the effort field conflates labour with elapsed time in at least eleven Moves that say so in their own prose, and because the brief makes that number decide where a Move lands on the reader's chart, the roadmap will under-forecast by about two quarters at exactly the two points — the thirty-day sampling window and the six-to-twelve-week circuit order — where being early is most expensive. Add a lead-time field the scheduler adds to the critical path but not to the person-day budget, populate it, and the book's central promise, that sequencing is the point, becomes true rather than aspirational. Do that and the eight corrections above, and this is a manifest worth eighteen months of writing — and unlike the last version, the eighteen months would produce something a reader could actually follow to the end.

## Factual corrections to apply

- CARRIED FORWARD — all twenty-three are fixed, and most are fixed properly rather than deleted.
  Verified: Backtrack correctly relocated to Move 77 and named as Aurora MySQL only; XtraBackup
  correctly refused against all three managed MySQL services in 77; Calico's iptables dataplane
  (not eBPF) named as the old-kernel path in 44 with the 5.3/5.8 kernel floors correct;
  OpenSearch Serverless and Azure AI Search both correctly excluded from the snapshot runbook in
  87; the DynamoDB export limitation stated accurately in 88, including that import can build
  GSIs from a supplied specification but can only create a new table; memcached moved to 79;
  ScyllaDB's source-available licence and capacity-limited free tier stated in 88; Graviton
  corrected in 02 and correctly extended to C4A/T2D/T2A/N4A/H3 and Cobalt 100 Dpsv6/Epsv6, all
  of which are genuinely one vCPU per physical core; reverse subscription built in 73 with
  reversibility 7 days; 103 now 10 min; 71 labels its reboot honestly; 22 reversible until 28/30
  sign; 47 and 106 both 'No'; email lossless qualified in 107; the /32-or-/29 LIR allocation and
  the never-held-IPv4 waiting-list condition both correct in 91; Terraform BUSL and the
  deprecated lock table in 65; EKS Pod Identity in 55 with the correct note that it does not
  exist outside the managed cluster; archive-async hyphenated with the busy-database RPO and the
  object-lock-at-bucket-creation requirement in 74; 'quorum commit' with fencing doing the
  safety work in 75; Contour resolved by committing to Envoy Gateway; matchbox/Tinkerbell/Omni
  support positions with Omni's BUSL-1.1 in 42; the Snowball claim gone. NIST SP 800-88r2 in
  Move 38 checks out — published 26 September 2025, deferring technique to IEEE 2883-2022.
  Kyverno's graduation in Move 59 checks out — CNCF announced it 24 March 2026. The Uptime
  Institute claims in Move 27 check out, including the 2009 removal of the nines. The new errors
  follow.

- Move 06, and it is in the Move whose output is a purchase order: 'the twelve-channel parts are
  one DIMM per channel only' is wrong for AMD. AMD SP5 (Genoa and Turin) supports two DIMMs per
  channel — 24 DIMM slots per socket is a shipping configuration from ASRock Rack, Tyan and
  Supermicro — at the usual 2DPC speed drop. The claim is true of Intel's twelve-channel Xeon 6
  6900P, which is 1DPC, and has been generalised onto the twelve-channel parts as a class. As
  printed it tells an EPYC reader that 'add memory later' is impossible when it is merely
  expensive, which distorts the memory line on the bill of materials in the same Move that calls
  memory the longest lead and the most price-volatile item. Fix: '...and the Intel twelve-
  channel parts are one DIMM per channel, while SP5 will take two at a documented speed drop.'

- Move 43 contradicts Moves 12 and 45, and it is build-breaking. Talos's own virtual-IP support
  is a layer-2 mechanism: it moves the address by gratuitous ARP and the Sidero documentation
  requires all control-plane nodes to share one broadcast domain with the VIP inside that
  subnet. Move 43 places the three control-plane nodes 'across the power feeds, switches and
  racks', and Move 45 commits to native routing with real pod prefixes advertised to two leaf
  switches per rack. Those two designs cannot both be true. Either the node network is a
  stretched layer-2 VLAN across racks — which needs saying, and which weakens the routed-fabric
  argument in 12 and 45 — or the API VIP needs a different mechanism (a BGP-advertised address,
  or kube-vip in BGP mode). This is one decision, but Part III cannot be drafted until it is
  taken, and it touches 12, 39, 43, 45 and 95.

- Move 62: 'both of which want the Move 49 object store rather than local disk' is false for
  VictoriaMetrics. VictoriaMetrics stores on block storage; vmstorage has no object-storage
  backend, and S3 appears only in vmbackup/vmrestore. Object storage as a primary backend is an
  open feature request, not a feature. Only Mimir wants the Move 49 store. This matters twice:
  it makes the dep on 54 conditional on the Mimir branch rather than universal, and it removes a
  local-NVMe capacity line from Move 10 that a VictoriaMetrics reader genuinely needs. Fix:
  'VictoriaMetrics under Apache-2.0 on the local NVMe of Move 47, against Mimir under AGPLv3
  with its replication factor of three on the Move 49 object store — which is a storage decision
  as much as a licence one.'

- Move 48: the two-against-one split is the wrong way round. Azure managed disks are encrypted
  at rest with a platform-managed key always and by default, and server-side encryption cannot
  be disabled — exactly like Google. The genuine outlier is AWS, where EBS default encryption is
  an opt-in per-region account setting that a reader may never have turned on. As written, an
  Azure reader is told they had a control to port when they had a default to replace, and a
  Google reader is singled out for a property Azure shares. Fix: 'On one of the three this was a
  control — EBS default encryption with a KMS key — while Azure and Google encrypted every disk
  with a platform key whether or not anyone asked, so those readers are replacing a default
  rather than porting a setting, and the customer-managed-key case is the only part that ports.'

- Move 52: 'only Google sold a backup product for cluster workloads at all' is false. Azure
  Backup for AKS is generally available, backs up cluster resources and CSI-driver-based
  persistent volumes via an in-cluster extension, and restores to the original or an alternate
  cluster. The surviving true half of the sentence — that none of the three ever exposed etcd,
  and that all three recover a control plane by recreating it — is the point worth keeping. Fix:
  'two of the three sold a backup product for cluster workloads, and neither restores etcd
  either.'

- Move 83: 'a product that is not Kafka underneath and does not support log compaction, which is
  the case that decides the answer for that reader' is false. Azure Event Hubs has supported log
  compaction since it went to preview in December 2022 and it is documented and available on
  every tier above Basic, enabled per event hub / Kafka topic. This is the one claim in the Move
  that is doing the decision-making for an entire reader population, so it is the worst place in
  the Part to be wrong. The genuine Event Hubs divergences are still there to be used — no
  transactional producer support, no idempotent producer, no dynamic partition addition on lower
  tiers, and a partition-key-as-compaction-key model that is not Kafka's key semantics.

- Move 08 is imprecise in a Move that exists to tell the reader what to put on a purchase order:
  'whether remote console and virtual media sit behind a licence — they do on Dell iDRAC
  Enterprise, on HPE iLO Advanced, and behind Supermicro's DCMS key.' Supermicro has shipped
  free HTML5 iKVM since X10; it is virtual media specifically that requires SFT-DCMS-SINGLE on
  X12 and X13, at roughly $130-200 per machine. Grouping console and virtual media together
  makes the Supermicro entry wrong on the half a reader is most likely to test on a loan unit.
  Split the two capabilities in the sentence and price them separately.

- Move 31 slips between kVA and kW inside one sentence, in the one place in the book where the
  power arithmetic is actually shown: 'a 208 volt three-phase 30 amp feed is 10.8 kVA on the
  nameplate and about 8.6 kW once the US continuous-load derate is applied.' Both numbers are
  right (10.806 kVA, 8.645 at 80%) but the unit changes without a stated power factor, and the
  paired European figure is left in kVA. A facility bills in kW and a breaker trips on amps; a
  handbook that has just spent a Move on derating conventions should say 'about 8.6 kVA, which
  is about 8.6 kW at the power factor a modern server supply holds' once, and then be
  consistent. Move 32's dual-feed arithmetic inherits the same slip.

- Move 09: 'a U.3 drive falls back into a U.2 bay and a U.2 drive does not work in a U.3 bay' is
  the SFF-TA-1001 position and is defensible, but it is stated as absolute where practice is
  not. Compliance varies on both sides: some U.3 drives do not actually implement the required
  U.2 fallback, and tri-mode U.3 backplanes from most vendors do accept U.2 NVMe drives in the
  field. Since the Move's own advice is that 'a mixed order can arrive unusable', the honest
  form is the spec direction plus one clause: 'and neither direction should be assumed without
  the vendor confirming the exact drive against the exact backplane in writing.'

- Move 53 and Move 116 disagree about the AWS free-egress terms. Move 53: AWS 'reviews each
  request and does not require closing the account'. Move 116: 'the free-egress-on-exit
  programmes generally require full departure, which is a conflict Move 122 has to settle'. Both
  can be technically true — AWS requires leaving AWS entirely without requiring account closure
  as the mechanism — but a reader planning the Move 116 retained overflow against the Move 122
  credit application needs one sentence, in one place, saying exactly what the condition is. As
  it stands the book contradicts itself across two Parts on a decision worth real money. The EU
  Data Act date in Move 53 (12 January 2027) is correct and worth keeping with its source.

- Move 05 omits the precondition that makes the whole Move work. The CPU Manager static policy
  allocates exclusive cores only to containers in Guaranteed-QoS pods with integer CPU requests;
  everything else stays in the shared pool regardless of full-pcpus-only, and the Topology
  Manager's single-numa-node policy admits or rejects pods rather than placing them. A reader
  who sets the two kubelet options and leaves their workloads on fractional requests gets none
  of the benefit and none of the symptoms, and will conclude the advice was wrong. One clause
  fixes it, and Move 69 is where the request accuracy that satisfies it is built — so 69 should
  be named here.

- Move 54: 'only Google sold a single bucket name spanning two regions' is contestable enough to
  be worth softening. Azure GRS is one storage account name replicated to a paired region, and
  S3 Multi-Region Access Points present one global endpoint over buckets in several regions.
  Google's dual-region bucket is genuinely the cleanest instance of the property, but 'only'
  invites a correction. The claim in the same Move that Ceph requires object lock at bucket
  creation before the Tentacle release is load-bearing for Move 74's runbook and I could not
  confirm the Tentacle half — print it with a citation and a review date, or drop to the safe
  form, which is that object lock must be set at bucket creation.

- Move 19's failure-rate figure is slightly under the source it is describing. The Backblaze
  fleet AFR has run around 1.3 to 1.7 per cent in recent years, not 'one to one and a half'. The
  Move is otherwise careful — it says out loud that it is a disk fleet rather than a flash one —
  so widen the range to match and keep the caveat.

## Ordering and scheduling

- The seven-Part order genuinely fixes the estate-cannot-be-built problem, and this is the most
  important thing to say. Identity is Move 55, secrets 56, root of trust 57, registry 58, supply
  chain 59, east-west policy 60, metrics 62, logs and traces 63, CI 64, delivery 65 and the
  first stateless service 67 — every one of them before Move 71, and Move 73 (production
  Postgres) deps 48, 56, 58, 60, 62 and 63 explicitly. The specific failure I described —
  Postgres landing on a cluster with static keys, Docker Hub pulls, no dashboards and a flat
  network — cannot now happen to a reader following the sequence. Move 74 names 49 and 55
  directly, Move 115 names 49 and 54 directly, Move 75 deps 74, 105 deps 103 and 104, 107 deps
  104, 89 deps 69, 111 deps 110, 122 deps 55/57/85/88/90/116/119/121, and the staffing
  arithmetic is pulled up to Move 22 where the reader can still act on it. Every one of my
  nineteen ordering complaints is addressed. The graph is still acyclic — I checked all 122
  dependency lists and no dep points higher. What follows is new.

- THE SCHEDULE IS SYSTEMATICALLY OPTIMISTIC BY MONTHS, and this is now the most serious defect
  in the manifest because the brief makes effort load-bearing. Effort and elapsed time are
  conflated in a single field, and at least eleven Moves say so in their own prose while the
  field records only the labour. Move 01 is 'about four days of work spread across a thirty-day
  window' — the website will start Move 02 on day five, when Move 02's entire input is a month
  of samples that does not exist yet. Move 53 is 'about 1 week of work, sitting inside a circuit
  lead time of six to twelve weeks, and it is the lead time that belongs on the schedule' — the
  Move says the right thing and the data model cannot record it. Same shape in 34 (five days
  inside six weeks), 91 (four days against a wait in months), 93 (two weeks against six to
  twelve weeks), 94 (plus a quarter of partner change calendars), 104 (plus the parent zone's NS
  TTL), 106 (a week against a month of procurement), 112 (a week spread across a quarter), 119
  (three weeks in other people's calendars), 122 (two weeks across a quarter of waiting
  periods), and 17 (three weeks of quoting against memory lead times measured in months). A
  reader planning against the computed chart will under-forecast the programme by roughly two
  quarters, concentrated at the two points — the sampling window and the circuit order — where
  being wrong costs the most. Fix: add a second field (lead, wait, or elapsed) that the
  scheduler adds to the critical path but not to the person-day budget, and populate it for
  those eleven Moves plus 06 and 20.

- Move 97 (cert-manager and the internal CA) is in Part VI and at least three Part IV Moves
  cannot be executed without it. Harbor in Move 58 is the registry of record and must present a
  certificate that every node's containerd trusts before anything can pull from it; Move 58 goes
  as far as powering the rack off to prove the circular boot dependency and never says where its
  certificate comes from. Grafana in 62, Loki in 63 and the namespace handover in 67 have the
  same need in weaker form. Move 97 is numbered higher than all of them so it cannot be dep'd,
  which makes it the one genuine substantive forward dependency left in the rebuild. Either
  split Move 97 — the internal hierarchy with step-ca into Part IV as a prerequisite of 58, the
  public ACME half staying in Part VI where the delegated challenge zone belongs — or state in
  Move 58 that the interim is a Talos machine-config trust bundle carrying a self-signed CA, and
  that Move 97 replaces it.

- Move 32 requires the output of Move 36, which deps it. Move 32's scope ends by pulling the A
  feed 'with the cabinet fully loaded and nothing yet depending on it' and measuring what
  tripped; Move 36 is the Move that racks and loads the cabinet, and its deps are [31, 32, 33,
  34, 35]. As drawn, the reader is told to load-test an empty cabinet. Move 33's thermal survey
  with a probe at the top of the cabinet inside containment has the same shape, though it is
  survivable with a heat-load rig. Fix: split 32 into the design half (feed budget, transfer
  switch for single-supply equipment, the one-feed rule) which precedes 36, and the proof half
  (pull the A feed) which follows it — or make 36 dep only the design half and add an explicit
  'test the feeds' step at the end of 36.

- Move 18 cannot run before Move 20 and its effort figure knows it: 'about one week to write the
  suite, and about one week of elapsed time per batch to run it.' Move 20 is the bill of
  materials and deps 18. The suite must be written before the purchase order because passing it
  is a term of the order — that is right and is the Move's best idea — but running it requires
  delivered hardware, which requires the order, which requires 20. The schedule will place a
  week of acceptance testing before anything has been bought. Same defect, smaller, in Move 17's
  'support-entitlement check per serial'. Fix: 18 is 'writes the acceptance suite' at one week
  and deps into 20; a short Move or an explicit step after delivery runs it.

- Move 112 (support contracts) is in Part VII and is needed in Part III. It deps 13, 41, 49 and
  73 — the switch OS, Talos, Ceph and Postgres — and its own scope says it is 'about a week of
  procurement spread across a quarter, most of it waiting for quotes'. Ceph takes its first
  bound volume at Move 49 and production Postgres lands at Move 73. Buying the Ceph subscription
  thirty-nine Moves and the better part of a year after Ceph became the durability floor means
  the first Ceph incident that matters happens with no contract and a quarter's procurement
  ahead of it. The Move is well written; it is filed where the reader can no longer act on it in
  time. Start it at Move 49 and let it complete in Part VII, or split the quote-gathering from
  the signature.

- Move 92 (dual-stack) is filed in Part VI, is marked reversible No, and recreates Services that
  Parts IV and V have already built. Its own scope concedes that 'the existing Services and Pods
  stay single-stack until they are recreated' — by Move 92 that is the whole platform and the
  whole data estate. It deps 44, 45 and 91, all of which are available by Move 45, and the RIR
  clock that gates 91 is started in Move 39. A decision that cannot be reversed and that touches
  every Service in the cluster belongs next to the CNI in Part III, taken once, before anything
  is built on top of it. Alternatively, state plainly in Move 44 that the cluster is being built
  single-stack deliberately and that Move 92 is a recreation exercise priced accordingly — but
  the current placement gets the cost without the warning.

- Dep discipline collapses in three Data Moves and it damages the computed schedule. Move 84
  deps [49, 54, 55, 60, 62] but not 58 — it runs mirroring and verification jobs from an image.
  Move 85 deps [84] alone and stands up Trino, DuckDB or ClickHouse on the cluster, which needs
  58 (registry), 60 (policy), 62 (metrics) and 69 (scheduling on a fixed fleet). Move 88 deps
  [72, 73, 84] and deploys a Cassandra cluster with no registry, no policy and no observability
  dep. Their siblings get this right — 86 deps 56, 58, 60, 62, 65 and 69; 73 deps ten Moves. The
  three thin ones will be scheduled earlier than they can be executed, which is exactly the
  failure mode the new ordering was built to eliminate.

- Move 51 (the second cluster) is dep-complete but its scope reaches forward: 'it does share the
  Move 50 identity provider and, from Move 58, the registry of record'. That is the correct
  relationship and the correct thing to say, but it means the non-production cluster is stood up
  in Part III pulling from somewhere unstated, and then re-pointed in Part IV. Say which — it is
  the same unstated interim registry that all of Part III depends on.

- The interim registry for Part III is still not stated anywhere, which is the one item from my
  original list that is only half fixed. Moving Harbor from old Move 48 to new Move 58 keeps it
  in Part IV, and the whole of Part III — Talos boot assets, Cilium, CoreDNS, Rook and Ceph,
  CloudNativePG for Harbor's own database, the local static provisioner — pulls images before it
  exists. This is genuinely unavoidable as a bootstrap, and Move 58 handles the steady state
  beautifully by powering the rack off to prove the dependency. What is missing is one sentence,
  in Move 42 or 49, naming what Part III pulls from and what the Docker Hub rate limit does to a
  rebuild attempted at that stage.

- Minor: Move 21 (what the desk cluster cannot tell you) duplicates the closing paragraph of
  Move 18, which already carries the brief's requirement that Part I says where the on-ramp
  stops being representative — and does it better, against ECC behaviour, dual-feed supplies,
  bonded links, BMC recovery and drive endurance under Ceph. Move 21 then repeats the same list
  in Part II with deps []. Either fold 21's forward-pointing map of which Move closes which gap
  into Move 18 and delete 21, or strip the duplicated list from 18 and leave 21 as the map.

## Coverage gaps

- ALL FIFTEEN of my original missing Moves are genuinely added, not gestured at: 51 (second
  cluster), 100 (API gateway), 68 (ECS/Fargate/Cloud Run/Container Apps), 78 (licensed engines +
  Windows), 48 (encryption at rest), 61 (east-west encryption), 70 (KubeVirt), 86
  (batch/Airflow/Spark), 80 (brokered messaging), 82 (event bus), 66 (CFN/CDK/Deployment
  Manager/Bicep), 54 (object-store durability), 112 (support contracts), 92 (dual-stack), 121
  (abort). Several are better than what I asked for — 68 correctly splits three unlike runtimes,
  66 correctly identifies the synthesiser estates as the hard half, 121 correctly names the
  point of no return as the Move 30 notice rather than a technical step. The gaps below are new.

- Nothing monitors the fabric or the facility. Move 111 instruments drives and Move 62
  instruments the cluster, but no Move collects switch telemetry (BGP session state, interface
  errors, optical DDM/receive power, buffer drops), PDU per-outlet metering, cabinet inlet
  temperature or the out-of-band estate's own health. Move 113 explicitly assumes this data
  exists — it budgets the rota against 'PDU, inlet temperature, fan, ECC and disk signals the
  managed monitor never surfaced' — and Move 33 commits to an inlet temperature nobody
  afterwards measures continuously. A dark optic degrading over a week is the single commonest
  cause of the intermittent packet loss a six-person team will spend a fortnight chasing. Needs
  a Move in Part VII depending on 13, 15, 31, 33 and 62.

- No Move upgrades the switches. Part VII covers the control plane (108), the nodes (109),
  firmware and BMCs (117) and even the support contract for the NOS (112), but nothing covers a
  NOS upgrade on a two-switch fabric with no spine, which is a production-affecting operation
  with no surge capacity: with MLAG you reload one peer and run single-homed, with BGP-to-the-
  host you drain routes first, and the ordering differs. The book buys the switch in Move 13 and
  configures it in 45 and 96 and then never touches it again for the life of the estate. Also
  absent: switch configuration as code, config backup and restore, and where the running config
  lives when the switch dies.

- No Move for the managed machine-learning estate. The book covers batch (86), functions (89),
  containers (68) and GPUs as a scheduling concern (69), but SageMaker, Vertex AI and Azure ML
  have no landing anywhere: training jobs, the model registry, feature stores and — the one that
  actually blocks — real-time inference endpoints. Move 116 mentions keeping 'intermittent GPUs'
  in the retained cloud footprint, which is the only acknowledgement that this estate exists.
  For a 2026 book about leaving all three clouds this is now the most conspicuous absence, and
  it is bigger than several Moves that did get written.

- Floor loading is missing from Part II. Move 34 books the dock and checks the lift against 'a
  cabinet approaching a tonne'; Move 36 checks rail kits against cabinet depth. Neither checks
  the floor. Raised-floor point loading and distributed load limits are a real and commonly
  binding colocation constraint, they are stated in the facility's own specification in kN/m2 or
  lb/ft2, and a cabinet filled with 2U chassis and a full DIMM population can exceed them. A
  first-time reader will not know to ask. It belongs in Move 25 (the address) or Move 31 (the
  cabinet plan).

- Time is a site service now and no Move builds it. Move 41 lists time sync as one item in a
  Talos machine-config sentence alongside conntrack and hugepages. On the clouds the link-local
  NTP endpoint (169.254.169.123, metadata.google.internal, the Azure host) was free, accurate
  and outside the failure domain. On your own metal somebody must choose upstream sources or a
  GPS/PTP appliance, decide whether the out-of-band network carries it, and hold the whole
  estate inside the skew that Kerberos, certificate validation, Ceph, etcd leases and log
  correlation all silently assume. Half a day of content, but it is load-bearing and it is not
  anywhere.

- Bonding and earthing. Move 14 buys two cards for two failure domains and Move 15 cables them,
  but no Move states the link-aggregation mode against the Move 12 MLAG-or-BGP answer — LACP to
  an MLAG pair versus two independent L3 uplinks with BGP unnumbered are different host
  configurations and Talos configures them differently. Move 45 assumes 'the two uplinks' behave
  per Move 12 without saying how the host is set up. Related and smaller: nothing covers rack
  bonding and earthing to TIA-607 or the facility's equivalent, which the reader will be asked
  about on the day of the racking.

## Hooks to rewrite

- FIXED: no hook exceeds 170 characters (longest is Move 55 at 165), none contains an
  exclamation mark or the banned word, and the imperative drift is gone — 'Become an LIR' is now
  'Takes an ASN...', 'Buy transit' is 'Buys transit...', 'Publishing your own service-account
  issuer' is 'Publishes the cluster's own service-account issuer...'. All nineteen offenders
  converted. The items below are new.

- Move 75 is broken English and is the only hook in the book that is not a sentence: 'Replaces
  the managed failover checkbox with quorum commit and only fencing gives safety.' Two
  independent clauses joined by 'and' with mismatched subjects, and at 88 characters it is 40
  shorter than the next shortest hook, so it looks truncated on the page as well as reading as
  truncated. The old hook it replaced was correct and grammatical. Replacement: 'Replaces the
  managed failover checkbox with quorum commit and explicit fencing, because quorum commit gives
  durability and only fencing stops a partitioned primary writing.' (170 — trim to 'Replaces the
  managed failover checkbox with quorum commit and explicit fencing, because quorum gives
  durability and only fencing stops a partitioned primary writing.', 160.)

- Move 108 states as fact something a reader can falsify and a competitor still sells: 'Upstream
  maintains a minor for about fourteen months and the extra year sold by the hour is gone, so
  the treadmill becomes a dated calendar with a named owner.' Extended support is not gone —
  EKS, GKE and AKS all still sell it, by the cluster-hour or as an LTS tier; it is gone for you,
  because you left. Replacement: 'Upstream maintains a minor for about fourteen months and the
  extra year you could buy by the hour is not on offer here, so the treadmill becomes a dated
  calendar with a named owner.' (166 — or trim 'you could buy by the hour' to 'you rented'.)

- Move 92 makes an absolute claim about other people's code: 'because a v6 literal breaks a
  parser that never saw one'. Some do, many do not, and the Move's own scope is more careful
  ('will meet an IPv6 literal for the first time'). Replacement: 'Turns on dual-stack Services
  and pod addressing, then audits the code, log parsers, allowlists and database columns that
  will meet an IPv6 literal for the first time.' (159)

- SYSTEMATIC, and it is a new drift replacing the one I flagged last time. Roughly sixteen hooks
  abandon the verb-first form the other hundred use and open with a statement of fact instead:
  57 'The managed key could be neither exfiltrated nor lost, so...', 60 'The pod network is flat
  until you say otherwise, so...', 64 'The control plane stays with the forge and...', 66
  'Provider-native templates have no target off the cloud...', 68 'A task definition is not a
  Deployment, so...', 69 'Node count is fixed, so...', 70 'Some workloads never containerised,
  so...', 90 'Argo Workflows and Temporal do not replace...', 108 as above, plus 56, 58, 59, 62,
  63, 65 and 67 in weaker form. Every one is grammatical and several are good sentences — 68 and
  69 in particular. But a roadmap chart renders these side by side, and the reader gets two
  different grammatical objects: 'this Move does X' and 'here is a fact about the world'. Pick
  the fact-first form for the Moves whose whole point is a constraint (60, 68, 69, 70, 90) and
  convert the rest to verb-first, or convert all sixteen. Do not leave it at sixteen against a
  hundred and six.

- Three hooks cite Move numbers, which the other hundred and nineteen do not: 40 'before Move 50
  can lock everyone out at once', 61 'which is the destination Move 55 named', 79 'and hands the
  durable half to the next Move'. Hooks appear in the roadmap chart's tooltips and in the
  contents, where the referenced Move is usually not on screen and, in 79's case, 'the next
  Move' is only true in one rendering order. Move the cross-reference into scope, where every
  other one lives. Replacements: 40 '...and drills the break-glass path before the identity
  provider becomes the only way in.'; 61 '...which is what SPIFFE was named for earlier and what
  an auditor asks for before data lands.'; 79 '...sends the genuinely ephemeral half to Valkey
  and hands the durable half to the queue Move.'

- LENGTH, carried forward and worse. I asked for the four hooks at 166 to be trimmed so a copy-
  edit has somewhere to go. Instead twenty-eight hooks now sit between 158 and 165, led by 55
  (165), 80 (164), 41/68/69/70 (163) and 67 (162). Nothing is over the limit, so the build
  passes, but there is no slack anywhere in the top quarter of the distribution and a single
  house-style substitution at proof stage ('managed' to 'provider-managed', say) breaks several
  at once. Trim a clause from everything above 155 now.

- Minor, Move 44: my own suggested replacement said 'ends the ENI address accounting behind pod
  density'; the rebuild dropped 'ENI' and left 'ends the address accounting behind pod density'.
  Now that the book leaves all three clouds the specific reference has to change rather than
  vanish, because pod density is ENI-limited on one, alias-range-limited on another and IP-
  allocation-limited on the third, and 'the address accounting' now names nothing. Replacement:
  '...which ends the provider address accounting behind pod density and turns service resolution
  into a hash-map lookup.' (158)

## Regressions from the previous manifest

- Move 75's hook was degraded from a correct, grammatical sentence in the old manifest
  ('Replaces the Multi-AZ checkbox with quorum-based synchronous replication and explicit
  fencing, so a partitioned old primary cannot keep accepting writes') into a broken one. My
  critique asked for 'quorum commit' to replace 'quorum-based synchronous replication'; the edit
  made that substitution and destroyed the clause that carried the reason. This is the clearest
  case in the rebuild of a fix applied to a word rather than to a sentence.

- Move 63 violates the book's own stack commitment in the act of claiming to honour it:
  'Promtail reached end of life in March 2026, so the collector question is settled as Alloy,
  Vector or the OpenTelemetry Collector rather than left open.' Settling a question with three
  answers is not settling it, and the sentence draws attention to the contradiction. The brief
  says name one. Move 62 has a softer version of the same problem, offering VictoriaMetrics
  against Mimir as a live choice where the brief named Prometheus and Loki, and Move 57 offers
  three custody models. Some of those are legitimate decision Moves and should say so; Move 63
  is not one, and should pick Alloy.

- Move 95 names no implementation at all. It describes layer-2 mode, gratuitous ARP, stale
  neighbour caches and externalTrafficPolicy without saying whether that is Cilium's L2
  announcements or MetalLB — in a book that commits to Cilium two Moves earlier and whose stated
  rule is name one, not three. Every other Move in Part VI names its component. This one names
  none, which is a worse failure of the same discipline than naming three.

- Part labelling is inconsistent in the rebuilt metadata. Moves 55 to 70 are tagged '[IV ·
  Platform]'; every other Move uses the bare Part name ('[Iron]', '[Site]', '[Cluster]',
  '[Data]', '[Edge]', '[Watch]'). If the website groups or sorts on that field, sixteen Moves
  will land in a Part of their own. Trivial to fix and worth fixing before it is baked into a
  URL scheme.

- Effort figures switch between words and numerals across Parts: Part I and II use 'About four
  days' and 'About one week'; Part III uses 'About 5 days of work', 'About 2 weeks', 'About 4
  days'; Parts IV to VII return to words. If the schedule is parsed from that field, two formats
  is a parser bug waiting; if it is read by a human, it is a house-style break down the middle
  of the book.

- The hook-length distribution got tighter rather than looser after I asked for slack — twenty-
  eight hooks between 158 and 165 where there were four at 166. The fixes were made by adding
  qualifying clauses (correctly, in most cases) without trimming anywhere, so accuracy improved
  and headroom vanished.

- Move 21 was created to do a job Move 18 already does. Both tell the reader where the front-
  matter homelab stops being representative, and Move 18's version is the better of the two
  because it is specific about ECC behaviour, dual-feed supplies, bonded links across two
  switches, BMC recovery and drive endurance under Ceph. One of them should be a cross-
  reference.

- Against all of that: the refusal count went up rather than down, which is the thing I most
  feared losing. The rebuild carries genuine refusals in 23 (mostly no), 24 (no second site this
  year), 85 (archive and warehouse stay), 105 (keep renting CDN), 106 (keep paying for
  mitigation), 107 (outbound email stays relayed) and 78 (sometimes this estate does not move at
  all), plus dated exceptions in 56, 90 and 116 and a keep-paying threshold in 88. The metadata
  honesty also survived — reversibility windows still track real retention periods, and Move
  103's cutover is now 10 minutes rather than a flattering zero. Nothing about the book's
  willingness to say no was lost in the rework.
