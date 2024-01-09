# Standard lib
from typing import Iterator

# 3rd party
from langchain.chat_models import ChatOpenAI
from langchain.agents.initialize import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

# Local
from chaingpt.api.workspace import Workspace
from chaingpt.api.wolfi import WolfiClient
from chaingpt.api.system import SystemEnvironment
from chaingpt.api.llm import LLMResponse
from chaingpt.cli.tools import get_tools
from chaingpt.utils import config


# TODO: Add configs for adjusting fields such as chunk size and chunk overlap
LLM_MODEL = config.config["llm"]["agent_model"]


class ChainGPTAgent:
    def __init__(self, url: str):
        self.url = url
        self._init_agent()

    def _init_agent(self):
        def callback(output: str):
            print(output, end="")

        tools = get_tools(self.url, callback)
        llm = ChatOpenAI(temperature=0, model=LLM_MODEL)
        agent_kwargs = {
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
        }

        memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

        context = f"""
        As an AI expert and extremely intelligent engineering assistant focusing on the {self.url} GitHub repository,
        your key role is to engage with engineers, offering precise and reliable
        information about repository-related issues. You are equipped with specialized
        tools for searching file names, reading files, and executing shell scripts. Your responses should be concise yet thorough,
        backed by diligent verification using these tools. You are expected to research exhaustively
        and consider multiple perspectives before finalizing an answer, demonstrating your commitment
        to accuracy and detail in engineering problem-solving. 
        """

        self.agent = initialize_agent(
            tools, llm, agent=AgentType.OPENAI_FUNCTIONS,
            agent_kwargs=agent_kwargs,
            memory=memory, context_prompt=context,
            verbose=True
        )

    def prompt(self, msg: str) -> Iterator[LLMResponse]:
        output = self.agent.run(msg)
