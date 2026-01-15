#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
import tempfile

REPO_URL = "https://github.com/dracohu2025-cloud/skills"

def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def sync_skill(skill_path):
    skill_path = os.path.abspath(skill_path)
    if not os.path.exists(skill_path):
        print(f"Error: Path {skill_path} does not exist.")
        sys.exit(1)

    skill_name = os.path.basename(skill_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Cloning repository to {temp_dir}...")
        run_command(["git", "clone", REPO_URL, "repo"], cwd=temp_dir)
        repo_path = os.path.join(temp_dir, "repo")

        target_path = os.path.join(repo_path, skill_name)
        if os.path.exists(target_path):
            print(f"Updating existing skill: {skill_name}")
            shutil.rmtree(target_path)
        else:
            print(f"Adding new skill: {skill_name}")

        shutil.copytree(skill_path, target_path)

        print("Committing and pushing changes...")
        run_command(["git", "add", "."], cwd=repo_path)

        # Check if there are changes to commit
        status = run_command(["git", "status", "--porcelain"], cwd=repo_path)
        if not status:
            print("No changes detected. Skipping commit.")
            return

        commit_msg = f"Sync skill: {skill_name}\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
        run_command(["git", "commit", "-m", commit_msg], cwd=repo_path)
        run_command(["git", "push", "origin", "main"], cwd=repo_path)
        print(f"Successfully synced {skill_name} to GitHub.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sync.py <path_to_skill>")
        sys.exit(1)

    sync_skill(sys.argv[1])
