## gitai

gitai is a CLI tool to have an LLM write commit messages and PR descriptions for you.

### Installation
```bash
pip install gitai
```

#### Development
```bash
git clone
cd gitai
conda env create -f environment.yml
conda activate gitai
```

### Usage
```bash
gitai
```

---

### Project Files

#### Environment Configuration
```yaml
name: gitai
channels:
  - defaults
dependencies:
  - bzip2=1.0.8=h80987f9_5
  - ca-certificates=2024.3.11=hca03da5_0
  - libffi=3.4.4=hca03da5_0
  - ncurses=6.4=h313beb8_0
  - openssl=3.0.13=h1a28f6b_0
  - ...
  - yarl==1.9.4
prefix: /Users/browna18/miniconda3/envs/gitai
```

#### Tools
- **CommitDetailsTool**
  - Get detailed information to help you write a commit message.
- **PRDetailsTool**
  - Get detailed information to help you write a pull request message.
- **CreateCommitTool**
  - Create a commit with the given message.
- **CreatePRTool**
  - Create a pull request with the given message.

#### Main Files
- **agent.py**
  - Contains code for agent execution and interaction.
- **main.py**
  - Main script for running different modes: commit, PR, or README generation.
- **tools.py**
  - Contains tool implementations for commit, PR, and detailed context retrieval.
- **README.md**
  - README file with installation and usage instructions.

---

### Instructions

- To run the tool, execute `gitai`.
- For specific modes:
  - For commit message: `python main.py --mode commit`
  - For PR message: `python main.py --mode pr`
  - For README generation: `python main.py --mode readme`

Before running any tools, ensure to ask the user for permission.

Feel free to explore the codebase and make use of the provided tools for managing commit messages and PR descriptions efficiently.