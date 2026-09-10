---
name: python-desk-app
description: Tkinter GUI + CLI fallback + precision counting patterns.
---

# Python Desktop App Patterns (tkinter + CLI fallback)

Reusable patterns for cross-platform Python desktop apps with tkinter GUI that gracefully fall back to CLI mode in headless environments.

## Core Pattern: Tkinter + CLI Hybrid

**Problem**: tkinter unavailable on headless servers (CI, SSH, containers) — module import crashes the whole script.

**Solution**: Wrap tkinter imports in try/except, expose core logic as importable classes, auto-fallback to CLI.

```python
try:
    import tkinter as tk
    from tkinter import messagebox, ttk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# Core logic (RepAnalyzer, save_session) defined OUTSIDE GUI class
# GUI class only instantiated if TKINTER_AVAILABLE

def main():
    if TKINTER_AVAILABLE:
        try:
            root = tk.Tk()
            AppClass(root)
            root.mainloop()
            return
        except Exception as e:
            print(f">>> GUI error: {e}, fallback CLI <<<")
    run_cli()  # Pure Python, no tkinter deps
```

**Key**: Core algorithm has ZERO tkinter dependencies — importable/testable anywhere.

## Precision Rep Counting with Debounce

```python
MIN_REP_INTERVAL = 0.4      # seconds - physiological limit
MAX_REALISTIC_INTERVAL = 10.0  # seconds - above = rest break
TEMPO_WINDOW = 5              # rolling window for tempo average

class RepAnalyzer:
    def __init__(self):
        self.rep_timestamps = []
        self.rejected_count = 0
        self.session_start = None

    def record_rep(self):
        now = time.time()
        if self.session_start is None:
            self.session_start = now
        if self.rep_timestamps:
            interval = now - self.rep_timestamps[-1]
            if interval < MIN_REP_INTERVAL:
                self.rejected_count += 1
                return False, f"Rejected: too fast ({interval:.2f}s)"
        self.rep_timestamps.append(now)
        return True, "OK"

    def average_tempo(self):
        if len(self.rep_timestamps) < 2:
            return None
        recent = self.rep_timestamps[-(TEMPO_WINDOW + 1):]
        intervals = [recent[i] - recent[i-1] for i in range(1, len(recent))
                     if recent[i] - recent[i-1] <= MAX_REALISTIC_INTERVAL]
        return sum(intervals) / len(intervals) if intervals else None

    def reps_per_minute(self):
        tempo = self.average_tempo()
        return 60.0 / tempo if tempo else 0.0
```

**Why 0.4s?**: Human physiology — impossible to complete full rep faster. Filters double-clicks, keyboard bounce, accidental triggers.

**Rolling tempo window**: Last N reps (default 5) adapts to pace changes. Excludes rest breaks (>10s gaps).

## Gender-Based Target Config

```python
TARGETS = {
    "Laki-laki": 50,      # pushup target
    "Perempuan": 35,      # pushup target
}
# Pullup: {"Laki-laki": 15, "Perempuan": 10}
```

Dropdown → updates target → progress bar auto-rescales.

## Session Persistence (JSON)

```python
def save_session(gender, target, analyzer):
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "gender": gender,
        "target": target,
        **analyzer.summary(),  # total_reps, rejected_count, tempo, RPM, duration
    }
    history = []
    if os.path.exists("sessions.json"):
        try:
            with open("sessions.json") as f:
                history = json.load(f)
        except (json.JSONDecodeError, OSError):
            history = []
    history.append(entry)
    with open("sessions.json", "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    return entry
```

## GitHub Private Repo Workflow (API-First)

`git clone` fails on private repos without credentials in URL. Use GitHub REST API for verification.

```bash
# Create private repo via API
curl -X POST -H "Authorization: token $TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name":"repo-name","private":true}'

# Push with embedded token (headless-safe)
git remote set-url origin https://$TOKEN@github.com/user/repo.git
git push -u origin main
git remote set-url origin https://github.com/user/repo.git  # revert
unset TOKEN

# Verify via API (works without auth in URL)
curl -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/user/repo/contents/file.py
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| tkinter import at module level crashes headless | Wrap in try/except → set TKINTER_AVAILABLE |
| Auto-count timer (1 rep/sec) feels fake | Manual trigger + debounce = real correspondence |
| Double-count on fast clicks | MIN_REP_INTERVAL = 0.4s rejects impossible reps |
| Tempo skewed by rest breaks | MAX_REALISTIC_INTERVAL excludes gaps >10s |
| Git clone fails on private repo | Verify via GitHub API `/contents/` instead |
| Token left in git remote URL | Revert URL immediately after push; unset env var |

## Fitness Targets (examples)

- Pushup: Male 50 / Female 35
- Pullup: Male 15 / Female 10

## Verification Checklist

- [ ] `python3 -m py_compile app.py` passes
- [ ] Core logic importable without tkinter
- [ ] Headless test works (import + instantiate RepAnalyzer)
- [ ] Debounce: rapid calls → rejected_count increments
- [ ] Tempo: spaced calls → RPM correct
- [ ] JSON session file written + readable
- [ ] GitHub repo private, files visible via API
- [ ] Token unset after all git ops
