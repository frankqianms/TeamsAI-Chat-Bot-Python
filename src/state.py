"""
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""

from typing import Optional

from botbuilder.core import Storage
from botbuilder.schema import Activity
from teams.state import DefaultConversationState, TurnState, DefaultUserState

class AppTurnState(TurnState):
    conversation: DefaultConversationState

    @classmethod
    async def from_activity(
        cls, activity: Activity, storage: Optional[Storage] = None
    ) -> "AppTurnState":
        return cls(
            conversation=await DefaultConversationState.from_activity(activity, storage),
            user=await DefaultUserState.from_activity(activity, storage),
        )