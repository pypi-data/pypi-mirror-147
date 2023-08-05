from typing import Optional


class CallbackExceptionCapturer:
    """
    Instances of this class can be passed to functions expecting (Optional[Exception]) -> None
    callbacks.

    In particular, the optional exception is stored into a field - which can be inspected later
    via the "exception" property.

    It is especially handy in specific multi-threaded contexts such as testing.
    """

    def __init__(self) -> None:
        self._exception: Optional[Exception] = None

    def __call__(self, exception: Optional[Exception]) -> None:
        self._exception = exception

    @property
    def exception(self) -> Optional[Exception]:
        return self._exception
