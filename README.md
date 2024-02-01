# ChainGPT

### Overview
---
An LLM chatbot connected to your GitHub repository of choice. Use ChainGPT to explore directories, read files, execute shell code and more!

### Setup
---

1. Clone the repository
```
git clone https://github.com/paulgibert/chaingpt.git
```

2. Run `generate_config.sh` and specify your [OpenAI API key](https://platform.openai.com/docs/quickstart?context=python) and [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens). The API key is used to access GPT-4 and the token is used for GitHub's API.
```
cd chaingpt
./generate_config.sh
Your OpenAI API key: [OPENAI API KEY]
Your GitHub personal access token: [GITHUB PAT]
Configuration successfully generated at .../chaingpt/config.yaml
```

3. Install the package

Globally:
```
pip install .
```

Virtual Environment:
```
pip install venv
python -m venv env
source env/bin/activate
pip install .
```

### Usage
```
python -m chaingpt [GITHUB REPO]
```

### Example
```
python -m chaingpt https://github.com/anchore/grype.git
```
