# Streamlit & SaaS Web Dashboard Standard

**Specification Addendum:** `STD-ADD-STREAMLIT-V1.0`

Guidelines and state isolation patterns for Streamlit dashboards, Cloud Run deployments, and SaaS web applications.

---

## 1. Widget State Key Isolation

In Streamlit, avoid `StreamlitValueAssignmentNotAllowedError` by strictly separating interactive button/action keys from persistent parameter keys:

- **Serializable Model Parameters**: Use domain prefixes, e.g.:
  - `driver_fs_hz`, `driver_qts`, `box_vb_l`, `port_fb_hz`
- **Interactive Action Buttons / Trigger Keys**: Use dedicated action prefixes:
  - `btn_apply_combo`, `btn_calculate_ts`, `action_reset`
- **Rule**: Action buttons and modal triggers must NEVER share a prefix with the model parameter dictionary or session-state collection loop.

---

## 2. Dynamic Module Reloading

Streamlit runs in a long-lived Python process. When developing modular backend components under `src/`:

```python
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
import my_engine

importlib.reload(my_engine)
```

---

## 3. Headless UI Testing

Always validate Streamlit rendering without a browser before committing:

```bash
python -c 'from streamlit.testing.v1 import AppTest; at = AppTest.from_file("app.py", default_timeout=30); at.run(); assert not at.exception, at.exception'
```
