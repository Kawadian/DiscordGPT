# Discord ChatGPT Bot

このプロジェクトは、OpenAI APIと連携してChatGPTを実装するDiscordボットです。<br>
ユーザーごとにAPIキーを登録する形となっています。<br>
Dockerを利用することが前提となっていますが、オンプレミスで構築することも可能です。<br>
その際は適宜スクリプトを書き換えてください。

## 必要なもの

- Python 3.7以上
- Docker と Docker Compose
- OpenAI APIキー
- Discordボットトークン

ここではDiscord botの作成方法は割愛します。

## インストール

1. リポジトリをクローンします：

    ```bash
    git clone https://github.com/Kawadian/DiscordGPT.git
    ```

2. データベースを使用するPythonスクリプトは「UseDB」内にあるので、そこに移動します：

    ```bash
    cd ./DiscordGPT/UseDB
    ```

3. 環境変数を設定します：

    `.env`ファイルを作成し、以下の形式でDiscordのボットトークンを設定します：

    ```
    DISCORD_BOT_TOKEN=your_bot_token_here
    ```

4. Dockerイメージをビルドし、コンテナを起動します：

    ```bash
    docker-compose up
    ```

## 使い方

Discord上でボットをメンションするか、ボットにDMを送ると、OpenAI APIを通じて応答を生成します。初めて使用する場合、ボットにDMを送信してOpenAI APIのトークンを設定する必要があります。

## データベース

このプロジェクトではMariaDBを使用しています。データベースの設定は`docker-compose.yml`ファイルで行います。

## 注意事項

- OpenAI APIとDiscordの両方で使用量に制限があるため、適切な使用量を確認してください。
- このボットは学習型AIを使用しており、ユーザーからのすべてのメッセージに対する正確な応答を保証するものではありません。使用には十分な注意が必要です。

## ライセンス

このプロジェクトはMITライセンスのもとで公開されています。詳細は[LICENSE](../LICENSE)をご覧ください。

## 貢献

プルリクエストやイシューの提出は大歓迎です。大規模な変更を提案する場合は、まずイシューを通じて変更を提案してください。

## お問い合わせ

何か質問や提案がある場合は、お気軽にイシューを作成してください。