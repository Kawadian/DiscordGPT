import discord
import openai
import re
import concurrent.futures
import asyncio

openai.api_key = 'token'

intents = discord.Intents.all()
client = discord.Client(intents=intents)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

def fetch_openai_response(message_history, question):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history + [
            {
                "role": "system",
                "content": "日本語で応答してください"
            },
            {
                "role": "user",
                "content": question
            },
        ],
    )

@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)

@client.event
async def on_message(message):
    if message.author.bot:
        return 

    # メンションされた時、またはDMでメッセージが送られた場合のみ応答
    if client.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        # メンションの部分を削除
        question = re.sub(r'<@!?\d+>', '', message.content).strip()
        # Get message history
        message_history = []
        async for msg in message.channel.history(limit=5):  # Change the limit as needed
            message_history.append({
                "role": "system" if msg.author == client.user else ("user" if msg.author == message.author else "assistant"),
                "content": msg.content
            })

        # Show typing status
        async with message.channel.typing():
            # Fetch OpenAI response in a separate thread
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(executor, fetch_openai_response, message_history, question)

        chat_results = response["choices"][0]["message"]["content"]
        await message.channel.send(chat_results)

client.run("token")