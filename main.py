import discord
import requests
import json
from bs4 import BeautifulSoup
from discord.ext import commands, tasks

# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config['token']
CHANNEL_ID = config['channel_id']
STATUS_PAGE_URL = config['status_page_url']
PREFIX = config['prefix']

bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    update_status_embed.start()

@tasks.loop(minutes=1)
async def update_status_embed():
    channel = bot.get_channel(CHANNEL_ID)
    response = requests.get(STATUS_PAGE_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        status_container = soup.find('div', class_='component-status')
        status = status_container.find('span', class_='component-status-status').text
        description = status_container.find('span', class_='component-status-description').text

        embed = discord.Embed(
            title='CFX Status',
            url=STATUS_PAGE_URL,
            description=f'Status: {status}\n\n{description}'
        )
        await channel.send(embed=embed)
    else:
        print(f'Error: Failed to fetch status (HTTP {response.status_code})')

bot.run(TOKEN)