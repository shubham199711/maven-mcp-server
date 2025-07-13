from tools.maven import MavenVersionTool
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Maven_Tools")


# Register the Maven version lookup tool
@mcp.tool()
def get_latest_maven_version(group_id: str, artifact_id: str) -> str:
    """Get the latest stable version of a Maven artifact from Maven Central."""
    tool = MavenVersionTool()
    return tool._run(group_id=group_id, artifact_id=artifact_id)
