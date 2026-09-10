---
name: mcp-server-integration-patterns
category: engineering
description: Integrate MCP servers via npx, npm, or docker.
---

## mcp-server-integration-patterns

Use this skill when integrating a third-party MCP server into the Hermes Agent.

### Integration Patterns:

#### 1. **npx-based MCP Server (Most Common):**
    *   **Structure:** Uses `npx` to run the server from npm.
    *   **Configuration:**
        ```yaml
        mcp_server_name:
          command: "npx"
          args: ["-y", "owner/repo-or-package-name"]
          timeout: 300
          connect_timeout: 60
        ```
    *   **Example:** `office_word` server:
        ```yaml
        office_word:
          command: "npx"
          args: ["-y", "github:gongrzhe/office-word-mcp-server"]
          timeout: 300
          ```

#### 2. **npm-installed MCP Server:**
    *   Use when the server is already installed globally or locally in a virtual environment.
    *   **Configuration:**
        ```yaml
        mcp_server_name:
          command: "node"
          args: ["/path/to/server.js"]
          timeout: 300
        ```

#### 3. **Docker-based MCP Server:**
    *   Use when the server only provides a Docker image.
    *   **Configuration:**
        ```yaml
        mcp_server_name:
          command: "docker"
          args: ["run", "--rm", "-i", "-v", "/data:/data", "image-name"]
          timeout: 300
        ```

### Prerequisites Check:

Before adding a new MCP server:
1.  **Verify it is NOT a standard GitHub repository** for document processors (like `AI-Youtube-Shorts-Generator`, `shellx-cut`). These are applications, NOT MCP servers.
2.  **Confirm the repository is an MCP server** by checking for:
    *   A `package.json` with an executable `bin` field.
    *   Instructions for use with `npx ghcr.io/...` or similar.
    *   A description explicitly mentioning "MCP".

### Pitfalls:
*   **Adding Non-MCP Repos:** Do NOT add standard GitHub repos like `Anil-matcha/AI-Youtube-Shorts-Generator`. These are full applications and won't work with the MCP Protocol. You must use them as standalone applications or create a wrapper.
*   **Node.js Version:** Ensure Node.js version (check with `node -v`) is compatible with the MCP server requirements (usually Node 16+).
*   **Timeout:** Some MCP servers (like file processors or models) require longer timeouts (up to 300s).

### Finding MCP Servers:
1.  Search GitHub: `topic:mcp` or search for "mcp server template".
2.  Check the official MCP servers list from Anthropic: https://github.com/modelcontextprotocol/servers

