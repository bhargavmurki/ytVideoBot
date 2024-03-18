# Discord Bot for Downloading and Uploading YouTube Videos

This Discord bot allows users to download YouTube videos and upload them to an S3 bucket.

## Setup

1. **Clone the repository.**

2. **Install the required dependencies using `pip install -r requirements.txt`.**

3. **Set up a `.env` file with the following variables:**
   - `DISCORD_TOKEN`: Your Discord bot token.
   - `DISCORD_GUILD`: The name of your Discord server.
   - `S3_BUCKET`: The name of your S3 bucket.
   - `FOLDER_NAME`: The name of the folder in your local machine where the videos are stored.
   - And set up the S3 Access Key and Secret Key using the `aws configure` command as it is not suggested to store them in .env file.

4. **Create a new Discord application and add a bot to it. Follow these steps:**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click on "New Application" and give your application a name.
   - Go to the "Bot" tab and click on "Add Bot".
   - Copy the bot token and paste it into your `.env` file as `DISCORD_TOKEN`.

5. **Invite the bot to your Discord server. Follow these steps:**
   - In the Discord Developer Portal, go to the "OAuth2" tab.
   - Under "OAuth2 URL Generator", select the "bot" scope.
   - Copy the generated URL and open it in your web browser.
   - Select the server you want to add the bot to and click "Authorize".

6. **Create an S3 bucket and configure AWS credentials on your machine.**

7. **Run the bot using `python main.py`.**

## Usage

Once the bot is running and added to your Discord server, you can use the following command to download and upload YouTube videos:

- `!download`: Downloads the video from the given URL and uploads it to the S3 bucket.

Follow the prompts to enter the number of videos to download and the YouTube links.
