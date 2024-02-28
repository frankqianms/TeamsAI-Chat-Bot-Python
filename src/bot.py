"""
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.

Description: initialize the app and listen for `message` activitys
"""

import sys
import traceback

from botbuilder.core import BotFrameworkAdapterSettings, TurnContext, MemoryStorage
from teams import Application, ApplicationOptions
from teams.ai.models import OpenAIModel, OpenAIModelOptions, AzureOpenAIModelOptions
from teams.ai.prompts import PromptManager, PromptManagerOptions
from teams.ai.planners import ActionPlanner, ActionPlannerOptions
from teams.ai.ai_options import AIOptions
from state import *

from config import Config
config = Config()

default_prompt_folder = "prompts"
default_prompt = "chat"

# Use Azure OpenAI
model_options = AzureOpenAIModelOptions(
    api_key=config.AZURE_OPENAI_API_KEY , 
    default_model=config.AZURE_OPENAI_MODEL_DEPLOYMENT_NAME, 
    endpoint=config.AZURE_OPENAI_ENDPOINT
)
model = OpenAIModel(model_options)
prompts = PromptManager(PromptManagerOptions(default_prompt_folder))
planner = ActionPlanner(ActionPlannerOptions(model, prompts, "chat"))

# Uncomment the following lines to use OpenAI
# planner = OpenAIPlanner(
#     OpenAIPlannerOptions(
#         config.OPENAI_API_KEY,
#         config.OPENAI_MODEL_DEPLOYMENT_NAME,
#         prompt_folder=default_prompt_folder,
#     )
# )
storage = MemoryStorage()
app = Application[TurnState](
    ApplicationOptions(
        storage,
        ai=AIOptions(
            planner=planner,
        )
    )
)
from botbuilder.integration.aiohttp import (
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
)
botFrameworkAuthentication = ConfigurationBotFrameworkAuthentication(
  {},
  ServiceClientCredentialsFactory({
    MicrosoftAppId: config.botId,
    MicrosoftAppPassword: process.env.BOT_PASSWORD,
    MicrosoftAppType: "MultiTenant",
  })
)

adapter = CloudAdapterBase(botFrameworkAuthentication)

@app.turn_state_factory
async def on_state_factory(activity: Activity):
    return await AppTurnState.from_activity(activity, storage)

@app.error
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")

# 


# from config import Config

# config = Config()

# if config.OPENAI_KEY is None and config.AZURE_OPENAI_KEY is None:
#     raise Exception('Missing environment variables - please check that OPENAI_KEY or AZURE_OPENAI_KEY is set.')

# # Create AI components
# model_options = OpenAIModelOptions(api_key=config.OPENAI_KEY , default_model="gpt-3.5-turbo")

# model = OpenAIModel(model_options)

# prompts = PromptManager(PromptManagerOptions("prompts"))

# planner = ActionPlanner(ActionPlannerOptions(model, prompts, "chat"))