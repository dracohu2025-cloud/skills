---
name: skill-repo-syncer
description: Automatically syncs local Claude skills to the user's central GitHub skills repository (dracohu2025-cloud/skills). Use this skill after creating a new skill or installing one from an external source to ensure the remote repository is up to date.
---

# Skill Repo Syncer

This skill provides a standardized way to synchronize local Claude skills with your personal GitHub skills repository.

## Prerequisites

- Python 3.x
- Git configured with `gh auth` or SSH access to `github.com/dracohu2025-cloud/skills`.

## How to Use This Skill

Whenever a new skill is created or an existing one is modified/installed locally, follow this workflow:

1. **Identify the local skill path**: Usually in `/Users/dracohu/.claude/skills/<skill-name>`.
2. **Execute the sync script**:

```bash
python3 /Users/dracohu/.claude/skills/skill-repo-syncer/scripts/sync.py /Users/dracohu/.claude/skills/<skill-name>
```

## Workflow Integration

- **After using `skill-creator`**: Immediately run this syncer to backup the newly created skill.
- **After manual installation**: Use this syncer to add the external skill to your central repository.
- **After major updates**: Run this syncer to keep the GitHub version in sync with local improvements.

## Rules

- Always ensure `gh auth status` is valid before running.
- The script handles temporary cloning and cleanup automatically.
- Commit messages are standardized as "Sync skill: <skill-name>".
