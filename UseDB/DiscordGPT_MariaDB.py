import os
import discord
import openai
import re
import concurrent.futures
import asyncio
import mysql.connector
from retry import retry
from openai.error import AuthenticationError
from mysql.connector import Error
from dotenv import load_dotenv

#Set DiscordBot Token
token = os.getenv('DISCORD_BOT_TOKEN')

# Generate an object with access rights to all Discord events
intents = discord.Intents.all()

# Create a Discord client object
client = discord.Client(intents=intents)

# Create a thread pool that allows a maximum of 3 tasks to be executed simultaneously
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

# Database configuration
db_config = {
    "host": "db",
    "database": "discord",
    "user": "discorduser",
    "password": "password"
}

# Print confirmation when client is ready
@client.event
async def on_ready():
    print("Bot is ready")
    print(discord.__version__)


# Function to get a user's token from the database
# If the connection to the database fails, it will retry 2 times, and if it still fails, it will return None
@retry(Error, tries=2, delay=2)
def get_token(user_id):
    connection = None
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor()
        # Use a parameterized query to get the token
        stmt = "SELECT token FROM tokens WHERE user_id = %s"
        cursor.execute(stmt, (user_id,))
        record = cursor.fetchone()
        return record[0] if record else None

    except Error as e:
        print(f"Error reading data from MySQL table: {e}")
        return None

    finally:
        # Disconnect from the database
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# Function to save a user's token in the database
# If the connection to the database fails, it will retry 2 times
@retry(Error, tries=2, delay=2)
def save_token(user_id, token):
    connection = None
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor()
        # Use a parameterized query to save the token
        stmt = "INSERT INTO tokens (user_id, token) VALUES (%s, %s)"
        cursor.execute(stmt, (user_id, token))
        connection.commit()

    except Error as e:
        print(f"Error writing data to MySQL table: {e}")

    finally:
        # Disconnect from the database
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Function to delete a user's token from the database
# If the connection to the database fails, it will retry 2 times
@retry(Error, tries=2, delay=2)
def delete_token(user_id):
    connection = None
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor()
        # Use a parameterized query to delete the token
        stmt = "DELETE FROM tokens WHERE user_id = %s"
        cursor.execute(stmt, (user_id,))
        connection.commit()

    except Error as e:
        print(f"Error deleting data from MySQL table: {e}")

    finally:
        # Disconnect from the database
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Function to get a response from OpenAI
# If an API connection error occurs, it will retry 2 times
@retry(openai.error.APIConnectionError, tries=2, delay=2)
def fetch_openai_response(message_history, question, token):
    openai.api_key = token
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history + [
            {
                "role": "user",
                "content": question
            },
        ],
    )

# Event handler that is called when a message is sent
@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author.bot:
        return

    # If a token is sent through a DM, save or delete the token
    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith('token:'):
            token = message.content[6:].strip()
            if token.startswith("sk-"):
                try:
                    # Check if token is valid
                    response = fetch_openai_response([], "Hello", token)
                    # If valid, save the token
                    save_token(message.author.id, token)
                    await message.channel.send('Token has been updated. To delete a token, send "delete token".')
                    return
                except AuthenticationError:
                    # If token is not valid, send error message
                    await message.channel.send("Invalid token. Please check your token and try again.")
                    return
            else:
                await message.channel.send("Invalid token format. Token must start with 'sk-'")
                return

        elif message.content.lower() == 'delete token':
            delete_token(message.author.id)
            await message.channel.send("Your token has been deleted.")
            return

    # If the bot is mentioned or a DM is sent, contact OpenAI
    if client.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        token = get_token(message.author.id)
        if token:
            question = re.sub(r'<@!?\d+>', '', message.content).strip()

            # Get message history
            message_history = []
            async for msg in message.channel.history(limit=5):  # Adjust how many past messages to get
                message_history.append({
                    "role": "assistant" if msg.author == client.user else ("user" if msg.author == message.author else "assistant"),
                    "content": msg.content
                })

            async with message.channel.typing():
                loop = asyncio.get_running_loop()
                try:
                    response = await loop.run_in_executor(executor, fetch_openai_response, message_history, question, token)
                    chat_results = response["choices"][0]["message"]["content"]
                    await message.channel.send(chat_results)
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    chat_results = "An error has occurred. Details are as follows.\n" + str(type(e).__name__)
                    await message.channel.send(chat_results)
        else:
            await message.channel.send("You must first register an OpenAI token. Send a DM with 'token:your-token-here'.")
            
# Launch the bot
client.run(token)