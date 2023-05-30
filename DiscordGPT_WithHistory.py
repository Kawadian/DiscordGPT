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
        question = re.sub(r'<@!?\d+>', '', message.content).strip()

        # メッセージの履歴を取得
        message_history = []
        async for msg in message.channel.history(limit=5):  # 送受信履歴の数を指定
            message_history.append({
                "role": "assistant" if msg.author == client.user else ("user" if msg.author == message.author else "system"),
                "content": msg.content
            })
        response = openai.ChatCompletion.create(
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

        chat_results = response["choices"][0]["message"]["content"]
        await message.channel.send(chat_results)


client.run("token")