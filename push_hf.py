"""
Push EmailOps-Env to Hugging Face Spaces.
Handles Windows encoding issues gracefully.
"""
import os
import sys

# Fix encoding for Windows
os.environ["PYTHONIOENCODING"] = "utf-8"

from huggingface_hub import HfApi

def push_to_space():
    api = HfApi()
    username = api.whoami()["name"]
    repo_name = "emailops-env"
    repo_id = f"{username}/{repo_name}"

    print(f"Creating Space: {repo_id}...")
    try:
        api.create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="docker",
            private=False,
            exist_ok=True
        )
        print(f"  Space ready: https://huggingface.co/spaces/{repo_id}")
    except Exception as e:
        print(f"  Space creation note: {e}")

    print(f"Uploading files from {os.getcwd()}...")

    # Exclude unnecessary files - keep only what's needed for the Docker build
    ignore_patterns = [
        # Python cache
        "*.pyc", "__pycache__/**", "*.egg-info/**",
        # Git
        ".git/**", ".gitignore",
        # Dev/debug files
        "*.log", "demo_output.txt", "val.txt", "pushout.txt", "foo.txt", "pusherr*.txt", "pushhelp.txt",
        # Temp/push scripts
        "push_hf.py", "demo.py",
        # Outputs
        "outputs/**",
        # Lock files
        "uv.lock",
        # Root-level re-exports (not needed, package has its own)
        "client.py", "models.py", "__init__.py",
        # Extra server directory (duplicate entry point)
        "server/**",
    ]

    try:
        response = api.upload_folder(
            folder_path=".",
            repo_id=repo_id,
            repo_type="space",
            ignore_patterns=ignore_patterns,
            commit_message="Deploy EmailOps-Env OpenEnv environment"
        )
        print(f"\n✅ Successfully deployed!")
        print(f"   View your space: https://huggingface.co/spaces/{repo_id}")
        print(f"   API endpoint:    https://{username}-{repo_name}.hf.space")
    except Exception as e:
        print(f"\n❌ Upload failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    push_to_space()
