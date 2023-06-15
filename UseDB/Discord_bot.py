import os
import discord
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import openai
from openai.error import AuthenticationError
import re
import concurrent.futures
import asyncio
from retry import retry
from dotenv import load_dotenv
import db_operations

load_dotenv()

#Set DiscordBot Token
discord_token = os.getenv('DISCORD_BOT_TOKEN')

# Generate an object with access rights to all Discord events
intents = discord.Intents.all()

# Create a Discord client object
client = discord.Client(intents=intents)

# Create a thread pool that allows a maximum of 3 tasks to be executed simultaneously
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
slash = SlashCommand(client, sync_commands=True)

# Function to get a response from OpenAI
# If an API connection error occurs, it will retry 2 times
@retry(openai.error.APIConnectionError, tries=2, delay=2)
def fetch_openai_response(user_id, model, message_history, question):
    openai.api_key = db_operations.get_token(user_id)
    return openai.ChatCompletion.create(
        model=model,
        messages=message_history + [
            {
                "role": "user",
                "content": question
            },
        ],
    )

async def get_message_history(channel, limit, current_message):
    message_history = []
    async for msg in channel.history(limit=limit):
        message_history.append({
            "role": "system" if msg.author == client.user else ("user" if msg.author == current_message.author else "assistant"),
            "content": msg.content
        })
    return message_history
# Print confirmation when client is ready
@client.event
async def on_ready():
    print("Bot is ready")
    print(discord.__version__)

@slash.slash(
        name="save_token",
        description="Save OpenAI token.",
        options=[
            create_option(
                name="token",
                description="Your OpenAI token.",
                option_type=3,
                required=True
            )
        ])
async def _token_save(ctx: SlashContext, token: str):
    if token.startswith("sk-"):
        try:
            openai.api_key = token  # スラッシュコマンドから提供されたトークンを直接使用
            openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}])
            db_operations.save_token(str(ctx.author_id), token)
            await ctx.send('Token has been updated.')
        except Exception as e:
            await ctx.send('Invalid token. Please check your token and try again.')
    else:
        await ctx.send("Invalid token format. Token must start with 'sk-'")

@slash.slash(
    name="delete_token",
    description="Delete OpenAI token.")
async def _token_delete(ctx: SlashContext):
    db_operations.delete_token(str(ctx.author_id))
    await ctx.send("Your token has been deleted.")

@slash.slash(
    name="set_model",
    description="Set your preferred language model",
    options=[
        create_option(
            name="model",
            description="Choose a model",
            option_type=3,
            required=True,
            choices=[
                create_choice(name="gpt-3.5-turbo", value="gpt-3.5-turbo"),     
                create_choice(name="gpt-3.5-turbo-16k", value="gpt-3.5-turbo-16k"),   
                create_choice(name="gpt-4", value="gpt-4"),    
                create_choice(name="gpt-4-32k", value="gpt-4-32k"),             
                # Add more models as desired
            ]
        )
    ]
)
async def _model(ctx, model: str): 
    print(f"Received command to change model to {model} for user {ctx.author_id}")  # Add this line
    db_operations.save_model(ctx.author_id, model)
    await ctx.send(f"Model changed to {model}", hidden=True)

@client.event
async def on_message(message):
    if message.author.bot:
        return 
    if client.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        question = re.sub(r'<@!?\d+>', '', message.content).strip()
        message_history = await get_message_history(message.channel, limit=5, current_message=message)
        model = db_operations.get_model(message.author.id) or "gpt-3.5-turbo"

        # Check if the user's API key is registered
        api_key = db_operations.get_token(message.author.id)
        if not api_key:
            await message.channel.send("The API key is not registered. Please use '/save_token' to register the API key and try again.")
            return

        async with message.channel.typing():
            loop = asyncio.get_running_loop()
            try:
                response = await loop.run_in_executor(executor, fetch_openai_response, message.author.id, model, message_history, question)
                chat_results = response["choices"][0]["message"]["content"] + "\n" + "by " + model
                await message.channel.send(chat_results)
            except Exception as e:
                print(f"Unexpected error: {e}")
                if "This model's maximum context length is" in str(e):
                    await message.channel.send("Token limit has been exceeded. Unable to respond. Here are the details\n" + str(e))
                    return
                chat_results = "An error has occurred. Here are the details\n" + str(type(e).__name__)
                await message.channel.send(chat_results)

# Launch the bot
client.run(discord_token)