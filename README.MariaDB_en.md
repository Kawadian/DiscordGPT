# Using MySQL and MariaDB for Discord OpenAI Bot (English README)

This program creates a Discord bot, registers each user's OpenAI token, and uses it to get responses from the GPT-3.5-turbo model. It stores each user's OpenAI token in a MySQL database and uses that token to get responses from OpenAI whenever a user asks the bot a question.

## Usage

1. Create a Discord Bot. Create a bot in the official Discord Developer Portal and take note of the bot's token.

2. Get your OpenAI API key. Log into the OpenAI website (https://platform.openai.com) and get your API key.

3. Set up a MySQL database. Create a table to store user tokens.

4. Download the source code and change the following sections to fit your information:

    - MySQL connection details (hostname, database name, username, password)
    - Discord bot token

<details>
  <summary>How to set up MySQL</summary>
First, use the following command to log in to MySQL as the root user.

```bash
sudo mysql -u root -p
```

Next, create a new database.

```mysql
CREATE DATABASE discord;
```

Create a new user. In the following example, the new user's name is 'discorduser', and the password is 'password'.

```mysql
CREATE USER 'discorduser'@'localhost' IDENTIFIED BY 'password';
```

Grant all privileges on the created database to the new user.

```mysql
GRANT ALL PRIVILEGES ON discord.* TO 'discorduser'@'localhost';
```

Flush privileges to make changes effective.

```mysql
FLUSH PRIVILEGES;
```

Exit the session.

```mysql
exit;
```

With these steps, you can create a new database and grant access rights to that database to a new user. You will use this user to access the database from a Python script later.

Then, execute the previously provided table creation command with the newly created user:

```mysql
CREATE TABLE tokens (
    user_id BIGINT NOT NULL,
    token VARCHAR(64) NOT NULL,
    PRIMARY KEY (user_id)
);
```

That completes the creation of the database, user, and table.
</details>

5. Set up the Python environment. Install the necessary libraries:

    ```bash
    pip install discord.py openai mysql-connector-python retry
    ```

6. Launch the bot. Run the Python script from the terminal:

    ```bash
    python3 discord_bot.py
    ```

7. Register your OpenAI token with the bot via a direct message on Discord. The format is `token:your-token-here`. For example, `token:sk-abcdefghi1234567890`.

8. Try asking the bot a question. When the bot is mentioned or a direct message is sent, the bot sends that message to OpenAI and sends the response back to the chat.

## Notes

- While the bot is running, your OpenAI API key will be stored on the server. From a security perspective, bot users should manage their own keys.

- The bot sends user queries to the OpenAI API. Therefore, OpenAI API usage fees apply. Also, because user queries are sent to OpenAI, please be careful not to send queries that contain confidential information.

- This code is for learning and experimentation and is not recommended for commercial use. If considering commercial use, you need to implement appropriate security measures and error handling.

## License

This project is released under the MIT license. For more information, please see the LICENSE file.
