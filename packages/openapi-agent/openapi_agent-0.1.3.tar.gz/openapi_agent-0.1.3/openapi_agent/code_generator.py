from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from openai import OpenAI
from langsmith.wrappers import wrap_openai
import os
from openapi_agent.utils.logging_config import get_logger
import json 

from openapi_agent.sandbox import PythonSandbox

logger = get_logger(__name__)

MODEL = "gpt-4o"

class CodeGenerationRequest(BaseModel):
    action: str
    operations: List[Dict[str, Any]]
    base_url: str
    auth_header: Optional[Dict[str, str]] = None

class CodeGenerationResult(BaseModel):
    exit_code: int
    output: str
    code: str
    attempts: int

class CodeGenerator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        # Wrap the OpenAI client for automatic tracing
        self.client = wrap_openai(OpenAI(api_key=api_key))
        self.sandbox = PythonSandbox()

    def generate(self, request: CodeGenerationRequest) -> CodeGenerationResult:
        assert len(request.operations) == 1, "Only one operation is supported"
        
        prompt = f"""
        Your goal is to execut python code to complete the task described in the section called [ACTION].
        Use the operations described in the section called [OPERATIONS] to complete the task.
        The base URL is provided in the section called [BASE_URL].
        If authentication is required, the auth headers are provided in the section called [AUTH_HEADER].

        Generate code that:
        1. Uses the requests library
        2. For error handling:
           - Capture the full response body when an error occurs
           - Print both the status code and the detailed error message from the response
           - For responses that might not contain JSON:
             * Try to parse JSON first
             * If that fails, print the raw response text
             * Handle empty responses appropriately
        3. Only uses the operations provided   
        4. If there are no errors, only print the response using json.dumps() if possible, otherwise prints the raw response text. 
        5. If there is no [AUTH_HEADER] section, do not include it in the request headers.
        6. Try to fill all the information you can.
        """

        prompt += f"\n[BASE_URL]: {request.base_url}"
        prompt += "\n[OPERATIONS]\n" + json.dumps(request.operations, indent=2)
        prompt += f"\n[ACTION]: {request.action}"
        if request.auth_header:
            prompt += f"\n[AUTH_HEADER]: {json.dumps(request.auth_header, indent=2)}"

        logger.debug(f"Code generation prompt: {prompt}")

        messages = [{"role": "user", "content": prompt}]
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            attempt += 1
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "run_code",
                        "description": "Run the Python code and return the result",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "The Python code to execute"
                                }
                            },
                            "required": ["code"]
                        }
                    }
                }]
            )
            
            message = response.choices[0].message
            messages.append(message)
            
            if not message.tool_calls:
                if attempt == max_attempts:
                    raise ValueError(f"Failed to generate working code after {max_attempts} attempts: {message.content}")
                continue
            
            tool_call = message.tool_calls[0]
            code = json.loads(tool_call.function.arguments)["code"]
            
            exit_code, output = self.sandbox.execute(code)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"Exit Code: {exit_code}\nOutput: {output}"
            })
            
            if exit_code == 0:
                return CodeGenerationResult(
                    exit_code=exit_code,
                    output=output,
                    code=code,
                    attempts=attempt
                )
        
        # If we get here, we've exhausted all attempts
        return CodeGenerationResult(
            exit_code=exit_code,
            output=output,
            code=code,
            attempts=attempt
        )