"""
Library for creating console spinners.

# Types

* SyncSpinner
* AsyncSpinner
* Xlog
* Ispinner
* Xspin
* Axspin

# Functions
* stop
"""

from typing import (
    Any,
    Callable,
    Concatenate,
    Iterable,
    Optional,
    ParamSpec,
    Self,
    TypeVar,
    Coroutine,
)

T = TypeVar("T")
Q = TypeVar("Q", bound=Coroutine[Any, Any, Any])
PS = ParamSpec("PS")

class SyncSpinner:
    """
    - Base class for spinners running synchronously.
    - Started and stopped using the `start` and `stop` methods.
    - Can be used with a `with` statement.
    """
    def __enter__(self) -> Self:
        pass

    def __exit__(self, et: type[Exception], e: Exception, tb: object) -> None:
        pass

    def start(self) -> None:
        """Starts the synchronous spinner."""

    def stop(self, *epilogue: Any, sep: str = " ", end: str = "\n") -> None:
        """
        Stops the synchronous spinner.

        # Parameters

        * `values`
            The values to be logged.
        * `sep`
            The string used to join the values into one string.
        * `end`
            The character logged at the end.
        """

    def bind(self, fn: Callable[Concatenate[Self, PS], T]) -> Callable[PS, T]:
        """
        Binds a function to a spinner such that when the function is called
        the spinner runs in the background.

        # Parameter

        * fn
            The function being bound. It should take in the spinner instance as
            its first parameter.

        # Example
        >>> spinner = Xspin("Running ...")
            @spinner.bind
            def pause(sp: Axspin, time: int):
                sleep(time)
                sp.echo("Done!")

        ... pause(5)
        """

class AsyncSpinner:
    """
    - Base class for spinners running asynchronously.
    - Started and stopped using the async `start` and `stop` methods.
    - Can be used with a `async with` statement.
    """
    async def __aenter__(self) -> Self:
        pass

    async def __aexit__(self, et: type[Exception], e: Exception, tb: object) -> None:
        pass

    async def start(self) -> None:
        """Starts the async spinner."""

    async def stop(self, *epilogue: Any, sep: str = " ", end: str = "\n") -> None:
        """
        Stops the async spinner.

        # Parameters

        * `values`
            The values to be logged.
        * `sep`
            The string used to join the values into one string.
        * `end`
            The character logged at the end.

        """

    def bind(self, fn: Callable[Concatenate[Self, PS], Q]) -> Callable[PS, Q]:
        """
        Binds an async function to a spinner such that when the function is awaited
        the spinner runs in the background.

        # Parameter

        * fn
            The function being bound. It should take in the spinner instance as
            its first parameter.

        # Example
        >>> spinner = Axspin("Running ...")
            @spinner.bind
            async def pause(sp: Axspin, time: int):
                await sleep(time)
                sp.echo("Done!")

        ... async def main():
                await pause(5)
        """

class XLog:
    """
    Object used to store the rules for formating
    log messages. The formats follow python's format
    string templating, but must contain a `text` parameter.

    # Example
    >>> error_format = "!! {text}"
    """
    def __init__(
        self,
        *,
        success: Optional[str] = None,
        error: Optional[str] = None,
        warn: Optional[str] = None,
        debug: Optional[str] = None,
        title: Optional[str] = None,
        stage: Optional[str] = None,
    ) -> None:
        pass

class ISpinner:
    """
    Interface for common attributes between Synchronous
    and async spinners.
    """
    def __init__(
        self,
        label: Optional[str] = None,
        frames: Optional[str] = None,
        format: Optional[str] = None,
        interval: Optional[int] = None,
        xlog: Optional[int] = None,
    ) -> None:
        """
        # Parameters

        * label
            The text displayed relative to the frames.
        * frames
            The characters changing on each spinner render.
        * format
            Rule defining the relative position of the label
            to the frame. eg "{frame} {label}"
        * interval
            Time in milliseconds between each spinner render.
        * xlog
            The logging configuration for the spinner that'll
            be used in the logging methods.
        """

    @property
    def label(self) -> str:
        """The text displayed relative to the spinner frames."""

    @label.setter
    def label(self, label: str) -> str:
        pass

    def echo(self, *values: Any, sep: str = " ", end: str = "\n") -> None:
        """
        Used for logging when the spinner is running.

        # Parameters

        * `values`
            The values to be logged.
        * `sep`
            The string used to join the values into one string.
        * `end`
            The character logged at the end.
        """

    def success(self, text: str) -> None:
        """
        Used when stopping a spinner if the process was successful.

        # Parameter

        * `text`
            The message to be logged.

        """

    def error(self, text: str) -> None:
        """
        Used when stopping a spinner when the process was
        unsuccessful.

        # Parameter

        * `text`
            The message to be logged.
        """

    def warn(self, text: str) -> None:
        """
        Used for printing warnings.
        # Parameter

        * `text`
            The message to be logged.
        """

    def debug(self, text: str) -> None:
        """
        Used for printing debug information.

        # Parameter

        * `text`
            The message to be logged.

        """

    def title(self, text: str) -> None:
        """
        Used mark the onset of a task in the process.

        # Parameter

        * `text`
            The message to be logged.
        """

    def stage(self, text: str) -> None:
        """
        Used to indicate a step in a task.

        # Parameter

        * `text`
            The message to be logged.
        """

class Xspin(ISpinner, SyncSpinner):
    r"""
    - Creates sync spinners.
    - Uses python format templating to define the label's position
    relative to the spinner.
    - Can take in an `Xlog` instance to define the formats used in
    the logging methods.

    # Example
    >>> spinner = Xspin(
            label="Donwnlading ...",
            frames="\|/-",
            interval=50,
        )
        with spinner as sp:
            sleep(5)
            sp.success("Done!")
    """

class Axspin(ISpinner, AsyncSpinner):
    r"""
    - Creates async spinners.
    - Uses python format templating to define the label's position
    relative to the spinner.
    - Can take in an `Xlog` instance to define the formats used in
    the logging methods.
    # Example
    >>> async def main():
            spinner = Axspin(
                label="Donwnlading ...",
                frames="\|/-",
                interval=50,
            )
            async with spinner as sp:
                await sleep(5)
                sp.success("Done!")
    """

class BaseSpinner(SyncSpinner):
    """
    - Base class for custom synchronous spinners.
    - Relies on the `frames` method to get the spinner's
    frame.
    """
    def __init__(self, interval: Optional[int] = None) -> None:
        """
        # Params

        * `interval`
            Time in milliseconds between each frame render.
        """

    def frames(self) -> Iterable[str]:
        """Generator for the spinner's frames."""

class BaseAspinner(AsyncSpinner):
    """
    - Base class for custom async spinners.
    - Relies on the `frames` method to get the spinner's
    frame.
    """
    def __init__(self, interval: Optional[int] = None) -> None:
        """
        # Params

        * `interval`
            Time im milliseconds between each frame render
        """

    def frames(self) -> Iterable[str]:
        """Generator for the spinner's frames."""

def stop() -> None:
    """Stops the spinner running currently."""

def force() -> None:
    """
    Forces the spinners to render even when the
    output stream is not a terminal device.
    """
