import json
from pymongo import MongoClient
from flask import Flask, request, jsonify
app = Flask(__name__)

client = MongoClient()

db = client.git_orgs

orgs = db.orgs


@app.route('/<org_id>', methods=['GET'])
def find_org(org_id):
    res = orgs.find_one({'org_id': org_id})
    print(res)
    if res is None:
        return {'repos': None}
    else:
        return {'repos': res['repos']}


@app.route('/<org_id>', methods=['POST'])
def insert_org(org_id):
    repos = json.loads(request.data)['repos']
    orgs.insert_one({'org_id': org_id, 'repos': repos})
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(port=5002, debug=True)
