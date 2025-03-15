import subprocess
import time
import signal
import os
import json
import requests
import asyncio

prompt = ""

def set_prompt() -> None:
    global prompt
    prompt = str(input("Enter the prompt:"))

def get_prompt() -> str:
    return prompt

async def main():
    set_prompt()
    proc = subprocess.Popen(["./.venv/lib/python3.13/site-packages/beam", "serve", "app.py:generate"], start_new_session=True, stdout=open("output.txt", 'w'))
    time.sleep(100)

    curl_command = ""
    with open("output.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[:4] == "curl":
                curl_command += line.strip()    

    proc_curl = await asyncio.create_subprocess_shell(
            curl_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    stdout, _ = await proc_curl.communicate()
    await proc_curl.wait()

    image_json = json.loads(stdout.decode())
    image_url = image_json["image"]
    image_data = await requests.get(image_url).content
    with open("image.jpg", 'wb') as handler:
        handler.write(image_data)
    if os.path.isfile("image.jpg"):
        print("Generated image downloaded at ./image.jpg.")
    
    os.remove("output.txt")
    os.killpg(os.getpgid(proc), signal.SIGTERM)

if __name__ == "__main__":
    asyncio.run(main())