"""
GitHub Plugin for Semantic Kernel
Provides functions to interact with GitHub repositories
"""

from semantic_kernel.functions import kernel_function
from operations.github_operations import GitHubOperations

github_operations = GitHubOperations()


class GitHubPlugin:
    """
    A plugin for interacting with GitHub repositories.
    Provides functions to list repositories, browse files, get file content, and create issues.
    """

    @kernel_function(
        name="get_repos_by_user",
        description="Get a list of repositories from a GitHub user account. Use this when you need to see what repositories a user has."
    )
    def get_repos_by_user(self, user: str) -> str:
        """
        Get a list of repositories for a given GitHub user.
        
        Args:
            user: The GitHub username to get repositories for
            
        Returns:
            A string representation of the list of repositories
        """
        try:
            repos = github_operations.get_repo_list_by_username(user)
            if repos:
                return f"Found {len(repos)} repositories for user '{user}':\n" + "\n".join(f"- {repo}" for repo in repos)
            else:
                return f"No repositories found for user '{user}'"
        except Exception as e:
            return f"Error getting repositories for user '{user}': {str(e)}"

    @kernel_function(
        name="get_files_by_repo",
        description="Get a list of files in a GitHub repository. The repository should be in the format 'username/repo_name'. Use this before getting file content to see what files are available."
    )
    def get_files_by_repo(self, repo: str) -> str:
        """
        Get a list of all files in a GitHub repository.
        
        Args:
            repo: The repository in format 'username/repo_name'
            
        Returns:
            A string representation of the list of files
        """
        try:
            files = github_operations.get_file_list_by_repo(repo)
            if files:
                return f"Found {len(files)} files in repository '{repo}':\n" + "\n".join(f"- {file}" for file in files)
            else:
                return f"No files found in repository '{repo}'"
        except Exception as e:
            return f"Error getting files for repository '{repo}': {str(e)}"

    @kernel_function(
        name="get_file_content",
        description="Get the content of a specific file from a GitHub repository. The repository should be in the format 'username/repo_name' and path should be the file path within the repository."
    )
    def get_file_content(self, repo: str, path: str) -> str:
        """
        Get the content of a specific file from a GitHub repository.
        
        Args:
            repo: The repository in format 'username/repo_name'
            path: The file path within the repository
            
        Returns:
            The file content as a string
        """
        try:
            content = github_operations.get_file_content_by_repo_and_path(repo, path)
            if content:
                return f"Content of file '{path}' from repository '{repo}':\n\n{content}"
            else:
                return f"File '{path}' not found in repository '{repo}'"
        except Exception as e:
            return f"Error getting file content for '{path}' in repository '{repo}': {str(e)}"

    @kernel_function(
        name="create_issue",
        description="Create a new issue in a GitHub repository. The repository should be in the format 'username/repo_name'. Use this to report bugs or request features."
    )
    def create_issue(self, repo: str, title: str, body: str) -> str:
        """
        Create a new issue in a GitHub repository.
        
        Args:
            repo: The repository in format 'username/repo_name'
            title: The issue title
            body: The issue description/body
            
        Returns:
            A message indicating success or failure with the issue URL
        """
        try:
            result = github_operations.create_issue(repo, title, body)
            return result
        except Exception as e:
            return f"Error creating issue in repository '{repo}': {str(e)}"
