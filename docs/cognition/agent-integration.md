# Agent integration

Run one MCP process per principal. Product receives `forge-cognition-product` and may additionally receive `forge-brain-product-read-only`. Red Team receives only `forge-cognition-reviewer`; factual knowledge must arrive through the review packet. Curator receives only the Curator cognition profile for governance work.

Never place all three cognition servers in a single agent's active tool set. The example file documents launch commands, not a recommendation to attach every server globally.

To add an agent:

1. Add a `Principal` and profile YAML with explicit project scope.
2. Extend `AccessPolicy` read/write zones with deny-by-default behavior.
3. Add a dedicated SQLite projection and exfiltration tests against every existing private namespace.
4. Add only business tools needed by the role; never add path or principal inputs.
5. Rebuild/verify the store and run the cross-profile E2E suite.
6. Create the evaluated prompt/Skill in a separate change after trigger and near-miss cases are user-approved.

Contract skeletons live under `mcp-forge-cognition/integrations/`; they are intentionally not auto-discovered Claude components.
