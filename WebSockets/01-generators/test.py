# firstn",  represents the first n non-negative integers, where n is a really 
# big number, and assume (for the sake of the examples in this section) that 
# each integer takes up a lot of space, say 10 megabytes each.

# Note: Please note that in real life, integers do not take up that much space,
# unless they are really, really, really, big integers. For instance you can 
# represent a 309 digit number with 128 bytes 
# (add some overhead, it will still be less than 150 bytes)

import time

# The code is quite simple and straightforward, but it builds the full list in
# memory. This is clearly not acceptable in our case, because we cannot afford 
# to keep all n "10 megabyte" integers in memory.
def first_n_1(n):
    '''Build and return a list'''
    num, nums = 0, []
    while num < n:
        nums.append(num)
        num += 1
    return nums

start_time = time.time() 
sum_of_first_n = sum(first_n_1(1000000))
end_time = time.time()
print(f"{sum_of_first_n} time_spent: {end_time - start_time}")


# So, we resort to the generator pattern. 
# The following implements generator as an
# iterable object.
# Using the generator pattern (an iterable)
# The sum is calculated as the generator yields the values. 
class first_n_2(object):
    def __init__(self, n):
        self.n = n
        self.num = 0

    def __iter__(self):
        return self

    # Python 3 compatibility
    def __next__(self):
        return self.next()

    def next(self):
        if self.num < self.n:
            cur, self.num = self.num, self.num+1
            return cur
        raise StopIteration()


start_time = time.time() 
sum_of_first_n = sum(first_n_2(1000000))
end_time = time.time()
print(f"{sum_of_first_n} time_spent: {end_time - start_time}")

# The above is a pattern that we will use over and over for many similar
# constructs. Imagine writing all that just to get an iterator.
# Python provides generator functions as a convenient shortcut to building
# iterators. Lets us rewrite the above iterator as a generator function:

# A generator that yields items instead of returning a list
def first_n_3(n):
    num = 0
    while num < n:
        yield num
        num += 1
        
start_time = time.time() 
sum_of_first_n = sum(first_n_3(1000000))
end_time = time.time()
print(f"{sum_of_first_n} time_spent: {end_time - start_time}")

# first_n_1 : 499999500000 time_spent: 0.041886091232299805
# first_n_2 : 499999500000 time_spent: 0.04609799385070801
# first_n_3 : 499999500000 time_spent: 0.017748594284057617
# Generator run much faster than the other two.

# Generator expressions provide an additional shortcut to build generators out
# of expressions similar to that of list comprehensions. In fact, we can turn
# a list comprehension into a generator expression by replacing the square 
# brackets ("[ ]") with parentheses. Alternately, we can think of list
# comprehensions as generator expressions wrapped in a list constructor.

# list comprehension
doubles = [2 * n for n in range(50)]
print(doubles)

# same as the list comprehension above
doubles = list(2 * n for n in range(50))
print(doubles)

# Notice how a list comprehension looks essentially like a generator expression
# passed to a list constructor.

numbers = list(2 * n for n in first_n_3(50))
print(numbers)
