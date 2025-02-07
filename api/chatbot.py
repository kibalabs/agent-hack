import asyncio
import os
import sys
import time

from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.tools import CdpTool
from cdp_langchain.utils import CdpAgentkitWrapper
from core.util import file_util
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from sign_message_action import SignMessageAction

walletDataFilePath = "../secrets/walletData.json"

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
CDP_API_KEY_NAME = os.environ["CDP_API_KEY_NAME"]
CDP_API_KEY_PRIVATE_KEY = os.environ["CDP_API_KEY_PRIVATE_KEY"]
NETWORK_ID = os.environ["NETWORK_ID"]

async def initialize_agent():
    values = {
        "cdp_api_key_name": CDP_API_KEY_NAME,
        "cdp_api_key_private_key": CDP_API_KEY_PRIVATE_KEY,
        "network_id": NETWORK_ID,
    }
    if os.path.exists(walletDataFilePath):
        walletData = await file_util.read_file(filePath=walletDataFilePath)
        values["cdp_wallet_data"] = walletData
    agentkit = CdpAgentkitWrapper(**values)
    walletData = agentkit.export_wallet()
    await file_util.write_file(filePath=walletDataFilePath, content=walletData)
    cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(cdp_agentkit_wrapper=agentkit)
    tools = cdp_toolkit.get_tools()
    signMessageAction = SignMessageAction()
    tools.append(
        CdpTool(
            name=signMessageAction.name,
            description=signMessageAction.description,
            cdp_agentkit_wrapper=agentkit,
            args_schema=signMessageAction.args_schema,
            func=signMessageAction.func,
        )
    )
    memory = MemorySaver()
    config = {
        "configurable": {
            "thread_id": "CDP Agentkit Chatbot Example!",
        },
    }
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
    )
    return create_react_agent(
        llm,
        tools=tools,
        checkpointer=memory,
        state_modifier=(
            "You are a helpful agent that can interact onchain using the Coinbase Developer Platform AgentKit. "
            "You are empowered to interact onchain using your tools. If you ever need funds, you can request "
            "them from the faucet if you are on network ID 'base-sepolia'. If not, you can provide your wallet "
            "details and request funds from the user. Before executing your first action, get the wallet details "
            "to see what network you're on. If there is a 5XX (internal) HTTP error code, ask the user to try "
            "again later. If someone asks you to do something you can't do with your currently available tools, "
            "you must say so, and encourage them to implement it themselves using the CDP SDK + Agentkit, "
            "recommend they go to docs.cdp.coinbase.com for more information. Be concise and helpful with your "
            "responses. Refrain from restating your tools' descriptions unless it is explicitly requested."
        ),
    ), config


# Autonomous Mode
def run_autonomous_mode(agent_executor, config, interval=10):
    """Run the agent autonomously with specified intervals."""
    print("Starting autonomous mode...")
    while True:
        try:
            # Provide instructions autonomously
            thought = (
                "Be creative and do something interesting on the blockchain. "
                "Choose an action or set of actions and execute it that highlights your abilities."
            )

            # Run agent in autonomous mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=thought)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

            # Wait before the next action
            time.sleep(interval)

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


# Chat Mode
def run_chat_mode(agent_executor, config):
    """Run the agent interactively based on user input."""
    print("Starting chat mode... Type 'exit' to end.")
    while True:
        try:
            user_input = input("\nPrompt: ")
            if user_input.lower() == "exit":
                break

            # Run agent with the user's input in chat mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


# Mode Selection
def choose_mode():
    """Choose whether to run in autonomous or chat mode based on user input."""
    while True:
        print("\nAvailable modes:")
        print("1. chat    - Interactive chat mode")
        print("2. auto    - Autonomous action mode")

        choice = input("\nChoose a mode (enter number or name): ").lower().strip()
        if choice in ["1", "chat"]:
            return "chat"
        elif choice in ["2", "auto"]:
            return "auto"
        print("Invalid choice. Please try again.")


async def main():
    agent_executor, config = await initialize_agent()
    mode = choose_mode()
    if mode == "chat":
        run_chat_mode(agent_executor=agent_executor, config=config)
    elif mode == "auto":
        run_autonomous_mode(agent_executor=agent_executor, config=config)


if __name__ == "__main__":
    print("Starting Agent...")
    asyncio.run(main())
