# import asyncio
# import os
# import sys
# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client

# # Path to our MCP server
# SERVER_PATH = os.path.join(
#     os.path.dirname(os.path.abspath(__file__)),
#     "mcp_server.py"
# )

# async def call_mcp_tool(tool_name: str, arguments: dict) -> str:
#     """
#     Real MCP Client — connects to our MCP server via stdio protocol
#     and calls the requested tool
#     """
#     server_params = StdioServerParameters(
#         command=sys.executable,
#         args=[SERVER_PATH]
#     )
#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             await session.initialize()
#             result = await session.call_tool(tool_name, arguments)
#             if result.content:
#                 return result.content[0].text
#             return ""

# def fetch_job_description_mcp(url: str) -> str:
#     """Fetch full JD via real MCP protocol"""
#     return asyncio.run(call_mcp_tool("fetch_job_description", {"url": url}))

# def save_report_mcp(brief: str) -> str:
#     """Save report via real MCP protocol"""
#     return asyncio.run(call_mcp_tool("save_report", {"brief": brief}))

import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "mcp_server.py"
)

async def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_PATH],
        env=None
    )
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                if result.content:
                    return result.content[0].text
                return ""
    except Exception as e:
        print(f"[MCP Client Error] {e}")
        # Fallback to direct function call if MCP fails
        return fallback(tool_name, arguments)

def fallback(tool_name: str, arguments: dict) -> str:
    """Fallback to direct calls if MCP protocol fails"""
    if tool_name == "fetch_job_description":
        import httpx
        from bs4 import BeautifulSoup
        url = arguments.get("url", "")
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            return soup.get_text(separator=" ", strip=True)[:1500]
        except Exception as e:
            return ""
    elif tool_name == "save_report":
        brief = arguments.get("brief", "")
        try:
            path = r"C:\Users\amitr\OneDrive\Desktop\job_search_agent\data\reports"
            os.makedirs(path, exist_ok=True)
            from datetime import date
            filepath = os.path.join(path, f"brief_{date.today().strftime('%Y-%m-%d')}.txt")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(brief)
            return f"Saved to {filepath}"
        except Exception as e:
            return f"Could not save: {e}"
    return ""

def fetch_job_description_mcp(url: str) -> str:
    """Fetch full JD via MCP protocol with fallback"""
    return asyncio.run(call_mcp_tool("fetch_job_description", {"url": url}))

def save_report_mcp(brief: str) -> str:
    """Save report via MCP protocol with fallback"""
    return asyncio.run(call_mcp_tool("save_report", {"brief": brief}))