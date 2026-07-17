# Integration contract skeletons

These files are intentionally not Claude Code `agents/*.md` or `SKILL.md` files. They define role/tool/data contracts after the MCP has passed its tests, while deferring prompt discovery, trigger evaluation and surface-specific enforcement to a separate evaluated change.

- Product should run in the main conversational context because it needs interactive ideation and repeated MCP writes.
- Red Team should run in an isolated session/task with only the reviewer profile. A native subagent is acceptable only after proving its MCP access on the target surface.
- Curator should be a main-thread Skill because it performs dense governed MCP writes.
