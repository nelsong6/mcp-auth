# mcp-auth

Admin MCP server fronting [auth.romaine.life](https://github.com/nelsong6/auth) user management. An admin running a tank-operator session pod calls this MCP server to list, promote, and enroll users without leaving the chat.

## Status

Scaffolded but not wired to any tools yet. The deployment, RBAC, and `/healthz` path exist so a follow-up PR can drop tools onto the existing service.

## Architecture (intended)

- **Inbound auth**: same shape as [mcp-glimmung](https://github.com/nelsong6/mcp-glimmung), [mcp-k8s](https://github.com/nelsong6/mcp-k8s), [mcp-argocd](https://github.com/nelsong6/mcp-argocd), and [mcp-azure-personal](https://github.com/nelsong6/mcp-azure-personal): two layers gate the tool surface.
  1. **kube-rbac-proxy** in front of this process: validates the calling pod's K8s SA token via TokenReview + SubjectAccessReview. No human identity, just "an allowed pod is talking to me."
  2. **auth.romaine.life JWT** (in this process): an `Authorization: Bearer` JWT signed by auth.romaine.life is verified via [`romaine-auth`](https://github.com/nelsong6/romaine-auth-py) against `https://auth.romaine.life/api/auth/jwks`. The resolved `Caller` (sub, email, role, actor_email) is bound to a ContextVar so tool handlers can attribute work to a specific human. Only the closed role set `{admin, user, service}` is accepted; admin-only tools enforce `role=admin` inside the handler.

  Session pods get the auth.romaine.life JWT from the in-pod mcp-auth-proxy sidecar, which exchanges the projected SA token at `https://auth.romaine.life/api/auth/exchange/k8s` and forwards the result as Bearer.

- **Outbound calls**: HTTP to `https://auth.romaine.life/admin/users` etc. The simplest credential plumbing forwards the inbound caller's JWT to auth.romaine.life (`auth_exchange.bearer_header` pattern from [mcp-glimmung's auth_exchange.py](https://github.com/nelsong6/mcp-glimmung/blob/main/src/mcp_glimmung/auth_exchange.py)) — auth.romaine.life's admin endpoints accept that same JWT for authorization, so no separate service-to-service credential is needed.

- **Tools** (planned, not yet wired):
  - `list_users()` → mirror of `/admin` table
  - `update_user(id, role, name, apps)` → mirror of `POST /admin/users/:id`
  - `enroll_user(email, name, role)` → mirror of `POST /admin/users`

  All three gated on `caller.is_admin` inside the handler. user-role callers get a structured "admin only" error.

## Local

```bash
pip install -e .
PORT=8080 mcp-auth-http
curl localhost:8080/healthz
```
