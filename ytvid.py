from pytube import YouTube
import requests
import json
import boto3
from botocore.exceptions import ClientError


def upload_file(title):
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        # pattern = re.compile(r"[A-Za-z0-9]+(-[A-Za-z0-9]+)*")
        # title = pattern.search(title.replace(' ', '-')).string
        print("1234567", title + '.mp4')

        s3_client.upload_file(title + '.mp4', "yt-vid-bucket", title + '.mp4')
    except ClientError as e:
        logging.error(e)
        print("Error uploading file to S3")
        return False
    print("Finished uploading file to S3")
    return True


web_hook_url = 'https://hooks.slack.com/services/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'

n = int(input("Enter the number of youtube videos to download:   "))

links = []

slack_msg = {'text': 'Enter all the links one per line:'}
requests.post(web_hook_url, data=json.dumps(slack_msg))
print("\nEnter all the links one per line:")

for i in range(0, n):
    temp = input()
    links.append(temp)

for i in range(0, n):
    link = links[i]
    yt = YouTube(link)
    print("\nDetails for Video", i + 1, "\n")
    print("Title of video:   ", yt.title)
    print("Number of views:  ", yt.views)
    print("Length of video:  ", yt.length, "seconds")

    stream = str(yt.streams.filter(progressive=True))
    stream = stream[1:]
    stream = stream[:-1]
    streamlist = stream.split(", ")
    print("\nAll available options for downloads:\n")

    for i in range(0, len(streamlist)):
        st = streamlist[i].split(" ")
        print(i + 1, ") ", st[1], " and ", st[3], sep='')

    l = yt.streams
    for i in l:
        print(i)
    tag = int(input("\nEnter the itag of your preferred stream to download:   "))
    ys = yt.streams.get_by_itag(tag)
    print("\nDownloading...")
    ys.download('./', filename=yt.title + '.mp4')
    print("\nDownload completed!!")
    print()

upload_file(yt.title)
