import discord
import os
from discord.ext import commands
from discord import app_commands
import re
import requests, uuid, json

intents = discord.Intents.default()
intents.message_content = True

#variables
bot = commands.Bot(command_prefix='!', intents=intents)
token = os.getenv("TOKEN")
translatorToken = os.getenv("KEY")
location1 = os.getenv("LOCATION")
@bot.event
async def on_ready():
    print('Bot is ready')
    try:
      synced = await bot.tree.sync()
      print(f"Synced {len(synced) } command(s)")
    except Exception as e:
      print(e)
@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message(f"Hey {interaction.user.mention}! Use this bot by typing `/translate` ")

#filters numbers

@bot.tree.command(name="translate")
@app_commands.describe(message = "What should I translate?")
async def translate(interaction: discord.Interaction, message: str):
  translatedMessage = translation(message)
  await interaction.response.send_message(f"{translatedMessage}")

#----- This is the function to translate ----
  # Add your key and endpoint
def translation(message):
  key = translatorToken
  endpoint = "https://api.cognitive.microsofttranslator.com"
  
  # location, also known as region.
  # required if you're using a multi-service or regional (not global) resource. It     can be found in the Azure portal on the Keys and Endpoint page.
  # location = location1
  
  path = '/translate'
  constructed_url = endpoint + path
  
  params = {
      'api-version': '3.0',
      'from': 'hi',
      'to': 'en'
  }
  
  headers = {
       'Ocp-Apim-Subscription-Key': key,
       # location required if you're using a multi-service or regional (not global)   resource.
       'Ocp-Apim-Subscription-Region': location1,
       'Content-type': 'application/json',
       'X-ClientTraceId': str(uuid.uuid4())
  }  
  
    # You can pass more than one object in body.
  body = [{
       'text': message
  }]
  
  request = requests.post(constructed_url, params=params, headers=headers, json=body)
  response = request.json()
  
  return response[0]['translations'][0]['text']
  
  
  
bot.run(token)
