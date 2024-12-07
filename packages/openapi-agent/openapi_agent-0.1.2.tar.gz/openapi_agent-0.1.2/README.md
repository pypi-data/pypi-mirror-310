# OpenAPI Agent

A Python library that enables natural language interaction with any OpenAPI-compliant API. The agent interprets natural language commands, matches them to appropriate API operations, and executes them safely.

## Features

- 🤖 Natural language understanding of API operations
- 🔒 Secure code execution in sandboxed environments
- 🔄 Automatic retry mechanisms
- 💾 Caching of API specifications
- 🔍 Smart operation matching using tags and descriptions

## Installation

```bash
pip install openapi-agent
```

## Quickstart

```python
from openapi_agent import Agent

# Initialize agent with OpenAPI spec
agent = Agent('path/to/openapi.yaml', auth_header="Bearer your-token")

# Execute operations using natural language
result = agent.execute_function("github_agent", {
    "action": "Create a new user repository called 'my-repo' and return its full name"
})
```


## Security

- All code execution happens in isolated Docker containers
- Automatic timeout handling prevents infinite loops
- No file system access outside the sandbox
- Limited network access within the container

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- Additional API-specific authentication tokens as needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
