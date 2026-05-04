import os
import urllib3
from kfp.client import Client

# Mute the lab's self-signed certificate warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. Grab credentials from GitHub Actions securely
token = os.environ.get('OPENSHIFT_TOKEN')
host_url = os.environ.get('OPENSHIFT_URL')

if not token or not host_url:
    raise ValueError("Missing OpenShift credentials in environment variables!")

# 2. Authenticate
client = Client(
    host=host_url,
    existing_token=token,
    verify_ssl=False
)

# 3. Upload the compiled YAML
client.upload_pipeline(
    pipeline_package_path='secure_pipeline.yaml',
    pipeline_name='enterprise-secure-s3-gitops',
    description='Automatically deployed via GitHub Actions!'
)

print("GitOps Deployment Successful!")