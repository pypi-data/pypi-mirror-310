import os
import shlex
import subprocess
import json
import click
import fnmatch
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
import tiktoken
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveJsonSplitter, CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.chains import RefineDocumentsChain, LLMChain
from langchain_core.prompts import PromptTemplate
import sys
from datetime import datetime
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Union
import time

load_dotenv()

MAX_COMPLETION_TOKENS = 16384
MAX_TOTAL_TOKENS = 128000
BUFFER_TOKENS = 1000

COMMIT_MESSAGE_TEMPLATE = """
You are a software developer. You have made some changes to the codebase. Please provide a commit message for the following changes (Before running any tools, make sure to ask the user for permission to run them):
"""

COMMIT_MESSAGE_TEMPLATE_SHORT = """
You are a software developer. You have made some changes to the codebase. Please provide a commit message for the following changes (Keep it short and concise):
"""

PR_MESSAGE_TEMPLATE = """
You are a software developer. You have made some changes to the codebase and are preparing to merge them into the main branch. Please provide a detailed pull request message for the following changes (Before running any tools, make sure to ask the user for permission to run them):
"""

PR_MESSAGE_TEMPLATE_SHORT = """
You are a software developer. You have made some changes to the codebase and are preparing to merge them into the main branch. Please provide a detailed pull request message for the following changes (Keep it short and concise):
"""

README_TEMPLATE = """
You are a software developer. You have made some changes to the codebase. Please review the provided files (including the current version of the README) and generate a comprehensive and updated README file. (Before running any tools, make sure to ask the user for permission to run them):
"""

README_TEMPLATE_SHORT = """
You are a software developer. You have made some changes to the codebase. Please review the provided files (including the current version of the README) and generate a comprehensive and updated README file. (Keep it short and concise):
"""

README_CONTEXT_TEMPLATE = """

Project files:
{project_files}
"""

DESCRIBE_TEMPLATE = """
You are an assistant who specializes synthesis and summarization. Please review the provided files and top-level folder structure and generate a description of the contents/purpose of the folder. (Before running any tools, make sure to ask the user for permission to run them) **Only respond with the description, and if there is not enough context, respond with "N/A"**:
"""

DESCRIBE_TEMPLATE_SHORT = """
You are an assistant who specializes synthesis and summarization. Please review the provided files and top-level folder structure and generate a description of the contents/purpose of the folder. (Keep it short and concise)  **Only respond with the description, and if there is not enough context, respond with "N/A"**:
"""

DESCRIBE_CONTEXT_TEMPLATE = """

Project files:
{project_files}

Top-level folder structure:
{top_level_structure}
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

COMMIT_DETAILED_CONTEXT_TEMPLATE = """
Files changed (summary):
{files_changed_summary}

Detailed diff of changes:
{detailed_diff}

Additional notes:
{additional_notes}
"""

def list_top_level(path):
    top_level_items = []
    items = os.listdir(path)
    for item in items:
        full_path = os.path.join(path, item)
        if os.path.isfile(full_path):
            top_level_items.append(full_path)
        elif os.path.isdir(full_path):
            top_level_items.append(full_path + '/')
    return top_level_items

def get_filtered_file_paths(base_path='.'):
    """Get all text files that are under git source control."""
    try:
        cmd = "git -C {} rev-parse --is-inside-work-tree".format(base_path)
        is_git_repo = subprocess.run(shlex.split(cmd), capture_output=True, text=True).stdout.strip()
        if is_git_repo != 'true':
            cmd = 'find {} -type f -maxdepth 1'.format(base_path)
        else:
            # Use git ls-files to get all tracked files
            cmd = 'git -C {} ls-files'.format(base_path)

        files = subprocess.run(shlex.split(cmd), capture_output=True, text=True).stdout.strip().split('\n')
        
        # Filter for text files
        text_files = []
        for file in files:
            if os.path.isfile(file):  # Check if file exists
                try:
                    # Use 'file' command to check if it's a text file
                    file_type = subprocess.run(['file', file], capture_output=True, text=True).stdout
                    if 'text' in file_type.lower() or 'ASCII' in file_type:
                        text_files.append(file)
                except Exception as e:
                    print(f"Warning: Error checking file type for {file}: {e}")
                    continue
        
        return text_files
    except Exception as e:
        print(f"Error getting filtered file paths: {e}")
        return []

def parse_gitignore(gitignore_path='.gitignore'):
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

def generate_files_dict(files):
    """Generate the dictionary of file paths and contents."""
    files_dict = {}
    for file in files:
        try:
            if os.path.isfile(file):  # Check if file exists
                with open(file, 'r', encoding='utf-8') as f:
                    files_dict[file] = f.read()
        except Exception as e:
            print(f"Warning: Could not read {file}: {e}")
            continue
    return files_dict

def get_project_files(files):
    """Get the content of project files as JSON string."""
    return json.dumps(generate_files_dict(files))

def get_last_commit_messages(n=3, base_path='.'):
    """Get the last n commit messages."""
    try:
        result = subprocess.run(
            ['git', '-C', base_path, 'log', f'-{n}', '--pretty=%B'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Warning: Error getting commit messages: {e}")
        return ""

def get_files_changed_summary(base_path='.'):
    """Get a summary of changed files."""
    try:
        result = subprocess.run(
            ['git', '-C', base_path, 'diff', '--cached', '--stat'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Warning: Error getting files changed summary: {e}")
        return ""

def get_diff_stat(base_path='.'):
    """Get diff statistics."""
    try:
        result = subprocess.run(
            ['git', '-C', base_path, 'diff', 'origin', '--stat'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Warning: Error getting diff stat: {e}")
        return ""

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def truncate_text_to_token_limit(text: str, max_tokens: int = 100000, encoding_name: str = "cl100k_base") -> str:
    """Truncates text to stay within token limit while preserving the most recent content."""
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    
    if len(tokens) <= max_tokens:
        return text
        
    # Keep the most recent content by truncating from the start
    truncated_tokens = tokens[-max_tokens:]
    return encoding.decode(truncated_tokens)

def get_detailed_diff(cached=True, max_tokens=100000, base_path='.'):
    """Get detailed diff with token limit handling."""
    cmd = ['git', '-C', base_path, 'diff', '--cached'] if cached else ['git', '-C', base_path, 'diff', 'origin']
    try:
        diff_text = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
        return truncate_text_to_token_limit(diff_text, max_tokens)
    except subprocess.CalledProcessError as e:
        print(f"Warning: Error getting detailed diff: {e}")
        return ""

def get_detailed_diff_of_files(files, max_tokens=100000, base_path='.'):
    """Get detailed diff of specific files with token limit handling."""
    try:
        diff_text = subprocess.run(
            ['git', '-C', base_path, 'diff', '--', *files],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        return truncate_text_to_token_limit(diff_text, max_tokens)
    except subprocess.CalledProcessError as e:
        print(f"Warning: Error getting detailed diff of files: {e}")
        return ""

def get_split_text_as_docs(text, max_chunk_size=80000):
    """Split text into smaller chunks to avoid token limits."""
    # First create a smaller chunk size to account for potential overhead
    adjusted_chunk_size = int(max_chunk_size * 0.8)  # 20% buffer
    
    # Create text splitter with smaller chunk size
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=adjusted_chunk_size,
        chunk_overlap=0,  # Reduce overlap to save tokens
        length_function=num_tokens_from_string,
        add_start_index=True
    )
    
    # Split into documents
    try:
        docs = text_splitter.create_documents([text])
        
        # Verify chunk sizes
        for doc in docs:
            tokens = num_tokens_from_string(doc.page_content)
            if tokens > max_chunk_size:
                print(f"Warning: Chunk size {tokens} exceeds maximum {max_chunk_size}")
                # Further split this chunk if needed
                smaller_docs = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                    encoding_name="cl100k_base",
                    chunk_size=int(adjusted_chunk_size * 0.5),  # Even smaller chunks
                    chunk_overlap=0,
                    length_function=num_tokens_from_string
                ).split_documents([doc])
                # Replace the large doc with smaller ones
                docs.remove(doc)
                docs.extend(smaller_docs)
        
        return docs
    except Exception as e:
        print(f"Error splitting text: {e}")
        # Fall back to aggressive splitting if needed
        emergency_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base",
            chunk_size=int(max_chunk_size * 0.4),  # Very conservative size
            chunk_overlap=0,
            length_function=num_tokens_from_string
        )
        return emergency_splitter.create_documents([text])

class TokenLimitExceededError(Exception):
    """Custom exception for token limit exceeded errors."""
    pass

def get_llm(llm, max_tokens=MAX_COMPLETION_TOKENS):
    """Initialize LLM with appropriate token limits."""
    if llm == 'openai':
        return ChatOpenAI(
            model="gpt-4o",
            max_tokens=min(max_tokens, MAX_COMPLETION_TOKENS),  # Ensure we don't exceed model limits
            temperature=0.7
        )
    else:
        raise ValueError("Language model not supported.")

def safe_llm_call(llm, messages, max_retries=3):
    """Make LLM API calls with retry logic and token limit handling."""
    for attempt in range(max_retries):
        try:
            return llm.invoke(messages)
        except Exception as e:
            if "context_length_exceeded" in str(e):
                if attempt == max_retries - 1:
                    raise TokenLimitExceededError("Maximum token limit exceeded even after retries")
                # Reduce content length for next attempt
                messages = truncate_messages(messages)
            else:
                raise e
            time.sleep(1)  # Wait before retry

def truncate_messages(messages, target_reduction=0.5):
    """Reduce the size of messages while preserving structure."""
    for msg in messages:
        if hasattr(msg, 'content') and isinstance(msg.content, str):
            current_tokens = num_tokens_from_string(msg.content)
            msg.content = truncate_text_to_token_limit(
                msg.content, 
                int(current_tokens * target_reduction)
            )
    return messages

def get_additional_notes():
    """Get any additional notes for PR."""
    # Placeholder - could be expanded to include more context
    return ""

def select_top_diff_files(diff_stat, llm):
    """Select the most important files from diff for review."""
    select_top_files_template = """
    Based on the diff overview, select what you think are the most important files to review.
    Select at most 10 files.
    {diff_stat}
    Respond only with the list of file names - 1 file name per line.
    """
    
    diff_stat = diff_stat.replace("{", "{{").replace("}", "}}")
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", select_top_files_template),
        ("human", json.dumps(diff_stat)),
    ])
    
    try:
        response = llm.invoke(
            chat_prompt.format_prompt(diff_stat=diff_stat).to_messages()
        )
        return response.content.split("\n")
    except Exception as e:
        print(f"Warning: Error selecting top diff files: {e}")
        return []

def select_top_files(filtered_files, llm, max_files=5, mode='readme'):
    """Select the most important files for README or Description generation."""
    if mode == 'readme':
        select_top_files_template = """
        Based on the following list of files, select what you think are the most important files
        needed to understand this repository. Select at most 10 files.
        {files}
        Respond only with the list of file names - 1 file name per line. Be sure to provide the full file path.
        """
    else:
        select_top_files_template = """
        Based on the following list of files, select what you think are the most important files
        needed to help describe the contents/purpose of the folder. Select at most 10 files.
        {files}
        Respond only with the list of file names - 1 file name per line. Be sure to provide the full file path.
        """

    files_str = json.dumps(filtered_files[:100])

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", select_top_files_template),
        ("human", files_str),
    ])
    
    try:
        response = llm.invoke(
            chat_prompt.format_prompt(
                files=files_str,
                max_files=max_files
            ).to_messages()
        )
        return response.content.strip().split("\n")[:max_files]  # Ensure we don't exceed max_files
    except Exception as e:
        print(f"Warning: Error selecting top files: {e}")
        # Fall back to selecting a few important files based on common patterns
        important_files = [f for f in filtered_files if f.lower() in [
            'readme.md', 'package.json', 'setup.py', 'requirements.txt',
            'main.py', 'app.py', 'index.ts', 'index.js'
        ]]
        return important_files[:max_files]

def get_refine_chain(llm):
    """Get the refine chain for summarizing content."""
    prompt_template = """Write a concise summary of the following:
    {text}
    CONCISE SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)

    refine_template = (
        "Your job is to produce a final summary\n"
        "We have provided an existing summary up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing summary"
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{text}\n"
        "------------\n"
        "Given the new context, refine the original summary"
        "If the context isn't useful, return the original summary."
    )
    refine_prompt = PromptTemplate.from_template(refine_template)

    class MyCustomHandler(BaseCallbackHandler):
        def on_chain_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
        ) -> Any:
            if isinstance(error, TokenLimitExceededError):
                print("Token limit exceeded. Attempting to reduce content size...")
                return True
            elif "context_length_exceeded" in str(error):
                time.sleep(60)
                print("Sleeping for a minute to avoid rate limiting")
                return True
            return False

    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=True,
        input_key="input_documents",
        output_key="output_text",
        callbacks=[MyCustomHandler()],
    )

    return chain

@click.command()
@click.argument('directory_path', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True), required=False, default='.')
@click.option('--mode', type=click.Choice(['commit', 'pr', 'readme', 'describe']), default='commit', required=True)
@click.option('--llm', default='openai', help='Which language model to use. Default is openai.')
@click.option('--short', is_flag=True, help='Run in short mode.', default=False)
@click.option('--max-tokens', default=100000, help='Maximum tokens to process at once.', type=int)
def main(directory_path, mode, llm, short, max_tokens):
    try:
        llm_instance = get_llm(llm, max_tokens)
        if mode == 'readme':
            filtered_files = get_filtered_file_paths(base_path=directory_path)
            try:
                top_selected_files = select_top_files(filtered_files, llm_instance, mode='readme')
                
                project_files_content = README_CONTEXT_TEMPLATE.format(
                    project_files=get_project_files(top_selected_files),
                )
                project_files_content = project_files_content.replace("{", "{{").replace("}", "}}")
                
                # Handle large content by splitting into smaller chunks
                split_docs = get_split_text_as_docs(project_files_content, max_chunk_size=max_tokens)
                
                refine_chain = get_refine_chain(llm_instance)
                final_content = refine_chain.invoke(
                    {"input_documents": split_docs},
                    return_only_outputs=True
                )
                final_content = final_content["output_text"]
                
                template = README_TEMPLATE_SHORT if short else README_TEMPLATE
                
                chat_prompt = ChatPromptTemplate.from_messages([
                    ("system", template),
                    ("human", final_content),
                ])
                
                response = safe_llm_call(llm_instance, 
                    chat_prompt.format_prompt(text=project_files_content).to_messages()
                )

                print(response.content)

                return response.content
                
            except TokenLimitExceededError as e:
                print(f"Error: {e}. Try using --short flag or reducing the number of files.")
                sys.exit(1)

        elif mode == 'describe':
            filtered_files = get_filtered_file_paths(base_path=directory_path)
            
            try:
                top_selected_files = select_top_files(filtered_files, llm_instance, mode='describe')

                project_files = get_project_files(top_selected_files)
                
                project_files_content = DESCRIBE_CONTEXT_TEMPLATE.format(
                    project_files=project_files,
                    top_level_structure=list_top_level(directory_path),
                )
                project_files_content = project_files_content.replace("{", "{{").replace("}", "}}")
                
                # Handle large content by splitting into smaller chunks
                split_docs = get_split_text_as_docs(project_files_content, max_chunk_size=max_tokens)
                
                refine_chain = get_refine_chain(llm_instance)
                final_content = refine_chain.invoke(
                    {"input_documents": split_docs},
                    return_only_outputs=True
                )
                final_content = final_content["output_text"]
                
                template = DESCRIBE_TEMPLATE_SHORT if short else DESCRIBE_TEMPLATE
                
                chat_prompt = ChatPromptTemplate.from_messages([
                    ("system", template),
                    ("human", final_content),
                ])
                
                response = safe_llm_call(llm_instance, 
                    chat_prompt.format_prompt(text=project_files_content).to_messages()
                )

                print(response.content)

                return response.content
                
            except TokenLimitExceededError as e:
                print(f"Error: {e}. Try using --short flag or reducing the number of files.")
                sys.exit(1)
                
        else:  # commit or pr mode
            cached = (mode == 'commit')
            
            try:
                last_commit_messages = get_last_commit_messages(base_path=directory_path)
                files_changed_summary = get_files_changed_summary(base_path=directory_path)
                detailed_diff = get_detailed_diff(cached, max_tokens=max_tokens, base_path=directory_path)
                
                if mode == 'pr':
                    additional_notes = get_additional_notes()
                    diff_stat = get_diff_stat(base_path=directory_path)
                    top_selected_diff_files = select_top_diff_files(diff_stat, llm_instance)
                    detailed_diff = get_detailed_diff_of_files(top_selected_diff_files, max_tokens=max_tokens, base_path=directory_path)
                    
                    detailed_context = DETAILED_CONTEXT_TEMPLATE.format(
                        last_commit_messages=last_commit_messages,
                        files_changed_summary=files_changed_summary,
                        detailed_diff=detailed_diff,
                        additional_notes=additional_notes,
                    )
                else:
                    detailed_context = COMMIT_DETAILED_CONTEXT_TEMPLATE.format(
                        files_changed_summary=files_changed_summary,
                        detailed_diff=detailed_diff,
                        additional_notes="",
                    )
                
                detailed_context = detailed_context.replace("{", "{{").replace("}", "}}")
                
                template = (COMMIT_MESSAGE_TEMPLATE_SHORT if mode == 'commit' else PR_MESSAGE_TEMPLATE_SHORT) if short else (COMMIT_MESSAGE_TEMPLATE if mode == 'commit' else PR_MESSAGE_TEMPLATE)
                
                split_docs = get_split_text_as_docs(detailed_context, max_chunk_size=max_tokens)
                refine_chain = get_refine_chain(llm_instance)
                
                final_content = refine_chain.invoke(
                    {"input_documents": split_docs},
                    return_only_outputs=True
                )
                final_content = final_content["output_text"]
                
                chat_prompt = ChatPromptTemplate.from_messages([
                    ("system", template),
                    ("human", final_content),
                ])
                
                response = safe_llm_call(llm_instance, 
                    chat_prompt.format_prompt(text=final_content).to_messages()
                )

                print(response.content)

                return response.content
                
            except TokenLimitExceededError as e:
                print(f"Error: {e}. Try using --short flag or reducing the scope of changes.")
                sys.exit(1)
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()