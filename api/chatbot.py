import asyncio
import os

from langchain_core.messages import HumanMessage

from agent_hack.agent_manager import AgentManager


GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
CDP_API_KEY_NAME = os.environ["CDP_API_KEY_NAME"]
CDP_API_KEY_PRIVATE_KEY = os.environ["CDP_API_KEY_PRIVATE_KEY"]
NETWORK_ID = os.environ["NETWORK_ID"]


async def main():
    print("Starting Agent... Type 'exit' to end.")
    agentManager = AgentManager(
        geminiApiKey=GEMINI_API_KEY,
        cdpApiKeyName=CDP_API_KEY_NAME,
        cdpApiKeyPrivateKey=CDP_API_KEY_PRIVATE_KEY,
        networkId=NETWORK_ID,
    )
    agentExecutor = await agentManager.get_agent_executor(userId="0x18090cDA49B21dEAffC21b4F886aed3eB787d032")
    config = {
        "configurable": {
            "thread_id": "Yield-Seeker",
        },
    }
    while True:
        try:
            userInput = input("\nPrompt: ").strip()
            if userInput.lower() == "exit":
                break
            message = HumanMessage(content=userInput)
            async for chunk in agentExecutor.astream({"messages": [message]}, config):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")
        except KeyboardInterrupt:
            print("Goodbye Agent!")
            return


if __name__ == "__main__":
    asyncio.run(main())
