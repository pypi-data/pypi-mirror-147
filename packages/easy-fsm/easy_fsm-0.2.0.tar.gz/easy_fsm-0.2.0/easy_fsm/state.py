from typing import Protocol, Generic, Optional

from .context import Context


class State(Protocol, Generic[Context]):
    def run(self, context: Context) -> Optional["State[Context]"]:
        raise NotImplementedError


class AsyncState(Protocol, Generic[Context]):
    async def run(self, context: Context) -> Optional["AsyncState[Context]"]:
        raise NotImplementedError
