# TfL Line Status MCP

A [MCP server](https://modelcontextprotocol.io/docs/getting-started/intro) to get the current status(es) of TFL lines using the [TfL Unified API](https://api-portal.tfl.gov.uk/). Built with FastMCP for easy deployment with streamable HTTP transport.

## Local Development

```bash
pip install -r requirements.txt
python src/server.py
```

## Deployment

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/reeceatkinson/TfL-line-status-mcp-DRAFT)

Click the button above to deploy your own instance to Render. Your server will be available at `https://your-service-name.onrender.com/mcp`


## Claude Desktop Setup

Add this to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "tfl-line-status": {
      "command": "python3",
      "args": ["/path/to/TfL-line-status-mcp-DRAFT/src/server.py"]
    }
  }
}
```

Replace `/path/to/` with the absolute path where you cloned this repository.

## Try It Out!

Restart the Claude Desktop app and then ask the status of a TfL line. You should get something like this...

<img width="1772" height="1378" alt="CleanShot 2025-12-29 at 1  32 06@2x" src="https://github.com/user-attachments/assets/304155e4-55be-4359-8081-21d1fae15a5a" />

## Tools

### `get_line_disruptions`

Get disruptions for specific TfL lines (e.g., district, windrush, victoria, northern).

**Parameters:**
- `lines` (string): Comma-separated list of line IDs (e.g., 'district,windrush' or 'victoria')

**Example:**
```python
get_line_disruptions("district,victoria")
```

### `get_mode_disruptions`

Get disruptions for TfL transport modes (tube, overground, dlr, elizabeth-line, tram, bus).

**Parameters:**
- `modes` (string): Comma-separated list of modes (e.g., 'tube,dlr' or 'overground')

**Example:**
```python
get_mode_disruptions("tube,overground")
```

## API Reference

- [TfL Line Disruptions API](https://api-portal.tfl.gov.uk/api-details#api=Line&operation=Line_DisruptionByPathIds)
- [TfL Mode Disruptions API](https://api-portal.tfl.gov.uk/api-details#api=Line&operation=Line_DisruptionByModeByPathModes)
