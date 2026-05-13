from kfp import dsl, compiler
from kfp import kubernetes

# 1. Define the component
@dsl.component(
    base_image="quay.io/opendatahub/workbench-images:runtime-datascience-ubi9-python-3.11"
)
def s3_test_step():
    # Instantiate your step(s)
    task1 = data_extraction_step()
    
    # SECURITY MAGIC: Inject the OpenShift Secret directly into the pod at runtime!
    kubernetes.use_secret_as_env(
        task=task1,
        secret_name='s3-data-lake-qwsd89',
        secret_key_to_env={
            'AWS_ACCESS_KEY_ID': 'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY': 'AWS_SECRET_ACCESS_KEY'
        }
    )

# Compile the Python code into a Kubeflow YAML blueprint
if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=secure_s3_pipeline,
        package_path='secure_pipeline.yaml' 
    )
    print("Mas que tod : Blueprint compiled to: secure_pipeline.yaml")