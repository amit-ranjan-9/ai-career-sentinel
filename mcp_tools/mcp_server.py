import asyncio
import os
import httpx
from bs4 import BeautifulSoup
from datetime import date
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# Initialize MCP Server
server = Server("career-sentinel-mcp")

#REPORTS_DIR = r"C:\Users\amitr\OneDrive\Desktop\job_search_agent\data\reports"
REPORTS_DIR = r"C:\Users\amitr\OneDrive\Desktop\job_search_agent\data"
REPORTS_DIR = os.path.join(REPORTS_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# ─── TOOL 1: fetch_job_description ───────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="fetch_job_description",
            description="Fetches full job description from a job posting URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The job posting URL to fetch"
                    }
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="save_report",
            description="Saves the daily job brief to a local text file",
            inputSchema={
                "type": "object",
                "properties": {
                    "brief": {
                        "type": "string",
                        "description": "The morning brief content to save"
                    }
                },
                "required": ["brief"]
            }
        )
    ]

# ─── TOOL EXECUTION ──────────────────────────────────────────────────────────

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:

    if name == "fetch_job_description":
        url = arguments.get("url", "")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=15, follow_redirects=True)
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator=" ", strip=True)[:1500]
            return [types.TextContent(type="text", text=text)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error fetching URL: {e}")]

    elif name == "save_report":
        brief = arguments.get("brief", "")
        try:
            if not os.path.exists(REPORTS_DIR):
                os.mkdir(REPORTS_DIR)
            today = date.today().strftime("%Y-%m-%d")
            filepath = os.path.join(REPORTS_DIR, f"brief_{today}.txt")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("AI Career Sentinel - Daily Brief\n")
                f.write(f"Date: {today}\n")
                f.write("=" * 50 + "\n\n")
                f.write(brief)
            return [types.TextContent(type="text", text=f"Report saved to: {filepath}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error saving report: {e}")]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

# ─── RUN SERVER ──────────────────────────────────────────────────────────────

async def main():
    print("[MCP Server] Career Sentinel MCP Server starting...")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())