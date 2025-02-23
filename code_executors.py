import asyncio
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor


async def main():
  local_code_executor = LocalCommandLineCodeExecutor(work_dir="coding")
  code_executor_agent = CodeExecutorAgent(
    name="code_executor",
    code_executor=local_code_executor
  )
  
  stream = code_executor_agent.run_stream(task="""
```python
print("Hello World")
```
""")
  
  await Console(stream)
  
asyncio.run(main())