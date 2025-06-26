import os

def get_env_tag():
    return os.environ.get("ENV_TAG", "")

def ensure_output_dir():
    output_path = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path