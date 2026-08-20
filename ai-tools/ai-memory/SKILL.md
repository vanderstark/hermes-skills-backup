---
name: ai-memory
category: ai-tools
description: Persistent memory storage and retrieval for Hermes
tags: [memory, persistence]
---

# AI Memory Skill for Hermes

## Trigger
Use when the user wants to remember, store, save, recall, or query memory.

## Description
This skill provides commands to store and retrieve information across sessions.

## Commands
| Command | Description |
|---------|-------------|
| `memory save <text>` | Store a fact or observation |
| `memory recall <keyword>` | Retrieve relevant memories |
| `memory list` | Show all stored items |
| `memory clear <keyword>` | Remove matching memories |

## Example Usage
```
> memory save "John's password is 12345"
> memory recall "password"
> memory list
```