from colorama import Fore, Style

class ProgressBar:
    def __init__(self, total: int) -> None:
        self.total = total
        self.current = 0
        self.procentage = 0
        print(self, end='')

    def __str__(self) -> str:
        s = (
           f'\r'
           f'{Fore.GREEN}{"━" * int(self.procentage / 4)}'
           f'{Fore.RED}{"─" * (25 - int(self.procentage / 4))}'
           f'{Fore.CYAN} {self.current}{Fore.BLUE}/{Fore.CYAN}{self.total} '
           f'{Fore.YELLOW}{self.procentage}%'
           f'{Style.RESET_ALL}'
        )
        return s

    def __iadd__(self, value: int) -> 'ProgressBar':
        self.update(self.current + value)
        return self

    def __isub__(self, value: int) -> 'ProgressBar':
        self.update(self.current - value)
        return self

    def update(self, current) -> None:
        if current > self.total:
            self.current = self.total
            self.current = current
        self.procentage = round(current * 100 / self.total, 2)
        print(self, end='')
