import requests
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/org/<org_name>')
def fetch_org(org_name):
    org_id = requests.get('http://localhost:5001/org_to_id/' + org_name).json()['id']

    # if org does not exist return immediately
    if org_id is None:
        return 'The organization name - {} - is not valid'.format(org_name)
    # otherwise check if id exists in db
    else:
        print('checking db for org {} with id {}...'.format(org_name, org_id))
        repos_req = requests.get('http://localhost:5002/' + org_id)
        repos = repos_req.json()['repos']

        # if org_id not in db, fetch it
        if repos is None:
            # fetch repository data from github
            print('fetching data from github...')
            repos_list = requests.get('http://localhost:5001/fetch_org/' + org_name).json()['repos']

            # add the data to the db
            print('inserting data into db...')
            resp = requests.post('http://localhost:5002/' + org_id, json={'repos': repos_list})
            print(resp)
            repos_req = requests.get('http://localhost:5002/' + org_id)
            repos = repos_req.json()['repos']
        else:
            print('found org {} with id {} in db...'.format(org_name, org_id))
        sorted_repos = (sort_repos(repos))
        return render_template('repos.html',
                               stars=sorted_repos['stars'],
                               forks=sorted_repos['forks'],
                               contributors=sorted_repos['contributors'])


def sort_repos(repos):
    # example: {'contributors_count': 1, 'forks_count': 0, 'name': 'mantis-ui', 'stars_count': 2}
    res = {
        'stars': [],
        'forks': [],
        'contributors': []
    }

    for repo in repos:
        res['stars'].append((repo['name'], repo['stars_count']))
        res['forks'].append((repo['name'], repo['forks_count']))
        res['contributors'].append((repo['name'], repo['contributors_count']))

    res['stars'].sort(key=lambda x: x[1], reverse=True)
    res['forks'].sort(key=lambda x: x[1], reverse=True)
    res['contributors'].sort(key=lambda x: x[1], reverse=True)

    return res


if __name__ == "__main__":
    app.run(port=5000, debug=True)
