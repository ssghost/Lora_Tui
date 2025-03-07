from app import *
import subprocess
import os
import json
import requests
import asyncio

async def main():
    prompt = str(input("Enter the prompt:"))
    await subprocess.run(f"beam serve app.py:generate({prompt}) > output.txt", shell=True)

    with open("output.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[:4] == "curl":
                curl_command = line.strip()    
    os.remove("output.txt")

    image_json = await json.loads(subprocess.run(f"{curl_command}", capture_output=True, text=True).stdout)
    image_url = image_json["image"]
    image_data = await requests.get(image_url).content
    with open('image.jpg', 'wb') as handler:
        handler.write(image_data)

if __name__ == "__main__":
    asyncio.run(main)