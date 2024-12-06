from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from tools import CreateCommitTool, CreatePRTool, CommitDetailsTool, PRDetailsTool, ReadmeDetailsTool, CreateReadmeTool
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import pprint
import asyncio
import tiktoken

load_dotenv()


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
	"""Returns the number of tokens in a text string."""
	encoding = tiktoken.get_encoding(encoding_name)
	num_tokens = len(encoding.encode(string))
	return num_tokens


async def main():
	tools = [
		CreateCommitTool(),
		CreatePRTool(),
		CommitDetailsTool(),
		PRDetailsTool(),
		ReadmeDetailsTool(),
		CreateReadmeTool(),
	]

	prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. You may not need to use tools for every query - the user may just want to chat!",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

	# prompt = hub.pull("hwchase17/openai-tools-agent")
	# print(prompt)
	# prompt = ChatPromptTemplate.from_messages(
	#     [
	#         (
	#             "system",
	#             "You are a helpful assistant. You are helping a software developer prepare to make a commit and a pull request.",
	#         ),
	#         MessagesPlaceholder(variable_name="chat_history"),
	#         MessagesPlaceholder(variable_name="agent_scratchpad"),
	#     ]
	# )

	llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)

	agent = create_openai_tools_agent(
		llm.with_config({"tags": ["agent_llm"]}),
		tools,
		prompt
	)

	agent_executor = AgentExecutor(agent=agent, tools=tools).with_config(
		{"run_name": "Agent"}
	)

	demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

	conversational_agent_executor = RunnableWithMessageHistory(
		agent_executor,
		lambda session_id: demo_ephemeral_chat_history_for_chain,
		input_messages_key="input",
		output_messages_key="output",
		history_messages_key="chat_history",
	)

	while True:
		user_input = input("You: ")
		if user_input == "exit":
			break
		
		async for event in conversational_agent_executor.astream_events(
			{"input": user_input},
			config={"configurable": {"session_id": "<foo>"}},
			version="v1",
		):
			kind = event["event"]
			# if kind == "on_chain_start":
			# 	if (
			# 		event["name"] == "Agent"
			# 	):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
			# 		print(
			# 			f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
			# 		)
			# elif kind == "on_chain_end":
			# 	if (
			# 		event["name"] == "Agent"
			# 	):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
			# 		print()
			# 		print("--")
			# 		print(
			# 			f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
			# 		)
			if kind == "on_chat_model_stream":
				content = event["data"]["chunk"].content
				if content:
					# Empty content in the context of OpenAI means
					# that the model is asking for a tool to be invoked.
					# So we only print non-empty content
					print(content, end="")
			# elif kind == "on_tool_start":
			# 	print("--")
			# 	print(
			# 		f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
			# 	)
			# elif kind == "on_tool_end":
			# 	print(f"Done tool: {event['name']}")
			# 	print(f"Tool output was: {event['data'].get('output')}")
			# 	print("--")
		print()
		# chunks =[]
		# for chunk in agent_executor.stream(
		# 	{"input": user_input},
		# 	config={"configurable": {"session_id": "<foo>"}},
		# ):
		# 	chunks.append(chunk)
		# 	pprint.pprint(chunk['output'], depth=1)
		# result = conversational_agent_executor.invoke({"input": user_input}, config={"configurable": {"session_id": "<foo>"}})
		# print(result["output"])

		
		# output = {}
		# curr_key = None
		# for chunk in conversational_agent_executor.stream({"input": user_input}, config={"configurable": {"session_id": "<foo>"}}):
		# 	for key in chunk:
		# 		if key not in output:
		# 			output[key] = chunk[key]
		# 		else:
		# 			output[key] += chunk[key]
		# 		if key != curr_key:
		# 			print(f"\n\n{key}: {chunk[key]}", end="", flush=True)
		# 		else:
		# 			print(chunk[key], end="", flush=True)
		# 		curr_key = key
		# print("\n\n")

if __name__ == "__main__":
	asyncio.run(main())