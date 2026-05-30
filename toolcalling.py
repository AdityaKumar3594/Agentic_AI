from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from rich import print

# Tool
@tool
def get_text_length(text: str) -> int:
    """Returns the number of characters in a given text"""
    return len(text)

tools = {
    "get_text_length": get_text_length
}

# LLM
llm = ChatMistralAI(model="mistral-small-2506")

# Bind Tool
llm_with_tool = llm.bind_tools([get_text_length])

# Chat Memory
messages = []

while True:

    prompt = input("You: ")

    # Exit condition
    if prompt.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        break

    query = HumanMessage(content=prompt)
    messages.append(query)

    # First LLM Call
    result = llm_with_tool.invoke(messages)
    messages.append(result)

    # Tool Calling
    if result.tool_calls:

        tool_call = result.tool_calls[0]

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        tool_result = tools[tool_name].invoke(tool_args)

        tool_message = ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"]
        )

        messages.append(tool_message)

        # Final LLM Response
        final_result = llm_with_tool.invoke(messages)

        messages.append(final_result)

        print(f"AI: {final_result.content}")

    else:
        print(f"AI: {result.content}")