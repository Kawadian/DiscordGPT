[MariaDBを使用したバージョンのREADMEはこちら](./UseDB/README.MariaDB.md)

[README in English Using MariaDB Script](./UseDB/README.MariaDB_en.md)

## DiscordでChatGPTを使用するためのPythonスクリプトの使い方

このPythonスクリプトは、直接メッセージを受信した時、またはメンションされたときに、ChatGPTを利用して自動的に応答します。<br>
また、過去5件のメッセージを参照しているので、継続的な会話にも対応します。<br>
Dockerを使用することを想定していますが、環境変数さえ設定すればローカル環境にて直接構築をすることができます。<br>

### 必要なもの
- Python3
- Discordボットのトークン
- OpenAIのAPIキー

## インストール

1. リポジトリをクローンします：

    ```bash
    git clone https://github.com/Kawadian/DiscordGPT.git
    ```

2. リポジトリのディレクトリに移動します：

    ```bash
    cd ./DiscordGPT
    ```

3. 環境変数を設定します：

    `.env`ファイルを作成し、以下の形式でDiscordのボットトークンを設定します：

    ```
    DISCORD_BOT_TOKEN=your_discord_bot_token_here
    OPENAI_API_TOKEN=your_openai_api_token_here
    ```

4. Dockerイメージをビルドし、コンテナを起動します：

    ```bash
    docker-compose up
    ```

### 注意事項

- OpenAIのAPIキーとDiscordのボットのトークンはとても重要です。絶対に他人に見られないようにしてください。それらはあなたのアカウントを制御するためのキーであり、それらを知られてしまうとあなたのアカウントが不正に利用される可能性があります。

- このスクリプトはサンプルであり、使用する際には適切なエラーハンドリングやセキュリティ対策を実装することを強く推奨します。

以上がこのPythonスクリプトの基本的な使い方です。詳細についてはDiscord botやOpenAIの公式ドキュメンテーションを参照してください。
また、作成者はまだまだ未熟なので、改善点などがあれば指摘いただけると幸いです。

