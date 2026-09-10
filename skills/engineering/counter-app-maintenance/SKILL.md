---
name: counter-app-maintenance
description: "Use when refactoring or fixing shared logic in counter apps."
---

# Counter App Maintenance & Refactoring

**Trigger**: Use when maintaining or refactoring similar counter applications (pushup, pullup) with shared logic and GUI+CLI support.

## Core Patterns

### 1. Structural Separation
Separate logic from UI to support CLI fallback (headless mode).
- **`*_lib.py`**: Precision logic, constants (`MIN_REP_INTERVAL`), and persistence.
- **`*_counter.py`**: Tkinter UI (conditional) and CLI loop.

### 2. Implementation Guard
Ensure core classes are defined **outside** conditional dependency blocks.
```python
# GOOD: Logic is always available
class RepAnalyzer: ...

# Conditional UI
try:
    import tkinter as tk
    GUI_OK = True
except ImportError:
    GUI_OK = False
```

## Common Fixes

### Headless AttributeError
- **Issue**: `module has no attribute 'RepAnalyzer'` in CLI mode.
- **Fix**: Move the class definition out of the `if TKINTER_AVAILABLE` block.

### Logic De-duplication
- **Step**: Extract `RepAnalyzer` and `save_session` to a common module if maintaining >1 app.
- **Verification**: Run `python3 -m py_compile <file>.py` then import test in headless env.

## Verification Checklist
- [ ] Logic accessible in CLI fallback?
- [ ] Debounce (0.4s) prevents double-counts?
- [ ] Syntax valid (`py_compile`)?
- [ ] README updated with new features?
- [ ] Sessions ignored in `.gitignore`?
