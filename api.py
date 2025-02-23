import asyncio
from autogenstudio.teammanager import TeamManager

async def main():
  manager = TeamManager()
  response = await manager.run(
    team_config="agent.json",
    task="ขอข้อมูลสภาพอากาศที่จังหวัดเชียงราย",
  )
  print(response)

asyncio.run(main())