import os
import discord
import openai
import re
import concurrent.futures
import asyncio
from retry import retry
from dotenv import load_dotenv

token = os.getenv('DISCORD_BOT_TOKEN')
openai.api_key = os.getenv('OPENAI_API_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

@retry(openai.error.APIConnectionError, tries=2, delay=2)
def fetch_openai_response(message_history, question):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
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

@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)

@client.event
async def on_message(message):
    if message.author.bot:
        return 

    if client.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        question = re.sub(r'<@!?\d+>', '', message.content).strip()
        message_history = await get_message_history(message.channel, limit=5, current_message=message)

        async with message.channel.typing():
            loop = asyncio.get_running_loop()
            try:
                response = await loop.run_in_executor(executor, fetch_openai_response, message_history, question)
                chat_results = response["choices"][0]["message"]["content"]
                await message.channel.send(chat_results)
            except Exception as e:
                print(f"Unexpected error: {e}")
                if "This model's maximum context length is" in str(e):
                    await message.channel.send("トークンの制限を超えています。応答することができません。詳細は以下の通りです\n" + str(e))
                    return
                chat_results = "エラーが発生しました。詳細は以下の通りです\n" + str(type(e).__name__)
                await message.channel.send(chat_results)

client.run(token)