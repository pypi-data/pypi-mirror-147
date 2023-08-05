from typing import Protocol, Generic, Optional

from .context import Context


class State(Protocol, Generic[Context]):
    def run(self, context: Context) -> Optional["State[Context]"]:
        raise NotImplementedError
