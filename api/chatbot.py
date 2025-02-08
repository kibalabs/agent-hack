import asyncio
import os

from agent_hack.agent_manager import AgentManager

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
CDP_API_KEY_NAME = os.environ["CDP_API_KEY_NAME"]
CDP_API_KEY_PRIVATE_KEY = os.environ["CDP_API_KEY_PRIVATE_KEY"]
NETWORK_ID = os.environ["NETWORK_ID"]


async def main():
    print("Starting Agent... (type 'exit' to end)")
    agentManager = AgentManager(
        geminiApiKey=GEMINI_API_KEY,
        cdpApiKeyName=CDP_API_KEY_NAME,
        cdpApiKeyPrivateKey=CDP_API_KEY_PRIVATE_KEY,
        networkId=NETWORK_ID,
        sqliteDbPath="./data/checkpoints.sqlite",
    )
    while True:
        try:
            userInput = input("\nPrompt: ").strip()
            if userInput.lower() == "exit":
                break
            agentResponse = await agentManager.get_agent_response(userId="0x18090cDA49B21dEAffC21b4F886aed3eB787d032", message=userInput)
            print(agentResponse)
        except KeyboardInterrupt:
            print("Goodbye Agent!")
            break


if __name__ == "__main__":
    asyncio.run(main())
