"""Deterministic fake clock for offline testing."""
import contextlib
import datetime
from typing import Generator
from unittest.mock import patch
import zoneinfo

DHAKA_TZ = zoneinfo.ZoneInfo("Asia/Dhaka")


class FakeClock:
    """Deterministic, thread-safe controllable clock."""

    def __init__(self, initial_datetime: datetime.datetime | None = None) -> None:
        if initial_datetime is None:
            # Baseline pinned date: 2026-10-06 00:00:00 in Asia/Dhaka
            self._current_dt = datetime.datetime(2026, 10, 6, 0, 0, 0, tzinfo=DHAKA_TZ)
        else:
            if initial_datetime.tzinfo is None:
                self._current_dt = initial_datetime.replace(tzinfo=DHAKA_TZ)
            else:
                self._current_dt = initial_datetime
        self._monotonic_val = 1000.0

    def now(self, tz: datetime.tzinfo | None = None) -> datetime.datetime:
        target_tz = tz or DHAKA_TZ
        return self._current_dt.astimezone(target_tz)

    def time(self) -> float:
        return self._current_dt.timestamp()

    def monotonic(self) -> float:
        return self._monotonic_val

    def advance(self, seconds: float) -> datetime.datetime:
        if seconds < 0:
            raise ValueError("Cannot advance time backward")
        self._current_dt += datetime.timedelta(seconds=seconds)
        self._monotonic_val += seconds
        return self._current_dt


@contextlib.contextmanager
def freeze_time(
    initial_datetime: datetime.datetime | None = None,
) -> Generator[FakeClock, None, None]:
    """
    Context manager that freezes time.time(), time.monotonic(), and django timezone.now()
    to a controllable FakeClock instance.
    """
    clock = FakeClock(initial_datetime)

    with (
        patch("time.time", side_effect=clock.time),
        patch("time.monotonic", side_effect=clock.monotonic),
    ):
        try:
            import django.utils.timezone as dj_tz
            with patch("django.utils.timezone.now", side_effect=clock.now):
                yield clock
        except ImportError:
            yield clock
