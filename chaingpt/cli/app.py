# Standard lib
import argparse

# 3rd party

# Local
from chaingpt.cli.agent import ChainGPTAgent


class ChainGPTApp:
    def __init__(self, url: str):
        self.url = url
        self.agent = ChainGPTAgent(self.url)

    def chatloop(self):
        while True:
            prompt = input("> ")
            self.agent.prompt(prompt)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The GitHub repository URL of interest")
    args = parser.parse_args()

    app = ChainGPTApp(args.url)
    app.chatloop()


if __name__ == "__main__":
    main()