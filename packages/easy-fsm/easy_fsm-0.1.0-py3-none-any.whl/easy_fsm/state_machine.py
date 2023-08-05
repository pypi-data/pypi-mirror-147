from typing import Generic, Optional

from .context import Context
from .state import State


class StateMachine(Generic[Context]):
    def __init__(self, context: Context):
        self.context = context

    def run_from(self, state: Optional[State[Context]]):
        while state is not None:
            state = state.run(self.context)
