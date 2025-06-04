from flask import Flask
from flask import jsonify
from flask import request
import helper

app = Flask(__name__)

def get_apps_list(app_name):
    return [f"{app_name}"]

###################################### multi-cluster operations ######################################


'''

# postman testing
http://127.0.0.1:5000/api/application/beta/ats-frontend-beta-nl/ats-frontend/version?namespace=beta-nl

'''


@app.route('/api/application/<env>/<app_name>/<rollout_name>/version')
def get_multi_cluster_rollout_version(env, app_name, rollout_name):
    appsList = get_apps_list(app_name)
    responsesList = []
    for app in appsList:
        responsesList.append(helper.get_rollout_version_helper(request, env, app, rollout_name))
    return jsonify({
        "responses": responsesList,
    })


'''

# postman testing
http://127.0.0.1:5000/api/application/beta/ats-frontend-beta-nl/ats-frontend/status

'''


@app.route('/api/application/<env>/<app_name>/<rollout_name>/status')
def get_multi_cluster_rollout_status(env, app_name, rollout_name):
    appsList = get_apps_list(app_name)
    responsesList = []
    for app in appsList:
        responsesList.append(helper.get_rollout_status_helper(request, env, app, rollout_name))
    return jsonify({
        "responses": responsesList,
    })


'''

# postman testing
http://127.0.0.1:5000/api/application/beta/ats-frontend-beta-nl/ats-frontend/resume

{
    "namespace": "beta-nl"
}

'''


@app.route('/api/application/<env>/<app_name>/<rollout_name>/resume', methods=['POST'])
def multi_cluster_rollout_resume(env, app_name, rollout_name):
    action_name = 'resume' # action can be abort, promote-full, restart, resume, retry
    appsList = get_apps_list(app_name)
    responsesList = []
    for app in appsList:
        responsesList.append(helper.rollout_action_helper(request, env, app, rollout_name, action_name))
    return jsonify({
        "responses": responsesList,
    })


'''

# postman testing
http://127.0.0.1:5000/api/application/beta/ats-frontend-beta-nl/ats-frontend/abort

{
    "namespace": "beta-nl"
}

'''


@app.route('/api/application/<env>/<app_name>/<rollout_name>/abort', methods=['POST'])
def multi_cluster_rollout_abort(env, app_name, rollout_name):
    action_name = 'abort' # action can be abort, promote-full, restart, resume, retry
    appsList = get_apps_list(app_name)
    responsesList = []
    for app in appsList:
        responsesList.append(helper.rollout_action_helper(request, env, app, rollout_name, action_name))
    return jsonify({
        "responses": responsesList,
    })


'''

# postman testing
http://127.0.0.1:5000/api/application/beta/ats-frontend-beta-nl/ats-frontend/retry

{
    "namespace": "beta-nl"
}

'''


@app.route('/api/application/<env>/<app_name>/<rollout_name>/retry', methods=['POST'])
def multi_cluster_rollout_retry(env, app_name, rollout_name):
    action_name = 'retry' # action can be abort, promote-full, restart, resume, retry
    appsList = get_apps_list(app_name)
    responsesList = []
    for app in appsList:
        responsesList.append(helper.rollout_action_helper(request, env, app, rollout_name, action_name))
    return jsonify({
        "responses": responsesList,
    })


'''

# postman testing
http://127.0.0.1:5000/api/application/beta/ats-frontend-beta-nl/ats-frontend/restart

{
    "namespace": "beta-nl"
}

'''


@app.route('/api/application/<env>/<app_name>/<rollout_name>/restart', methods=['POST'])
def multi_cluster_rollout_restart(env, app_name, rollout_name):
    action_name = 'restart' # action can be abort, promote-full, restart, resume, retry
    appsList = get_apps_list(app_name)
    responsesList = []
    for app in appsList:
        responsesList.append(helper.rollout_action_helper(request, env, app, rollout_name, action_name))
    return jsonify({
        "responses": responsesList,
    })


'''

# postman testing
http://127.0.0.1:5000/api/application/beta/ats-frontend-beta-nl/sync

'''


@app.route('/api/application/<env>/<app_name>/sync')
def multi_cluster_application_sync_status(env, app_name):
    appsList = get_apps_list(app_name)
    responsesList = []
    for app in appsList:
        responsesList.append(helper.application_sync_status_helper(request, env, app))
    return jsonify({
        "responses": responsesList,
    })


'''

# postman testing
http://127.0.0.1:5000/api/application/beta/ats-frontend-beta-nl/sync

# For syncing all resources.
{
"dryRun": false
}

# For syncing Argo-Rollout resources only when doing progressive delivery with autoPromotionEnabled flag set to false.
{
    "dryRun": false,
    "resources": [
        {
            "group": "argoproj.io",
            "kind": "Rollout",
            "name": "ats-frontend"
        }
    ]
}

'''


@app.route('/api/application/<env>/<app_name>/sync', methods=['POST'])
def sync_multi_cluster_application(env, app_name):
    appsList = get_apps_list(app_name)
    responsesList = []
    for app in appsList:
        responsesList.append(helper.sync_application_helper(request, env, app))
    return jsonify({
        "responses": responsesList,
    })


'''

# postman testing
http://127.0.0.1:5000/api/application/beta/ats-frontend-beta-nl/delete-pod

{
"namespace": "beta-nl",
"podName": "ats-frontend-5b96dd9945-5rjjf"
}

Note: CI_USER is part of dbz-dev role and therefore does not have capability to delete any resource.
https://github.com/dbz/helmfiles-ops/blob/main/values/cicd/argocd/config/policy.yaml#L23C1-L23C30

'''


@app.route('/api/application/<env>/<app_name>/delete-pod', methods=['POST'])
def delete_application_pod_resource(env, app_name):
    appsList = get_apps_list(app_name)
    responsesList = []
    for app in appsList:
        responsesList.append(helper.delete_pod_resource_helper(request, env, app))
    return jsonify({
        "responses": responsesList,
    })


'''

# postman testing
http://127.0.0.1:5000/api/application/beta/ats-frontend-beta-nl/rollback-sync

{
"id": 23
}

'''


@app.route('/api/application/<env>/<app_name>/rollback-sync', methods=['POST'])
def rollback_sync_multi_cluster_application(env, app_name):
    appsList = get_apps_list(app_name)
    responsesList = []
    for app in appsList:
        responsesList.append(helper.rollback_sync_application_helper(request, env, app))
    return jsonify({
        "responses": responsesList,
    })

if __name__ == "__main__":
    app.run(debug=True)
