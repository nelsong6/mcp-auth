"""HTTP entrypoint for the auth.romaine.life MCP server.

Scaffold only — tools are not registered yet. The follow-up PR will add:
  * list_users / update_user / enroll_user — wrappers around
    auth.romaine.life's /admin endpoints
  * outbound credential plumbing (service-to-service token from auth)

For now this serves /healthz so the deployment becomes Ready and the
ingress / RBAC / inbound-attestation path can be exercised end-to-end
before any tool surface exists.
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
