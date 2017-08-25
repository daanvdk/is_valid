import hypothesis.strategies as hs


varying = hs.one_of(hs.integers(), hs.floats(), hs.text(), hs.booleans())
for _ in range(3):
    varying = hs.one_of(
        varying,
        hs.lists(varying, max_size=10),
    )

numbers = hs.one_of(hs.integers(), hs.floats())
