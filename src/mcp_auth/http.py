"""HTTP entrypoint for the auth.romaine.life MCP server.

Scaffold only — tools are not registered yet. The follow-up PR will add:
  * list_users / update_user / enroll_user — wrappers around
    auth.romaine.life's /admin endpoints
  * inbound auth via the shared romaine-auth verifier (same shape as
    mcp-glimmung / mcp-k8s / mcp-argocd / mcp-azure-personal); admin-only
    tools enforce role=admin inside the handler
  * outbound credential plumbing — forwards the inbound caller's JWT
    to auth.romaine.life rather than minting a separate service-to-
    service credential

For now this serves /healthz so the deployment becomes Ready and the
ingress / RBAC path can be exercised end-to-end before any tool
surface exists.
"""

import logging
import os

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

log = logging.getLogger(__name__)


async def healthz(_request: Request) -> PlainTextResponse:
    return PlainTextResponse("ok")


def create_app() -> Starlette:
    return Starlette(routes=[Route("/healthz", healthz)])


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run(create_app(), host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
