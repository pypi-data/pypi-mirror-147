import os
import asyncio
import contextlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qtasync.qasyncio._loop import _QEventLoop


if os.name == "nt":
    from qtasync.qasyncio._windows import QtProactorEventLoop

    QtEventLoop = QtProactorEventLoop
else:
    from qtasync.qasyncio._unix import QtSelectorEventLoop  # noqa

    QtEventLoop = QtSelectorEventLoop


class QtEventLoopPolicyMixin(asyncio.DefaultEventLoopPolicy):
    def new_event_loop(self) -> "_QEventLoop":
        return QtEventLoop()


@contextlib.contextmanager
def _set_event_loop_policy(policy):
    old_policy = asyncio.get_event_loop_policy()
    asyncio.set_event_loop_policy(policy)
    try:
        yield
    finally:
        asyncio.set_event_loop_policy(old_policy)


def run(*args, **kwargs):
    with _set_event_loop_policy(QtEventLoopPolicyMixin()):
        return asyncio.run(*args, **kwargs)
