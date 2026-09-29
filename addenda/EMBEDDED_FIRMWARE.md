# Embedded Firmware & IoT Standard

**Specification Addendum:** `STD-ADD-EMBEDDED-V1.0`

Guidelines and safety invariants for embedded microcontrollers (ESP32, STM32, Arduino, RP2040), RTOS, and sensor/actuator projects.

---

> **antirez style reminder:** minimalism, near-zero dependencies, efficiency, zero complexity. Firmware also follows the antirez style: keep the smallest correct implementation, avoid unnecessary dependencies, and never trade safety for complexity.

## 1. Hardware Safety Invariants

- **Safe Default Boot State**: All actuator pins (relays, MOSFETs, motors, heaters) must remain in a de-energized/safe state during boot and reset.
- **Fail-Safe Watchdog**: Control loops involving mechanical or thermal actuators must implement an active watchdog timer (WDT) and brown-out protection.
- **No Silent Pin / Voltage Changes**: Never modify GPIO numbers, electrical direction, pull-up/pull-down modes, or ADC voltage dividers without explicit documentation and tests.

---

## 2. Realtime & Control Loops

- **Non-blocking ISRs**: Interrupt service routines must perform minimal work (flag raising or queue dispatch) and must never perform blocking delays, I/O operations, or memory allocations.
- **Debouncing & Timeouts**: All hardware inputs and network/bus requests (I2C, SPI, UART, Modbus) must enforce deterministic timeouts and non-blocking state machines.

---

## 3. Flash & Non-Volatile Storage (NVS/EEPROM)

- Maintain explicit layout documentation for persistent config tables.
- Protect against flash wear (avoid excessive write cycles inside fast control loops).
- Implement migration and default fallback logic for missing or corrupted keys.

---

## 4. Hardware Documentation & Delivery Contract

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

Before integration or release of firmware changes, run the full project build/test matrix. For local commits, branch pushes, draft PRs, and handoffs, use affected targets and tests unless broader impact requires the full matrix, following [the core testing contract](../GOLDEN_STD.md#7-testing). Example full-matrix commands:

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
- validation matches impact and delivery stage: affected targets/tests for local patches, full build/test matrix before integration or release; documentation-only patches follow the core §7, but changes to documented pin/protocol/storage/timing or safety assumptions require the relevant engineering validation above
