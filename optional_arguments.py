from typing import Optional


def greet(name: Optional[str] = None):
    if name:
        print("Hello, {}!".format(name))
    else:
        print("Hello, world.")


greet()
greet("Kostis")

