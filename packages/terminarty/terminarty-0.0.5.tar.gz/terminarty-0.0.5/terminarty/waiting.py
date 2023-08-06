import time
import threading
from colorama import Fore, Style
from typing import Optional

class Waiting:
    def __init__(self, doing: str, delay: Optional[float] = 0.3) -> None:
        self.doing = doing.strip().rstrip('...')
        self.delay = delay
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def __enter__(self) -> 'Waiting':
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._stop()
        if exc_type is not None:
            print(f'\r{self.doing}... {Fore.RED}ERROR{Style.RESET_ALL}')
        else:
            print(f'\r{self.doing}... {Fore.GREEN}DONE{Style.RESET_ALL}')

    def _loop(self):
        dots = 1
        while self._running:
            print(f'\r{self.doing}{dots * "."}{" " * (3 - dots)}{Style.RESET_ALL}', end='')
            dots += 1 if dots < 3 else -2
            time.sleep(self.delay)

    def _stop(self) -> None:
        self._running = False
        self._thread.join()

    def start(self) -> None:
        self._running = True
        self._thread.start()

    def done(self) -> None:
        self._stop()
        print(f'\r{self.doing}... {Fore.GREEN}DONE{Style.RESET_ALL}')

    def error(self) -> None:
        self._stop()
        print(f'\r{self.doing}... {Fore.RED}ERROR{Style.RESET_ALL}')