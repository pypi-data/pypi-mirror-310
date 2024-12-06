import sys
from asyncio import create_task, CancelledError, sleep as asleep, Task, run as arun
from functools import wraps
from math import ceil
from os import environ, get_terminal_size
from re import compile as re_compile
from sys import stdout, stderr
from threading import Thread
from time import sleep
from types import MethodType
from typing import Any, Callable, Generic, Iterable, Iterator, Optional, TypeVar
from unicodedata import category, combining, east_asian_width

if sys.platform == "win32":

    def _():
        """
        Enable virtual terminal processing for windows
        so ansi escape codes are parsed.
        """
        try:
            from ctypes import byref, c_ulong, windll
        except ImportError:
            return
        VT_PROCESSING_MODE = 0x0004
        OUTPUT_HANDLE = sys.stdout.isatty() and -11 or -12
        kernel32 = windll.kernel32
        kernel32 = windll.kernel32
        GetStdHandle = kernel32.GetStdHandle
        GetConsoleMode = kernel32.GetConsoleMode
        SetConsoleMode = kernel32.SetConsoleMode
        handle = GetStdHandle(OUTPUT_HANDLE)
        mode = c_ulong()
        GetConsoleMode(handle, byref(mode))
        mode.value |= VT_PROCESSING_MODE
        SetConsoleMode(handle, mode)

    echo = None
    _()
else:
    import termios
    from sys import stdin

    class echo:
        """
        Used to disable keystrokes from being echoed
        while the spinner is running
        """

        fd = stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        @classmethod
        def disable(cls):
            new_settings = termios.tcgetattr(cls.fd)
            new_settings[3] = new_settings[3] & ~termios.ECHO
            termios.tcsetattr(cls.fd, termios.TCSADRAIN, new_settings)

        @classmethod
        def enable(cls):
            termios.tcsetattr(cls.fd, termios.TCSADRAIN, cls.old_settings)


pattern = None


def get_pattern():
    global pattern
    if pattern:
        return pattern
    pattern = re_compile("\x1b" r"[^m]*?m")
    return pattern


def chwidth(char: str) -> int:
    if category(char) in ["Cc", "Cf"]:
        return -1
    if combining(char):
        return 0
    width = east_asian_width(char)
    if width in ["W", "F"]:
        return 2
    return 1


def terminal_width(fallback: int = 80):
    try:
        columns = max(int(environ.get("COLUMNS", 0)), 0)
    except ValueError:
        columns = 0

    if not columns:
        try:
            columns, _ = get_terminal_size(stderr.fileno())
        except (AttributeError, ValueError, OSError):
            pass
    return columns or fallback


def get_lines(text: str):
    width = terminal_width()
    text = get_pattern().sub("", text)
    check_width = not text.isascii()
    for line in text.splitlines():
        length = check_width and sum(map(chwidth, line)) or len(line)
        yield max(1, ceil(length / width))


class state:
    spinner: Optional[Any] = None
    stream = stdout.isatty() and stdout or stderr
    istty = stream.isatty()
    enabled = istty
    thread: Optional[Thread] = None
    task: Optional[Task[None]] = None


def hide_cursor():
    if echo:
        echo.disable()
    stream = state.stream
    stream.write("\x1b[?25l")
    stream.flush()


def show_cursor():
    if echo:
        echo.enable()
    stream = state.stream
    stream.write("\x1b[?25h")
    stream.flush()


T = TypeVar("T", bound=Iterator[str])


class View(Generic[T]):
    def __init__(self, frames: T) -> None:
        self.frames = frames
        self.message = ""
        self._lines = None

    def render(self):
        message = self.message
        frames = self.frames
        stream = state.stream
        self.clear()
        if self.message:
            stream.write(message)
            self.message = ""
        view = next(frames)
        stream.write(view)
        stream.flush()
        self._lines = get_lines(view)

    def clear(self):
        if not state.enabled:
            return
        lgen = self._lines
        if not lgen:
            return
        lines = sum(lgen)
        if not lines:
            return
        stream = state.stream
        if lines == 1:
            stream.write("\n")
        for _ in range(lines):
            stream.write("\x1b[F\x1b[K")


class SyncSpinner:
    view: View[Any]
    interval: float

    def __init__(self) -> None:
        self._running = False

    def __enter__(self):
        self.start()

    def __exit__(self, et: type[BaseException], e: Exception, traceback: object):
        if et is KeyboardInterrupt:
            self.stop("^c")
        else:
            self.stop()
        return self

    def loop(self):
        try:
            render = self.view.render
            interval = self.interval

            while self._running:
                render()
                sleep(interval)

        except Exception:
            self.stop()
            raise

    def start(self):
        if self._running or not state.enabled:
            return
        if state.spinner and state.spinner is not self:
            return stop()
        self._running = True
        state.spinner = self
        hide_cursor()
        state.thread = Thread(target=self.loop, daemon=True)
        state.thread.start()

    def stop(self, *epilogue: Any, sep: str = " ", end: str = "\n"):
        message = ""
        if epilogue:
            message = sep.join(map(str, epilogue)) + end
        if not state.spinner:
            return write(message)
        elif state.spinner is not self:
            write(message)
            return stop()
        self._running = False
        view = self.view
        if state.thread:
            state.thread.join()
        view.clear()
        if view.message:
            message = view.message + message
            view.message = ""
        if message:
            write(message)
        state.spinner = None
        state.thread = None
        show_cursor()

    def bind(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(self: SyncSpinner, *args: Any, **kwargs: Any):
            with self:
                return fn(self, *args, **kwargs)

        return MethodType(wrapper, self)


class AsyncSpinner:
    view: View[Any]
    interval: float

    def __init__(self) -> None:
        self._running = False

    async def __aenter__(self):
        await self.start()

    async def __aexit__(self, et: type[BaseException], e: Exception, traceback: object):
        if et is KeyboardInterrupt:
            await self.stop("^c")
        else:
            await self.stop()
        return self

    async def loop(self):
        try:
            render = self.view.render
            interval = self.interval
            while self._running:
                render()
                await asleep(interval)

        except Exception:
            await self.stop()
            raise

    async def start(self):
        if self._running or not state.enabled:
            return
        if state.spinner and state.spinner is not self:
            return stop()
        self._running = True
        state.spinner = self
        hide_cursor()
        state.task = create_task(self.loop())

    async def stop(self, *epilogue: Any, sep: str = " ", end: str = "\n"):
        message = ""
        if epilogue:
            message = sep.join(map(str, epilogue)) + end
        if not state.spinner:
            return write(message)
        elif state.spinner is not self:
            write(message)
            return stop()
        self._running = False
        if state.task:
            try:
                await state.task
            except CancelledError:
                pass
        view = self.view
        view.clear()
        if view.message:
            message = view.message + message
            view.message = ""
        write(message)
        state.spinner = None
        state.task = None
        show_cursor()

    def bind(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        async def wrapper(self: AsyncSpinner, *args: Any, **kwargs: Any):
            async with self:
                return fn(self, *args, **kwargs)

        return MethodType(wrapper, self)


def write(message: str) -> None:
    if state.istty:
        state.stream.write(message)
    else:
        state.stream.buffer.write(message.encode("utf-8"))


def stop() -> None:
    spinner = state.spinner
    if spinner:
        if isinstance(spinner, SyncSpinner):
            spinner.stop()
        elif isinstance(spinner, AsyncSpinner):
            arun(spinner.stop())
        state.spinner = None


def force():
    state.enabled = True


class FormatFrames:
    def __init__(self, label: str, frames: Iterable[str], format: str) -> None:
        self.label = label
        if not isinstance(frames, (str, list, set, tuple)):
            frames = list(frames)
        self.frames = frames
        self.format = format
        self.iterable = iter(self)

    def __next__(self) -> str:
        return next(self.iterable)

    def __iter__(self) -> Iterator[str]:
        while True:
            for frame in self.frames:
                yield self.format.format(frame=frame, label=self.label)


class XLog:
    def __init__(self, **formats: str) -> None:
        self.__dict__.update(formats)

    def __getattribute__(self, name: str) -> Optional[str]:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return None


XLOG = XLog(title=" * {message}", stage="     - {message}")


class ISpinner:
    stop: Any

    def __init__(
        self,
        label: Optional[str] = None,
        frames: Optional[str] = None,
        format: Optional[str] = None,
        interval: Optional[int] = None,
        xlog: Optional[XLog] = None,
    ) -> None:
        frame_gen = FormatFrames(
            label or "",
            frames or r"\|/-",
            format or "{frame} {label}",
        )
        self.view = View(frame_gen)
        self.interval = max(interval or 50, 50) / 1000
        self.xlog = xlog or XLOG

    @property
    def label(self) -> str:
        return self.view.frames.label

    @label.setter
    def label(self, label: str) -> None:
        self.view.frames.label = label

    def echo(self, *values: Any, sep: str = " ", end: str = "\n"):
        message = sep.join(map(str, values)) + end
        if state.spinner is not self:
            return write(message)
        self.view.message += message

    def success(self, text: str):
        fmt = self.xlog.success
        if fmt:
            text = fmt.format(message=text)
        self.stop(text)

    def error(self, text: str):
        fmt = self.xlog.error
        if fmt:
            text = fmt.format(message=text)
        self.stop(text)

    def warn(self, text: str):
        fmt = self.xlog.warn
        if fmt:
            text = fmt.format(message=text)
        self.echo(text)

    def debug(self, text: str):
        fmt = self.xlog.debug
        if fmt:
            text = fmt.format(message=text)
        self.echo(text)

    def title(self, text: str):
        fmt = self.xlog.title
        if fmt:
            text = fmt.format(message=text)
        self.echo(text)

    def stage(self, text: str):
        fmt = self.xlog.stage
        if fmt:
            text = fmt.format(message=text)
        self.echo(text)


class Xspin(ISpinner, SyncSpinner):
    def __init__(
        self,
        label: str | None = None,
        frames: str | None = None,
        format: str | None = None,
        interval: int | None = None,
        xlog: XLog | None = None,
    ) -> None:
        SyncSpinner.__init__(self)
        super().__init__(label, frames, format, interval, xlog)


class Axspin(ISpinner, AsyncSpinner):
    def __init__(
        self,
        label: str | None = None,
        frames: str | None = None,
        format: str | None = None,
        interval: int | None = None,
        xlog: XLog | None = None,
    ) -> None:
        AsyncSpinner.__init__(self)
        super().__init__(label, frames, format, interval, xlog)


class BaseSpinner(SyncSpinner):
    def __init__(self, interval: Optional[int] = None) -> None:
        super().__init__()
        self.view = View(self.frames())
        self.interval = max(interval or 50, 50) / 1000

    def frames(self) -> Iterable[str]:
        raise NotImplementedError()


class BaseAspinner(AsyncSpinner):
    def __init__(self, interval: Optional[int] = None) -> None:
        super().__init__()
        self.view = View(self.frames())
        self.interval = max(interval or 50, 50) / 1000

    def frames(self) -> Iterable[str]:
        raise NotImplementedError()
