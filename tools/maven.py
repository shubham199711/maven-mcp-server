import httpx
from typing import Optional, ClassVar, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

MAVEN_API = "https://search.maven.org/solrsearch/select"


def is_stable(version: str) -> bool:
    """Check if a version string represents a stable release."""
    return not any(
        tag in version.lower()
        for tag in ["snapshot", "rc", "beta", "alpha", "milestone"]
    )


async def get_latest_version(group_id: str, artifact_id: str) -> Optional[str]:
    """Get the latest stable version of a Maven artifact."""
    params = {
        "q": f"g:{group_id} AND a:{artifact_id}",
        "rows": 50,
        "wt": "json",
        "core": "gav",
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(MAVEN_API, params=params)
            resp.raise_for_status()
            data = resp.json()

        docs = data.get("response", {}).get("docs", [])
        if not docs:
            return None

        # Extract versions and filter stable ones
        versions = []
        for doc in docs:
            version = doc.get("v")
            if version and is_stable(version):
                versions.append(version)

        if not versions:
            return None

        # Sort by semantic versioning and return the latest
        from packaging import version as pkg_version

        latest = max(versions, key=lambda v: pkg_version.parse(v))
        return latest

    except Exception as e:
        print(f"Error fetching Maven version: {e}")
        return None


class MavenVersionInput(BaseModel):
    group_id: str = Field(
        ..., description="The Maven group ID (e.g., 'org.springframework.boot')"
    )
    artifact_id: str = Field(
        ..., description="The Maven artifact ID (e.g., 'spring-boot-starter-web')"
    )


class MavenVersionTool(BaseTool):
    name: str = "maven_latest_version_lookup"
    description: str = """
    Get the latest stable version of a Maven artifact from Maven Central.
    Use this tool when you need to find the most recent stable release of a Java library.
    """
    args_schema: ClassVar[Type[BaseModel]] = MavenVersionInput

    async def _arun(self, group_id: str, artifact_id: str) -> str:
        """Async implementation of the tool."""
        version = await get_latest_version(group_id, artifact_id)
        if version:
            return version
        else:
            return f"No stable version found for {group_id}:{artifact_id}"

    def _run(self, group_id: str, artifact_id: str) -> str:
        """Sync implementation of the tool."""
        import asyncio

        return asyncio.run(self._arun(group_id, artifact_id))
