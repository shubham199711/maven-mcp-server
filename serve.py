from fastapi import FastAPI, Query
from tools.maven import MavenVersionTool
import uvicorn

# Import FastApiMCP
from fastapi_mcp import FastApiMCP

app = FastAPI(title="Maven Version Lookup API")
tool = MavenVersionTool()


# Define your routes FIRST
@app.get("/latest-version", operation_id="get_maven_latest_version")
async def latest_version(group_id: str = Query(...), artifact_id: str = Query(...)):
    result = await tool._arun(group_id=group_id, artifact_id=artifact_id)
    return {f"{group_id}:{artifact_id}": result}


# NOW, initialize FastApiMCP and mount it, after all routes are defined
mcp = FastApiMCP(
    app,
    name="Maven Tools",
    description="API for looking up Maven artifact versions.",
)

# Mount the MCP endpoint
mcp.mount()


if __name__ == "__main__":
    # Ensure your uvicorn command runs the application where the MCP server is mounted
    uvicorn.run("serve:app", host="127.0.0.1", port=8000, reload=True)
