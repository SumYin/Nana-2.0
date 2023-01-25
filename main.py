import nextcord
from nextcord.ext import commands
import os
import json
import re
import translation

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'We have logged in as {client.user}')
TESTING_GUILD_ID = 1066065492671987722

intents = nextcord.Intents.default()
intents.messages = True
client = Bot(intents=intents)

counting_channel = 1066065833069133864

def get_current_number():
    with open('counting.json') as f:
        return json.load(f)["current_number"]

class Dropdown (nextcord.ui.Select):
    def __init__(self, message):
        self.message = message
        languages={
            "en":"English",
            "es":"Spanish",
            "fr":"French",
            "de":"German",
            "it":"Italian",
            "ja":"Japanese",
            "ko":"Korean",
            "pt":"Portuguese",
            "zh-hans" : "Chinese Simplified",
            "ru":"Russian",
            "ar":"Arabic",
            "tr":"Turkish",
            "nl":"Dutch",
            "pl":"Polish",
            "sv":"Swedish",
            "da":"Danish",
            "fi":"Finnish",
        }
        select_options = []
        for i in languages:
            select_options.append(nextcord.SelectOption(label=languages[i], value=i))

        super().__init__(placeholder="Select a language", options=select_options, delete_after=10)
    
    async def callback(self, interaction: nextcord.Interaction):
        translated=await translation.translate(self.message.content, self.values[0], os.getenv("KEY"))
        await interaction.response.send_message(f"{translated}", ephemeral=True)

class DropdownView(nextcord.ui.View):
    def __init__(self, message):
        super().__init__()
        self.add_item(Dropdown(message))

@client.message_command(name='translate', guild_ids=[TESTING_GUILD_ID])
async def say(interaction: nextcord.Interaction, message: nextcord.Message):
    """Sends the drop down with the languages"""

    old_message = await interaction.response.send_message("Select a language", view=DropdownView(message), ephemeral=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = re.sub(r"[^0-9+\-*/]", "", message.content)
    if message.channel.id == counting_channel and content!="":
        next_number = get_current_number() + 1
        if eval(content) == next_number:
            # update the json file value current_number to be 1 higher
            data={"current_number":next_number}
            with open("counting.json", "w") as jsonFile:
                json.dump(data, jsonFile)
        else:
            await message.delete()
    elif message.channel.id == counting_channel and content=="":
        await message.delete()

@client.slash_command(description="My first slash command")
async def hello(interaction: nextcord.Interaction):
    await interaction.send("Hello! I am Nana 2.0!")

client.run(os.getenv("TOKEN"))
