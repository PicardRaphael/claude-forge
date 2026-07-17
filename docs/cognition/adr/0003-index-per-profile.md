# ADR 0003 — One lexical index per profile

Status: Accepted

## Decision

Build `forge-product.sqlite`, `red-team.sqlite` and `curator.sqlite` from ACL-filtered canonical sets.

## Consequences

An omitted query filter cannot leak an unauthorized document. Rebuild cost is multiplied by profiles but remains acceptable for v1 scale.
