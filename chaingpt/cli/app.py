# Standard lib
from typing import Dict, List, Any
import argparse

# 3rd party
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs.llm_result import LLMResult 
from langchain_core.agents import AgentAction

# Local
from chaingpt.cli.agent import ChainGPTAgent
from chaingpt.cli.display import display_tool_call, display_response


class ChainGPTAgentCallback(BaseCallbackHandler):
    # def on_llm_start(self,
    #     serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    # ) -> Any:
    #     print(prompts)
    
    # def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
    #     import pdb
    #     pdb.set_trace()
    #     display_response(response)
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        display_response(outputs["output"])
    
    # def on_tool_start(self,
    #     serialized: Dict[str, Any], input_str: str, **kwargs: Any
    # ) -> Any:
    #     import pdb
    #     pdb.set_trace()
    #     print(input_str)
    
    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        display_tool_call(tool_name=action.tool, tool_input=action.tool_input)
    
    # def on_tool_end(self, output: str, **kwargs: Any) -> Any:
    #     print(output)


class ChainGPTApp:
    def __init__(self, url: str):
        self.url = url
        self.agent = ChainGPTAgent(self.url)

    def chatloop(self):
        while True:
            prompt = input("> ")
            self.agent.prompt(prompt, ChainGPTAgentCallback())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The GitHub repository URL of interest")
    args = parser.parse_args()

    app = ChainGPTApp(args.url)
    app.chatloop()


if __name__ == "__main__":
    main()