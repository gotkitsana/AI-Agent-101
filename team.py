import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily
from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination, TokenUsageTermination, TimeoutTermination
from autogen_agentchat.teams import RoundRobinGroupChat


async def main():
  model_client_openai = OpenAIChatCompletionClient(model="gpt-4o-mini")
  model_client_ollama = OpenAIChatCompletionClient(
    model="llama3.2",
    base_url=os.environ["OLLAMA_BASE_URL"],
    model_info=ModelInfo(
      vision=False,
      function_calling=True,
      json_output=False,
      family=ModelFamily.UNKNOWN,
    )
  )
  
  writer_agent = AssistantAgent(
    name="writer",
    model_client=model_client_openai,
    system_message="You're a writer, write well"
  )
  
  editor_agent = AssistantAgent(
    name="editor",
    model_client=model_client_openai,
    system_message="""
You're an editor, provide critical feedback.
Response with 'APPROVE' if the text addresses all feedback. 
"""
  )
  
  termination = TextMentionTermination(text="APPROVE") | MaxMessageTermination(max_messages=5)
  team = RoundRobinGroupChat(
      participants=[writer_agent,editor_agent],
      termination_condition=termination
  )
  
  society_of_mind_agent = SocietyOfMindAgent(
    name="society_of_mind",
    team=team,
    model_client=model_client_openai
  )
  
  translator_agent = AssistantAgent(
    name="translator",
    model_client=model_client_openai,
    system_message="Translate the text to Thai."
  )
  
  final_team = RoundRobinGroupChat(
    participants=[society_of_mind_agent, translator_agent],
    max_turns=2
  )
   
  stream = final_team.run_stream(task="Write a short story about green tea.")
  await Console(stream)

asyncio.run(main())