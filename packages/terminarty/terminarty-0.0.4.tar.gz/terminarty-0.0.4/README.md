# Terminarty 
###### A simple CLI helper for Python
[![License: MIT](https://img.shields.io/pypi/l/terminarty)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/pypi/v/terminarty)](https://pypi.org/project/terminarty/)
[![Python versions](https://img.shields.io/pypi/pyversions/terminarty)](https://python.org/)
[![Downloads](https://img.shields.io/pypi/dm/terminarty)](https://pypi.org/project/terminarty/)

## Installation

```bash
$ pip install terminarty
```
## Features
**Inputs**
```python
from terminarty import Terminal

terminal = Terminal()

name = terminal.input("What is your name?")
```
!["What is yout name?"](https://imgur.com/huf4E5P.png)

**Choises**
```python
from terminarty import Choises

choise = Choises.choise(["red", "green", "blue"], "What is your favorite color?")

if choise == "green":
    print("I like green too!")
else:
    print("Ok.")
```
!["What is your favorite color?" (red, green, blue)](https://imgur.com/NQwkfj6.png)

**Text Boxes**
```python
from terminarty import Box, BoxStyles

print(Box("Hello World!", BoxStyles.Ascii))
```
There are several box styles available.
```text
Ascii:
    +───────────+
    │Hello World│
    +───────────+
Thin:
    ┌───────────┐
    │Hello World│
    └───────────┘
Thick:
    ┏━━━━━━━━━━━┓
    ┃Hello World┃
    ┗━━━━━━━━━━━┛
Double:
    ╔═══════════╗
    ║Hello World║
    ╚═══════════╝
Round:
    ╭───────────╮
    │Hello World│
    ╰───────────╯
```

## And that is all?
*Yes.*