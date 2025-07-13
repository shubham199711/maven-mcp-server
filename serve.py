from fastapi import FastAPI, Query
from tools.maven import MavenVersionTool
import uvicorn

app = FastAPI(title="Maven Version Lookup API")
tool = MavenVersionTool()


@app.get("/latest-version")
async def latest_version(group_id: str = Query(...), artifact_id: str = Query(...)):
    result = await tool._arun(group_id=group_id, artifact_id=artifact_id)
    return {f"{group_id}:{artifact_id}": result}


if __name__ == "__main__":
    uvicorn.run("serve:app", host="127.0.0.1", port=8000, reload=True)
