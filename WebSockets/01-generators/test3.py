def test():
    yield 1
    return "abc"

gen = test()
print(next(gen))

try:
    next(gen)
except StopIteration as exc:
    print(exc.value)