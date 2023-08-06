"""
Debug facilities

Copyright (c) 2022 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""
from typing import Any, Callable
from pprint import pprint


def q(x: Any, tr: Callable[[Any], Any]=lambda x: x, cond:Callable[[Any], bool]=lambda x: True) -> Any:
    """Print tr(x) when cond(x) holds, and return x.
    """
    if cond(x):
        pprint(tr(x))

    return x
