# GOLDEN_STD.md - Universal Development & AI Agent Contract

**Specification Version:** `1.3.1`

**Last Updated:** `2026-09-08`

**Standard Identifier:** `STD-AGY-DEV-CONTRACT-V1.3.1`

**Central Canonical Repository:** `https://github.com/playloud679/dev_standards`

---

## 0. Modular Development & Module Documentation

Software MUST be developed as cohesive modules with clear responsibilities and explicit interfaces. A module is a logical unit of behavior, implemented by one source file or a coherent group of files; it is not necessarily a single class or function.

For every module:

- Define its responsibility, public interface, dependencies, and boundaries. Keep unrelated responsibilities separate and avoid circular dependencies.
- Adequately comment the source: include a short module-level description and document public APIs, non-obvious decisions, invariants, and edge cases as needed. Follow §6; comments must explain intent rather than repeat instructions.
- Maintain a dedicated Markdown document, by default `docs/modules/<module-path>.md`. Record the source files it covers and link to it from the module-level source comment or docstring.
- Register the module, its source paths, and its dedicated document in `docs/INDEX.md`. Existing documentation paths are acceptable when this mapping is explicit and unambiguous.
- Apply the Documentation Contract (§2) after every patch affecting the module. Code comments and the dedicated document are complementary obligations.

Prefer boundaries that match the project's behavior and architecture; avoid arbitrary file-size limits or splitting code into modules without a clear responsibility. When patching existing code, apply these requirements to the affected modules without refactoring unrelated areas.

---

> [!IMPORTANT]
> ### Sync & Version Check Rule for AI Coding Assistants
> At the start of a new major task or repository setup, the agent should check whether a newer version of `GOLDEN_STD.md` exists in the canonical repository:
> ```bash
> curl -s https://raw.githubusercontent.com/playloud679/dev_standards/refs/heads/main/VERSION
> ```
> If a newer version is available and compatible with the project, propose synchronizing via:
> ```bash
> curl -s https://raw.githubusercontent.com/playloud679/dev_standards/refs/heads/main/GOLDEN_STD.md -o GOLDEN_STD.md
> ```

---

> [!WARNING]
> ### Universal Context & Conflict-Resolution Disclaimer
> `GOLDEN_STD.md` defines universal engineering standards, safety invariants, and quality rules across software, embedded systems, and audio/acoustic engineering.
>
> **AI Agent Operating Directive**:
> 1. You must ALWAYS verify whether any general rule in this document conflicts with the specific intent, domain constraints, or explicit instructions of the active user request.
> 2. **Precedence Hierarchy**:
>    - **Priority 1**: Explicit user instructions in the active conversation.
>    - **Priority 2**: Project-specific requirements, domain physics, or explicit local architecture.
>    - **Priority 3**: `GOLDEN_STD.md` universal engineering rules.
> 3. If a general guideline contradicts a specific user goal (e.g. rapid prototype vs strict production gating, experimental algorithm vs classic invariant), **the user request and project intent take precedence**.
> 4. In case of ambiguity, decide reasonably in the user's best interest or briefly ask for clarification rather than stubbornly applying a conflicting general rule.

---

### Specification Revision History

| Version | Date | Author / Context | Changes / Additions |
|---|---|---|---|
| `1.3.1` | 2026-09-08 | Core Engineering | Required version bumps for application patches only, exempted documentation/test-only changes, assigned lifecycle state to each project, and added documentation-only validation rules. |
| `1.3.0` | 2026-09-08 | Core Engineering | Added initial modular development contract (§0), explicit module-to-doc mapping and post-patch obligations (§2), and aligned module comments, done criteria, and agent template. |
| `1.2.1` | 2026-08-30 | Core Engineering | Added Project Lifecycle & Versioning Stages (§8): Alpha stage (`0.x.y`, current active), Beta stage, and locked Major `1.0.0+` release strictly upon exit from Beta. |
| `1.2.0` | 2026-08-30 | Core Engineering | Added Mandatory Version Bump Rule (§8): Every modification, bug fix, or feature committed MUST increment the release version with tags, changelog, and UI alignment. |
| `1.1.0` | 2026-08-30 | Core Engineering | Added central sync instructions, conflict resolution disclaimer, UI key isolation (§3), Streamlit headless `AppTest` validation (§7), release tagging workflow (§8), Conventional Commits convention (§10), and Audio DSP & Acoustic Test Benches Addendum (§14). |
| `1.0.0` | 2026-08-30 | Core Engineering | Initial baseline specification: branching strategy, documentation contract, token-efficient reading, change scope, tiered testing, error handling, and embedded firmware addendum. |

---

## 1. Branching

Do not develop directly on the default branch.

Use `dev` as the integration branch:

```bash
git switch dev
```

If `dev` does not exist:

```bash
git switch -c dev
git push -u origin dev
```

Default flow:

1. Work on `dev`.
2. Commit scoped changes.
3. Push `dev`.
4. Open a draft PR from `dev` to the default branch when requested.
5. Merge manually after review.

Before staging or committing:

```bash
git status -sb
git diff --stat
git diff --check
```

Stage explicit files only. Do not use broad staging (`git add .` or `git add -A`) when the worktree contains unrelated or untracked files.

---

## 2. Documentation Contract

Documentation must stay in sync with source.

When modifying a source module, update the matching documentation in the same change:

| Changed file | Required documentation |
|---|---|
| `src/foo.py` | `docs/modules/foo.md` |
| `src/services/bar.ts` | `docs/modules/services/bar.md` |
| `src/drivers/bar.cpp` and `src/drivers/bar.h` (one logical module) | `docs/modules/drivers/bar.md` |
| user-visible UI behavior | `USER_GUIDE.md` and/or `docs/INDEX.md` |
| release/version behavior | `CHANGELOG.md`, `VERSION`, package metadata |

Use the module-to-doc mapping established in §0. If a matching doc or `docs/INDEX.md` does not exist, create it. Preserve source-relative paths by default to avoid collisions between modules with the same basename. A module spanning multiple source files has one dedicated document listing all covered files.

Docs should explain public APIs, invariants, assumptions, edge cases, failure modes, and the tests protecting the behavior. Future agents should be able to read docs before source to save tokens.

### Post-Patch Documentation Obligations

Before handing off any patch affecting source:

1. Identify all affected modules, including dependent modules whose contracts changed, and locate their dedicated `.md` files through `docs/INDEX.md`.
2. Update each affected module document in the same change to match the resulting behavior, interfaces, dependencies, and constraints. For an internal-only patch, record the relevant implementation rationale or validation without inventing an API change.
3. Review and update module descriptions, API documentation, inline comments, and source-to-doc pointers where needed.
4. For added, renamed, split, or removed modules, update the source-to-doc mapping, references, and index; remove or explicitly archive obsolete module documents.
5. Record relevant validation commands and actual outcomes in the module document, including checks not run and why. Update user guides and release documentation when affected.
6. Verify that source-to-doc links and index entries resolve, and mention the affected modules and updated documentation in the final handoff.

---

## 3. Source-to-UI Contract

If backend behavior changes, update every dependent UI and caller.

Checklist:

- New function/module: add caller or UI integration.
- Changed function signature: update all call sites and tests.
- Changed behavior: update user-facing text if users need to understand it.
- New parameter: hide it unless it is relevant for the active mode.
- Disabled component: hide its parameters instead of leaving confusing controls.
- Generated output: update previews, labels, downloads, and tests.

UI rule:

```text
Include selected     -> relevant parameters visible
Include not selected -> related parameters hidden
```

UI state and widget key isolation:
- Serialized parameter state keys must have domain prefixes (e.g. `driver_`, `box_`, `ts_`).
- Interactive action buttons, triggers, and temporary widget keys must use distinct prefixes (e.g. `btn_`, `action_`, `temp_`).
- Action buttons must NEVER share prefixes with persistent/serializable parameters to prevent widget state assignment collisions (e.g., `StreamlitValueAssignmentNotAllowedError`).

Primary/base controls must not be hidden in an `Advanced` section. Use `Advanced` only for rare, dangerous, or expert-only controls.

---

## 4. Token-Efficient Reading

Do not read the whole repo unless needed.

Preferred order:

1. Read `GOLDEN_STD.md`, `AGENTS.md`, `README.md`, and `docs/INDEX.md`.
2. Use `rg` to locate relevant symbols.
3. Read matching docs before source.
4. Read only the source slices needed.
5. Read focused tests around the behavior.
6. Expand scope only when evidence requires it.

Preferred commands:

```bash
rg "symbol_or_text"
rg --files
sed -n '120,220p' file.py
git diff -- file.py
```

Avoid dumping large files into context.

---

## 5. Change Scope

Keep edits narrow.

Do:

- fix the requested behavior
- update directly related tests and docs
- preserve existing style
- use existing helpers and patterns

Do not:

- refactor unrelated code
- rename unrelated things
- reformat whole files
- delete user work
- modify generated or temporary files unless explicitly required

If the worktree is dirty, assume unknown changes are user-owned.

Never run destructive commands such as `git reset --hard`, `git checkout -- .`, or broad `rm -rf` unless explicitly requested and confirmed.

---

## 6. Code Comments

Every module must be adequately commented as required by §0. Keep comments concise and useful; comment density is not a quality metric. Include a module-level description and a pointer to the dedicated Markdown document, and document public API inputs, outputs, and failure behavior where these are not already clear from the language's declarations.

Use comments to explain:

- why a non-obvious choice exists
- invariants that future edits must preserve
- geometry, state, API, or UI contracts
- workarounds for library behavior
- edge cases that tests protect

Avoid comments that merely restate the code.

Good:

```python
# Adapter owns driver-side geometry; keep throat flange UI status-only
# while preserving generation defaults for the assembly path.
_ft_sp = _ta_flange_sp
```

Bad:

```python
# Set _ft_sp equal to _ta_flange_sp.
_ft_sp = _ta_flange_sp
```

If the explanation needs more than a few lines, put the full reasoning in the matching doc file and leave only a short pointer in code.

---

## 7. Testing

Use tiered tests.

During focused development and minor patches, run the smallest relevant checks:

```bash
python -m py_compile path/to/file.py
python tests/test_specific.py --match "relevant behavior"
# For Streamlit apps, run a headless AppTest to verify rendering with no exceptions:
python -c 'from streamlit.testing.v1 import AppTest; at = AppTest.from_file("app.py", default_timeout=30); at.run(); assert not at.exception, at.exception'
```

For shared logic, run the affected suite after focused checks.

Do not run the full suite after every small edit by default. Full runs are expensive and should be reserved for push, PR, release, or final handoff readiness, or for changes with broad blast radius.

For changes affecting executable behavior (including source, tests, dependencies, build/runtime configuration, or executable documentation examples), run the full active suite before push, PR, release, or final handoff of a completed change:

```bash
make test
```

If the project uses another standard command, use that instead:

```bash
npm test
pnpm test
pytest
cargo test
```

For documentation-only patches, including accompanying version strings, badges, and changelog entries that do not affect executable behavior, the application suite is not required. Instead:

- Run `git diff --check`.
- Verify changed local links, anchors, and module-to-doc mappings where applicable.
- Check consistency of instructions, cross-references, versions, and changelog entries.
- Run the project's documentation lint/build checks when configured.

If a patch also affects executable behavior, apply the code validation requirements above. Classify by impact, not file extension; a documentation file containing changed executable examples may require relevant code checks. Changes to firmware hardware assumptions also follow §13.

Report exact validation commands and outcomes, including why the application suite was not run for a documentation-only patch. Do not claim a test passed unless it was actually run.

---

## 8. Versioning & Mandatory Bump per Application Patch

> [!IMPORTANT]
> ### Mandatory Version Bump Rule
> **EVERY application patch MUST increment the release version. Changes limited to documentation, tests, or both do not require a version bump.**
> Application patches include application or firmware source changes, refactoring, bug fixes, UX changes, features, and changes to dependencies or build/runtime configuration that affect the delivered application. Mixed patches containing application changes require a bump even when they also update docs or tests.
> For application patches, the bump is mandatory before final handoff, commit, or deployment and does not require a separate user request. A patch is a coherent change, not each intermediate file save; every subsequent application change commit must advance the version again. Every deployed application state must have a monotonically increasing, unambiguous release version.
>
> 1. **Patch (`0.y.Z+1` / `x.y.Z+1`)**: Bug fixes, calculation corrections, UX tweaks, refactoring, and other minor application patches.
> 2. **Minor (`0.Y+1.0` / `x.Y+1.0`)**: New features, new workflows/tabs, hardware integrations, cloud sync additions.
> 3. **Major (`1.0.0` / `X+1.0.0`)**: Transition from Beta to Production General Availability (GA), or subsequent breaking changes in GA.

### Project Lifecycle & Versioning Stages:

Each project declares its own current lifecycle stage in `README.md` or `AGENTS.md`, together with its release criteria. This universal standard does not prescribe a current stage. Preserve the project's declared stage and version series; adopting this standard must not reset an existing version to `0.x.y`. If the stage is undocumented, preserve the existing version series and report the missing declaration without assuming Alpha or promoting the project to GA.

- **Alpha Stage (`0.x.y`)**:
  - Rapid evolution, active experimentation, UI refinement, and foundational mechanics.
  - All version bumps are strictly within `0.x.y` (e.g. `0.4.1`, `0.5.0`, `0.12.32`).
  - Major version `1.0.0` is strictly locked and prohibited during Alpha.
- **Beta Stage (`0.x.y` / feature-complete)**:
  - Architecture stabilized, full feature set implemented, undergoing real-world validation, user testing, and hardening.
- **Production / General Availability (`1.0.0+`)**:
  - Major release `1.0.0` is cut ONLY upon formal exit from Beta once production stability and specification completeness are certified.
  - Subsequent `X+1.0.0` bumps are reserved exclusively for breaking architectural changes in GA.

For EVERY application patch:

1. Update `VERSION` (single-line SemVer string).
2. Update package metadata where present (`pyproject.toml`, `package.json`, or `Cargo.toml`).
3. Update `CHANGELOG.md` with date, summary, actual validation outcomes, and pass counts when tests ran. Record checks not run and why instead of inventing pass counts.
4. Update visible badges and versions in `README.md` and UI where present.

When a release is requested or already authorized, create an annotated Git tag (`git tag -a vX.Y.Z -m "Release vX.Y.Z: summary"`) and push the authorized branch and release tag. The mandatory local bump does not itself authorize a commit, tag, push, or release.

Changelog format:

```markdown
## x.y.z (YYYY-MM-DD)

- **Area**: concise description of what changed and why.
- **Docs/Test**: mention updated docs, tests, and version files.
```

### Specification (`GOLDEN_STD.md`) Versioning:
The specification version tracks published editions of this standard independently of application releases. Documentation-only and test-only patches, including edits to this standard, do not require a version bump. When publishing a new specification edition, synchronize its header `Specification Version`, identifier, revision history, `VERSION`, README badge, and changelog.

---

## 9. Error Handling

Do not hide failures.

When generation or transformation can fail:

- validate inputs before expensive work
- show a clear user-facing error
- preserve technical detail in logs or tests
- add a regression test for known failures

Generated outputs must satisfy project invariants, for example:

- closed mesh
- positive volume
- single body where expected
- non-empty output
- no silent fallback that changes semantics

---

## 10. Commit and PR

Before commit:

```bash
git status -sb
git diff --check
```

Before push, PR, release, or final handoff, complete the validation required by §7. For changes affecting executable behavior:

```bash
make test
```

Stage only intended files:

```bash
git add file1 file2 docs/file.md tests/test_file.py
```

Commit with a terse concrete message using Conventional Commits:

```bash
git commit -m "feat(ui): add dual Le metrics display"
```

Conventional commit prefixes:
- `feat:` new user-facing functionality
- `fix:` bug fix
- `docs:` documentation updates
- `test:` test suite updates
- `refactor:` code restructuring without external behavior change
- `release:` version release and metadata synchronization

Push:

```bash
git push origin dev
```

PR body:

```markdown
## Summary

- What changed.
- Why it changed.
- User or developer impact.

## Validation

- Commands run.
- Test results.

## Notes

- Known limitations.
- Anything not run.
```

Default PR state is draft unless the user explicitly asks otherwise.

---

## 11. Agent Operating Rules

The agent should:

- explain briefly what it is doing while working
- implement when the request is clear
- ask only when blocked or ambiguity is risky
- prefer existing project patterns over new abstractions
- use structured APIs instead of fragile string manipulation when reasonable
- use `apply_patch` or `replace_file_content` for manual edits
- never overwrite unrelated changes
- never stop at analysis when asked to complete work

---

## 12. Done Definition

A task is done only when:

- requested behavior is implemented
- relevant docs are updated
- affected modules have adequate source comments, dedicated `.md` documentation, and current mappings in `docs/INDEX.md`; §2 post-patch obligations are complete
- relevant focused tests and the full active suite pass for executable changes as required by §7
- documentation-only patches pass the documentation checks in §7; the reason for not running the application suite is reported
- version/changelog and existing version metadata are updated for application patches as required by §8; documentation-only and test-only patches do not require a version bump
- commit is created when requested
- push/PR is done when requested
- remaining risks are explicitly stated

---

## 13. Embedded Firmware Addendum

Use this section for firmware, board-support packages, device drivers, and hardware-facing applications (ESP32, STM32, Arduino, Raspberry Pi, Zephyr, FreeRTOS).

### Required Hardware Docs

Maintain these docs when applicable:

| Area | Suggested doc |
|---|---|
| Board/MCU/clock/flash/RAM assumptions | `docs/hardware.md` |
| Pin assignments, electrical direction, boot states | `docs/pinout.md` |
| Wiring, connectors, power rails, voltage levels | `docs/wiring.md` |
| UART/I2C/SPI/CAN/BLE/WiFi protocol payloads | `docs/protocol.md` |
| Build, flash, debug, monitor commands | `docs/build.md` |
| EEPROM/NVS/flash config layout | `docs/storage.md` |
| Timing, ISR, watchdog, debounce, retry policy | `docs/timing.md` |

If the project uses different names, follow the local convention.

### Hardware Safety Contract

Never silently change:

- pin assignments
- pin direction or default boot state
- voltage/current assumptions
- relay, motor, heater, charger, battery, or high-current behavior
- watchdog, brownout, fail-safe, or emergency-stop behavior
- persistent storage layout
- protocol framing, baudrate, checksum, or compatibility

When touching any of these, update docs, tests, and the final report with the hardware risk.

Default outputs must boot into a safe state. Actuators should remain disabled until configuration and sanity checks complete.

### Build Matrix

Document all build environments and board variants.

Examples:

```bash
pio run -e esp32-c6-devkitc-1
pio run -e release
cmake --build build
make firmware
```

For minor patches, build only the affected target. For shared drivers, HAL/platform code, protocol changes, or release readiness, build every affected environment.

### Upload Policy

Do not flash hardware by default.

Upload only when:

- explicitly requested by the user
- required to validate a hardware-facing change
- the target board and port are known

Always state the target and port before upload.

Examples:

```bash
pio run -e board_name -t upload --upload-port /dev/cu.usbmodem101
```

Never guess a serial port when multiple devices are connected.

### Embedded Test Hierarchy

During minor firmware patches:

```bash
pio run -e affected_env
python -m pytest tests/test_specific.py
```

For shared firmware logic:

```bash
pio run -e affected_env_1
pio run -e affected_env_2
python -m pytest
```

Before push, PR, release, or final handoff of firmware changes:

```bash
pio run
python -m pytest
```

If hardware-facing behavior changed, add a smoke test on the real board before release when hardware is available. Keep the smoke test short and explicit:

- boot confirms safe state
- expected peripheral initializes
- serial/log output is sane
- actuator outputs remain safe unless intentionally tested
- protocol command returns expected response

### Realtime and Timing Contract

Document and protect:

- ISR responsibilities and maximum expected duration
- polling rates
- debounce intervals
- timeout values
- retry/backoff behavior
- watchdog feed points
- blocking calls in control loops
- sleep/power-save behavior

Code comments should mark local invariants briefly. Detailed timing rationale belongs in `docs/timing.md` or the matching module doc.

### Protocol and Storage Contract

Protocol changes require:

- payload/schema docs
- backwards-compatibility note
- parser/encoder tests
- version bump if external behavior changes

Persistent storage changes require:

- layout docs
- migration/default behavior
- corruption or missing-key behavior
- tests for old and new layouts when practical

### Logging Contract

Logs must help debug hardware without breaking realtime behavior.

- Keep high-frequency loops quiet by default.
- Use log levels or compile-time flags.
- Do not print secrets, WiFi credentials, tokens, or private keys.
- Do not add blocking logs in ISR or tight control paths.

### Embedded Done Definition

An embedded task is done only when:

- affected firmware targets build
- relevant unit/host tests pass
- docs match hardware assumptions
- pin/protocol/storage/timing changes are called out
- upload/hardware smoke test is run when required or explicitly skipped with a reason
- full build/test matrix passes before push, PR, release, or final handoff of firmware changes; documentation-only patches follow §7, but changes to documented pin/protocol/storage/timing or safety assumptions require the relevant engineering validation above

---

## 14. Audio DSP & Acoustic Test Benches Addendum

Use this section for acoustic simulators, impedance analyzers, audio test benches, and loudspeaker DSP.

### Acoustic & Physical Invariants

Never violate physical and electroacoustic constraints:
- **Resonance & Impedance**: $Z_{\text{max}} > R_e > 0$, and bandwidth $f_2 > f_1 > 0$.
- **Quality Factors**: $Q_{ts} = \frac{Q_{ms} \cdot Q_{es}}{Q_{ms} + Q_{es}} < \min(Q_{es}, Q_{ms})$.
- **Half-Power Bandwidth**: If voice coil inductance $L_e$ masks high-frequency crossing $f_2$, resolve via the AES/Thiele-Small geometric mean relation: $f_s = \sqrt{f_1 \cdot f_2} \implies f_2 = \frac{f_s^2}{f_1}$.
- **Inductance Frequencies**: Report voice coil inductance at standard frequencies ($L_e @ 1\text{ kHz}$ and $L_e @ 10\text{ kHz}$) to account for iron losses and eddy current dispersion.
- **Mechanical Resonance Search**: Identify true local maxima (with zero phase crossing) rather than broad `argmax()` across high-frequency inductive ramps up to 20 kHz.

### Audio Device & Sampling Safety

- Validate duplex audio support (stereo input and output channels $\ge 2$) before initiating sweeps.
- Verify sample rate consistency (e.g. 44.1 kHz on both input/output host APIs).
- Add leading/trailing latency cushions (e.g. $\ge 0.5\text{ s}$) to prevent truncating high-frequency chirp tails.
- Handle empty device lists safely without crashing UI rendering.
