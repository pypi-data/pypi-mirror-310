from abc import ABC, abstractmethod
import docker
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import requests
import subprocess
import sys
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

class BaseSandbox(ABC):
    @abstractmethod
    def execute(self, code: str) -> Tuple[int, str]:
        pass

    def _sanitize_code(self, code: str) -> str:
        return code.replace('```python\n', '').replace('```', '').strip()

class PythonSandbox(BaseSandbox):
    def __init__(self, timeout_seconds: int = 300):
        self.timeout = timeout_seconds

    def execute(self, code: str) -> Tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            code = self._sanitize_code(code)
            restricted_env = {
                'PYTHONPATH': '',
                'PATH': os.environ.get('PATH', ''),
            }
            
            output = StringIO()
            try:
                with redirect_stdout(output), redirect_stderr(output):
                    # Execute in separate process for better isolation
                    cmd = [
                        sys.executable,
                        '-c',
                        code
                    ]
                    proc = subprocess.run(
                        cmd,
                        env=restricted_env,
                        timeout=self.timeout,
                        capture_output=True,
                        text=True
                    )
                return proc.returncode, proc.stdout + proc.stderr
            except subprocess.TimeoutExpired:
                return 124, "Execution timed out"

class DockerSandbox(BaseSandbox):
    def __init__(self, image_name: str = "python-sandbox", timeout_seconds: int = 300):
        self.image_name = image_name
        self.timeout = timeout_seconds
        self.client = docker.from_env()
        self._ensure_image()

    def _ensure_image(self):
        """Ensures the sandbox image exists, builds if necessary."""
        try:
            self.client.images.get(self.image_name)
        except docker.errors.ImageNotFound:
            dockerfile_path = Path(__file__).parent / "Dockerfile.sandbox"
            self.client.images.build(
                path=str(dockerfile_path.parent),
                dockerfile=str(dockerfile_path.name),
                tag=self.image_name
            )

    def execute(self, code: str) -> Tuple[int, str]:
        """
        Execute Python code in a sandboxed container.
        Returns: tuple of (exit_code, output)
        Default timeout is 5 minutes, configurable via timeout_seconds parameter.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            code_file = Path(tmp_dir) / "code.py"
            code = self._sanitize_code(code)

            code_file.write_text(code)
            print(code)
            container = self.client.containers.run(
                self.image_name,
                volumes={str(tmp_dir): {'bind': '/sandbox', 'mode': 'ro'}},
                detach=True
            )
            
            try:
                result = container.wait(timeout=self.timeout)
                output = container.logs().decode('utf-8')
                return result['StatusCode'], output
            except requests.exceptions.ConnectionError:  # Timeout occurred
                container.kill()  # Force stop the container
                return 124, "Execution timed out"  # 124 is standard timeout exit code
            finally:
                container.remove(force=True)