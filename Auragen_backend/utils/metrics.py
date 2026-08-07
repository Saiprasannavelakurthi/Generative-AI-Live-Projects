import time


class Timer:
    """
    Simple performance timer.

    Example:
        timer = Timer()

        timer.start()

        # Some work...

        print(timer.elapsed())
    """

    def __init__(self):
        self.start_time: float | None = None

    def start(self) -> None:
        """
        Start (or restart) the timer.
        """
        self.start_time = time.perf_counter()

    def elapsed(self) -> float:
        """
        Return elapsed time in seconds.
        """

        if self.start_time is None:
            return 0.0

        return round(
            time.perf_counter() - self.start_time,
            4,
        )

    def reset(self) -> None:
        """
        Reset the timer.
        """
        self.start_time = None

    def restart(self) -> None:
        """
        Reset and immediately start the timer.
        """
        self.start()

    def is_running(self) -> bool:
        """
        Check whether the timer has started.
        """
        return self.start_time is not None