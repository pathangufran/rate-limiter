import time

def current_timestamp() -> int:
    return int(time.time())

def get_window_number(
    timestamp: int,
    window_seconds: int,
) -> int:

    if window_seconds <= 0:
        raise ValueError(
            "window_seconds must be greater than zero"
        )

    return timestamp // window_seconds

def get_window_end(
    timestamp: int,
    window_seconds: int,
) -> int:

    window_number = get_window_number(
        timestamp,
        window_seconds
    )

    return (
        (window_number + 1)
        * window_seconds
    )

def get_seconds_until_window_reset(
    timestamp: int,
    window_seconds: int,
) -> int:

    window_end = get_window_end(
        timestamp,
        window_seconds
    )

    return max(0,window_end - timestamp)