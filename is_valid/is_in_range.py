from .base import Predicate
from .explanation import Explanation
from .is_lt import is_lt
from .is_leq import is_leq
from .is_gt import is_gt
from .is_geq import is_geq


class is_in_range(Predicate):
    """
    Generates a predicate that checks if the data is within the range specified
    by ``start`` and ``stop``. The optional arguments ``start_in`` and
    ``stop_in`` specify whether respectively ``start`` and ``stop`` should be
    included or excluded from the range.
    """

    def __init__(
        self, start, stop,
        start_in=True, stop_in=False, start_rep=None, stop_rep=None
    ):
        if start_rep is None:
            start_rep = repr(start)
        if stop_rep is None:
            stop_rep = repr(stop)
        self._start = (is_geq if start_in else is_gt)(start, rep=start_rep)
        self._stop = (is_leq if stop_in else is_lt)(stop, rep=stop_rep)
        self._valid_exp = Explanation(
            True, 'in_range',
            self._start._valid_exp.message + ' and ' +
            self._stop._valid_exp.message,
        )

    def _evaluate_explain(self, data, context):
        res = self._start.explain(data, context)
        if not res:
            return res
        res = self._stop.explain(data, context)
        if not res:
            return res
        return self._valid_exp

    def _evaluate_no_explain(self, data, context):
        return (
            self._start(data, context=context) and
            self._stop(data, context=context)
        )
