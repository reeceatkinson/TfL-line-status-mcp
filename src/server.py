import os
from typing import Optional
import httpx
from fastmcp import FastMCP

TFL_API_BASE = "https://api.tfl.gov.uk"
USER_AGENT = "tfl-mcp-server/1.0"

# Initialize FastMCP server
mcp = FastMCP("TfL Line Status MCP Server")


async def make_tfl_request(endpoint: str) -> Optional[list]:
    """Make a request to the TfL API."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{TFL_API_BASE}{endpoint}", headers=headers)
            response.raise_for_status()
            return response.json()
    except Exception as error:
        print(f"Error making request: {error}")
        return None


def format_disruption(disruption: dict, index: int) -> str:
    """Format a single disruption for display."""
    lines = [
        f"Disruption #{index + 1}:",
        f"  Category: {disruption.get('category', 'N/A')}",
        f"  Type: {disruption.get('type', 'N/A')}",
        f"  Description: {disruption.get('description', 'N/A')}",
    ]

    if disruption.get('closureText'):
        lines.append(f"  Closure: {disruption['closureText']}")

    if disruption.get('additionalInfo'):
        lines.append(f"  Additional Info: {disruption['additionalInfo']}")

    return "\n".join(lines)


@mcp.tool
async def get_line_disruptions(lines: str) -> str:
    """Get disruptions for specific TfL lines (e.g., district, windrush, victoria, northern).

    Args:
        lines: Comma-separated list of line IDs (e.g., 'district,windrush' or 'victoria')

    Returns:
        A formatted string describing any disruptions on the specified lines
    """
    data = await make_tfl_request(f"/Line/{lines}/Disruption")

    if data is None:
        return "❌ Failed to retrieve disruption data"

    if len(data) == 0:
        line_names = ", ".join(lines.split(","))
        return f"✅ No disruptions on {line_names} line(s)"

    formatted_disruptions = [format_disruption(disruption, idx) for idx, disruption in enumerate(data)]
    disruption_text = f"🚨 Found {len(data)} disruption(s):\n\n" + "\n\n".join(formatted_disruptions)

    return disruption_text


@mcp.tool
async def get_mode_disruptions(modes: str) -> str:
    """Get disruptions for TfL transport modes (tube, overground, dlr, elizabeth-line, tram, bus).

    Args:
        modes: Comma-separated list of modes (e.g., 'tube,dlr' or 'overground')

    Returns:
        A formatted string describing any disruptions on the specified transport modes
    """
    data = await make_tfl_request(f"/Line/Mode/{modes}/Disruption")

    if data is None:
        return "❌ Failed to retrieve disruption data"

    if len(data) == 0:
        return f"✅ No disruptions on {modes.upper()} services"

    formatted_disruptions = [format_disruption(disruption, idx) for idx, disruption in enumerate(data)]
    disruption_text = f"🚨 Found {len(data)} disruption(s) for {modes.upper()}:\n\n" + "\n\n".join(formatted_disruptions)

    return disruption_text


if __name__ == "__main__":
    # Use stdio transport for Claude Desktop, HTTP for remote deployment
    if os.environ.get("PORT"):
        # HTTP transport for remote deployment (Render, etc.)
        port = int(os.environ.get("PORT", 8000))
        mcp.run(transport="http", host="0.0.0.0", port=port)
    else:
        # stdio transport for Claude Desktop
        mcp.run(transport="stdio")
