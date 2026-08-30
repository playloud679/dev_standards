# Embedded Firmware & IoT Standard

**Specification Addendum:** `STD-ADD-EMBEDDED-V1.0`

Guidelines and safety invariants for embedded microcontrollers (ESP32, STM32, Arduino, RP2040), RTOS, and sensor/actuator projects.

---

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
