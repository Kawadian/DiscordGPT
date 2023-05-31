import discord
import openai
import re
import concurrent.futures
import asyncio
import os
import mysql.connector
from retry import retry
from mysql.connector import Error

# discordの全てのイベントに対するアクセス権限を持つオブジェクトを生成
intents = discord.Intents.all()
# Discordのクライアントオブジェクトを作成
client = discord.Client(intents=intents)
# 同時に実行可能な最大のタスク数を3に設定したスレッドプールを作成
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

# データベースからユーザのトークンを取得する関数
# データベースへの接続が失敗した場合は2回リトライし、それでも失敗した場合はNoneを返す
@retry(Error, tries=2, delay=2)
def get_token(user_id):
    try:
        # MySQLに接続
        connection = mysql.connector.connect(
            host='localhost',
            database='discord',
            user='discorduser',
            password='password'
        )

        # 接続に成功した場合
        if connection.is_connected():
            cursor = connection.cursor()
            # パラメータ化されたクエリを使って、トークンを取得
            stmt = "SELECT token FROM tokens WHERE user_id = %s"
            cursor.execute(stmt, (user_id,))
            record = cursor.fetchone()
            return record[0] if record else None

    except Error as e:
        print(f"Error reading data from MySQL table: {e}")
        return None

    finally:
        # データベースからの切断
        if connection.is_connected():
            cursor.close()
            connection.close()

# データベースにユーザのトークンを保存する関数
# データベースへの接続が失敗した場合は2回リトライする
@retry(Error, tries=2, delay=2)
def save_token(user_id, token):
    try:
        # MySQLに接続
        connection = mysql.connector.connect(
            host='localhost',
            database='discord',
            user='discorduser',
            password='password'
        )

        # 接続に成功した場合
        if connection.is_connected():
            cursor = connection.cursor()
            # パラメータ化されたクエリを使って、トークンを保存
            stmt = "INSERT INTO tokens (user_id, token) VALUES (%s, %s)"
            cursor.execute(stmt, (user_id, token))
            connection.commit()

    except Error as e:
        print(f"Error writing data to MySQL table: {e}")

    finally:
        # データベースからの切断
        if connection.is_connected():
            cursor.close()
            connection.close()

# OpenAIから応答を取得する関数
# API接続エラーが発生した場合は2回リトライする
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

# botが準備完了したときに呼び出されるイベントハンドラ
@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)

# メッセージが送信されたときに呼び出されるイベントハンドラ
@client.event
async def on_message(message):
    # メッセージがbotからのものであれば無視
    if message.author.bot:
        return 

    # DMを通じてトークンが送信された場合、トークンを保存
    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith('token:'):
            token = message.content[6:].strip()
            if token.startswith("sk-"):
                save_token(message.author.id, token)
                await message.channel.send("Token has been saved.")
            else:
                await message.channel.send("Invalid token.")

    # botにメンションがあった場合、またはDMが送られた場合、OpenAIに問い合わせ
    if client.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        token = get_token(message.author.id)
        if token:
            question = re.sub(r'<@!?\d+>', '', message.content).strip()

            #メッセージの履歴を取得
            message_history = []
            async for msg in message.channel.history(limit=5):  #過去何件のメッセージを取得するか調整
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
                    if "This model's maximum context length is" in str(e):
                        await message.channel.send("Token limit exceeded. Unable to respond. Details are as follows.\n" + str(e))
                        return
                    chat_results = "An error has occurred. Details are as follows.\n" + str(type(e).__name__)
                    await message.channel.send(chat_results)
        else:
            await message.channel.send("You must first register an OpenAI token. Send a DM with 'token:your-token-here'.")

# botを起動
client.run("discord_token")