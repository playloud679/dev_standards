# Development Standards & AI Agent Engineering Guide

[![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)](VERSION)
[![Standard](https://img.shields.io/badge/standard-GOLDEN__STD-gold.svg)](GOLDEN_STD.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Central single source of truth for engineering contracts, coding standards, AI agent operating directives, and project templates across software, firmware, and acoustics.

---

## 📖 Core Documents

- [**`GOLDEN_STD.md`**](GOLDEN_STD.md): The universal development contract (modular architecture, module comments and dedicated docs, post-patch doc sync, branching, UI isolation, testing, commit conventions, versioning, source-of-truth protection for generated artifacts, conflict-resolution disclaimer).
- [**`CHANGELOG.md`**](CHANGELOG.md): Revision history of the specification.

### 🧩 Modular Addenda

- [**Audio DSP & Acoustics Standard**](addenda/AUDIO_DSP_ACOUSTICS.md)
- [**Embedded Firmware & IoT Standard**](addenda/EMBEDDED_FIRMWARE.md)
- [**Streamlit & SaaS Web Dashboard Standard**](addenda/STREAMLIT_SAAS.md)

The core contains universal rules; domain details live in these addenda. Declare the applicable addenda in each project's `AGENTS.md` or `README.md`.

### 📋 Project Templates

- [**`AGENTS.md.template`**](templates/AGENTS.md.template)
- [**`CHANGELOG.md.template`**](templates/CHANGELOG.md.template)

---

## ⚡ Quick Sync into Any Project

To check for updates or pull the latest `GOLDEN_STD.md` into any repository:

```bash
# Direct one-line curl download:
curl -s https://raw.githubusercontent.com/playloud679/dev_standards/refs/heads/main/GOLDEN_STD.md -o GOLDEN_STD.md
```

Or using the built-in sync tool:

```bash
# Check version:
python scripts/sync_standards.py --check --target /path/to/my_project

# Synchronize:
python scripts/sync_standards.py --target /path/to/my_project
```

Both methods synchronize only `GOLDEN_STD.md`. Copy applicable files from `addenda/` separately, from the same canonical revision, keeping their relative paths. See [addendum selection and synchronization](GOLDEN_STD.md#15-selecting-and-synchronizing-addenda).

---

## 🛡️ AI Agent Directive & Conflict Resolution

AI Coding Assistants working in any repository adhering to this standard must follow the [Universal Context & Conflict-Resolution Disclaimer](GOLDEN_STD.md):
1. **Priority 1**: Explicit user instructions in the active conversation.
2. **Priority 2**: Project-specific constraints, physics, and local architecture.
3. **Priority 3**: General `GOLDEN_STD.md` rules.

*When in doubt, the agent makes reasoned decisions in the user's best interest or briefly asks for clarification rather than blindly enforcing conflicting rules.*
