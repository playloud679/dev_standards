# Changelog - dev_standards

All notable changes to the development standards specification and tooling are documented in this file.

## [1.3.1] - 2026-09-08

### Changed
- Required a version bump for application patches only, exempted documentation/test-only changes, and aligned completion criteria and the agent template.
- Clarified that specification editions are versioned on publication; editing the standard alone does not require a bump.
- Assigned lifecycle declarations and release criteria to individual projects, preserving existing version series.
- Added documentation-only validation requirements and aligned handoff and firmware guidance; executable changes retain code validation requirements.
- Synchronized specification and repository version metadata to `1.3.1`.

### Validation
- `git diff --check` passed; reviewed the diff and verified version consistency and section references with `rg`.
- No local link targets changed. No documentation lint/build configuration is present; application tests were not run because this patch changes documentation and version metadata only.

## [1.3.0] - 2026-09-08

### Added
- Initial modular development contract: clear responsibilities, explicit interfaces, adequate source comments, and one dedicated Markdown document per logical module.
- Explicit source-to-doc mapping in `docs/INDEX.md` and post-patch obligations covering affected modules, comments, validation, and module lifecycle changes.

### Changed
- Aligned the agent instructions template, code comment requirements, and done criteria with the module documentation contract.
- Synchronized the specification header, `VERSION`, and README badge to `1.3.0`.

## [1.1.0] - 2026-08-30

### Added
- Central synchronization directive and `scripts/sync_standards.py` tool.
- Universal context and conflict-resolution disclaimer for AI agents.
- Section 3: UI State Key Isolation (`btn_` / `action_` vs model params).
- Section 7: Streamlit headless `AppTest` validation.
- Section 8: Formal release workflow and SemVer tagging guidelines.
- Section 10: Conventional Commits standard (`feat:`, `fix:`, `docs:`, `test:`, `release:`).
- Section 14: Audio DSP & Acoustic Test Benches Addendum (`addenda/AUDIO_DSP_ACOUSTICS.md`).
- Addenda for Embedded Firmware (`addenda/EMBEDDED_FIRMWARE.md`) and Streamlit/SaaS (`addenda/STREAMLIT_SAAS.md`).
- Project templates for `AGENTS.md` and `CHANGELOG.md`.

## [1.0.0] - 2026-08-30

### Added
- Initial baseline specification: branching strategy, documentation contract, token-efficient reading, change scope, tiered testing, error handling, and embedded firmware addendum.
