import time
from typing import Union
from mmget.reporters.reporter import Reporter, ReporterItemState


class ThreadSafeProgressReporter(Reporter):
    def __init__(self, wrapped: Reporter, loop):
        self._wrapped = wrapped
        self._loop = loop
        self._last_progress_time = {}  # Store last progress time for each id
        self._debounce_interval = 1.0  # 1 second debounce interval

    def set_reporter(self, reporter):
        self._wrapped = reporter

    def add_report_item(self) -> int:
        raise NotImplementedError(
            "ThreadSafeProgressReporter: Don't call add_report_item"
        )

    def set_title(self, id: int, title: str):
        self._loop.call_soon_threadsafe(
            lambda: self._wrapped.set_title(id, title)
        )

    def set_state(self, id: int, state: ReporterItemState):
        self._loop.call_soon_threadsafe(
            lambda: self._wrapped.set_state(id, state)
        )

    def set_progress(self, id: int, bytes_received: int, total_bytes: int):
        # Add debouncer to prevent 'IOPub data rate exceeded
        # in Jupyter notebook' error in jupyter
        current_time = time.time()
        last_time = self._last_progress_time.get(id, 0)

        if (
            current_time - last_time >= self._debounce_interval
            or bytes_received == total_bytes
        ):
            self._last_progress_time[id] = current_time
            self._loop.call_soon_threadsafe(
                lambda: self._wrapped.set_progress(
                    id, bytes_received, total_bytes
                )
            )

    def show_message(self, id: int, message: str):
        self._loop.call_soon_threadsafe(
            lambda: self._wrapped.show_message(id, message)
        )

    def ask_options(self, id: int, message: str, options, callback):
        self._loop.call_soon_threadsafe(
            lambda: self._wrapped.ask_options(id, message, options, callback)
        )

    def can_ask_options(self) -> bool:
        return self._wrapped.can_ask_options()

    def set_error(self, id: int, error: Union[str, Exception]):
        self._loop.call_soon_threadsafe(
            lambda: self._wrapped.set_error(id, error)
        )

    def start(self):
        raise NotImplementedError()

    def stop(self, message: str = None):
        raise NotImplementedError()
