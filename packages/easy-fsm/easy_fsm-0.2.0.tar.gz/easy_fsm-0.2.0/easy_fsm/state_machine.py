from typing import Generic, Optional

from .context import Context
from .state import State, AsyncState


class StateMachine(Generic[Context]):
    def __init__(self, context: Context):
        self.context = context

    def run_from(self, state: Optional[State[Context]]):
        while state is not None:
            state = state.run(self.context)


class AsyncStateMachine(Generic[Context]):
    def __init__(self, context: Context):
        self.context = context

    async def run_from(self, state: Optional[AsyncState[Context]]):
        while state is not None:
            state = await state.run(self.context)
