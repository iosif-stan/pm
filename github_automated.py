import os 
import requests
import subprocess
import platform

# -------- USER CONFIG -----------
GITHUB_USERNAME = "iosif-stan"
GITHUB_TOKEN = "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"
REPO_NAME = os.path.basename(os.getcwd()) # The name of the current directory
# --------------------------------

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        print(result.stderr)
    return result.stdout.strip()

#Only call this for the first time
def repo_init(PRIVATE):
    # Initialize a new git repository
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"name": REPO_NAME, "private": PRIVATE}
    res = requests.post(url, headers=headers, json=data)

    if res.status_code == 201:
        repo_url = res.json()["clone_url"]

        run("git init")
        run(f"git remote add origin {repo_url}")
        run("git branch -M main")
        
        print("✅ Repository created successfully.")
    else:
        print("❌ Failed to create repository:", res.json())


# Pushes the current directory to GitHub
def commit_and_push():
    run("git add .")
    run('git commit -m "Automated commit"')
    run("git push origin main")
    
    print("✅ Changes pushed to GitHub.")

def pull():
    run("git pull origin main")
    print("✅ Changes pulled from GitHub.")


def main():
    if not os.path.exists(".git"):
        print("❌ Not a git repository. Initializing...")
        action = input("Do you want the repository to be private ? 'yes'/'no'").strip().lower()
        if action == "yes":
            PRIVATE = True
        elif action == "no":
            PRIVATE = False
        else:
            print("❌ Invalid input. Please enter 'yes' or 'no'.")
            return
        repo_init(PRIVATE)
    else:
        print("✅ Git repository found.")

    # Ask the user for the action to perform
    action = input("Enter 'push' to push changes or 'pull' to pull changes: ").strip().lower()
    if action == "push":
        commit_and_push()
    elif action == "pull":
        pull()
    else:
        print("❌ Invalid action. Please enter 'push' or 'pull'.")


if __name__ == "__main__":
    main()


    
    
    
