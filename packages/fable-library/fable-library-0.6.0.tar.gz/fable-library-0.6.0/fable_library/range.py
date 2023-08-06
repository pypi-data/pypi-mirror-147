from decimal import Decimal
from typing import (TypeVar, Any, Optional, Tuple, Callable)
from .big_int import (from_zero, op_addition)
from .char import char_code_at
from .decimal import (from_parts, op_addition as op_addition_1)
from .long import op_addition as op_addition_2
from .seq import (delay, unfold)
from .util import (compare, IEnumerable)

_T = TypeVar("_T")

def make_range_step_function(step: _T, stop: _T, zero: _T, add: Any) -> Callable[[_T], Optional[Tuple[_T, _T]]]:
    step_compared_with_zero : int = compare(step, zero) or 0
    if step_compared_with_zero == 0:
        raise Exception("The step of a range cannot be zero")

    step_greater_than_zero : bool = step_compared_with_zero > 0
    def arrow_123(x: Optional[_T]=None, step: _T=step, stop: _T=stop, zero: _T=zero, add: Any=add) -> Optional[Tuple[_T, _T]]:
        compared_with_last : int = compare(x, stop) or 0
        return ((x, add(x, step))) if (True if ((compared_with_last <= 0) if step_greater_than_zero else False) else ((compared_with_last >= 0) if (not step_greater_than_zero) else False)) else None

    return arrow_123


def integral_range_step(start: _T, step: _T, stop: _T, zero: _T, add: Any) -> IEnumerable[_T]:
    step_fn : Callable[[_T], Optional[Tuple[_T, _T]]] = make_range_step_function(step, stop, zero, add)
    def arrow_124(start: _T=start, step: _T=step, stop: _T=stop, zero: _T=zero, add: Any=add) -> IEnumerable[_T]:
        return unfold(step_fn, start)

    return delay(arrow_124)


def range_big_int(start: int, step: int, stop: int) -> IEnumerable[int]:
    def arrow_125(x: int, y: int, start: int=start, step: int=step, stop: int=stop) -> int:
        return op_addition(x, y)

    return integral_range_step(start, step, stop, from_zero(), arrow_125)


def range_decimal(start: Decimal, step: Decimal, stop: Decimal) -> IEnumerable[Decimal]:
    def arrow_126(x: Decimal, y: Decimal, start: Decimal=start, step: Decimal=step, stop: Decimal=stop) -> Decimal:
        return op_addition_1(x, y)

    return integral_range_step(start, step, stop, from_parts(0, 0, 0, False, 0), arrow_126)


def range_double(start: float, step: float, stop: float) -> IEnumerable[float]:
    def arrow_127(x: float, y: float, start: float=start, step: float=step, stop: float=stop) -> float:
        return x + y

    return integral_range_step(start, step, stop, 0, arrow_127)


def range_int64(start: int, step: int, stop: int) -> IEnumerable[int]:
    def arrow_129(x: int, y: int, start: int=start, step: int=step, stop: int=stop) -> int:
        return op_addition_2(x, y)

    return integral_range_step(start, step, stop, 0, arrow_129)


def range_uint64(start: int, step: int, stop: int) -> IEnumerable[int]:
    def arrow_130(x: int, y: int, start: int=start, step: int=step, stop: int=stop) -> int:
        return op_addition_2(x, y)

    return integral_range_step(start, step, stop, 0, arrow_130)


def range_char(start: str, stop: str) -> IEnumerable[str]:
    int_stop : int = char_code_at(stop, 0) or 0
    def arrow_131(start: str=start, stop: str=stop) -> IEnumerable[str]:
        def step_fn(c: int) -> Optional[Tuple[str, int]]:
            if c <= int_stop:
                return (chr(c), c + 1)

            else: 
                return None


        return unfold(step_fn, char_code_at(start, 0))

    return delay(arrow_131)


