# 38 · The drives that leave, and the snapshots that stay

**Layer:** Site · **Leaving:** Provider-managed snapshot, image and backup retention · **Risk:** High · **Cutover:** 0 min · **Reversible:** No

> Sanitises the drives that leave against serial-level certificates and destroys the key material behind the snapshots, images and vaults that stay.

## Leaving from
- **AWS:** EBS snapshots, AMIs and Backup vaults — deletion is an API call, and vault lock and recycle bin settings can prevent it entirely.
- **Google Cloud:** Persistent Disk snapshots, machine images and Backup vaults — the same, with retention policies that outlive the resources they protected.
- **Azure:** Managed Disks snapshots, images and Recovery Services vaults — the same again, with soft delete on by default and purge protection that delays completion by days.

## Why this works
Decommissioning has two halves and most programmes do only one. On hardware you hold, sanitisation follows the current standard, which now defers technique to the media-specific specification: cryptographic erase for self-encrypting media, the drive's own sanitise command for NVMe, and physical destruction only where a data classification or a contract demands it — because multi-pass overwriting a solid-state device is theatre when wear levelling keeps cells out of reach of the write path. On the cloud side you will never hold the platter, so the only real lever is the key. Destroy the key material first, then delete the snapshots, images, object versions and vaults, and expect deletion to complete days after you asked.

## Before you start

**Access**
- Administrative rights to delete snapshots, images and vaults in every account, including the locked ones
- The key management permissions needed to schedule destruction of the keys that wrapped them

**Software**
- An inventory of every snapshot, image, object version and vault, per account, exported rather than browsed
- A sanitisation tool appropriate to each media type, and the certificate template you will require from a processor

**People**
- Whoever owns data classification, because destruction is their decision and their sign-off

## The runbook
1. Build the inventory first, across every account and region. Snapshots outlive the resources they protected, and copies made into other regions do not appear in the region you are looking at.
2. Confirm what can still be restored from each item and for how long, and get written agreement from the data owner that it is no longer needed. Nothing in this Move is undone, so the check happens before, not after.
3. On hardware you hold, sanitise per media type: cryptographic erase where the device supports it, the device's own sanitise command for NVMe, physical destruction only where policy requires it. Verify each unit and record the result against its serial number.
4. Require a certificate listing serial numbers from any processor you use, under a chain of custody, and check their certification before the equipment leaves the building. Keep the disposal note that satisfies your waste-electricals obligation.
5. On the cloud side, schedule destruction of the key material that wrapped the data before deleting anything, and confirm the destruction has completed rather than merely been scheduled.
6. Delete the snapshots, images, object versions and vaults, then verify. Allow for soft-delete windows, recycle bins and purge protection, all of which mean the deletion you requested completes days later, and some of which will refuse until a lock expires.
7. Re-run the inventory afterwards and confirm it is empty. An inventory that still lists items after a deletion pass is the normal outcome of the first attempt.

## Operator's notes
- **Swap:** Where a vault lock prevents deletion until a retention period expires, the honest answer is to diary the date and pay the storage until then. Locks exist precisely so that they cannot be worked around.
- **Do it faster:** Destroy the key first. On every provider, that renders the data unreadable immediately even where the objects themselves take days to disappear.
- **Watch out:** Cross-region and cross-account copies are the ones that survive a cleanup. Search by account and by region rather than trusting a single console view.
- **Leftovers:** Object storage keeps non-current versions and delete markers after a delete. A lifecycle rule that expires them is required, and it takes at least a day to run.

## Rollback
This Move is irreversible by design and there is no rollback: once the key material is destroyed the data cannot be restored, and a sanitised drive cannot be read back. The point of no return is the key destruction, which precedes the deletions and is the moment everything downstream becomes unrecoverable. That is why step two requires written agreement from the data owner first. Keep the inventory, the certificates and the destruction records for the audit in Move 119.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | 2 weeks |

## What you can turn off
Snapshots, machine images, object versions and backup vaults in the accounts that have been emptied — after the data owner has signed, and never before.
