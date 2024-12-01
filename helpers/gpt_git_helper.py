from git import Repo
import os
import openai

# OpenAI GPT setup
openai.api_key = "your_openai_api_key"

# Clone or access a Git repository
def clone_repo(repo_url, local_path="./repo"):
    if os.path.exists(local_path):
        repo = Repo(local_path)
    else:
        repo = Repo.clone_from(repo_url, local_path)
    return repo

# List all files in the repository
def list_repo_files(local_path="./repo"):
    files = []
    for root, _, filenames in os.walk(local_path):
        for filename in filenames:
            files.append(os.path.relpath(os.path.join(root, filename), local_path))
    return files

# Summarize a file in the repository
def summarize_repo_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    prompt = f"Summarize the following file:\n\n{content}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()