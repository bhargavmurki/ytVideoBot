import logging

from flask import Flask, request
from pytube import YouTube
import boto3
from botocore.exceptions import ClientError
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# app = Flask(__name__)

SLACK_TOKEN = "xoxb-2464400019841-5709104579636-44xZbATwWAAVN7q3xLK9Nnph"
SLACK_CHANNEL = "#general"


def upload_file(title):
    # Upload the file to S3
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(title + '.mp4', "yt-vid-bucket", title + '.mp4')
    except ClientError as e:
        logging.error(e)
        print("Error uploading file to S3")
        message = "Error uploading file to S3"
        send_slack_message(message)
        return False
    print("Finished uploading file to S3")
    message = "Finished uploading file to S3"
    send_slack_message(message)
    return True


def send_slack_message(message):
    client = WebClient(token=SLACK_TOKEN)
    try:
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        return response["ts"]  # timestamp of the message
    except SlackApiError as e:
        logging.error("Error posting message to Slack: %s", e.response["error"])
        return None


# @app.route('/slack-command', methods=['POST'])
# def slack_command():
#     command_text = request.form.get('text', '').strip()
#
#     # Process the command_text and execute your video download logic here
#     if not command_text.startswith("https://www.youtube.com/"):
#         response_message = "Invalid YouTube link. Please provide a valid YouTube video link."
#         send_slack_message(response_message)
#         return '', 200
#
#     # Example: Download the video from a given YouTube link
#     yt = YouTube(command_text)
#     ys = yt.streams.get_highest_resolution()
#     ys.download('./', filename=yt.title + '.mp4')
#
#     # Upload the downloaded video to S3
#     upload_file(yt.title)
#
#     # Send a response to Slack
#     response_message = f"Video '{yt.title}' downloaded and uploaded to S3!"
#     send_slack_message(response_message)
#
#     return '', 200
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

n = int(input("Enter the number of videos to download: "))
links = []

print("Enter the links one per line: ")

for i in range(0, n):
    temp = input()
    links.append(temp)

for i in range(0, n):
    link = links[i]
    yt = YouTube(link)
    message = f"\nDetails for Video {i + 1}\nTitle: {yt.title}\nLength: {yt.length} seconds"
    send_slack_message(message)

    stream = str(yt.streams.filter(progressive=True))
    stream = stream[1:]
    stream = stream[:-1]
    streamlist = stream.split(", ")
    options_message = "\nAll available options for downloads:\n"

    for j in range(0, len(streamlist)):
        st = streamlist[j].split(" ")
        options_message += f"{j + 1}) {st[1]} and {st[3]}\n"

    send_slack_message(options_message)

    l = yt.streams
    for j in l:
        print(j)

    tag = int(input("\nEnter the itag: "))
    ys = yt.streams.get_by_itag(tag)
    print("\nDownloading")
    ys.download('./', filename=yt.title + '.mp4')
    print("\nDownload done")

    upload_file(yt.title)
    upload_message = "Uploaded to S3: " + yt.title
    send_slack_message(upload_message)
