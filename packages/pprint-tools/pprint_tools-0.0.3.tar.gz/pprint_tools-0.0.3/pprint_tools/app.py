import asyncio
import functools
import inspect
import time
from contextlib import contextmanager
from typing import Any, Callable, Coroutine, Generator

from logrich import log


class SyncAsyncDeco:
    """Фабрика декораторов. Декорирует как синхронный так и асинхронный код."""

    def __init__(self, payload: Callable) -> None:
        # payload - тот дополнительный функционал, что появиться в результате декорирования
        self.payload = contextmanager(payload)

    def __call__(self, *args_or_func: list[Callable] | Callable, **deco_kwargs: Any) -> Callable:
        # args_or_func - может быть пустым списком, если декоратор без скобок
        # или списком из одного эл-та - декорируемой функции
        # метод будет вызван на этапе загрузки модуля
        def inner(func: Callable):  # noqa WPS430
            def wrapper():  # noqa WPS430
                def decorating_context(*args_context, **kwargs_context) -> Any:  # noqa WPS430
                    # deco_kwargs замыкается как параметр метода __call__
                    # *args_context, **kwargs_context замыкаются как параметры decorating_context
                    return self.payload(func, deco_kwargs, *args_context, **kwargs_context)

                return self.decorate_sync_async(
                    func=func,
                    decorating_context=decorating_context,
                )

            return wrapper()

        return (
            args_or_func and callable(args_or_func[0]) and inner(args_or_func[0]) or inner
        )  # noqa

    @staticmethod
    def decorate_sync_async(func: Callable, decorating_context: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):

            async def async_decorated(
                *args: list, **kwargs: dict
            ) -> Coroutine[Any, Any, Callable]:  # noqa WPS430
                with decorating_context(*args, **kwargs):
                    return await func(*args, **kwargs)

            return functools.wraps(func)(async_decorated)

        def decorated(*args: list, **kwargs: dict) -> Callable:  # noqa WPS430
            with decorating_context(*args, **kwargs):
                return func(*args, **kwargs)

        return functools.wraps(func)(decorated)


def dump_args_def(
    func: Callable,
    deco_kwargs: dict[str, Any],
    *args,
    **kwargs,
) -> Generator:
    """Печатает аргументы функции перед запуском, по выполнении печатает затраченное время."""

    if deco_kwargs.get("skip"):
        yield
        return

    file = inspect.getsourcefile(func)
    file = file and file[-35:]
    _, line = inspect.getsourcelines(func)
    log.start(f":yarn: [cyan]{func.__name__}[/]", file_name=file, line=line + 1)
    arg_lst = {k + 1: repr(v) for k, v in enumerate(args)}
    # arg_lst = {k + 1: reprlib.repr(v) for k, v in enumerate(args)}
    args and log.list(arg_lst, title="Position arguments")  # noqa WPS428
    kwargs and log.list(kwargs, title="Named arguments")  # noqa WPS428
    tic = time.perf_counter()
    yield
    toc = time.perf_counter()
    delta = toc - tic
    format_time = f"[yellow1 r i] {delta:0.3f} [/][steel_blue] sec.[/]"
    log.end(
        f":clock1: [cyan]{func.__name__}[/][gray70]...[/]{format_time}",
        file_name=file,
        line=line + 1,
    )


def elapce_timer(
    func: Callable,
    deco_kwargs: dict[str, Any],
    *args,  # noqa
    **kwargs,  # noqa
) -> Generator:
    """Печатает время выполнения кода."""

    tic = time.perf_counter()
    yield
    toc = time.perf_counter()
    delta = toc - tic

    format_time = f"[yellow1 r i] {delta:0.3f} [/] sec."
    if delta > deco_kwargs.get("over", 1):
        _, line = inspect.getsourcelines(func)
        file = inspect.getsourcefile(func)
        file = file and file[-30:]
        log.elapce(
            f":clock1: [cyan]{func.__name__}[/][gray70]...[/]{format_time}",
            file_name=file,
            line=line,
        )


dump_args = SyncAsyncDeco(payload=dump_args_def)
timer = SyncAsyncDeco(payload=elapce_timer)
