"""
AI Production Support Assistant - Semantic Kernel Version
A conversational AI assistant for production support using Semantic Kernel
"""

import os
import asyncio
import datetime
from time import sleep
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions import KernelArguments

from plugins.github_plugin import GitHubPlugin
from plugins.elasticsearch_plugin import ElasticsearchPlugin
from plugins.servicenow_plugin import ServiceNowPlugin

load_dotenv(override=True)

# Get current date/time for context
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Today's date and time:", current_datetime)

# System message with instructions for the AI
SYSTEM_MESSAGE = f"""Today's date and time: {current_datetime}

You are an application support agent. You will help developers with their questions about the application.
You have access to several tools to assist you:

**GitHub Tools:**
- List repositories for a GitHub user
- Browse files in a repository
- Get file content from repositories
- Create issues in repositories

**Elasticsearch Tools:**
- Search application logs stored in Elasticsearch
- Query logs using KQL (Kibana Query Language)
- The logs contain fields like: levelname, message, host, timestamp, filename, funcName, etc.

**ServiceNow Tools:**
- Create new support cases
- Query open cases and high priority cases
- Search cases by text
- Add comments to cases
- Close resolved cases

**Default Values:**
- Default GitHub user: drewelewis
- Default repository: drewelewis/ContosoBankAPI
- Always verify with the user if they want to use different values

**Instructions:**
- Use your tools to answer user questions whenever possible
- If you're not sure which tool to use, ask clarifying questions
- Be helpful, clear, and concise in your responses
- When searching logs, convert natural language queries to proper Elasticsearch JSON format
- When creating cases or issues, provide clear summaries of what was created

Always think step by step and use the appropriate tools to help the user effectively.
"""


class SemanticKernelChat:
    """Main chat class using Semantic Kernel"""
    
    def __init__(self):
        """Initialize the Semantic Kernel chat assistant"""
        self.kernel = Kernel()
        self.chat_history = ChatHistory()
        self.setup_ai_service()
        self.setup_plugins()
        
    def setup_ai_service(self):
        """Configure Azure OpenAI service"""
        # Add Azure OpenAI chat completion service
        self.service_id = "chat"
        self.kernel.add_service(
            AzureChatCompletion(
                service_id=self.service_id,
                deployment_name=os.getenv('OPENAI_API_MODEL_DEPLOYMENT_NAME'),
                endpoint=os.getenv('OPENAI_API_ENDPOINT'),
                api_key=os.getenv('OPENAI_API_KEY'),
                api_version=os.getenv('OPENAI_API_VERSION')
            )
        )
        
    def setup_plugins(self):
        """Register all plugins with the kernel"""
        # Add GitHub plugin
        self.kernel.add_plugin(
            GitHubPlugin(),
            plugin_name="GitHub"
        )
        
        # Add Elasticsearch plugin
        self.kernel.add_plugin(
            ElasticsearchPlugin(),
            plugin_name="Elasticsearch"
        )
        
        # Add ServiceNow plugin
        self.kernel.add_plugin(
            ServiceNowPlugin(),
            plugin_name="ServiceNow"
        )
        
        print("Loaded plugins:", list(self.kernel.plugins.keys()))
        
    async def chat(self, user_input: str) -> str:
        """
        Process user input and generate a response
        
        Args:
            user_input: The user's message
            
        Returns:
            The assistant's response
        """
        # Add user message to history
        self.chat_history.add_user_message(user_input)
        
        # Get the chat completion service
        chat_completion: ChatCompletionClientBase = self.kernel.get_service(
            service_id=self.service_id
        )
        
        # Configure function calling to be automatic
        execution_settings = chat_completion.get_prompt_execution_settings_class()(
            service_id=self.service_id
        )
        execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto(
            auto_invoke=True,
            filters={}
        )
        
        # Get response with automatic function calling
        response = await chat_completion.get_chat_message_contents(
            chat_history=self.chat_history,
            settings=execution_settings,
            kernel=self.kernel,
            arguments=KernelArguments()
        )
        
        # Extract the response text
        if response:
            assistant_message = str(response[0])
            self.chat_history.add_assistant_message(assistant_message)
            return assistant_message
        
        return "I apologize, but I couldn't generate a response."
    
    def add_system_message(self, message: str):
        """Add a system message to chat history"""
        self.chat_history.add_system_message(message)


async def main():
    """Main async function to run the chat loop"""
    print("\n" + "="*60)
    print("AI Production Support Assistant (Semantic Kernel)")
    print("="*60 + "\n")
    
    # Initialize the chat assistant
    assistant = SemanticKernelChat()
    
    # Add system message
    assistant.add_system_message(SYSTEM_MESSAGE)
    
    # Loading animation
    for _ in range(3):
        sleep(0.3)
        print(".", end="", flush=True)
    print("\n")
    
    print("How can I help you? (type '/q' to exit, '/clear' to clear history)")
    print()
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input("> ")
            print()
            
            # Check for exit command
            if user_input.lower() in ["/q", "/quit", "/exit"]:
                print("Goodbye!")
                break
            
            # Check for clear history command
            if user_input.lower() in ["/clear", "/reset"]:
                assistant.chat_history = ChatHistory()
                assistant.add_system_message(SYSTEM_MESSAGE)
                print("Chat history cleared!")
                print()
                continue
            
            # Skip empty input
            if not user_input.strip():
                continue
            
            # Get and display response
            response = await assistant.chat(user_input)
            print(f"Assistant: {response}")
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print()


def run():
    """Entry point that handles the async event loop"""
    # Run the async main function
    asyncio.run(main())


if __name__ == "__main__":
    run()
