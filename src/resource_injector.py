from flask import Flask, request, jsonify
from kubernetes.client import AdmissionReview
import os
import json
import base64
import logging
from prometheus_client import start_http_server, Counter

# Initialize Flask app
app = Flask(__name__)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("resource-injector")

# Prometheus metrics
REQUEST_COUNT = Counter('admission_requests_total', 'Total number of admission review requests')
MUTATED_COUNT = Counter('mutated_requests_total', 'Total number of mutated requests')

# Default resource values (can be overridden via environment variables)
DEFAULT_CPU_REQUEST = os.getenv("DEFAULT_CPU_REQUEST", "500m")
DEFAULT_MEMORY_REQUEST = os.getenv("DEFAULT_MEMORY_REQUEST", "512Mi")
DEFAULT_CPU_LIMIT = os.getenv("DEFAULT_CPU_LIMIT", "1000m")
DEFAULT_MEMORY_LIMIT = os.getenv("DEFAULT_MEMORY_LIMIT", "1Gi")

@app.route('/mutate', methods=['POST'])
def mutate():
    REQUEST_COUNT.inc()
    try:
        # Parse the admission review request
        request_data = request.get_json()
        admission_review = request_data.get('request', {})
        uid = admission_review.get('uid')
        pod_spec = admission_review.get('object', {}).get('spec', {})
        mutated = False

        # Iterate through containers to check and inject resource requirements
        containers = pod_spec.get('containers', [])
        patches = []

        for i, container in enumerate(containers):
            container_patch = {}
            if 'resources' not in container:
                container_patch['resources'] = {}

            if not container.get('resources', {}).get('requests'):
                container_patch.setdefault('resources', {}).update({
                    'requests': {
                        'cpu': DEFAULT_CPU_REQUEST,
                        'memory': DEFAULT_MEMORY_REQUEST
                    }
                })
                mutated = True

            if not container.get('resources', {}).get('limits'):
                container_patch.setdefault('resources', {}).update({
                    'limits': {
                        'cpu': DEFAULT_CPU_LIMIT,
                        'memory': DEFAULT_MEMORY_LIMIT
                    }
                })
                mutated = True

            if container_patch:
                patches.append({"op": "add", "path": f"/spec/containers/{i}/resources", "value": container_patch['resources']})

        if mutated:
            MUTATED_COUNT.inc()
            patch_base64 = base64.b64encode(json.dumps(patches).encode()).decode()
            return jsonify({
                'response': {
                    'uid': uid,
                    'allowed': True,
                    'patchType': 'JSONPatch',
                    'patch': patch_base64
                }
            })
        else:
            return jsonify({
                'response': {
                    'uid': uid,
                    'allowed': True
                }
            })

    except Exception as e:
        logger.error(f"Error processing admission review: {e}")
        return jsonify({
            'response': {
                'uid': None,
                'allowed': False,
                'status': {
                    'message': str(e)
                }
            }
        })

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(9000)
    logger.info("Starting Resource Injector Webhook on port 8443")
    app.run(host='0.0.0.0', port=8443, ssl_context=None)  # Remove SSL context for now
