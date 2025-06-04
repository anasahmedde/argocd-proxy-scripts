import json
from urllib.parse import urljoin

from flask import Flask
from flask import jsonify
from flask import request
import requests
import settings

app = Flask(__name__)


def get_resource_manifest(app_name, namespace, rollout_name, env, auth):
    response = requests.get(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}/resource?namespace={namespace}&resourceName={rollout_name}&kind=Rollout&group=argoproj.io',
        ),
        headers={'Authorization': auth},
    )
    response.raise_for_status()
    return json.loads(response.json()['manifest'])

@app.route('/api/application/<env>/<app_name>/<rollout_name>/version')
def get_rollout_version(env, app_name, rollout_name):
    namespace = request.args['namespace']
    return jsonify({
        "response": get_resource_manifest(
            app_name=app_name,
            namespace=namespace,
            rollout_name=rollout_name,
            env=env,
            auth=request.headers['Authorization']
        )['spec']['template']['spec']['containers'][1]['image'].split(':')[1]
    })

@app.route('/api/application/<env>/<app_name>/<rollout_name>/status')
def get_rollout_status(env, app_name, rollout_name):
    response = requests.get(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}',
        ),
        headers={'Authorization': request.headers['Authorization']},
    )
    response.raise_for_status()
    rollout_status = {}
    for resource in response.json()['status']['resources']:
        if resource['name'] == rollout_name and resource['kind'] == 'Rollout' and 'health' in resource:
            rollout_status = resource['health']
    return jsonify({
        "response": rollout_status
    })

@app.route('/api/application/<env>/<app_name>/<rollout_name>/resume', methods=['POST'])
def resume_rollout(env, app_name, rollout_name):
    namespace = request.json['namespace']
    response = requests.post(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}/resource/actions?namespace={namespace}&resourceName={rollout_name}&kind=Rollout&group=argoproj.io',
        ),
        headers={
            'Authorization': request.headers['Authorization'],
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data='"resume"',
    )
    print(response.json())
    response.raise_for_status()
    return jsonify({
        "response": response.json()
    })

@app.route('/api/application/<env>/<app_name>/<rollout_name>/abort', methods=['POST'])
def abort_rollout(env, app_name, rollout_name):
    namespace = request.json['namespace']
    rollout_manifest = get_resource_manifest(
        app_name=app_name,
        rollout_name=rollout_name,
        namespace=namespace,
        auth=request.headers['Authorization'],
    )
    rollout_manifest['status'] = {
        "abort": True,
    }
    response = requests.post(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}/resource?namespace={namespace}&resourceName={rollout_name}&kind=Rollout&group=argoproj.io',
        ),
        headers={
            'Authorization': request.headers['Authorization'],
        },
        json={
            'manifest': rollout_manifest,
        },
    )
    print(response.json())
    response.raise_for_status()
    return jsonify({
        "response": response.json()
    })

@app.route('/api/application/<env>/<app_name>/sync')
def application_sync_status(env, app_name):
    response = requests.get(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}',
        ),
        headers={'Authorization': request.headers['Authorization']},
    )
    response.raise_for_status()
    return jsonify({
        "response": response.json()['status']['sync']['status']
    })

@app.route('/api/application/<env>/<app_name>/sync', methods=['POST'])
def sync_application(env, app_name):
    payload = {'dryRun': False}
    if request.json.get('resources'):
        payload['resources'] = request.json.get('resources')
    response = requests.post(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}/sync',
        ),
        headers={'Authorization': request.headers['Authorization']},
        json=payload,
    )
    response.raise_for_status()
    return jsonify({
        "response": response.json()['status']['sync']['status']
    })


if __name__ == "__main__":
    app.run(debug=True)
