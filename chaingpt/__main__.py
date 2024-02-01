# Standard lib
import os

# Local
from chaingpt.utils import config






if __name__ == "__main__":
    # Environmental variable must be set before app is imported
    os.environ["OPENAI_API_KEY"] = config.config["secrets"]["openai_api_key"]

    import chaingpt.cli.app as app
    app.main()
