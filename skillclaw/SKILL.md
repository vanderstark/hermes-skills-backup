---
name: skillclaw
description: "SkillClaw — Let Skills Evolve Collectively with Agentic Evolver. Auto-evolve, auto-deduplicate, and auto-improve AI agent skills from real session data. Integrates with Hermes, Codex, Claude Code, OpenClaw, and 8+ other agent frameworks."
---

# SkillClaw: Collective Skill Evolution for AI Agents

## 🚀 What Is SkillClaw?

SkillClaw makes AI agent skills progressively better by **evolving reusable skills** from real session data. It works across sessions, agents, devices, and users — experience compounds.

### Key Features

- **Auto-evolution**: Skills evolve from every real session without manual intervention
- **Auto-deduplication**: Removes duplicate and outdated skills automatically
- **Multi-agent compatibility**: Works with Hermes, Codex, Claude Code, OpenClaw, QwenPaw, IronClaw, PicoClaw, ZeroClaw, NanoClaw, NemoClaw, and any OpenAI-compatible API
- **Broad compatibility**: Native integration with 8+ agent frameworks
- **Collective improvement**: Team skills benefit from all members' experience

## 📦 Installation

### Prerequisites

- macOS, Linux, or Windows
- Python >= 3.10
- A provider account with OpenAI-compatible API (or AWS Bedrock)
- Optional: `openclaw` CLI for agent workspace features

### Quick Install (macOS/Linux)

```bash
git clone https://github.com/AMAP-ML/SkillClaw.git
cd SkillClaw
bash scripts/install_skillclaw.sh
source .venv/bin/activate
```

### Quick Install (Windows PowerShell)

```powershell
git clone https://github.com/AMAP-ML/SkillClaw.git
Set-Location SkillClaw
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".[evolve,sharing,server]"
```

### Setup

```bash
skillclaw setup
```

The setup wizard prompts for:
- Provider choice (Hermes recommended for default `~/.hermes/skills`)
- Model selection
- Local skills directory
- Shared storage configuration (optional)

### Start Service

```bash
skillclaw start --daemon
skillclaw status
```

## 🔧 Hermes Integration

If you use Hermes, get seamless integration:

1. Install Hermes first
2. Run `skillclaw setup` and choose `hermes` for CLI agent configuration
3. SkillClaw rewrites `~/.hermes/config.yaml` to point Hermes at the local proxy
4. Hermes uses `~/.hermes/skills` as the default library (SkillClaw prepares this automatically)

### Verify Integration

```bash
skillclaw start --daemon
hermes chat -Q -m skillclaw-model -q "Reply with exactly HERMES_SKILLCLAW_OK and nothing else."
```

### Diagnostic Commands

```bash
skillclaw doctor hermes      # Verify Hermes integration
skillclaw restore hermes     # Undo integration changes
```

## 🌐 Shared Group Mode

For teams, run an evolve server:

```bash
skillclaw-evolve-server --port 8787 --interval 300 --storage-backend oss \
  --oss-endpoint "$EVOLVE_STORAGE_ENDPOINT" \
  --oss-bucket "$EVOLVE_STORAGE_BUCKET" \
  --group-id my-group
```

Client join:

```bash
skillclaw config sharing.enabled true
skillclaw config sharing.backend oss
skillclaw config sharing.endpoint https://oss-cn-hangzhou.aliyuncs.com
skillclaw config sharing.bucket my-skillclaw-bucket
skillclaw config sharing.access_key_id "$OSS_ACCESS_KEY_ID"
skillclaw config sharing.secret_access_key "$OSS_ACCESS_KEY_SECRET"
skillclaw config sharing.group_id my-group
skillclaw start --daemon
skillclaw skills pull
```

## 📊 Dashboard (Optional)

```bash
skillclaw dashboard sync
skillclaw dashboard serve
# Visit: http://127.0.0.1:3791
```

## Related Skills

- `hermes-skill-factory` — Automatically turn workflows into reusable skills
- `brainstorming` — Design before implementation
- `writing-plans` — Create implementation plans
- `verification-before-completion` — Quality gates before shipping

## References

- GitHub: https://github.com/AMAP-ML/SkillClaw
- Paper: https://arxiv.org/abs/2604.08377
- Docs: `README.md`, `README_ZH.md`