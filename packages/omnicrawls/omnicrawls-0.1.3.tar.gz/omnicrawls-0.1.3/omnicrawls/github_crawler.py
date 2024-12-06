import os
import tempfile
import git

class GithubCrawler:
    @staticmethod
    def extract(repo_url):
        contents = {}  # Dictionary to store file contents
        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                # Clone the repo to a temporary directory
                git.Repo.clone_from(repo_url, tmp_dir, branch='main', depth=1)
            except Exception as e:
                return {"error": f"Error cloning repository: {e}"}

            # Traverse the cloned repository directory
            for root, dirs, files in os.walk(tmp_dir):
                # Skip hidden directories (like .git)
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    file_path = os.path.join(root, file)

                    try:
                        # Read and store file content (only text-based files)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            contents[file] = content[:500]  # Store first 500 characters
                    except Exception as e:
                        contents[file] = f"Error reading {file}: {e}"

        return contents

