from src.bot import *
from teams import ConversationHistory, ConversationState, TempState, UserState
from botbuilder.schema import ChannelAccount, ConversationAccount
from unittest.mock import MagicMock 

# mock the TurnContext object
context=MagicMock(spec=TurnContext)

# mock the TurnState object
temp=TempState(input='hi', history='', output='')
user=UserState(__key__='mock_key', channel=ChannelAccount())
conversation=ConversationState(
    __key__='mock_key',
    account=ConversationAccount(),
    channel=ChannelAccount(),
    history=ConversationHistory()
)
state=TurnState(
    temp=temp,
    user=user,
    conversation=conversation
)