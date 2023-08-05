from queue import Queue
from typing import Callable, Iterable, TypeVar

from ...functional import ContinuationProvider

T = TypeVar("T")

QueueWriter = Callable[[Queue[T], ContinuationProvider, Iterable[T]], None]
QueueReader = Callable[[Queue[T], ContinuationProvider], None]
