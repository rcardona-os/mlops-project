from kfp import dsl, compiler
from kfp import kubernetes

# 1. Define the Step (Component)
@dsl.component(
    base_image="quay.io/opendatahub/workbench-images:runtime-datascience-ubi9-python-3.11"
)
def s3_test_step():
    import os
    
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    if access_key and secret_key:
        print("SUCCESS! Secure environment variables are loaded!")
        print(f"Access Key ID starts with: {access_key[:4]}...")
    else:
        print("FAILED: Secrets were not mounted.")

# 2. Define the Pipeline (This was the missing piece!)
@dsl.pipeline(
    name="enterprise-secure-s3-gitops",
    description="A pipeline showing secure S3 secret injection via GitOps"
)
def secure_s3_pipeline():
    task1 = s3_test_step()
    
    # Inject the secret
    kubernetes.use_secret_as_env(
        task=task1,
        secret_name='s3-data-lake-qwsd89',
        secret_key_to_env={
            'AWS_ACCESS_KEY_ID': 'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY': 'AWS_SECRET_ACCESS_KEY'
        }
    )

# 3. Compile the Blueprint
if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=secure_s3_pipeline,
        package_path='secure_pipeline.yaml'
    )
    print("Pipeline successfully compiled to: secure_pipeline.yaml")