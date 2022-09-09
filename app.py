import subprocess

subprocess.run("python3 ./src/chatbot/main.py & python3 ./src/data/data_ingest.py", shell=True)