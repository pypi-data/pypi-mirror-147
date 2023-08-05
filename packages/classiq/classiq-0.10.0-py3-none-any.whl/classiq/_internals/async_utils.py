import asyncio
import itertools
import time
from typing import (
    AsyncGenerator,
    Awaitable,
    Callable,
    Iterable,
    Optional,
    SupportsFloat,
    TypeVar,
    Union,
)

T = TypeVar("T")


def enable_jupyter_notebook() -> None:
    import nest_asyncio  # type: ignore[import]

    nest_asyncio.apply()


def _make_iterable_interval(
    interval_sec: Union[SupportsFloat, Iterable[SupportsFloat]]
) -> Iterable[float]:
    if isinstance(interval_sec, Iterable):
        return map(float, interval_sec)
    return itertools.repeat(float(interval_sec))


async def poll_for(
    poller: Callable[..., Awaitable[T]],
    timeout_sec: Optional[float],
    interval_sec: Union[float, Iterable[float]],
) -> AsyncGenerator[T, None]:
    if timeout_sec is not None:
        end_time = time.perf_counter() + timeout_sec
    else:
        end_time = None
    interval_sec_it = iter(_make_iterable_interval(interval_sec))
    while end_time is None or time.perf_counter() < end_time:
        yield await poller()
        cur_interval_sec = next(interval_sec_it)
        if cur_interval_sec:
            await asyncio.sleep(cur_interval_sec)


# =======================================================================
# According to stackoverflow.com's license
# taken from:
#   https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
# from the user:
#   https://stackoverflow.com/users/2132753/gustavo-bezerra
def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__  # type: ignore[name-defined]
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


# =======================================================================
