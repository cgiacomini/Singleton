def test():
    yield 1
    yield 2
    
gen = test()
print(next(gen))
print(next(gen))
print(next(gen))