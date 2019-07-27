import os
import requests
from github import Github
from flask import Flask
app = Flask(__name__)

GITHUB_API_TOKEN = os.environ.get('GIT_ORG_DASHBOARD_API_TOKEN')
print(GITHUB_API_TOKEN)

g = Github(GITHUB_API_TOKEN)

BASE_ORG_URL = "https://api.github.com/orgs/"


@app.route('/fetch_org/<org_name>')
def fetch_org(org_name):

    repos = []

    org = g.get_organization(org_name)
    for repo in org.get_repos():
        repos.append({'name': repo.name,
                      'stars_count': repo.stargazers_count,
                      'forks_count': repo.forks_count,
                      'contributors_count': repo.get_contributors().totalCount})
    return {'repos': repos}


@app.route('/org_to_id/<org_name>')
def org_name_to_id(org_name):
    headers = {'Authorization': 'token ' + GITHUB_API_TOKEN}
    res = requests.get(BASE_ORG_URL + org_name, headers=headers)

    if res.status_code == 404:
        return {'id': None}
    else:
        return {'id': str(res.json()['id'])}


if __name__ == "__main__":
    app.run(port=5001, debug=True)
