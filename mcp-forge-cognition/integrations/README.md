# Integration contract skeletons

These legacy contracts remain for the original Product/Red Team flow. The
Codex-native project-brainstorm roles are installed globally under
`~/.codex/agents/`, with their Skills under `~/.codex/skills/`; see
`docs/agents/project-brainstorm.md`.

- CDC, Architect and Reviewer run as narrow global Codex subagents.
- Each role writes only its assigned handoff and does not modify product code.
- Curator should be a main-thread Skill because it performs dense governed MCP writes.
