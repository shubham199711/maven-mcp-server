import httpx

MAVEN_API = "https://search.maven.org/solrsearch/select"


def is_stable(version: str) -> bool:
    return not any(
        tag in version.lower() for tag in ["snapshot", "rc", "beta", "alpha"]
    )


async def get_latest_version(group_id: str, artifact_id: str) -> str:
    params = {
        "q": f"g:{group_id} AND a:{artifact_id}",
        "rows": 20,
        "wt": "json",
        "core": "gav",
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(MAVEN_API, params=params)
            resp.raise_for_status()
            data = resp.json()
        versions = [
            (doc["timestamp"], doc["v"])
            for doc in data.get("response", {}).get("docs", [])
        ]
        stable_versions = sorted(
            [v for v in versions if is_stable(v[1])], key=lambda x: x[1], reverse=True
        )
        return stable_versions[0][1] if stable_versions else "unknown"
    except Exception as e:
        print(e)
        return "unknown"
