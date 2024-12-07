import os
import time
import yaml
import jsonref
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from langsmith.wrappers import wrap_openai

from openai import OpenAI
from openapi_spec_validator import validate
from openapi_agent.utils.logging_config import get_logger

from openapi_agent.agent_cache import AgentCache
from openapi_agent.code_generator import CodeGenerator, CodeGenerationRequest

logger = get_logger(__name__)

MODEL = "gpt-4o-mini"

class Task(BaseModel):
    """Task that can be executed by the agent."""
    operationID: str = Field(description="The operation ID to execute.")
    description: str = Field(description="The description of the task and what are we trying to achieve.")

class Plan(BaseModel):
    """Plan of the execution of the action."""
    tasks: List[Task] = Field(description="The tasks to execute in order to perform the action.")


class Agent(BaseModel):
    """Agent that can execute operations based on natural language description against an OpenAPI spec."""
    client: Any = Field(default=None)

    api_spec: Dict[str, Any] = Field(default_factory=dict)
    name: str = Field(default="")
    description: str = Field(default="")
    tags: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    base_url: str = Field(default="")
    operations: Dict[str, Any] = Field(default_factory=dict)
    version_hash: str = Field(default="")
    auth_header: str = Field(default="")
    

    def __init__(self, openapi_spec_path: str, auth_header: str = "", cache_dir: str = ".cache"):
        super().__init__()
        
        spec_path = Path(openapi_spec_path)
        if not self._load_from_cache(spec_path, Path(cache_dir)):
            self._init_from_spec(spec_path)
            self._save_to_cache(Path(cache_dir))

        api_key = os.getenv('OPENAI_API_KEY')
        self.client = wrap_openai(OpenAI(api_key=api_key))
        self.auth_header = auth_header

    def _calculate_hash(self, spec_path: Path) -> str:
        return hashlib.sha256(spec_path.read_bytes()).hexdigest()

    def _load_from_cache(self, spec_path: Path, cache_dir: Path) -> bool:
        """Attempt to load from cache. Returns True if successful."""
        try:
            self.version_hash = self._calculate_hash(spec_path)
            cache_path = cache_dir / f"agent_{self.version_hash}.pkl"
            
            cached_data = AgentCache.load(cache_path)
            self.__dict__.update(cached_data)
            return True
        except (FileNotFoundError, EOFError):
            return False

    def _save_to_cache(self, cache_dir: Path):
        """Save current state to cache"""
        cache_path = cache_dir / f"agent_{self.version_hash}.pkl"
        cache_data = {k:v for k,v in self.__dict__.items() if k != 'client'}
        AgentCache.save(cache_path, cache_data)


    def _init_from_spec(self, spec_path: Path):
        """Initialize agent from OpenAPI spec"""
        self.version_hash = self._calculate_hash(spec_path)
        self.api_spec = self._load_openapi_spec(str(spec_path))
        self.name = self.api_spec['info']['title']
        self.description = self.api_spec['info']['description']
        self.base_url = self.api_spec.get('servers', [{'url': ''}])[0]['url']
        self.tags = {
            tag.get('name'): {
                'name': tag.get('name', ''),
                'description': tag.get('description', '')
            }
            for tag in self.api_spec.get('tags', [])
        }
        self.operations = self._extract_operations(self.api_spec)

    def _load_openapi_spec(self, file_path):
        """Loads the OpenAPI spec from a file and validates it."""
        start_time = time.time()

        try:
            with open(file_path) as f:
                raw_spec = yaml.safe_load(f)
            
            # Resolve all $ref references but keep path parameters as-is
            spec = jsonref.JsonRef.replace_refs(raw_spec)
            
            # Skip validation since Fly.io uses valid but unresolved path parameters
            # like '/apps/{app_name}/secrets' 
            # validate(spec)  # Comment out or remove validation
            
            elapsed_time = time.time() - start_time
            print(f"Loaded spec in {elapsed_time:.2f}s ({len(spec.get('paths', {}))} endpoints)")
            return spec
        
        except FileNotFoundError:
            raise ValueError(f"OpenAPI spec file not found: {file_path}")
        
        except Exception as e:
            raise ValueError(f"Failed to parse OpenAPI spec: {e}")
        
    def _extract_operations(self, spec) -> Dict[str, Any]:
        """Extracts all the operations from the OpenAPI spec."""
        operations = {}
        for path, methods in spec['paths'].items():
            for method, details in methods.items():
                op_id = details.get('operationId', f"{method}_{path}")
                
                # Extract response schemas for different status codes
                responses = {}
                for status_code, response_info in details.get('responses', {}).items():
                    responses[status_code] = {
                        'description': response_info.get('description', ''),
                        'schema': response_info.get('content', {}).get('application/json', {}).get('schema', {}),
                    }

                operations[op_id] = {
                    'method': method.upper(),
                    'path': path,
                    'summary': details.get('summary', ''),
                    'description': details.get('description', ''),

                    'parameters': details.get('parameters', []),
                    'requestBody': details.get('requestBody', {}),

                    'responses': responses,

                    'tags': details.get('tags', []),
                    'security': details.get('security', []),
                    'deprecated': details.get('deprecated', False)
                }
        return operations

    def execute_function(self, function_name: str, function_args: Dict[str, Any]) -> Dict[str, Any]:
        """Executes an action against the API."""
        action = function_args.get('action')
        if not action:
            raise ValueError("Action is required")
        
        # Get relevant operations
        relevant_tags = self._match_relevant_tags(action) if self.tags else []
        logger.info(f"execute_function: relevant tags: {relevant_tags}")

        relevant_operations = self._match_relevant_operations(action, relevant_tags)
        if len(relevant_operations) == 0:
            raise ValueError(f"No relevant operations found for {action}")
        logger.info(f"execute_function: relevant operations: {[op['method'] + ' ' + op['path'] + ' ' + op['summary'] for op in relevant_operations.values()]}")

        # Select specific operation to use
        selected_operation = self._select_operation(action, relevant_operations)
        
        # Generate and execute code with automatic retries
        request = CodeGenerationRequest(
            action=action,
            operations=[selected_operation],  # Now passing only the selected operation
            base_url=self.base_url,
            auth_header=self._get_auth_headers()
        )
        
        generator = CodeGenerator()
        result = generator.generate(request)
        
        return result.output

    def _match_relevant_tags(self, action: str) -> List[str]:
        """Matches relevant tags for the given action."""
        # Build tag descriptions
        tag_descriptions = "\n".join([
            f"{tag}: {details['description']}"
            for tag, details in self.tags.items()
        ])

        prompt = f"""
        You are an expert at matching tags to actions.
        You need to match a list of tags from the {self.name} API to the following action: {action}

        Tags:
        {tag_descriptions}

        Reply with the following format and do not add any other text:
        tag1, tag2, tag5...
        If none of the tags are relevant, reply with NONE.
        """

        # Match relevant tags
        relevant_tags = []
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
            
        assistant_message = response.choices[0].message
        for tag in self.tags.keys():
            if tag in assistant_message.content:
                relevant_tags.append(tag)
        

        return relevant_tags
    
    def _match_relevant_operations(self, action: str, relevant_tags: List[str]) -> List[str]:
        """Matches relevant operations for the given tags."""
        # First filter operations by tags
        tagged_operations = {
            op_id: op_details for op_id, op_details in self.operations.items()
            if any(tag in relevant_tags for tag in op_details['tags'])
        }
        
        if not tagged_operations:
            return []

        # Build operations description for the prompt
        operations_desc = "\n".join([
            f"{op_id}: {details['method']} {details['summary']}"
            for op_id, details in tagged_operations.items()
        ])

        prompt = f"""
        You are an expert at matching operations to actions.
        You need to match operations from the {self.name} API to the following action: {action}

        Available Operations:
        {operations_desc}

        Reply with the following format and do not add any other text:
        operation_id1, operation_id2, operation_id3...
        If none of the operations are relevant, reply with NONE.
        """

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        
        assistant_message = response.choices[0].message.content.strip()
        
        if 'none' in assistant_message.lower():
            return []
            
        return {op_id.strip(): tagged_operations[op_id.strip()] 
                for op_id in assistant_message.split(',') 
                if op_id.strip() in tagged_operations}
    
    def _plan_execution(self, action: str, relevant_operations_ids: List[str]) -> Plan:
        """Plans the execution of the given action."""

        operations_desc = "\n".join([
            f"{op_id}: {details['method']} {details['summary']}"
            for op_id, details in self.operations.items()
            if op_id in relevant_operations_ids
        ])

        prompt = f"""
        You are an expert at planning actions.
        You need to plan the execution of the following action: {action}

        Available Operations:
        {operations_desc}

        For each operation needed, provide:
            - operationID: The exact operation to execute
            - description: What this step achieves and what parameters are needed
        """

        try:
            response = self.client.beta.chat.completions.parse(
                model=MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                response_format=Plan
            )
            return response.choices[0].message.parsed

        except Exception as e:
            print(e)
            return None
        

    def as_tool(self) -> Dict[str, Any]:
        """Returns a function definition that can be used with ChatGPT function calling."""
        return {
            "type": "function",
            "function": {
                "name": f"{self.name.lower().replace(' ', '_')}_agent",
                "description": f"Execute operations against the {self.name} API. {self.description}. Each call should be only one operation/action.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": f"The action to perform against the {self.name} API. Should be a natural language description of the desired operation. {self.description}."
                        }
                    },
                    "required": ["action"]
                }
            }
        }
    
    def _get_auth_headers(self) -> Optional[Dict[str, str]]:
        return {"Authorization": self.auth_header} if self.auth_header else None

    def _select_operation(self, action: str, relevant_operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Makes final decision on which operation to use based on the action description.
        Returns a single operation or raises an exception if disambiguation is needed.
        """
        if not relevant_operations:
            raise ValueError("No relevant operations found")
        
        # We get an extra LLM call if we have more than one operation, but we can pre-validate parameters
        # not sure if it's worth it.
        # if len(relevant_operations) == 1:
        #     return relevant_operations[0]

        prompt = f"""
        Analyze if we can definitively choose one operation for this action: '{action}'
        from the list [AVAILABLE OPERATIONS]. If you can choose one operation, return ONLY
        the operation ID. If you can not make an educated guess on which operation to use,
        respond with NEEDS_CLARIFICATION <explanation of what information is needed>.

        [AVAILABLE OPERATIONS]
        {relevant_operations}

        """

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )

        decision = response.choices[0].message.content.strip()
        
        if decision.startswith("NEEDS_CLARIFICATION"):
            raise ValueError(decision)
            
        # Find the operation that matches the returned operation ID
        if decision in relevant_operations:
            return relevant_operations[decision]
                
        raise ValueError("Failed to select operation - invalid operation ID from model")

