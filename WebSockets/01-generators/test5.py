# Suppose you have two generators, gen1 and gen2, and you want to yield all the
# values from both generators combined. Instead of manually iterating over each
# generator and yielding its values, you can use yield from to delegate this 
# task to another generator.

def gen1():
    for i in range(3):
        print(f"gen1: {i}")
        yield i

def gen2():
    for i in range(3, 6):
        print(f"gen2: {i}")
        yield i

def combined_generator():
    yield from gen1()  # Yield all values from gen1
    yield from gen2()  # Yield all values from gen2
        
# Using the combined generator
combined = combined_generator()
for value in combined:
    print(value)

# Inner Generator Delegation:
def outer_generator():
    inner_values = ['a', 'b', 'c']
    for value in inner_values:
        yield value

def main_generator():
    yield 'Start'
    yield from outer_generator()  # Delegate to the outer generator
    yield 'End'

# Using the main generator
gen = main_generator()
for value in gen:
    print(value)

