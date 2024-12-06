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
import tiktoken
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import CharacterTextSplitter
import time

load_dotenv()



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

class CreateCommitMessage(BaseModel):
    commit_message: str = Field(
        ..., description="The commit message for the changes made."
    )

class CreatePRMessage(BaseModel):
    pr_message: str = Field(
        ..., description="The pull request message for the changes made."
    )
    
def num_tokens_from_messages(messages, model="gpt-4-0125-preview"):
    """Return the number of tokens used by a list of messages."""
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        # Every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(str(value)))
            if key == "name":  # If there's a name, the role is omitted
                num_tokens += -1  # Role is always required and always 1 token
    num_tokens += 2  # Every response is primed with <im_start>assistant
    return num_tokens

def truncate_text_to_token_limit(text, max_tokens, model="gpt-4-0125-preview"):
    """Truncate text to fit within token limit."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        text = encoding.decode(tokens)
    return text

def safe_get_detailed_diff(cached=True, max_tokens=100000):
    """Get detailed diff with token limit consideration."""
    cmd = ['git', 'diff', '--cached'] if cached else ['git', 'diff', 'origin']
    diff = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    return truncate_text_to_token_limit(diff, max_tokens)

def safe_invoke_llm(llm, messages, max_retries=3, initial_wait=60):
    """Safely invoke LLM with retries and token management."""
    wait_time = initial_wait
    for attempt in range(max_retries):
        try:
            # Check token count before making the request
            token_count = num_tokens_from_messages(messages)
            if token_count > 128000:  # GPT-4's context limit
                raise ValueError(f"Input too long: {token_count} tokens. Must be under 128000.")
            
            return llm.invoke(messages)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Attempt {attempt + 1} failed. Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
            wait_time *= 2  # Exponential backoff

def get_last_commit_messages(n=3):
    return subprocess.run(['git', 'log', f'-{n}', '--pretty=%B'], capture_output=True, text=True).stdout.strip()

def get_files_changed_summary():
    return subprocess.run(['git', 'diff', '--cached', '--stat'], capture_output=True, text=True).stdout.strip()

def get_diff_stat():
    return subprocess.run(['git', 'diff', 'origin', '--stat'], capture_output=True, text=True).stdout.strip()

def get_detailed_diff_of_files(files):
    return subprocess.run(['git', 'diff', '--', *files], capture_output=True, text=True).stdout.strip()

def get_detailed_diff(cached=True):
    cmd = ['git', 'diff', '--cached'] if cached else ['git', 'diff', 'origin']
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

def get_additional_notes():
    # Placeholder for any additional notes you might want to include for PRs
    return ""

def get_current_readme():
    with open('README.md', 'r') as f:
        return f.read()

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

def get_filtered_file_paths():
    cmd = 'git ls-files | xargs file | grep "ASCII text" | cut -d ":" -f 1'
    files_under_source_control = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT, text=True).communicate()[0].strip().split('\n')
    # files_under_source_control = subprocess.run(shlex.split(cmd), capture_output=True, text=True).stdout.strip().split('\n')
    return files_under_source_control

def generate_files_dict(files):
    """Generate the dictionary of file paths and contents."""
    files_dict = {}
    for file in files:
        try:
            with open(file, 'r') as f:
                files_dict[file] = f.read()
        except Exception:
            pass
    return files_dict
    # gitignore_path = os.path.join(start_path, '.gitignore')
    # ignore_patterns = parse_gitignore(gitignore_path)

    # files_dict = {}
    # for root, dirs, files in os.walk(start_path):
    # 	# Filter out ignored directories
    # 	dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_patterns)]
    # 	for file in files:
    # 		relative_path = os.path.relpath(os.path.join(root, file), start_path)
    # 		if relative_path.startswith('.'):
    # 			continue
    # 		if not should_ignore(relative_path, ignore_patterns):
    # 			try:
    # 				with open(os.path.join(root, file), 'r') as f:
    # 					files_dict[relative_path] = f.read()
    # 			except UnicodeDecodeError:
    # 				pass
    # return files_dict

def get_project_files(files):
    return json.dumps(generate_files_dict(files))


def get_llm(llm):
    if llm == 'openai':
        return ChatOpenAI(model="gpt-4-0125-preview")
    else:
        raise ValueError("Language model not supported.")

def get_refine_chain(llm):
    # document_prompt = PromptTemplate(
    # 	input_variables=["page_content"],
    # 	template="{page_content}"
    # )
    # document_variable_name = "context"
    # # The prompt here should take as an input variable the
    # # `document_variable_name`
    # prompt = PromptTemplate.from_template(
    # 	"Summarize this content: {context}"
    # )
    # initial_llm_chain = LLMChain(llm=llm, prompt=prompt)
    # initial_response_name = "prev_response"
    # # The prompt here should take as an input variable the
    # # `document_variable_name` as well as `initial_response_name`
    # prompt_refine = PromptTemplate.from_template(
    # 	"Here's your first summary: {prev_response}. "
    # 	"Now add to it based on the following context: {context}"
    # )
    # refine_llm_chain = LLMChain(llm=llm, prompt=prompt_refine)
    # chain = RefineDocumentsChain(
    # 	initial_llm_chain=initial_llm_chain,
    # 	refine_llm_chain=refine_llm_chain,
    # 	document_prompt=document_prompt,
    # 	document_variable_name=document_variable_name,
    # 	initial_response_name=initial_response_name,
    # )
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
        "Given the new context, refine the original summary in Italian"
        "If the context isn't useful, return the original summary."
    )
    refine_prompt = PromptTemplate.from_template(refine_template)
    class MyCustomHandler(BaseCallbackHandler):
        def on_chain_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
        ) -> Any:
            # sleep for a minute to avoid rate limiting
            time.sleep(60)
            print("Sleeping for a minute to avoid rate limiting")
            # pick up where we left off
            return True
    
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

def get_split_text_as_docs(text, max_tokens=80000):
    """Split text into documents with token limit consideration."""
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=max_tokens,
        chunk_overlap=1000  # Added overlap for better context
    )
    return text_splitter.create_documents([text])

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def select_top_diff_files(diff_stat, llm):
    select_top_files_template = """
    Based on the diff overview, your task is to select what you think are the most important files from the diff that you'd like to review in detail for the purpose of writing a pull request message.
    Select at most 10 files.
    {diff_stat}
    Respond only with the list of file names - 1 file name per line.
    ## Example response:
    file1
    dir/file2
    file3
    """
    
    diff_stat = diff_stat.replace("{", "{{").replace("}", "}}")
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", select_top_files_template),
            ("human", json.dumps(diff_stat)),
        ]
    )
    response = llm.invoke(
        chat_prompt.format_prompt(
            diff_stat=diff_stat
        ).to_messages()
    )
    return response.content.split("\n")

def select_top_files(filtered_files, llm):
    select_top_files_template = """
    Based on the following list of files in the project, your task is to select what you think are the most important files needed to understand this repository for the purpose of updating the README file.
    Select at most 10 files.
    {files}
    Respond only with the list of file names - 1 file name per line.
    ## Example response:
    file1
    dir/file2
    file3
    """

    # filtered_files = filtered_files.replace("{", "{{").replace("}", "}}")
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", select_top_files_template),
            ("human", json.dumps(filtered_files)),
        ]
    )
    response = llm.invoke(
        chat_prompt.format_prompt(
            files=json.dumps(filtered_files)
        ).to_messages()
    )
    return response.content.split("\n")


@click.command()
@click.option('--mode', type=click.Choice(['commit', 'pr', 'readme']), default='commit', required=True)
@click.option('--llm', default='openai', help='Which language model to use. Default is openai.')
@click.option('--short', is_flag=True, help='Run in short mode.', default=False)
def main(mode, llm, short):
    llm = get_llm(llm)
    # if mode == 'readme':
    #     filtered_files = get_filtered_file_paths()
    #     print("Filtered files: ", filtered_files)
    #     top_selected_files = select_top_files(filtered_files, llm)
    #     print("Top selected files: ", top_selected_files)
    #     # Limit the number of files processed
    #     top_selected_files = top_selected_files[:5]  # Process only top 5 files
        
    #     project_files_content = README_CONTEXT_TEMPLATE.format(
    #         project_files=get_project_files(top_selected_files),
    #     )
    #     project_files_content = project_files_content.replace("{", "{{").replace("}", "}}")
    #     refine_chain = get_refine_chain(llm)
    #     split_docs = get_split_text_as_docs(project_files_content)
    #     final_content = refine_chain.invoke(
    #         {"input_documents": split_docs},
    #         return_only_outputs=True
    #     )
    #     final_content = final_content["output_text"]

    #     template = README_TEMPLATE
    #     if short:
    #         template = README_TEMPLATE_SHORT

    #     chat_prompt = ChatPromptTemplate.from_messages(
    #         [
    #             ("system", README_TEMPLATE),
    #             ("human", final_content),
    #         ]
    #     )
    #     print()
    #     response = llm.invoke(
    #         chat_prompt.format_prompt(
    #             text=project_files_content
    #         ).to_messages()
    #     )
    #     print(response.content)
    #     return

    # # llm_with_tools = llm.bind_tools(
    # # 	[CreateCommitMessage, CreatePRMessage],
    # # )
    # additional_notes = ""
    # cached = True if mode == 'commit' else False

    # # Gather detailed information
    # last_commit_messages = get_last_commit_messages()
    # files_changed_summary = get_files_changed_summary()
    # detailed_diff = get_detailed_diff(cached)
    
    # if mode == 'pr':
    #     additional_notes = get_additional_notes()
    #     diff_stat = get_diff_stat()
    #     top_selected_diff_files = select_top_diff_files(diff_stat, llm)
    #     print("Top selected diff files: ", top_selected_diff_files)
    #     detailed_diff = get_detailed_diff_of_files(top_selected_diff_files)
    #     print("Detailed diff: ", detailed_diff)
    
    #     # Prepare the detailed context
    #     detailed_context = DETAILED_CONTEXT_TEMPLATE.format(
    #         last_commit_messages=last_commit_messages,
    #         files_changed_summary=files_changed_summary,
    #         detailed_diff=detailed_diff,
    #         additional_notes=additional_notes,
    #     )
    # elif mode == 'commit':
    #     detailed_context = COMMIT_DETAILED_CONTEXT_TEMPLATE.format(
    #         files_changed_summary=files_changed_summary,
    #         detailed_diff=detailed_diff,
    #         additional_notes=additional_notes,
    #     )
    # # replace curly braces with double curly braces to escape them
    # detailed_context = detailed_context.replace("{", "{{").replace("}", "}}")

    # if mode == 'commit':
    #     template = COMMIT_MESSAGE_TEMPLATE
    #     if short:
    #         template = COMMIT_MESSAGE_TEMPLATE_SHORT
    # elif mode == 'pr':
    #     template = PR_MESSAGE_TEMPLATE
    #     if short:
    #         template = PR_MESSAGE_TEMPLATE_SHORT
    
    # # template = COMMIT_MESSAGE_TEMPLATE if mode == 'commit' else PR_MESSAGE_TEMPLATE

    # refine_chain = get_refine_chain(llm)
    # split_docs = get_split_text_as_docs(detailed_context)
    # final_content = refine_chain.invoke(
    #     {"input_documents": split_docs},
    #     return_only_outputs=True
    # )
    # final_content = final_content["output_text"]
    # chat_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", template),
    #         ("human", final_content),
    #     ]
    # )
    
    # response = llm.invoke(
    #     chat_prompt.format_prompt(
    #         text=final_content
    #     ).to_messages()
    # )
    # print(response.content)

    if mode == 'readme':
        filtered_files = get_filtered_file_paths()
        print("Filtered files: ", filtered_files)
        top_selected_files = select_top_files(filtered_files, llm)
        print("Top selected files: ", top_selected_files)
        
        # Limit the number of files processed
        top_selected_files = top_selected_files[:5]  # Process only top 5 files
        
        project_files_content = README_CONTEXT_TEMPLATE.format(
            project_files=get_project_files(top_selected_files),
        )
        project_files_content = project_files_content.replace("{", "{{").replace("}", "}}")
        
        # Split into smaller chunks with token limit consideration
        split_docs = get_split_text_as_docs(project_files_content, max_tokens=60000)
        
        template = README_TEMPLATE_SHORT if short else README_TEMPLATE
        
        try:
            chat_prompt = ChatPromptTemplate.from_messages([
                ("system", template),
                ("human", split_docs[0].page_content if split_docs else ""),
            ])
            
            response = safe_invoke_llm(
                llm,
                chat_prompt.format_prompt().to_messages()
            )
            print(response.content)
            
        except Exception as e:
            print(f"Error processing README: {str(e)}")
            return
        
    else:  # commit or pr mode
        cached = (mode == 'commit')
        additional_notes = ""
        
        # Get diffs with token limits
        detailed_diff = safe_get_detailed_diff(cached, max_tokens=80000)
        
        if mode == 'pr':
            template = PR_MESSAGE_TEMPLATE_SHORT if short else PR_MESSAGE_TEMPLATE
            diff_stat = get_diff_stat()
            top_selected_diff_files = select_top_diff_files(diff_stat, llm)[:5]  # Limit to top 5 files
            detailed_diff = get_detailed_diff_of_files(top_selected_diff_files)
            
            context = DETAILED_CONTEXT_TEMPLATE.format(
                last_commit_messages=get_last_commit_messages(2),  # Limit to last 2 commits
                files_changed_summary=get_files_changed_summary(),
                detailed_diff=truncate_text_to_token_limit(detailed_diff, 60000),
                additional_notes=additional_notes
            )
        else:
            template = COMMIT_MESSAGE_TEMPLATE_SHORT if short else COMMIT_MESSAGE_TEMPLATE
            context = COMMIT_DETAILED_CONTEXT_TEMPLATE.format(
                files_changed_summary=get_files_changed_summary(),
                detailed_diff=truncate_text_to_token_limit(detailed_diff, 60000),
                additional_notes=additional_notes
            )
        
        context = context.replace("{", "{{").replace("}", "}}")
        split_docs = get_split_text_as_docs(context, max_tokens=60000)
        
        try:
            chat_prompt = ChatPromptTemplate.from_messages([
                ("system", template),
                ("human", split_docs[0].page_content if split_docs else ""),
            ])
            
            response = safe_invoke_llm(
                llm,
                chat_prompt.format_prompt().to_messages()
            )
            print(response.content)
            
        except Exception as e:
            print(f"Error processing {mode}: {str(e)}")
            return


if __name__ == '__main__':
    main()
