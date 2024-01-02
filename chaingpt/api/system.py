# Standard lib
from typing import List
from dataclasses import dataclass

# 3rd party

# Local


@dataclass
class RunResult():
    return_code: str
    stdout: str
    stderr: str


class SystemEnvironment():
    def run(self, script: str, deps=List[str]):
        # TODO
        return RunResult(0, f"Some standard output with {', '.join(deps)}", "Some standard error")
