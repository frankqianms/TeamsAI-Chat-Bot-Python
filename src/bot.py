import os
import sys
import traceback
from typing import Any, Dict

from botbuilder.core import MemoryStorage, TurnContext
from teams import Application, ApplicationOptions, TeamsAdapter
from teams.ai import AIOptions
from teams.ai.actions import ActionTurnContext
from teams.ai.models import AzureOpenAIModelOptions, OpenAIModel, OpenAIModelOptions
from teams.ai.planners import ActionPlanner, ActionPlannerOptions
from teams.ai.prompts import PromptManager, PromptManagerOptions
from teams.state import TurnState

from config import Config

config = Config()

import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler
handler = logging.FileHandler('bot.log')
handler.setLevel(logging.DEBUG)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

if config.OPENAI_API_KEY=="<your-key>" and config.AZURE_OPENAI_API_KEY=="<your-key>":
    raise RuntimeError(
        "Missing environment variables - please check that OPENAI_API_KEY or AZURE_OPENAI_API_KEY is set."
    )

# Create AI components
model: OpenAIModel

if config.AZURE_OPENAI_API_KEY != "<your-key>":
    model = OpenAIModel(
        AzureOpenAIModelOptions(
            api_key=config.AZURE_OPENAI_API_KEY,
            default_model=config.AZURE_OPENAI_MODEL_DEPLOYMENT_NAME,
            endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_version="2023-03-15-preview",
            logger=logger
        )
    )
elif config.OPENAI_API_KEY != "<your-key>":
    model = OpenAIModel(
        OpenAIModelOptions(api_key=config.OPENAI_API_KEY, default_model=config.OPENAI_MODEL_DEPLOYMENT_NAME)
    )
    
prompts = PromptManager(PromptManagerOptions(prompts_folder=f"{os.getcwd()}/prompts"))



planner = ActionPlanner(
    ActionPlannerOptions(model=model, prompts=prompts, default_prompt="chat", logger=logger)
)

# Define storage and application
storage = MemoryStorage()
app = Application[TurnState](
    ApplicationOptions(
        bot_app_id=config.APP_ID,
        storage=storage,
        adapter=TeamsAdapter(config),
        ai=AIOptions(planner=planner),
    )
)

@app.error
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")