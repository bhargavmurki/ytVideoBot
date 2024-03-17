import logging

from pytube import YouTube
import boto3
from botocore.exceptions import ClientError
import os


def upload_file(title):
    getFilepathFromPath = '../yt-Videos/' + title
    filenameActual = title
    if not os.path.exists(getFilepathFromPath):
        logging.error("File '%s' does not exist.", getFilepathFromPath)
        print("Error: File not found.")
        return False

    # Upload the file to S3
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(getFilepathFromPath, "yt-vid-bucket", filenameActual)
    except ClientError as e:
        logging.error(e)
        print("Error uploading file to S3")
        return False
    print("Finished uploading file to S3")
    return True


n = int(input("Enter the number of videos to download: "))
links = []

print("Enter the links one per line: ")
for i in range(0, n):
    temp = input()
    links.append(temp)

for i in range(0, n):
    link = links[i]
    yt = YouTube(link)
    title = yt.title + '.mp4'
    print('start', title)

    message = f"\nDetails for Video {i + 1}\nTitle: {title}\nLength: {yt.length} seconds"

    stream = str(yt.streams.filter(progressive=True))
    stream = stream[1:]
    stream = stream[:-1]

    l = yt.streams
    for j in l:
        print(j)

    tag = int(input("\nEnter the itag: "))
    ys = yt.streams.get_by_itag(tag)

    # Download file to local folder
    print("\nDownloading")
    ys.download('../yt-Videos/', filename=yt.title + '.mp4')
    print("\nDownload done")

    # Upload file to S3
    upload_file(title)
    upload_message = "Uploaded to S3: " + title
