# Specs

Living documentation for the sports tournament app.

| File | Purpose |
|---|---|
| `00-tech-stack.md` | Technology decisions and rationale |
| `01.index-information.md` | Index page and global shell: typography, colour, motion, i18n, theme |
| `02-floci-local-aws.md` | Floci local AWS emulator: setup and candidate services |
| `03-domain-model.md` | Entities, relationships, invariants (pending) |
| `04-api-contract.md` | Endpoints and schemas (pending) |
| `05-adr/` | Architecture Decision Records |
| `05-adr/001-background-work.md` | Background work runs on SQS + Lambda (accepted) |

## Conventions

- Every spec has a `Status:` line: `proposed` / `accepted` / `superseded`.
- Decisions that change an accepted spec get an ADR instead of a silent edit.
