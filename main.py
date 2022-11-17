import discord
from discord import app_commands
import random
import time


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Python"))

        print(f"{self.user} has been logged in.")

client = Client()
tree = app_commands.CommandTree(client)

@tree.command(name="hello", description="say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user}!")

@tree.command(name="bye", description="say goodbye")
async def bye(interaction: discord.Interaction):
    await interaction.response.send_message(f"Goodbye {interaction.user}!")


@tree.command(name="status", description="change bot status")
async def changed_status(interaction: discord.Interaction, activity: str, status: str):
  
    match(activity.lower()):
        case "playing": activity = discord.ActivityType.playing
        case "watching": activity = discord.ActivityType.watching
        case "listening": activity = discord.ActivityType.listening
        case _:
            await interaction.response.send_message("Invalid activity")
            return

    await client.change_presence(activity=discord.Activity(type=activity, name=status.title()))
    await interaction.response.send_message("Done.")



@tree.command(name="help", description="show bot info")
async def help(interaction: discord.Interaction):
    info = discord.Embed(title="Elon can:", description="Say hello/goodbye\nPlay Rock Paper Scissors\nBe your calculator\nChange Status", colour=discord.Colour.red())
    info.set_image(url="https://i.pinimg.com/originals/5f/91/f4/5f91f46852965b1e366b526ab8089a06.gif")
    await interaction.response.send_message(content=None, embed=info)


@tree.command(name="average", description="calculate average of numbers")
async def average(interaction: discord.Interaction, values:str):
    values = [float(value) for value in values.split(" ")]
    avg = sum(values) / len(values)
    await interaction.response.send_message(avg)

@tree.command(name="rps", description="Rock paper scissors game")
async def rps(interaction:discord.Interaction, play:str):
    plays = ['rock','paper','scissors']
    user_play = play.lower()
    bot_play = random.choice(plays)
    plays = [user_play, bot_play]
    winning_plays = [["rock", "scissors"], ["scissors", "paper"], ["paper", "scissors"]]

    if(user_play == bot_play):
        # draw
        await interaction.response.send_message(f"elon played **{bot_play}**... draw!")
    elif(plays in winning_plays):
        #win
        await interaction.response.send_message(f"elon played **{bot_play}**... {interaction.user} wins!")
    else:
        #lose
        await interaction.response.send_message(f"elon played **{bot_play}**... elon wins!")


@tree.command(name="calculate", description="Perform simple math calculations")
async def calculate(interaction: discord.Interaction, num1:int, operation:str, num2:int):

    match(operation):
        case "+": await interaction.response.send_message(num1 + num2)
        case "-": await interaction.response.send_message(num1 - num2)
        case "*": await interaction.response.send_message(num1 * num2)
        case "/": await interaction.response.send_message(num1 / num2)
        case "**": await interaction.response.send_message(num1 ** num2)
        case _: await interaction.response.send_message("Invalid operation")
  

TOKEN = ""
client.run(TOKEN)
