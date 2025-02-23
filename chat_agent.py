import os
import asyncio
import json
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

async def main():
  model_client_ollama = OpenAIChatCompletionClient(
    model="llama3.2:latest",
    base_url=os.environ["OLLAMA_BASE_URL"],
    model_info=ModelInfo(
      vision=False,
      function_calling=False,
      json_output=False,
      family=ModelFamily.UNKNOWN,
    )
  )
  
  assistant_agent = AssistantAgent(
    name="assistant",
    model_client=model_client_ollama,
    system_message="You're a helpful personal assistant.",
  )
  
  if os.path.exists("assistant_agent.json"):
    with open("assistant_agent.json", "r") as f:
      state = json.load(f)
      await assistant_agent.load_state(state)
  
  while True:
    user_message = input("User: ")
    if user_message == "bye":
      break
    
    cancellation_token = CancellationToken()
    message = TextMessage(content=user_message, source="user")
    response = await assistant_agent.on_messages(
      messages=[message],
      cancellation_token=cancellation_token
    )
    print(f"{response.chat_message.content}\n{response.chat_message.models_usage}")
    
  with open("assistant_agent.json", "w") as f:
    state = await assistant_agent.save_state()
    json.dump(state, f, indent=4)
  
asyncio.run(main())