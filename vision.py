import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import Image

async def main():
  model_client_ollama = OpenAIChatCompletionClient(
    model="llama3.2-vision",
    base_url=os.environ["OLLAMA_BASE_URL"],
    model_info=ModelInfo(
      vision=True,
      function_calling=True,
      json_output=False,
      family=ModelFamily.UNKNOWN,
    )
  )
  
  vision_agent = AssistantAgent(
    name="vision",
    model_client=model_client_ollama,
    system_message="คุณคือนักวิเคราะห์รูปภาพ",
  )
  
  message = MultiModalMessage(
    content=[
      "describe this image",
      Image.from_file("check.png"),
    ],
    source="vision"
  )
  
  stream = vision_agent.run_stream(task=message)
  await Console(stream)
  
asyncio.run(main())