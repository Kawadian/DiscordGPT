import discord
import openai

openai.api_key = 'token'

intents = discord.Intents.all()
client = discord.Client(intents=intents)

target_channel_ids = [12345, 12345, 12345]  # 監視したいチャンネルのIDをリストで保持

@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)

@client.event
async def on_message(message):
    if message.author.bot:
        return 

    # メンションされた時、またはDMでメッセージが送られた場合、特定のチャンネル内のみ応答
    if message.channel.id in target_channel_ids or client.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        # メンションの部分を削除
        question = message.content.replace(f'<@!{client.user.id}>', '').strip()
        # Show typing status
        async with message.channel.typing():
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f'"{question}"'
                    },
                ],
            )

        chat_results = response["choices"][0]["message"]["content"]
        await message.channel.send(chat_results)


client.run("token")