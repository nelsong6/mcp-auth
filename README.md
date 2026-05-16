# mcp-auth

Tank-bound MCP server fronting [auth.romaine.life](https://github.com/nelsong6/auth) user management. An admin running a tank-operator session pod calls this MCP server to list, promote, and enroll users without leaving the chat.

## Status

Scaffolded but not wired to any tools yet. The deployment, RBAC, and inbound Tank-attestation auth path exist so a follow-up PR can drop tools onto the existing service.

## Architecture (intended)

- **Inbound auth**: same shape as [mcp-github](https://github.com/nelsong6/mcp-github) — session pod's mcp-auth-proxy attaches a Tank-signed session attestation as bearer; this service verifies against `tank-operator/api/internal/jwks` with audience `mcp-auth-tank`.
- **Outbound calls**: HTTP to `https://auth.romaine.life/admin/users` etc. The auth service grants this MCP a service-to-service credential (out-of-scope for the initial scaffold).
- **Tools** (planned, not yet wired):
  - `list_users()` → mirror of `/admin` table
  - `update_user(id, role, name, apps)` → mirror of `POST /admin/users/:id`
  - `enroll_user(email, name, role)` → mirror of `POST /admin/users`

## Local

```bash
pip install -e .
PORT=8080 mcp-auth-http
curl localhost:8080/healthz
```
