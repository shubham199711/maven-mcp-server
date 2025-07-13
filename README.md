# Maven Version Lookup Tool

A LangChain tool for getting the latest stable versions of Maven artifacts from Maven Central.

## Features

- 🔍 Look up latest stable versions of Maven artifacts
- 🚫 Filter out unstable versions (SNAPSHOT, RC, Beta, Alpha, Milestone)
- 🔄 Both async and sync support
- 🛠️ Easy integration with LangChain agents
- 📦 Proper semantic version comparison

## Installation

```bash
# Install dependencies
pip install -e .
```

## Quick Start

### Basic Usage

```python
from tools.maven import MavenVersionTool

# Create tool instance
maven_tool = MavenVersionTool()

# Async usage
import asyncio
result = await maven_tool._arun(
    group_id="org.springframework.boot",
    artifact_id="spring-boot-starter-web"
)
print(result)  # "Latest stable version of org.springframework.boot:spring-boot-starter-web is 3.2.0"

# Sync usage
result = maven_tool._run(
    group_id="com.fasterxml.jackson.core",
    artifact_id="jackson-core"
)
print(result)  # "Latest stable version of com.fasterxml.jackson.core:jackson-core is 2.16.0"
```

### Run Examples

```bash
# Run basic examples
python main.py

# Run agent example (requires OpenAI API key)
python example_agent.py
```

## Integration with LangChain Agents

```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from tools.maven import MavenVersionTool

# Create agent with Maven tool
tools = [MavenVersionTool()]
llm = ChatOpenAI(model="gpt-3.5-turbo")
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Use the agent
result = await agent_executor.ainvoke({
    "input": "What's the latest version of Spring Boot?"
})
```

## Tool Details

The `MavenVersionTool` provides:

- **Name**: `maven_version_lookup`
- **Description**: Get the latest stable version of a Maven artifact from Maven Central
- **Parameters**:
  - `group_id`: The Maven group ID (e.g., 'org.springframework.boot')
  - `artifact_id`: The Maven artifact ID (e.g., 'spring-boot-starter-web')

## API

The tool queries the Maven Central Search API and:
1. Fetches up to 50 versions of the specified artifact
2. Filters out unstable versions (SNAPSHOT, RC, Beta, Alpha, Milestone)
3. Sorts by semantic versioning to find the latest stable release
4. Returns a human-readable result

## Dependencies

- `langchain>=0.2.0` - LangChain framework
- `langchain-core>=0.2.0` - Core LangChain components
- `httpx>=0.28.1` - HTTP client for API calls
- `pydantic>=2.0.0` - Data validation
- `packaging>=23.0` - Semantic version comparison

## License

MIT