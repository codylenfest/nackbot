from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents

from functions import *

load_dotenv()
api_token = os.getenv("botAPIKey")
percentChanceResponse = os.getenv("responsePercentChance")

# intents are necessary since an upgrade was made to discordBot api a long time ago
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

# Globals
# NGA guild information (387429109049065472)

try:
	databaseConnection = sqlite3.connect('main.db')
	print("Nackbot successfully connected to database successfully.")
	databaseCursor = databaseConnection.cursor()
except:
	print("Nackbot didn't connect to the database")


@bot.event
async def on_ready():
	print('Bot is online')


@bot.command(aliases=['HUT'])
async def hut(context):
	await context.send('2 3 Ner')


@bot.command(aliases=['percent', 'changePercent', 'changepercentchance', 'changePercentChance'])
async def change_percent_chance(context, newPercent):
	global percentChanceResponse
	oldPercent = percentChanceResponse
	print(newPercent)
	if (context.author.id == 81085202499112960):
		# Read in the file
		with open('.env', 'r') as file:
			filedata = file.read()

		# Replace the target string
		filedata = filedata.replace('responsePercentChance = ' + percentChanceResponse, 'responsePercentChance = ' + newPercent)

		# Write the file out again
		with open('.env', 'w') as file:
			file.write(filedata)
		percentChanceResponse = newPercent
		await context.send(f'My response percent chance has been changed from {oldPercent} to {newPercent}')


@bot.listen('on_message')
async def message_listener(message):
	# NackBot shouldn't respond to itself
	if random.randrange(100) < int(percentChanceResponse) and message.author.id != 944428991828344883:
		nackResponse = databaseCursor.execute("SELECT message FROM nack ORDER BY RANDOM() LIMIT 1")
		nackResponse = databaseCursor.fetchone()
		# response is actually a tuple so get the value at position zero
		nackResponse = nackResponse[0]

		await message.reply(nackResponse)


bot.run(api_token)
