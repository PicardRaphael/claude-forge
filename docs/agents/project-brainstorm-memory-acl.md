# Project brainstorm memory and ACL

Authorization is startup-fixed and deny-by-default. `PipelineAuthorization` is
the single decision path for direct ID reads, project projections, lexical index
contents and store verification.

- Curator can read all cognition and alone records approvals/gates/handoffs.
- Product receives its project and current CDC bindings.
- Architect receives the exact approved CDC/current architecture bindings.
- Reviewer receives the exact neutral packet and evidence allowlist.
- Private namespaces always use owner matching; grants never override them.
- Rework appends state that revokes incompatible downstream grants and pointers.

Forbidden and absent IDs both return `resource not found`. SQLite indexes are
separate per principal and rebuilt atomically after each mutation. Canonical
Markdown/YAML remains authoritative; indexes are disposable.
