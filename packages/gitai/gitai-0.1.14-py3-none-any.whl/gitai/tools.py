from langchain.tools import BaseTool, tool
from typing import Union, Dict, Tuple
import subprocess
import json
import os
import fnmatch


README_TEMPLATE = """
You are a software developer. You have made some changes to the codebase. Please review the provided files (including the current version of the README) and generate a comprehensive and updated README file. (Before running any tools, make sure to ask the user for permission to run them):
"""

README_CONTEXT_TEMPLATE = """

Project files:
{project_files}
"""

DETAILED_CONTEXT_TEMPLATE = """
Last few commit messages:
{last_commit_messages}

Files changed (summary):
{files_changed_summary}

Detailed diff of changes:
{detailed_diff}

Additional notes:
{additional_notes}
"""

def parse_gitignore(gitignore_path):
	"""Parse .gitignore and return a list of patterns to ignore."""
	ignore_patterns = []
	if os.path.exists(gitignore_path):
		with open(gitignore_path, 'r') as f:
			for line in f:
				stripped_line = line.strip()
				if stripped_line and not stripped_line.startswith('#'):
					ignore_patterns.append(stripped_line)
	return ignore_patterns

def should_ignore(path, ignore_patterns):
	"""Determine if the file should be ignored based on .gitignore patterns."""
	for pattern in ignore_patterns:
		if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
			return True
	return False

def generate_files_dict(start_path):
	"""Generate the dictionary of file paths and contents."""
	files_dict = {}
	files_under_source_control = subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.strip().split('\n')
	for file in files_under_source_control:
		try:
			with open(file, 'r') as f:
				files_dict[file] = f.read()
		except UnicodeDecodeError:
			pass
	return files_dict

def get_project_files():
	return json.dumps(generate_files_dict(os.getcwd()))

def get_last_commit_messages(n=3):
	return subprocess.run(['git', 'log', f'-{n}', '--pretty=%B'], capture_output=True, text=True).stdout.strip()

def get_files_changed_summary():
	return subprocess.run(['git', 'diff', '--cached', '--stat'], capture_output=True, text=True).stdout.strip()

def get_detailed_diff(cached=True):
	cmd = ['git', 'diff', '--cached'] if cached else ['git', 'diff']
	return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

def get_additional_notes():
	# Placeholder for any additional notes you might want to include for PRs
	return ""


class ReadmeDetailsTool(BaseTool):
	name = "Readme-Details-Tool"
	description = "Get detailed information to help you write a README.md."

	def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
		return (), {}

	def _run(self):
		project_files_content = README_CONTEXT_TEMPLATE.format(
			project_files=get_project_files(),
		)
		# replace curly braces with double curly braces to escape them
		project_files_content = project_files_content.replace("{", "{{").replace("}", "}}")
		readme_context = README_TEMPLATE + "\n\n" + project_files_content
		return readme_context
	
	async def _arun(self):
		return self._run()


class CommitDetailsTool(BaseTool):
	name = "Commit-Details-Tool"
	description = "Get detailed information to help you write a commit message."

	def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
		return (), {}

	def _run(self):
		cached = True
		additional_notes = ""
		last_commit_messages = get_last_commit_messages()
		files_changed_summary = get_files_changed_summary()
		detailed_diff = get_detailed_diff(cached)
		detailed_context = DETAILED_CONTEXT_TEMPLATE.format(
			last_commit_messages=last_commit_messages,
			files_changed_summary=files_changed_summary,
			detailed_diff=detailed_diff,
			additional_notes=additional_notes,
		)
		return detailed_context
	
	async def _arun(self):
		return self._run()


class PRDetailsTool(BaseTool):
	name = "PR-Details-Tool"
	description = "Get detailed information to help you write a pull request message."

	def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
		return (), {}

	def _run(self):
		cached = False
		additional_notes = get_additional_notes()
		last_commit_messages = get_last_commit_messages()
		files_changed_summary = get_files_changed_summary()
		detailed_diff = get_detailed_diff(cached)
		detailed_context = DETAILED_CONTEXT_TEMPLATE.format(
			last_commit_messages=last_commit_messages,
			files_changed_summary=files_changed_summary,
			detailed_diff=detailed_diff,
			additional_notes=additional_notes,
		)
		return detailed_context
	
	async def _arun(self):
		return self._run()


class CreateReadmeTool(BaseTool):
	name = "Create-Readme-Tool"
	description = "Create a README.md with the given message."

	def _run(self, message: str):
		with open('README.md', 'w') as f:
			f.write(message)
		return f"Created README with message: {message}"
	
	async def _arun(self, message: str):
		return self._run(message)

class CreatePRTool(BaseTool):
	name = "Create-PR-Tool"
	description = "Create a pull request with the given message."

	def _run(self, message: str):
		subprocess.run(['hub', 'pull-request', '-m', message])
		return f"Created PR with message: {message}"
	
	async def _arun(self, message: str):
		return self._run(message)


class CreateCommitTool(BaseTool):
	name = "Create-Commit-Tool"
	description = "Create a commit with the given message."

	def _run(self, message: str):
		subprocess.run(['git', 'add', '.'])
		subprocess.run(['git', 'commit', '-m', message])
		return f"Committed changes with message: {message}"
	
	async def _arun(self, message: str):
		return self._run(message)

class CreatePRTool(BaseTool):
	name = "Create-PR-Tool"
	description = "Create a pull request with the given message."

	def _run(self, message: str):
		subprocess.run(['hub', 'pull-request', '-m', message])
		return f"Created PR with message: {message}"
	
	async def _arun(self, message: str):
		return self._run(message)


@tool
def get_details_for_commit_message() -> str:
	"""Get detailed information to help you write a commit message."""
	cached = True
	additional_notes = ""
	last_commit_messages = get_last_commit_messages()
	files_changed_summary = get_files_changed_summary()
	detailed_diff = get_detailed_diff(cached)
	detailed_context = DETAILED_CONTEXT_TEMPLATE.format(
    	last_commit_messages=last_commit_messages,
    	files_changed_summary=files_changed_summary,
    	detailed_diff=detailed_diff,
		additional_notes=additional_notes,
    )
	return detailed_context


@tool
def get_details_for_pr_message() -> str:
	"""Get detailed information to help you write a pull request message."""
	cached = False
	additional_notes = get_additional_notes()
	last_commit_messages = get_last_commit_messages()
	files_changed_summary = get_files_changed_summary()
	detailed_diff = get_detailed_diff(cached)
	detailed_context = DETAILED_CONTEXT_TEMPLATE.format(
		last_commit_messages=last_commit_messages,
		files_changed_summary=files_changed_summary,
		detailed_diff=detailed_diff,
		additional_notes=additional_notes,
	)
	return detailed_context


@tool
def create_commit(message: str) -> str:
	"""Create a commit with the given message."""
	subprocess.run(['git', 'add', '.'])
	subprocess.run(['git', 'commit', '-m', message])
	return f"Committed changes with message: {message}"

@tool
def create_pr(message: str) -> str:
	"""Create a pull request with the given message."""
	subprocess.run(['hub', 'pull-request', '-m', message])
	return f"Created PR with message: {message}"