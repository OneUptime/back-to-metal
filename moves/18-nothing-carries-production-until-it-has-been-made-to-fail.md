# 18 · Nothing carries production until it has been made to fail

**Layer:** Iron · **Leaving:** — · **Risk:** High · **Cutover:** 0 min · **Reversible:** Immediately; this is the last cheap moment

> Writes the acceptance suite before the order is placed and makes passing it a term of the purchase order, so a failed machine is a return rather than an argument.

## Leaving from
- **AWS:** EC2 instance retirement notices — a failing host was replaced by somebody else, usually before you knew there was a problem.
- **Google Cloud:** Compute Engine live migration — the same protection, applied transparently, which is why nobody who grew up on it has ever burned in a server.
- **Azure:** Virtual Machines planned maintenance and health events — the same again, surfaced as a notification rather than as a hardware fault you had to diagnose.

## Why this works
A machine that has never been pushed hard has not been tested; it has been switched on. Infant mortality in server hardware is real and it concentrates in the first weeks, which means the cheapest moment to find a bad machine is before it has anything on it and while the supplier's return window is still open. That is only true if the acceptance criteria were written down before the order went in and made a term of it. Written afterwards, they become a negotiation. Written into the purchase order, a machine that fails them is a return.

## Before you start

**Access**
- Power and cooling for the whole batch at full load, which is often the constraint on how many can be tested at once
- The supplier's return terms from Move 17, with the acceptance criteria referenced in them

**Software**
- A memory test capable of multiple full passes, and a disk exerciser that can run your own access profile
- A way to log inlet and exhaust temperature and machine check events per machine, unattended

**People**
- Whoever will sign off the delivery, so that pass and fail mean the same thing to them as to you

## The runbook
1. Write the suite before the order goes in and attach it to the purchase order. Every machine runs a multi-pass memory test, a disk exerciser at the workload's own profile plus a full-surface pass per device, a sustained processor and thermal soak with temperatures logged, and both network ports at line rate on the cable that will actually be used.
2. Define failure in advance and in writing: any machine check exception, any correctable memory error trend rather than a single event, any storm of correctable errors on the bus, and any thermal throttle at the rated inlet temperature. A machine that throttles in a cool room will throttle in a warm aisle.
3. Run the suite for long enough to matter. Twenty-four hours of soak per machine is a reasonable floor and forty-eight is better, and the batch can run in parallel if the power is there.
4. Log everything per serial number, and keep the logs. They are the evidence in a return conversation and the baseline you will compare against in Move 111 when a machine starts misbehaving in production.
5. Return the failures immediately rather than setting them aside. A machine kept because it only failed once is a machine that will fail again on a Sunday.
6. Record the point this makes explicitly: the three second-hand machines under a desk that proved the software estate proved nothing about memory error behaviour, dual-feed supplies, bonded links across two switches, controller recovery or drive endurance under a replicated storage cluster. The homelab is an excellent on-ramp and it is not an acceptance test.

## Operator's notes
- **Swap:** Where the batch is too large to soak at once, test in waves and accept the schedule cost. Testing half the machines properly beats testing all of them for an hour.
- **Do it faster:** Automate the suite so a machine is racked, powered and tested without anyone watching it. The suite will be run again on every replacement machine for the next five years.
- **Watch out:** A correctable memory error is not a passing grade. Correctable errors trend upward before a module fails, and the machine that reports a handful during acceptance is the one that reports thousands in month four.
- **Leftovers:** Test images, temporary credentials and the scratch network used for the soak all outlive the exercise unless someone removes them.

## Rollback
Everything here is reversed by putting a machine back in its box, which is exactly why it happens now. The point of no return is the expiry of the supplier's return window: after that a failed acceptance test is a warranty claim rather than a refund, and a machine you have to keep. Keep the per-serial logs somewhere durable and backed up, so the acceptance baseline can be restored and compared when the same machine misbehaves two years later.

## The numbers

| Was | Now | Saved | Cutover | Effort | Wait |
|---|---|---|---|---|---|
| — | — | — | 0 min | 1 week | 1 week |

## What you can turn off
Nothing yet. This Move spends a week to avoid spending a quarter chasing a machine that was never healthy.
