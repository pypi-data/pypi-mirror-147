"""Helpers to let you quickly define epoch / batching semantics.

Use these to wrap an existing iterator which yields items.

"""

import datetime
import heapq

from .bytewax import AdvanceTo, Emit

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Tuple


def yield_epochs(fn: Callable):
    """A decorator function to unwrap an iterator of [epoch, item]
    into successive `AdvanceTo` and `Emit` classes with the
    contents of the iterator.

    Use this when you have an input_builder function that returns
    a generator of (epoch, item) to be used with `cluster_main` or
    `spawn_cluster`:

    >>> from bytewax import Dataflow, cluster_main
    >>> from bytewax.inputs import yield_epochs, fully_ordered
    >>> flow = Dataflow()
    >>> flow.capture()
    >>> @yield_epochs
    ... def input_builder(i, n):
    ...   return fully_ordered(["a", "b", "c"])
    >>> cluster_main(flow, input_builder, lambda i, n: print, [], 0, 1)
    (0, 'a')
    (1, 'b')
    (2, 'c')
    """

    def inner_fn(worker_index, worker_count):
        gen = fn(worker_index, worker_count)
        for (epoch, item) in gen:
            yield AdvanceTo(epoch)
            yield Emit(item)

    return inner_fn


def single_batch(wrap_iter: Iterable) -> Iterable[Tuple[int, Any]]:
    """All input items are part of the same epoch.

    Use this for non-streaming-style batch processing.

    >>> from bytewax import Dataflow, run
    >>> flow = Dataflow()
    >>> flow.capture()
    >>> out = run(flow, single_batch(["a", "b", "c"]))
    >>> sorted(out)
    [(0, 'a'), (0, 'b'), (0, 'c')]

    Args:

        wrap_iter: Existing input iterable of just items.

    Yields:

        Tuples of `(epoch, item)`.

    """
    for item in wrap_iter:
        yield (0, item)


def tumbling_epoch(
    wrap_iter: Iterable,
    epoch_length: Any,
    time_getter: Callable[[Any], Any] = lambda _: datetime.datetime.now(),
    epoch_start_time: Any = None,
    epoch_start: int = 0,
) -> Iterable[Tuple[int, Any]]:
    """All inputs within a tumbling window are part of the same epoch.

    The time of the first item will be used as start of the 0
    epoch. Out-of-order items will cause issues as Bytewax requires
    inputs to dataflows to be in epoch order. See
    `bytewax.inputs.fully_ordered()`.

    >>> from bytewax import Dataflow, run
    >>> items = [
    ...     {
    ...         "timestamp": datetime.datetime(2022, 2, 22, 1, 2, 3),
    ...         "value": "a",
    ...     },
    ...     {
    ...         "timestamp": datetime.datetime(2022, 2, 22, 1, 2, 4),
    ...         "value": "b",
    ...     },
    ...     {
    ...         "timestamp": datetime.datetime(2022, 2, 22, 1, 2, 8),
    ...         "value": "c",
    ...     },
    ... ]
    >>> flow = Dataflow()
    >>> flow.map(lambda item: item["value"])
    >>> flow.capture()
    >>> out = run(flow, tumbling_epoch(
    ...     items,
    ...     datetime.timedelta(seconds=2),
    ...     lambda item: item["timestamp"],
    ... ))
    >>> sorted(out)
    [(0, 'a'), (0, 'b'), (2, 'c')]

    By default, uses "ingestion time" and you don't need to specify a
    way to access the timestamp in each item.

    >>> import pytest; pytest.skip("Figure out sleep in test.")
    >>> items = [
    ...     "a", # sleep(4)
    ...     "b", # sleep(1)
    ...     "c",
    ... ]
    >>> list(tumbling_epoch(items, datetime.timedelta(seconds=2)))
    [(0, 'a'), (2, 'b'), (2, 'c')]

    Args:

        wrap_iter: Existing input iterable of just items.

        epoch_length: Length of each epoch window.

        time_getter: Function that returns a timestamp given an
            item. Defaults to current wall time.

        epoch_start_time: The timestamp that should correspond to
            the start of the 0th epoch. Otherwise defaults to the time
            found on the first item.

        epoch_start: The integer value to start counting epochs from.
            This can be used for continuity during processing.

    Yields:

        Tuples of `(epoch, item)`.

    """
    for item in wrap_iter:
        time = time_getter(item)

        if epoch_start_time is None:
            epoch_start_time = time
            epoch = epoch_start
        else:
            epoch = int((time - epoch_start_time) / epoch_length) + epoch_start

        yield (epoch, item)


def fully_ordered(wrap_iter: Iterable) -> Iterable[Tuple[int, Any]]:
    """Each input item increments the epoch.

    Be careful using this in high-volume streams with many workers, as
    the worker overhead goes up with finely granulated epochs.

    >>> from bytewax import Dataflow, run
    >>> flow = Dataflow()
    >>> flow.capture()
    >>> out = run(flow, fully_ordered(["a", "b", "c"]))
    >>> sorted(out)
    [(0, 'a'), (1, 'b'), (2, 'c')]

    Args:

        wrap_iter: Existing input iterable of just items.

    Yields:

        Tuples of `(epoch, item)`.

    """
    epoch = 0
    for item in wrap_iter:
        yield (epoch, item)
        epoch += 1


@dataclass
class _HeapItem:
    """Wrapper class which holds pairs of time and item for implementing
    `sorted_window()`.

    We need some class that has an ordering only based on the time.

    """

    time: Any
    item: Any

    def __lt__(self, other):
        """Compare just by timestamp. Ignore the item."""
        return self.time < other.time


def sorted_window(
    wrap_iter: Iterable,
    window_length: Any,
    time_getter: Callable[[Any], Any],
    on_drop: Callable[[Any], None] = None,
) -> Iterable[Tuple[int, Any]]:
    """Sort a iterator to be increasing by some timestamp.

    To support a possibly infinite iterator, store a limited sorted
    buffer of items and only emit things downstream once a certain
    window of time has passed, as indicated by the timestamp on new
    items.

    New input items which are older than those already emitted will be
    dropped to maintain sorted output.

    The window length needs to be tuned for how "out of order" your
    input data is and how much data you're willing to drop: Already
    perfectly ordered input data can have a window of "0" and nothing
    will be dropped. Completely reversed input data needs a window
    that is the difference between the oldest and youngest timestamp
    to ensure nothing will be dropped.

    >>> from bytewax import Dataflow, run
    >>> items = [
    ...     {
    ...         "timestamp": datetime.datetime(2022, 2, 22, 1, 2, 4),
    ...         "value": "c",
    ...     },
    ...     {
    ...         "timestamp": datetime.datetime(2022, 2, 22, 1, 2, 3),
    ...         "value": "b",
    ...     },
    ...     {
    ...         "timestamp": datetime.datetime(2022, 2, 22, 1, 2, 0),
    ...         "value": "a",
    ...     },
    ... ]
    >>> sorted_items = list(
    ...     sorted_window(
    ...         items,
    ...         datetime.timedelta(seconds=2),
    ...         lambda item: item["timestamp"],
    ...     )
    ... )
    >>> sorted_items
    [{'timestamp': datetime.datetime(2022, 2, 22, 1, 2, 3), 'value': 'b'},
    {'timestamp': datetime.datetime(2022, 2, 22, 1, 2, 4), 'value': 'c'}]

    You could imagine using it with `tumbling_epoch()` to ensure you
    get in-order, bucketed data into your dataflow.

    >>> flow = Dataflow()
    >>> flow.map(lambda item: item["value"])
    >>> flow.capture()
    >>> out = run(flow, tumbling_epoch(
    ...     sorted_items,
    ...     datetime.timedelta(seconds=0.5),
    ...     lambda item: item["timestamp"],
    ... ))
    >>> sorted(out)
    [(0, 'b'), (2, 'c')]

    Args:

        wrap_iter: Existing input iterable.

        window_length: Buffering duration. Values will be emitted once
            this amount of time has passed.

        time_getter: Function to call to produce a timestamp for each
            value.

        on_drop: Function to call with each dropped item. E.g. log or
            increment metrics on drop events to refine your window
            length.

    Yields:

        Values in increasing timestamp order.

    """
    sorted_buffer = []
    newest_time = None
    drop_older_than = None

    def is_too_late(time):
        return drop_older_than is not None and time <= drop_older_than

    def is_newest_item(time):
        return newest_time is None or time > newest_time

    def emit_all(emit_older_than):
        while len(sorted_buffer) > 0 and sorted_buffer[0].time <= emit_older_than:
            sort_item = heapq.heappop(sorted_buffer)
            yield sort_item.item

    for item in wrap_iter:
        time = time_getter(item)

        if is_too_late(time):
            if on_drop:
                on_drop(item)
        else:
            heapq.heappush(sorted_buffer, _HeapItem(time, item))

            if is_newest_item(time):
                newest_time = time
                drop_older_than = time - window_length

                yield from emit_all(drop_older_than)

    yield from emit_all(newest_time)
