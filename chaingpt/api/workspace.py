# Standard lib
from typing import List
from dataclasses import dataclass

# 3rd party

# Local


@dataclass
class LLMResponse():
    output: str
    model: str
    input_tokens: int
    output_tokens: int


class Workspace():
    def __init__(self, url: str):
        # TODO
        self.url = url

    def fileqa(self, question: str, file_path: str) -> LLMResponse:
        # TODO
        return LLMResponse(f"You asked a \"{question}\" about {file_path}", "gpt-4", 1000, 12)

    def search(self, path: str) -> List[str]:
        # TODO
        return ["file1", "file2", "file3"]
