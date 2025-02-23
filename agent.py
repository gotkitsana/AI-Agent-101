import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
import json 

async def get_weather(city:str) -> str:
  return f"อุณหภูมิที่{city} คือ 40 องศา"

async def main():
  model_client_ollama = OpenAIChatCompletionClient(
    model="llama3.2:latest",
    base_url=os.environ["OLLAMA_BASE_URL"],
    model_info=ModelInfo(
      vision=False,
      function_calling=True,
      json_output=False,
      family=ModelFamily.UNKNOWN,
    )
  )
  
  weather_agent = AssistantAgent(
    name="weather",
    model_client=model_client_ollama,
    system_message="คุณคือนักพยากรณ์อากาศ จงนำข้อมูลที่ได้มาสรุป และตอบกลับ",
    tools=[get_weather],
    reflect_on_tool_use=True
  )
  
  # with open("agent.json", "w") as f:
  #   json.dump(weather_agent.dump_component().model_dump(), f, indent=4)
  
  stream = weather_agent.run_stream(task="ขอข้อมูลสภาพอากาศที่จังหวัดเชียงราย")
  await Console(stream)

  
asyncio.run(main())