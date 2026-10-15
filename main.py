import hashlib
import os

from mcp.server.fastmcp import FastMCP, Context

# Your registered email, trimmed and lowercased
EMAIL = "23f3002833@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP(
    "exam-server",
    host="0.0.0.0",                          # accept outside traffic
    port=int(os.environ.get("PORT", 8000)),  # hosting sites tell us the port
    stateless_http=True,                     # no sessions to lose on restart
    json_response=True,                      # plain JSON replies
)


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Return the exam fingerprint for this call's challenge header."""
    request = ctx.request_context.request           # the raw HTTP request
    challenge = request.headers.get("x-exam-challenge", "")  # read the header
    digest = hashlib.sha256(f"{challenge}:{EMAIL}".encode()).hexdigest()
    return digest[:16]                                # first 16 hex characters


if __name__ == "__main__":
    mcp.run(transport="streamable-http")  # serves at /mcp
