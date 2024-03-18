import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pytube import YouTube
import boto3

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Define intents
intents = discord.Intents.default()

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Event to print activity when bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(f'Guild: {GUILD}')

# Function to upload file to S3
def upload_file(title):
    filepath = f'../yt-Videos/{title}'
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        return False

    # Upload the file to S3
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(filepath, "yt-vid-bucket", title)
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return False
    # print("Finished uploading file to S3")
    return True

# Command to download and upload YouTube videos
@bot.command(name='download')
async def download(ctx):
    await ctx.send("Enter the number of videos to download:")
    try:
        response = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
        n = int(response.content)
    except TimeoutError:
        await ctx.send("Timed out. Please try again.")
        return

    links = []
    await ctx.send("Enter the links one per line:")
    for i in range(n):
        try:
            response = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
            links.append(response.content)
        except TimeoutError:
            await ctx.send("Timed out. Please try again.")
            return

    for i, link in enumerate(links, start=1):
        try:
            yt = YouTube(link)
            title = f'{yt.title}.mp4'
            await ctx.send(f"\nDetails for Video {i}\nTitle: {title}\nLength: {yt.length} seconds")
            # ys = yt.streams.filter(adaptive=True, only_audio=False, res='720p', file_extension='mp4')[0]
            ys = yt.streams.get_highest_resolution()
            await ctx.send("Downloading...")
            ys.download('../yt-Videos/', filename=title)
            await ctx.send("Download completed.")
            await ctx.send("Uploading to S3...")
            if upload_file(title):
                await ctx.send(f"Uploaded to S3: {title}")
            else:
                await ctx.send(f"Failed to upload {title} to S3.")
        except Exception as e:
            await ctx.send(f"Error processing video {i}: {e}")

# Run the bot
bot.run(TOKEN)
