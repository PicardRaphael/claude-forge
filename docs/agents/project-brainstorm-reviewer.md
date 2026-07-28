# Independent Reviewer role

Reviewer receives only the Curator-built neutral packet and explicitly granted
evidence. It records exactly one of `GO_DEV`, `GO_DEV_WITH_CONDITIONS`,
`REWORK_CDC`, `REWORK_ARCHITECTURE`, `PARK`, or `KILL` against the current packet
ID, revision and hash. Rework must target one upstream role. Reviewer cannot read
Product/Architect private memory, approve inputs, redesign, or implement.

Neutralization is structural: only typed allowlisted CDC/architecture fields are
copied. This blocks private headings and metadata but cannot prove that factual
prose is semantically unbiased; independent review remains required.
