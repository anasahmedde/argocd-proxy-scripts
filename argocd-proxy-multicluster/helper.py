import json
from urllib.parse import urljoin
import requests
import settings


def get_rollout_version_helper(request, env, app_name, rollout_name):
    namespace = request.args['namespace']
    response = requests.get(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}/resource?namespace={namespace}&resourceName={rollout_name}&version=v1alpha1&kind=Rollout&group=argoproj.io',
        ),
        headers={'Authorization': request.headers['Authorization']},
    )
    response.raise_for_status()
    return json.loads(response.json()['manifest'])['spec']['template']['spec']['containers'][1]['image'].split(':')[1]


def get_rollout_status_helper(request, env, app_name, rollout_name):
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
    return rollout_status

def rollout_action_helper(request, env, app_name, rollout_name, action_name):
    namespace = request.json['namespace']
    response = requests.post(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}/resource/actions?appNamespace=argocd&namespace={namespace}&resourceName={rollout_name}&version=v1alpha1&kind=Rollout&group=argoproj.io',
        ),
        headers={
            'Authorization': request.headers['Authorization'],
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data=f'"{action_name}"',
    )
    print(response.json())
    response.raise_for_status()
    return response.json()

def application_sync_status_helper(request, env, app_name):
    response = requests.get(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}',
        ),
        headers={'Authorization': request.headers['Authorization']},
    )
    response.raise_for_status()
    return { "Phase": response.json()['status']['operationState']['phase'] }


def sync_application_helper(request, env, app_name):
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
    return response.json()['status']['sync']['status']

def delete_pod_resource_helper(request, env, app_name):
    namespace = request.json['namespace']
    pod_name = request.json['podName']
    # HTTP DELETE request 
    response = requests.delete(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}/resource?appNamespace=argocd&namespace={namespace}&resourceName={pod_name}&version=v1&kind=Pod&group=&force=true&orphan=false',
        ),
        headers={'Authorization': request.headers['Authorization']},
    )
    # Do not raise
    # response.raise_for_status()
    return response.json()

def rollback_sync_application_helper(request, env, app_name):
    # For rollback, just setting dryRun True to discourage the use of this endpoint
    payload = {'dryRun': True}
    payload['id'] = request.json.get('id')
    payload['appNamespace'] = "argocd"
    response = requests.post(
        urljoin(
            settings.ARGO_CD_URL_MAPPINGS[env],
            f'/api/v1/applications/{app_name}/rollback',
        ),
        headers={'Authorization': request.headers['Authorization']},
        json=payload,
    )
    return response.json()
