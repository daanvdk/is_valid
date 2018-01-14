from .base import Predicate
from .explanation import Explanation
from .is_str import is_str
import re


class is_match(Predicate):
    """
    A predicate that checks if the data matches the given pattern. If a string
    is provided as a pattern this predicate will compile it first. The
    optional parameter ``flags`` allows you to specify flags for this
    aforementioned compilation.
    """

    prerequisites = [is_str]

    def __init__(self, regex, flags=0, full=False, rep=None):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)
        if rep is None:
            rep = '/{}/{}'.format(
                regex.pattern,
                ''.join(char for flag, char in [
                    (re.A, 'a'), (re.I, 'i'), (re.L, 'l'),
                    (re.M, 'm'), (re.S, 's'), (re.X, 'x'),
                ] if regex.flags & flag)
            )
        self._regex = regex
        self._full = full
        self._valid_exp = Explanation(
            True, 'match', 'Data does match {}'.format(rep)
        )
        self._not_valid_exp = Explanation(
            False, 'not_match', 'Data does not match {}'.format(rep)
        )

    def _evaluate(self, data, explain, context):
        return (
            (self._valid_exp if explain else True)
            if (
                self._regex.fullmatch(data)
                if self._full else
                self._regex.match(data)
            ) else
            (self._not_valid_exp if explain else False)
        )
