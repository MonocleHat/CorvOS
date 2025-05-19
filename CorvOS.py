#!/bin/env python3
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#config main function
def main():
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix="$",intents=intents)

    @client.event 
    async def on_ready():
        print(f"{client.user.name} has logged in")
        tester_channel = client.get_channel(1362960799160860844)
        await tester_channel.send("CorvOS Online -- What you see I see")
        await tester_channel.send("Also, get me some birdseed")
        
        for folder in os.listdir("modules"):
            if os.path.exists(os.path.join("modules",folder,"cog.py")):
                await client.load_extension(f"modules.{folder}.cog")

    client.run(TOKEN)

if __name__ == '__main__':
    main()
