# Standard lib
from typing import List
import uuid
import os

# 3rd party
from sh import git

# Local
from llm import text_qa, text_qa_refine, LLMResponse


def _random_parent_dir(prefix: str="/tmp") -> str:
    """
    Generate a random parent directory for a workspace.
    """
    dir = "chaingpt" + str(uuid.uuid4())
    return os.path.join(prefix, dir)


def _validate_path_name(path: str):
    """
    Ensures `path` is properly formed and does
    not contain `..` or other attempts at directory
    traversal. 
    """
    # TODO
    

def _validate_git_url(url: str):
    """
    Ensures `url` is a properly formed GitHub repository URL.
    """
    # TODO
    pass


def _repo_name(url: str) -> str:
    """
    Returns the repo name.
    """
    repo = os.path.basename(url)
    if repo.endswith(".git"):
        repo = repo[-4:]
    return repo


class Workspace():
    def __init__(self, url: str):
        self.url = url
        self.parent_dir = _random_parent_dir()
        os.makedirs(self.parent_dir, exist_ok=False)
        self._clone(url)

    def _clone(self, url: str):
        """
        Clone the repository into the workspace parent directory.
        Sets `self.repo_dir`.
        """
        _validate_git_url(url)
        self.repo_dir = os.path.join(self.parent_dir, _repo_name(url))
        git.clone(url, self.repo_dir)

    def _read_n(self, n: int, file_path: str) -> str:
        """
        Reads `n` characters from `file_path`. The `file_path`
        is relative to the top-level directory of the repository.
        """
        full_path = os.path.append(self.repo_dir, file_path)
        with open(full_path, encoding="utf-8") as f:
            return f.read(n)

    def fileqa(self, question: str, file_path: str) -> LLMResponse:
        """
        Analyzes the contents of `file_path` to answer the `question` using an LLM.
        Files larger than 10000 characters are split into chunks and analyzed
        via a refine method. Files larger than 100000 are truncated to only the
        first 100000 characters.

        Args:
            question (str): The question to ask.
            file_path (str): The file to analyze. The path is relative to the
                             top-level directory of the repository.
        
        Returns:
            An `LLMResponse` containing the output from the LLM's analysis.
        
        Raises:
            FileNotFoundError: If the file does not exist.
        """
        # TODO: Feature that returns if the file was truncated.
        _validate_path_name(file_path)
        text = self._read_n(100000, file_path)
        if len(text) > 10000:
            return text_qa(question, text, file_path=file_path, chunk_size=10000)
        return text_qa_refine(question, text, file_path=file_path)

    def search(self, path: str) -> List[str]:
        # TODO
        return ["file1", "file2", "file3"]
