## WithHistoryとの違い

DiscordGPT.pyとDiscordGPT_WithHistory.pyの違いは、直近の会話をAIが参照するか否かの違いです。<br>
参照することで過去の会話に関連した返答をすることができますが、token数が多くなります。<br>
また、DiscordGPT_WithHistory.pyの方は時々エラーが発生するため、安定しているとは言い切れません。ご注意ください。<br>

## DiscordでChatGPTを使用するためのPythonスクリプトの使い方

このPythonスクリプトは、Discordの特定のチャンネルでメッセージを受信したとき、または直接メッセージやメンションを受信したときに、ChatGPTを利用して自動的に応答します。

### 必要なもの
- Python3
- Discordボットのトークン
- OpenAIのAPIキー

### インストール

Pythonが既にインストールされていることを確認します。次に、以下のコマンドを実行して必要なライブラリをインストールします。

```
pip install discord.py openai
```

### 使用方法

1. まず、Discord botとOpenAIのAPIキーを取得します。

2. Pythonスクリプトに、Discord botのトークンとOpenAIのAPIキーを記入します。

   ```python
   openai.api_key = 'your-openai-api-key' 
   client.run("your-discord-bot-token")
   ```

3. `target_channel_ids` のリストに、監視したいDiscordチャンネルのIDを追加します。

   ```python
   target_channel_ids = [12345, 67890, 12345]
   ```

4. すべての設定が完了したら、Pythonスクリプトを実行します。

   ```
   python your-script.py
   ```

ボットが起動したら、指定されたDiscordチャンネルでメッセージを送信するか、ボットに直接メッセージを送信するか、メンションすると、自動的に応答します。注意すべき点として、ボットは他のボットからのメッセージには応答しません。

### 注意事項

- OpenAIのAPIキーとDiscordのボットのトークンはとても重要です。絶対に他人に見られないようにしてください。それらはあなたのアカウントを制御するためのキーであり、それらを知られてしまうとあなたのアカウントが不正に利用される可能性があります。

- このスクリプトはサンプルであり、使用する際には適切なエラーハンドリングやセキュリティ対策を実装することを強く推奨します。

以上がこのPythonスクリプトの基本的な使い方です。詳細についてはDiscord botやOpenAIの公式ドキュメンテーションを参照してください。
また、作成者はまだまだ未熟なので、改善点などがあれば指摘いただけると幸いです。

