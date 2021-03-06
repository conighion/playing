from lxml import etree as et
from typing import Optional

# Trick 1: Typing and Optional Arguments
from typing import Optional


def greet(name: Optional[str] = None):
    if name:
        print("Hello, {}!".format(name))
    else:
        print("Hello, world.")

import lxml

lxml.etree
