# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# The environment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /discord_bot

# Set the working directory to /discord_bot
WORKDIR /discord_bot

# Copy the current directory contents into the container at /discord_bot
ADD . /discord_bot/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run bot.py when the container launches
CMD ["python", "DiscordGPT_MariaDB.py"]
