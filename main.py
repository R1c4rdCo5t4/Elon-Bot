import datetime
import discord
from discord import app_commands
from discord.ui import Select, View, Button
import random
import time
from colors import Colors
import requests


# bot client startup
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


# greetings command
@tree.command(name="hello", description="say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user}!")
    await interaction.followup.send("I'm elon!")

# bye command
@tree.command(name="bye", description="say goodbye")
async def bye(interaction: discord.Interaction):
    await interaction.response.send_message(f"Goodbye {interaction.user}!")

# help command
@tree.command(name="help", description="show bot info")
async def help(interaction: discord.Interaction):
    info = discord.Embed(title="Elon can:", description="Say hello/goodbye\nPlay Rock Paper Scissors\nBe your calculator\nChange Status", colour=discord.Colour.red())
    info.set_image(url="https://i.pinimg.com/originals/5f/91/f4/5f91f46852965b1e366b526ab8089a06.gif")
    await interaction.response.send_message(content=None, embed=info)

    
# command that calculates averages
@tree.command(name="average", description="calculate average of numbers")
async def average(interaction: discord.Interaction, values:str):
    values = [float(value) for value in values.split(" ")]
    avg = sum(values) / len(values)
    await interaction.response.send_message(avg)


# command that performs + - / * ** calculations
@tree.command(name="calculate", description="Perform simple math calculations")
async def calculate(interaction: discord.Interaction, num1:int, operation:str, num2:int):

    match(operation):
        case "+": await interaction.response.send_message(num1 + num2)
        case "-": await interaction.response.send_message(num1 - num2)
        case "*": await interaction.response.send_message(num1 * num2)
        case "/": await interaction.response.send_message(num1 / num2)
        case "**": await interaction.response.send_message(num1 ** num2)
        case _: await interaction.response.send_message("Invalid operation")
  

# command that gives a random number from an interval
@tree.command(name="random", description="Generates a random number from range")
async def random_number(interaction: discord.Interaction, num1:int, num2:int):
    await interaction.response.send_message(random.randint(num1, num2))
    
# command that flips a coin
@tree.command(name="flipcoin", description="Flips a coin")
async def flipcoin(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(["Heads", "Tails"]))


# command that adds roles to user
@tree.command(name="role", description="Add a role to yourself")
async def role(interaction: discord.Interaction, role: discord.Role):
    await interaction.user.add_roles(role)
    await interaction.response.send_message(f"Added {role} to {interaction.user}")


class MyButton(Button):
    def __init__(self, author, id, emoji): # override 
        super().__init__(emoji=emoji) # init parent class
        self.id = id
        self.author = author

    async def callback(self, interaction):

        if(self.author != interaction.user):
            await interaction.response.send_message("Not your game")
            return

        plays = ['rock','paper','scissors']
        user_play = self.id
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


# command to play rock paper scissors
@tree.command(name="rps", description="Rock paper scissors game")
async def rps(interaction: discord.Interaction):

    view = View()
    buttons = [
        MyButton(interaction.user, "rock", emoji="🪨"),
        MyButton(interaction.user, "paper", emoji="📄"),
        MyButton(interaction.user, "scissors", emoji="✂️")
    ]

    for button in buttons:
        view.add_item(button)


    await interaction.response.send_message("Let's play!", view=view, delete_after=60)


# command that changes bot's current status
@tree.command(name="status", description="change bot status")
async def changed_status(interaction: discord.Interaction, status: str):
    status = status.title()

    activities = {
        "Playing": discord.ActivityType.playing,
        "Watching": discord.ActivityType.watching,
        "Listening": discord.ActivityType.listening,
        "Streaming": discord.ActivityType.streaming
    }

    select = Select(
        placeholder = "Select an Activity!",
        min_values = 1,
        max_values = 1,
        options = [discord.SelectOption(label=activity, description=f"Display '{activity} {status}'") for activity in activities.keys()]
    )

    async def changed_status_callback(interaction):
        await client.change_presence(activity=discord.Activity(type=activities[select.values[0]], name=status))

        
    select.callback = changed_status_callback
    view = View()
    view.add_item(select)

    await interaction.response.send_message("Choose an Activity to Display!", view=view, ephemeral=True,delete_after=10)
    

# ping command
@tree.command(name="ping", description="Tests the bot's response time (latency)")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! :ping_pong:\n**Time:** {round (client.latency * 1000)} ms")

    
# command that displays user information
@tree.command(name="user", description="Displays user information in the server")
async def user(interaction: discord.Interaction):


    def format_date(d: datetime) -> str:
        return str(f"{d.day}-{d.month}-{d.year}")

    embed = discord.Embed(
        title=interaction.user.name,
        description=f"**Joined Discord:** {format_date(interaction.user.created_at)}\n**Joined Server:** {format_date(interaction.user.joined_at)}",
        colour=interaction.user.color)
    embed.set_image(url=interaction.user.avatar)

    await interaction.response.send_message(content=None, embed=embed)
    
   
# command that translates a sentence to given language
@tree.command(name="translate", description="Translate a sentence to the selected language")
async def translate(interaction: discord.Interaction, target: str, text: str):

    try:
        url = "https://microsoft-translator-text.p.rapidapi.com/translate"

        querystring = {"to[0]": target,"api-version":"3.0","profanityAction":"NoAction","textType":"plain"}

        body = [{"Text": text}]
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "4ddb97d8a5mshb6e76b5a66a0d12p193670jsnaba4c2cbf173",
            "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
        }
        response = requests.request("POST", url, json=body, headers=headers, params=querystring)

    except discord.app_commands.errors.CommandInvokeError:
        await interaction.response.send_message("Invalid target langugae {target}")
        return

    except:
        await interaction.response.send_message("An error occured")
        return

    await interaction.response.send_message(f"{response.json()[0]['translations'][0]['text']}")



# command that sends a random meme
@tree.command(name="meme", description="Sends a random meme")
async def meme(interaction: discord.Interaction):
    meme = requests.get("https://meme-api.herokuapp.com/gimme")
    meme = meme.json()
    embed = discord.Embed(title=meme["title"], colour=discord.Colour.blue())
    embed.set_image(url=meme["url"])
    await interaction.response.send_message(content=None, embed=embed)


# command that gets the code from a github repository
@tree.command(name="code", description="Gets the files from a github repository")
async def code(interaction: discord.Interaction, repo: str):
    repo = repo.split("/")
    url = f"https://api.github.com/repos/{repo[0]}/{repo[1]}/contents"
    code = requests.get(url)
    code = code.json()
    files = []
    for file in code:
        files.append(file["name"])
    embed = discord.Embed(title="Files", description="\n".join(files), colour=discord.Colour.blue())
    await interaction.response.send_message(content=None, embed=embed)

# command that sends you a private message
@tree.command(name="dm", description="Sends you a private message")
async def dm(interaction: discord.Interaction, message: str):
    await interaction.user.send(message)
    await interaction.response.send_message("Message sent!")
    


TOKEN = ""
client.run(TOKEN)
