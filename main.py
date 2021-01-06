import requests
import json
from dotenv import load_dotenv
import os
from pathlib import Path
import sys


def createRepo(api, name, private=False, auto_init=True):

    url = 'https://api.github.com/user/repos'

    headers = {
        'Authorization': 'token ' + api,
        'Accept': 'application/vnd.github.v3 json'
    }

    data = {
        'name': name,
        'private': private,
        'auto_init': auto_init,
    }
    data = json.dumps(data, indent=4)

    response = requests.post(url, headers=headers, data=data)
    return json.loads(response.text)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f'usage: {sys.argv[0]} <repo name>')
        exit(1)

    load_dotenv()
    api_key = os.getenv('API_KEY')
    projectPath = Path(os.getenv('PROJECT_PATH'))
    editor = os.getenv('DEFAULT_EDITOR')

    repoName = sys.argv[1]
    response = createRepo(api_key, repoName)
    ssh_url = response['ssh_url']

    os.system(f'git clone {ssh_url} {projectPath/repoName}')
    os.system(f'{editor} {projectPath/repoName}')
