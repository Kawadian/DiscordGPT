# MySQLとMariaDBを使用したDiscord用のOpenAI Bot（日本語版 README）

このプログラムは、Discordボットを作成し、各ユーザーのOpenAIトークンを登録し、それを使用してGPT-3.5-turboモデルからの応答を取得します。MySQLデータベースに各ユーザーのOpenAIトークンを保存し、ユーザーがボットに質問するたびにそのトークンを使用してOpenAIから応答を取得します。

## 使用方法

1. Discord Botを作成します。公式Discord開発者ポータルでBotを作成し、Botのトークンをメモしておきます。

2. OpenAI APIキーを取得します。OpenAIのウェブサイト(https://platform.openai.com)にログインし、APIキーを取得します。

3. MySQLデータベースをセットアップします。ユーザートークンを保存するためのテーブルを作成します。

4. ソースコードをダウンロードし、以下の箇所を自身の情報に合わせて変更します：

    - MySQL接続情報（ホスト名、データベース名、ユーザー名、パスワード）
    - ディスコードボットトークン

<details>
  <summary>MySQLのセットアップ方法</summary>
まず、以下のコマンドを使ってMySQLにrootユーザーとしてログインします。

```bash
sudo mysql -u root -p
```

次に、新たにデータベースを作成します。

```mysql
CREATE DATABASE discord;
```

新しいユーザーを作成します。以下の例では、新しいユーザーの名前は'discorduser'、パスワードは'password'になります。

```mysql
CREATE USER 'discorduser'@'localhost' IDENTIFIED BY 'password';
```

新しいユーザーに、作成したデータベースに対する全ての特権を付与します。

```mysql
GRANT ALL PRIVILEGES ON discord.* TO 'discorduser'@'localhost';
```

変更を有効にするために特権をフラッシュします。

```mysql
FLUSH PRIVILEGES;
```

セッションを終了します。

```mysql
exit;
```

この手順で新しいデータベースを作成し、新しいユーザーに対してそのデータベースへのアクセス権限を付与することができます。このユーザーはあとでPythonスクリプトからデータベースにアクセスする際に使用します。

そして、以前提供したテーブル作成コマンドを新たに作成したユーザーで実行します：

```mysql
CREATE TABLE tokens (
    user_id BIGINT NOT NULL,
    token VARCHAR(64) NOT NULL,
    PRIMARY KEY (user_id)
);
```

これでデータベースとユーザー、テーブルの作成が完了です
</details>


5. Python環境をセットアップします。必要なライブラリをインストールします：

    ```bash
    pip install discord.py openai mysql-connector-python retry
    ```

6. ボットを起動します。ターミナルからPythonスクリプトを実行します：

    ```bash
    python3 discord_bot.py
    ```

7. ディスコードのダイレクトメッセージを通じて、ボットに対してOpenAIトークンを登録します。フォーマットは `token:your-token-here`です。例えば、 `token:sk-abcdefghi1234567890`。

8. ボットに質問を投げかけてみましょう。ボットがメンションされたり、ダイレクトメッセージが送られた場合、ボットはそのメッセージをOpenAIに送信し、その応答をチャットに送り返します。

## 注意事項

- ボットが動作している間、OpenAIのAPIキーはサーバーに保存されます。セキュリティ上の観点から、ボットの利用者自身がキーの管理を行うべきです。

- ボットはユーザーの質問をOpenAI APIに送信します。そのため、OpenAI APIの利用料金が発生します。また、ユーザーの質問はOpenAIに送信されるため、機密情報を含む質問を送信しないように注意してください。

- このコ

ードは学習・実験用であり、商用利用を推奨していません。商用利用を検討する場合は、適切なセキュリティ対策やエラーハンドリングを実装する必要があります。

## ライセンス

このプロジェクトはMITライセンスの下でリリースされています。詳細はLICENSEファイルをご覧ください。