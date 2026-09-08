"""A deeper pass than verify.py: the content, not just the shape.

verify.py guarantees every Move has the right sections and that the cost
arithmetic closes. This one goes after the things that are actually wrong in
infrastructure writing: a runbook that calls a tool the prerequisites never
mentioned, a prerequisite listed and never used, a destructive command with
nothing standing behind it, software installed without a version, an AWS
service spelled four ways across the book, and prose copy-pasted between Moves.

Both gates must come back clean before a commit.
"""
import re, sys
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse import load_all, section, MOVES
import equivalents as EQ
import deps as DEPS
import symptoms as SYM

# ---- the tools a runbook may reach for -----------------------------------
# A command named here must be declared in "Before you start", and anything
# declared there should get used. The analogue of an ingredient list.
TOOLS = {
    'kubectl': 'kubectl', 'helm': 'helm', 'talosctl': 'talosctl', 'kubeadm': 'kubeadm',
    'k9s': 'k9s', 'argocd': 'argocd', 'flux': 'flux', 'kustomize': 'kustomize',
    'velero': 'velero', 'etcdctl': 'etcdctl', 'cilium': 'cilium', 'calicoctl': 'calico',
    'psql': 'psql', 'pg_dump': 'pg_dump', 'pg_dumpall': 'pg_dump',
    'pg_basebackup': 'pg_basebackup', 'pgbackrest': 'pgbackrest', 'pg_restore': 'pg_dump',
    'mysql': 'mysql', 'mysqldump': 'mysql', 'mydumper': 'mydumper',
    'redis-cli': 'redis-cli', 'valkey-cli': 'valkey-cli',
    'mc': 'mc', 'rclone': 'rclone', 's5cmd': 's5cmd', 'restic': 'restic',
    'aws': 'aws', 'gcloud': 'gcloud', 'az': 'az', 'gsutil': 'gsutil',
    'azcopy': 'azcopy', 'terraform': 'terraform', 'ansible': 'ansible',
    'ansible-playbook': 'ansible', 'pulumi': 'pulumi',
    'docker': 'docker', 'podman': 'podman', 'buildah': 'buildah',
    'skopeo': 'skopeo', 'crane': 'crane', 'oras': 'oras',
    'openssl': 'openssl', 'cmctl': 'cmctl', 'step': 'step-cli',
    'dig': 'dig', 'mtr': 'mtr', 'ipmitool': 'ipmitool', 'ceph': 'ceph',
    'vault': 'vault', 'sops': 'sops', 'age': 'age',
    'promtool': 'promtool', 'logcli': 'logcli', 'vector': 'vector',
    'kafka-topics.sh': 'kafka', 'rpk': 'redpanda', 'nats': 'nats',
}

# ---- cloud service names, spelled the one way the book spells them --------
# Three clouds means three chances to spell the same product two ways. Each
# pattern below matches every form that shows up in the wild; anything matching
# it and not in ACCEPT is a spelling that has drifted.
CANON = {
    r'\bRoute\s?53\b': 'Route 53', r'\bRoute53\b': 'Route 53',
    r'\bCloud\s?[Ff]ront\b': 'CloudFront', r'\bCloudfront\b': 'CloudFront',
    r'\bCloud\s?[Ww]atch\b': 'CloudWatch', r'\bCloudwatch\b': 'CloudWatch',
    r'\bDynamo\s?DB\b': 'DynamoDB', r'\bDynamoDb\b': 'DynamoDB',
    r'\bElasti[Cc]ache\b': 'ElastiCache', r'\bElastic\s?Cache\b': 'ElastiCache',
    r'\bOpen\s?[Ss]earch\b': 'OpenSearch', r'\bOpensearch\b': 'OpenSearch',
    r'\bSecrets\s?Manager\b': 'Secrets Manager', r'\bSecretsManager\b': 'Secrets Manager',
    r'\bStep\s?Functions\b': 'Step Functions', r'\bStepFunctions\b': 'Step Functions',
    r'\bSavings\s?Plans?\b': 'Savings Plans',
    r'\bkubernetes\b': 'Kubernetes',
    r'\bpostgres(ql)?\b': 'PostgreSQL or Postgres, consistently',
    # --- Google Cloud
    r'\bCloud\s?SQL\b': 'Cloud SQL', r'\bCloudSQL\b': 'Cloud SQL',
    r'\bCompute\s?Engine\b': 'Compute Engine',
    r'\bCloud\s?Storage\b': 'Cloud Storage',
    r'\bArtifact\s?Registry\b': 'Artifact Registry',
    r'\bSecret\s?Manager\b': 'Secret Manager',
    r'\bPub\s?/?\s?Sub\b': 'Pub/Sub', r'\bPubSub\b': 'Pub/Sub',
    r'\bBig\s?Query\b': 'BigQuery', r'\bBigquery\b': 'BigQuery',
    r'\bAlloy\s?DB\b': 'AlloyDB', r'\bAlloyDb\b': 'AlloyDB',
    r'\bMemorystore\b': 'Memorystore', r'\bMemory\s?Store\b': 'Memorystore',
    r'\bPersistent\s?Disk\b': 'Persistent Disk',
    r'\bCloud\s?Armor\b': 'Cloud Armor',
    r'\bgoogle\s?cloud\b': 'Google Cloud',
    r'\bGCP\b': 'Google Cloud',
    # --- Azure
    r'\bBlob\s?Storage\b': 'Blob Storage',
    r'\bManaged\s?Disks?\b': 'Managed Disks',
    r'\bEvent\s?Hubs?\b': 'Event Hubs', r'\bEventHubs?\b': 'Event Hubs',
    r'\bService\s?Bus\b': 'Service Bus',
    r'\bCosmos\s?DB\b': 'Cosmos DB', r'\bCosmosDB\b': 'Cosmos DB',
    r'\bKey\s?Vault\b': 'Key Vault', r'\bKeyVault\b': 'Key Vault',
    r'\bFront\s?Door\b': 'Front Door',
    r'\bLog\s?Analytics\b': 'Log Analytics',
    r'\bApplication\s?Insights\b': 'Application Insights',
    r'\bContainer\s?Registry\b': 'Container Registry',
    r'\bazure\b': 'Azure',
}
# The forms the book accepts. Anything matching a pattern above but not in here
# is a spelling that has drifted.
ACCEPT = {
    'Route 53', 'CloudFront', 'CloudWatch', 'DynamoDB', 'ElastiCache',
    'OpenSearch', 'Secrets Manager', 'Step Functions', 'Savings Plans',
    'Savings Plan', 'Kubernetes', 'PostgreSQL', 'Postgres',
    'Cloud SQL', 'Compute Engine', 'Cloud Storage', 'Artifact Registry',
    'Secret Manager', 'Pub/Sub', 'BigQuery', 'AlloyDB', 'Memorystore',
    'Persistent Disk', 'Cloud Armor', 'Google Cloud',
    'Blob Storage', 'Managed Disks', 'Managed Disk', 'Event Hubs', 'Event Hub',
    'Service Bus', 'Cosmos DB', 'Key Vault', 'Front Door', 'Log Analytics',
    'Application Insights', 'Container Registry', 'Azure',
}

DESTRUCTIVE = re.compile(
    r'(rm\s+-[a-z]*[rf]|mkfs|dd\s+if=|wipefs|shred\b|'
    r'\bDROP\s+(TABLE|DATABASE|SCHEMA)|TRUNCATE\b|'
    r'terraform\s+destroy|--force\b|--cascade|'
    r'\bdelete-(bucket|db-instance|cluster|volume)|'
    r'kubectl\s+delete\s+(pvc|pv|ns|namespace)|'
    r'\bdestroy\b|\bwipe\b|\bformat the\b)', re.I)

# An installed thing without a version is a runbook that will not reproduce.
INSTALLS = re.compile(r'\b(helm\s+install|helm\s+upgrade|apt(-get)?\s+install|'
                      r'dnf\s+install|yum\s+install|kubectl\s+apply\s+-f\s+https?://|'
                      r'curl\s+-\S*[Ll]\S*\s+https?://\S+\s*\|\s*(ba)?sh)', re.I)
VERSION = re.compile(r'(v?\d+\.\d+(\.\d+)?|--version|:\d+\.\d+|@\d+\.\d+|'
                     r'--chart-version|\bpinned\b|\bversion\b)', re.I)

PLACEHOLDER = re.compile(r'\b(TODO|TBD|FIXME|XXX|lorem ipsum|PLACEHOLDER|\?\?\?)\b')

STOP = set("""a an and or of the with to for in into on at from plus about your you it its
this that these those is are be been will would can could should must may might
one two three all any each every some no not only also then than when where which
new old same other more most less least first last next each""".split())


def strip_code(t):
    """Prose only: fenced blocks and inline spans are not held to prose rules."""
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)
    return re.sub(r'`[^`]*`', ' ', t)


def code_spans(t):
    return re.findall(r'`([^`]+)`', t)


def head_words(line):
    """The content words of a prerequisite line, before any parenthesis or comma."""
    s = line.split('(')[0].split(',')[0].lower()
    s = re.sub(r'[^a-z0-9\s._-]', ' ', s)
    return [w for w in s.split() if w not in STOP and len(w) > 2]


# ---- the fleet, as the prose spells it -----------------------------------
# THE COUNTS ONLY EXIST IN ONE PLACE, and prose has to agree with it. The
# reference build has been resized three times in one edition - five nodes and
# a spare, then three and a spare, then sixteen and two - and each time a
# handful of "six machines" survived in Move hooks, runbook steps and code
# comments, because a number written as a word is invisible to every check
# that looks for figures. Ten of them shipped.
#
# So: every spelled-out count next to machines, nodes or boxes is compared with
# kit.REFERENCE. The allowlist is for the ones that are legitimately a
# different number - the homelab's three, a Ceph quorum's three, an etcd
# control plane's three - and each entry says why, because an allowlist nobody
# has to justify is a way of turning a check off.
WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
         'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11,
         'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
         'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'twenty': 20}

FLEET = re.compile(
    r'\b(' + '|'.join(WORDS) + r')[\s-](machines|nodes|boxes)\b', re.I)

# (the count, what it is counting, why it is not the fleet)
FLEET_OK = {
    (3, 'machines'): 'the homelab on-ramp, and an etcd control-plane quorum',
    (3, 'nodes'): 'the homelab on-ramp, and an etcd control-plane quorum',
    (2, 'machines'): 'a pair - switches, feeds, the survivors of a failure',
    (2, 'nodes'): 'a pair',
}


def check_fleet(out):
    """Every fleet count in prose against kit.REFERENCE."""
    from kit import REFERENCE as R
    ok = {R['nodes'], R['spares'], R['nodes'] + R['spares']}
    for path in sorted(MOVES.glob('*.md')):
        for m in FLEET.finditer(path.read_text(encoding='utf-8')):
            n, noun = WORDS[m.group(1).lower()], m.group(2).lower()
            if n in ok or (n, noun) in FLEET_OK:
                continue
            out.append(
                f'{path.name}: "{m.group(0)}" - the reference build is '
                f'{R["nodes"]} nodes and {R["spares"]} spares, so a count of '
                f'{n} is either stale or needs an entry in FLEET_OK saying '
                f'what it is counting')


def main():
    ms = load_all()
    if not ms:
        print('0 moves audited - 0 findings')
        return 0
    problems = defaultdict(list)
    by_num = {m['num']: m for m in ms}

    for m in ms:
        n = m['num']
        raw = (MOVES / m['file']).read_text(encoding='utf-8')
        run = section(raw, 'The runbook')
        pre = section(raw, 'Before you start')
        run_low = run.lower()
        pre_lines = [i for g in m['pre_groups'] for i in g['items']]
        pre_low = ' '.join(pre_lines).lower()

        # --- 1. a tool the runbook uses that nothing declared ----------------
        used = set()
        for span in code_spans(run):
            first = span.strip().split()
            if first and first[0] in TOOLS:
                used.add(TOOLS[first[0]])
        for tool in sorted(used):
            if tool.lower() not in pre_low and tool.lower() not in raw.lower().split('## the runbook')[0]:
                problems[n].append(f'runbook uses `{tool}` but "Before you start" never names it')

        # --- 2. a prerequisite listed and never used ------------------------
        # A step may refer to a whole group ("bring up every node", "the stack"),
        # which counts as using its members.
        collective = bool(re.search(
            r'\bthe (stack|cluster|nodes|switches|prerequisites|above|rest|remaining)\b'
            r'|everything|all the|each of', run_low))
        for line in pre_lines:
            words = head_words(line)
            if not words:
                continue
            if any(w.rstrip('s') in run_low or w in run_low for w in words):
                continue
            if collective:
                continue
            problems[n].append(f'listed but never used in the runbook: "{line[:56]}"')

        # --- 3. a destructive command with nothing standing behind it -------
        for i, step in enumerate(m['steps'], 1):
            if DESTRUCTIVE.search(step):
                guard = re.search(
                    r'\b(backup|snapshot|restore|verified|verify|confirm|check|'
                    r'after|once|only|first|rollback|retain|keep)\b', step, re.I)
                if not guard:
                    problems[n].append(
                        f'step {i} is destructive with no guard in the same step: '
                        f'"{step[:60]}"')

        # --- 4. software installed without a version ------------------------
        for i, step in enumerate(m['steps'], 1):
            if INSTALLS.search(step) and not VERSION.search(step):
                problems[n].append(f'step {i} installs something without pinning a version')

        # --- 5. names that have drifted --------------------------------------
        prose = strip_code(raw)
        for pat in CANON:
            wrong = {mm.group(0) for mm in re.finditer(pat, prose)
                     if mm.group(0) not in ACCEPT}
            for found in sorted(wrong):
                problems[n].append(f'service name spelled "{found}" - the book spells it '
                                   f'"{CANON[pat]}"')

        # --- 5b. every Move must say something real about all three clouds ---
        seen_services = {o['service'].lower() for o in m['origins']}
        if len(seen_services) < len(m['origins']):
            problems[n].append('two clouds are given the same service name in '
                               '"Leaving from" - name each provider\'s own product')
        for o in m['origins']:
            if o['service'].strip() in ('-', '\u2014', 'n/a', 'N/A', 'none', 'None'):
                problems[n].append(f'{o["cloud"]} has no named service. If the provider has '
                                   f'no equivalent, say what people use there instead')

        # --- 6. placeholders that escaped -----------------------------------
        for hit in set(PLACEHOLDER.findall(raw)):
            problems[n].append(f'placeholder left in the file: {hit}')

        # --- 7. unbalanced backticks -----------------------------------------
        for ln in raw.split('\n'):
            if ln.count('`') % 2 and not ln.strip().startswith('```'):
                problems[n].append(f'unbalanced backtick: "{ln.strip()[:52]}"')
                break

        # --- 8. risk and cutover have to agree -------------------------------
        if m['cutover'] > 15 and m['risk'] == 'Low':
            problems[n].append(f'{m["cutover"]} min of downtime is not a Low-risk Move')
        if m['oneway'] and m['risk'] != 'High':
            problems[n].append(f'Reversible is No but the risk is {m["risk"]} - a Move you '
                               f'cannot undo is High by definition')
        # There is deliberately NO rule here against "High risk, reversible
        # immediately". That combination is not a contradiction, it is the best
        # kind of Move: turning off kube-proxy breaks every service in the
        # cluster if it goes wrong, and is undone by reverting one flag. Risk is
        # blast radius; reversibility is the way back. They are independent.

        # --- 9. the saving has to be the right direction ---------------------
        if m['was'] is not None and m['now'] is not None:
            if m['now'] > m['was'] and not re.search(
                    r'\b(more|increase|costs? more|pay|worth paying|keep paying)\b',
                    m['why'] + ' ' + m['hook'], re.I):
                problems[n].append(f'costs more after (${m["was"]:,.0f} -> ${m["now"]:,.0f}) '
                                   f'but neither the hook nor "Why this works" says so')

    # --- 10. the dependency graph ------------------------------------------
    problems['book'].extend(DEPS.check(ms))

    # --- 11. the equivalence table and the symptom index point at real Moves
    problems['book'].extend(EQ.check(ms))
    problems['book'].extend(SYM.check(ms))

    # --- 12. duplicated prose across the book -------------------------------
    for h, c in Counter(m['hook'] for m in ms).items():
        if c > 1:
            problems['book'].append(f'hook used {c} times: "{h[:60]}"')
    sents = Counter()
    for m in ms:
        body = ' '.join([m['why'], m['rollback'], *m['steps']])
        for s in re.split(r'(?<=[.?])\s+', body):
            s = s.strip()
            if len(s) > 60:
                sents[s] += 1
    for s, c in sents.items():
        if c > 1:
            problems['book'].append(f'sentence repeated {c}x: "{s[:70]}"')
    for t, c in Counter(m['title'].lower() for m in ms).items():
        if c > 1:
            problems['book'].append(f'duplicate title: {t}')

    fleet = []
    check_fleet(fleet)
    problems['book'].extend(fleet)

    problems = {k: v for k, v in problems.items() if v}
    total = sum(len(v) for v in problems.values())
    print(f'{len(ms)} moves audited - {total} findings\n')
    for n in sorted(problems, key=lambda x: (x == 'book', x)):
        print(f'  {n}:')
        for p in problems[n]:
            print(f'      {p}')
    return total


if __name__ == '__main__':
    sys.exit(0 if main() == 0 else 1)
