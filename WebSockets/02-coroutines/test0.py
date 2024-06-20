# Coroutines are functions that can be stopped and resumed while being run. 
# In Python, they are defined using the async def keyword. 
# Much like generators, they too use their own form of yield from which is await.
# Before async and await were introduced in Python 3.5, we created coroutines 
# in the exact same way generators were created (with yield from instead of await).

# Just like all iterators and generators implement the __iter__() method, 
# all coroutines implement __await__() 
# which allows them to continue on every time await coro is called.

# Ref: https://dabeaz.com/coroutines/

import asyncio

async def my_coroutine():
    print("Coroutine is starting")
    await asyncio.sleep(2)
    print("Coroutine is done")

async def main():
    print("Main function is starting")
    await my_coroutine()
    print("Main function is ending")

asyncio.run(main())

