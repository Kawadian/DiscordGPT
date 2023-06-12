# Discord ChatGPT Bot

This project is a Discord bot that implements ChatGPT in conjunction with the OpenAI API.<br>
It allows each user to register their own API key.<br>
While it is designed to work with Docker, it can also be set up on-premises.<br>
Please adjust the script as needed for such cases.

## Prerequisites

- Python 3.7 or above
- Docker and Docker Compose
- OpenAI API key
- Discord bot token

The creation of the Discord bot is omitted here.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Kawadian/DiscordGPT.git
    ```

2. Move to the 'UseDB' directory where the Python scripts that use the database are located:

    ```bash
    cd ./DiscordGPT/UseDB
    ```

3. Set up the environment variable:

    Create a `.env` file and set your Discord bot token in the following format:

    ```
    DISCORD_BOT_TOKEN=your_bot_token_here
    ```

4. Build the Docker image and start the containers:

    ```bash
    docker-compose up
    ```

## Usage

When you mention the bot on Discord or send a DM to the bot, it generates a response through the OpenAI API. If you are using it for the first time, you need to set up your OpenAI API token by sending a DM to the bot.

## Database

This project uses MariaDB. Database settings are configured in the `docker-compose.yml` file.

## Notes

- Both the OpenAI API and Discord have usage limits, so please be aware of the appropriate usage amounts.
- This bot uses a learning AI and does not guarantee accurate responses to all messages from users. Please use it with caution.
- I am a beginner in programming, so there might be some shortcomings.

## License

This project is released under the MIT license. For more details, please see [LICENSE](../LICENSE).

## Contributing

Pull requests and issues are welcome. If you propose a major change, please propose it through an issue first.

## Contact

If you have any questions or suggestions, feel free to create an issue.
