from typing import Any, Callable, TypeVar, Union

AnyCallable = Callable[..., Any]

T = TypeVar("T")

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")

Consumer = Callable[[TInput], None]
Producer = Callable[[], TOutput]
Lender = Callable[[], TOutput]

Unit = Callable[[], None]
TriggerListener = Callable[[], None]

Result = Union[TOutput, Exception]

Mapper = Callable[[TInput], TOutput]
Predicate = Mapper[TInput, bool]

ContinuationProvider = Producer[bool]
