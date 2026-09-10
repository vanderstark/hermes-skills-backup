# Debugging Headless Failures in Counter Apps

## Transcript of AttributeError Fix (2026-08-29)

### Issue
When running a counter app (pushup or pullup) in a headless environment, the application failed with:
`AttributeError: module 'pullup_counter' has no attribute 'RepAnalyzer'`

### Root Cause
The `RepAnalyzer` class was defined inside a conditional block that checked for `tkinter` availability:

```python
if TKINTER_AVAILABLE:
    class RepAnalyzer: ...
    class CounterApp: ...
```

When `tkinter` was missing (headless), the module loaded but `RepAnalyzer` was never defined, breaking the `run_cli()` fallback which depended on it.

### Resolution
Move the shared logic classes **outside** the conditional GUI block:

```python
class RepAnalyzer:
    # Always defined

if TKINTER_AVAILABLE:
    class CounterApp:
        # GUI specific
```

### Verification Script
Use this pattern to verify if the class is accessible when GUI is "hidden":

```python
import importlib.util
spec = importlib.util.spec_from_file_location('mod', 'app.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
assert hasattr(mod, 'RepAnalyzer'), "RepAnalyzer must be accessible without GUI"
```
