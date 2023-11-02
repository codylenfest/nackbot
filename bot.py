from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents

from functions import *

CODY_ID = 81085202499112960

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


@bot.command(aliases=['addNack', 'addnack', 'addresponse', 'addResponse'])
async def add(context, message):
    isAlreadyResponse = None
    if context.author.id == CODY_ID:
        # Check to see if the URL provided already exists in the frogs table or the posts_for_voting table awaiting votes
        for row in databaseCursor.execute("SELECT * FROM nack WHERE message=?", (message,)):
            isAlreadyResponse = row
        if isAlreadyResponse:
            await context.send("This is already a nackbot response.")
        else:
            databaseCursor.execute("INSERT INTO nack (message) VALUES (?);",(message,))
            databaseConnection.commit()

            await context.send("Message has been added to my potential responses.")


@bot.command(aliases=['percent', 'changePercent', 'changepercentchance', 'changePercentChance','change'])
async def change_percent_chance(context, newPercent):
    global percentChanceResponse
    oldPercent = percentChanceResponse
    print(newPercent)
    if (context.author.id == CODY_ID):
        # Read in the file
        with open('.env', 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('responsePercentChance = ' + percentChanceResponse,
                                    'responsePercentChance = ' + newPercent)

        # Write the file out again
        with open('.env', 'w') as file:
            file.write(filedata)
        percentChanceResponse = newPercent
        await context.send(f'My response percent chance has been changed from {oldPercent} to {newPercent}')


@bot.command(aliases=['current', 'currentpercent', 'current_percent', 'currentPercent'])
async def currentpercentchance(context):
    global percentChanceResponse

    await context.send(f'Current percent chance is {percentChanceResponse}')


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
