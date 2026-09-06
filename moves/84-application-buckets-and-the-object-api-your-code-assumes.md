# 84 · Application buckets, and the object API your code assumes

**Layer:** Data · **Leaving:** Managed object storage (application buckets) · **Risk:** High · **Cutover:** 0 min · **Reversible:** 30 days

> Mirrors application buckets onto the cluster's own object store behind a dual-write window, then audits every client for the object-store behaviour it assumes.

## Leaving from
- **AWS:** S3 — multipart entity tags that are not a plain digest, so verification needs matching part sizes to mean anything.
- **Google Cloud:** Cloud Storage — a separate checksum alongside the digest, with the digest absent on composed objects.
- **Azure:** Blob Storage — a block composition model, so the checksum you compare is not the one you uploaded.

## Why this works
Copying objects is the easy half and it still has three traps: the entity tag on a multipart object is not a digest of the content, so a naive comparison reports every large object as different; non-current versions and delete markers are not copied by any sync tool; and storage class, access policy, immutability, lifecycle, cross-origin rules and event wiring are all configuration that has to be rebuilt by hand. The larger half is the client audit, because application code accumulates assumptions about the object store it was written against, and those assumptions are invisible until they are wrong.

## Before you start

**Access**
- Read access to every bucket, including the ones only a pipeline uses, and write access to the destination
- The object store from Move 49, made durable by Move 54, with capacity checked against the real total

**Software**
- `rclone` or `mc` at a pinned version, with the checksum mode chosen per source cloud rather than defaulted
- A comparison script written once with three modes, or three times, because the verification differs per provider

**People**
- The owner of every application that reads or writes a bucket, for the client audit

## The runbook
1. Inventory the buckets and their real sizes, including non-current versions, which are frequently larger than the current data and are not copied by any tool.
2. Write the comparison properly. A multipart entity tag is a digest of digests, so it only matches when the part size matches; one provider gives a separate checksum that is absent on composed objects; and one composes blocks so that the value you compare is not the value you uploaded. Choose the mode per source.
3. Rebuild the configuration by hand: storage class, access policy, immutability, lifecycle rules, cross-origin rules and event wiring. None of it is copied by a sync tool and all of it is load-bearing somewhere.
4. Do the client audit, which is most of the four weeks. Addressing style, signature clock skew, presigned link lifetimes, assumptions about part sizes, and conditional writes. Each of these is a code change or a configuration change, and each is silent until it fails.
5. Dual-write for a period: the application writes to both stores and reads from the old one. This is what makes the thirty-day window real rather than nominal.
6. Run the initial copy, then repeated incremental copies until the delta is small, then switch reads. Verify with the comparison script rather than with a file count.
7. Keep both stores for thirty days, with the dual-write running, before deleting anything on either side.

## Operator's notes
- **Swap:** Where a bucket is only read by one application and is small, a straight copy during a short outage is far simpler than a dual-write window and finishes in an hour.
- **Do it faster:** Copy the cold data weeks in advance and the hot data at the end. Most buckets are mostly cold and the final delta is then measured in gigabytes rather than terabytes.
- **Watch out:** Presigned links generated before the switch keep pointing at the old store until they expire. Their lifetime is the minimum length of your dual-read window, and somebody has always set one to a year.
- **Leftovers:** Non-current versions and delete markers keep billing after the current objects are deleted. A lifecycle rule that expires them is required and takes at least a day to run.

## Rollback
For thirty days the old bucket still holds everything and the application can be pointed back at it, with anything written in the interim restored by copying the delta in the other direction. That reverse copy is why the dual-write exists. The point of no return is the deletion of the source bucket in Move 38, against a signed data-owner approval. Verify the comparison script passes on the last day before that deletion rather than trusting a copy that finished weeks earlier.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| $2,940/mo | $210/mo | 93% | 0 min | 4 weeks | 30 days |

## What you can turn off
Application buckets and their versions after thirty days, and their lifecycle and replication rules once the comparison passes on the final day. Archive buckets stay, per Move 85.
