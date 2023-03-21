import requests

url = 'https://api.github.com/search/repositories?q=docker-compose.yaml+in:file'
response = requests.get(url)

if response.status_code == 200:
    results = response.json()['items']
    for result in results:
        print(result['full_name'])
else:
    print('Failed to retrieve data from GitHub API')