from fastapi import FastAPI
from fastapi.responses import FileResponse
from tools.maven import get_latest_version

app = FastAPI(
    title="MCP Chatbot Tool Server",
    description="Model-callable API for chatbot tools like Maven version lookup.",
    version="1.0.0",
)


@app.get("/get-latest-maven-version", summary="Get latest stable Maven version")
async def get_latest_maven_version(groupId: str, artifactId: str):
    version = await get_latest_version(groupId, artifactId)
    if version:
        return {"latest_version": version}
    return {"error": "No stable version found"}


@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def serve_manifest():
    return FileResponse(".well-known/ai-plugin.json")


@app.get("/openapi.yaml", include_in_schema=False)
async def serve_openapi():
    return FileResponse("openapi.yaml")
