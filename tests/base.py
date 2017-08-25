import re

import hypothesis.strategies as hs


varying = hs.one_of(hs.integers(), hs.floats(), hs.text(), hs.booleans())
for _ in range(3):
    varying = hs.one_of(
        varying,
        hs.lists(varying, max_size=10),
    )

numbers = hs.one_of(hs.integers(), hs.floats())


regexs = [r'\d+', r'^foo(bar){3}$', re.compile(r'^FoOBaR$', flags=re.I)]


@hs.composite
def regex_with_match(draw):
    regex = draw(hs.sampled_from(regexs))
    match = draw(hs.from_regex(regex))
    return (regex, match)
