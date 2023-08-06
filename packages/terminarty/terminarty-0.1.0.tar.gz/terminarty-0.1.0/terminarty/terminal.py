from colorama import Fore, Style
from typing import Optional
import os
import sys

class Terminal:
    _instantiated = False
    INPUT_STYLE = f'{Fore.YELLOW} > {Style.RESET_ALL}'

    def __init__(self) -> None:
        if Terminal._instantiated:
            raise RuntimeError('Only one instance of Terminal is allowed')
        Terminal._instantiated = True

    @staticmethod
    def clear() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def input(text: str) -> str:
        Terminal.clear()
        print(text)
        inp = input(Terminal.INPUT_STYLE)
        Terminal.clear()
        return inp

    @staticmethod
    def choise(text: str, choises: list[str]) -> str:
        inp = 0
        while not isinstance(inp, int) or inp < 1 or inp > len(choises):
            Terminal.clear()
            print(text)
            for i, c in enumerate(choises):
                print(f'{Fore.RED}[{Fore.YELLOW}{i + 1}{Fore.RED}]{Style.RESET_ALL} {c}')
            try:
                inp = int(input(Terminal.INPUT_STYLE).strip())
            except ValueError:
                pass
        Terminal.clear()
        return choises[inp - 1]