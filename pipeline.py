@dsl.pipeline(
name="enterprise-secure-s3-pipeline",
description="A production-ready pipeline using injected Kubernetes Secrets"
)
def secure_s3_pipeline():
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
    print("Mas que nada : Blueprint compiled to: secure_pipeline.yaml")