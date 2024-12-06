import agiverse

building = agiverse.SmartBuilding(api_key=1, building_id=26)

@building.event
async def on_ready():
    print(f"Smart building {building.building_id} is ready to use")

@building.event
async def on_building_info(building_info):
    print(f"Building info: {building_info}")

@building.event
async def on_players(players):
    print(f"Current players in the building: {players}")

@building.action(action="echo", payload_description='{"content": string}')
async def echo(ctx: agiverse.ActionContext, payload):
    if payload and "content" in payload:
        await ctx.send_result(f'You are player {ctx.player_id}, you said "{payload["content"]}". There are {len(ctx.building.players)} players in the building now.')
    else:
        await ctx.send_result({"error": "You didn't say anything!"})

building.run()
