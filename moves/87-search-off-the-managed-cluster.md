# 87 · Search off the managed cluster

**Layer:** Data · **Leaving:** Managed search clusters · **Risk:** Medium · **Cutover:** 0 min · **Reversible:** 7 days

> Restores a snapshot into a self-hosted OpenSearch cluster, dual-writes across the gap and cuts the read alias, because the index is rebuildable.

## Leaving from
- **AWS:** OpenSearch Service — a provisioned domain exits cleanly through a manual snapshot repository; the serverless collection type has no snapshot API at all.
- **Google Cloud:** Elasticsearch through the marketplace or self-managed — usually already yours, so the exit is a network change rather than a migration.
- **Azure:** Azure AI Search — no backup or restore of any kind, so this estate exits by reindexing from the source of truth.

## Why this works
Search indexes are derived data, which makes this the cleanest exit in the Part: the worst case is a rebuild from the source of truth, and the best case is a restore. For a provisioned domain the path is short — register a manual snapshot repository on the source, restore into a self-hosted cluster reading the same repository, dual-write across the gap, then move the read alias. The automated snapshots cannot be restored off the domain at all, so registering a manual repository is a mandatory first step rather than a convenience. Two service variants have no snapshot path and exit by reindexing instead.

## Before you start

**Access**
- Permission to register a manual snapshot repository on the source domain, and a bucket both sides can read
- The source of truth for every index, because reindexing is the fallback and sometimes the only path

**Software**
- OpenSearch at a pinned version, sized for your hardware rather than for the source's instance types
- A dual-write path in the application, or an indexer that can write to both clusters

**People**
- The owner of each index, to say whether a rebuild is acceptable and how long it takes

## The runbook
1. Establish which variant you have. A provisioned domain restores from a manual repository; a serverless collection and one provider's search service have no restore path and must be reindexed from the source of truth.
2. Register a manual snapshot repository on the source and take a snapshot. The automated ones are not restorable outside the domain, which is the single most important fact in this Move.
3. Size the destination for your hardware rather than copying the source's shape. Shard count and shard size chosen against your machines, dedicated master nodes, and heap at half of memory and below the threshold where compressed pointers stop working.
4. Restore into the self-hosted cluster from the same repository, remembering that restores are constrained by the source's version lineage and that a version gap can block the restore entirely.
5. Dual-write from the application or the indexer, so both clusters stay current while you compare them.
6. Compare result sets on real queries, not document counts. Relevance can differ across versions and configurations, and a search that returns the same number of different documents is a regression nobody will attribute to this Move.
7. Move the read alias, watch for a week, then stop the dual-write.

## Operator's notes
- **Swap:** Where the index is small and rebuildable in under an hour, skip the snapshot entirely and reindex. It is simpler and it proves the rebuild path works, which you want anyway.
- **Do it faster:** Restore into the second cluster from Move 51 first to validate the version lineage. A blocked restore discovered there costs an hour rather than a window.
- **Watch out:** Heap above the compressed-pointer threshold makes a node slower rather than faster, and it is the single most common sizing error on a self-hosted search cluster.
- **Leftovers:** The managed domain bills per instance-hour and per gigabyte of storage, and a domain with no traffic still bills both.

## Rollback
For seven days the alias is moved back and the managed domain is still current because the dual-write is still running. That is the whole rollback and it takes seconds. The point of no return is stopping the dual-write, after which the managed side goes stale — and even then the index can be restored by rebuilding from the source of truth, which is why this Move is Medium risk rather than High.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,240/mo | $180/mo | 92% | 0 min | 2 weeks | 7 days |

## What you can turn off
The managed domain and its storage, seven days after the alias moved and the dual-write stopped.
