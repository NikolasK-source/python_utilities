# Python utilities

collection of python utilities

## exec_cmd

Execute command as subprocess

```python
def execute(cmd: str, 
            args: list[str] | None = None, 
            cmd_input: bytes | None = None,
            timeout: float | None = None 
            ) -> CommandResult
```
