# In asyncio, apart from coroutine functions, we have 2 important objects: 
#
#      tasks 
#   and 
#      futures.


import asyncio

# Define an asynchronous function to print "Hello, World!"
async def hello():
    print("Hello, World!")

# Create an event loop
loop = asyncio.get_event_loop()

# Run the hello() coroutine until it completes
loop.run_until_complete(hello())

# Close the event loop
loop.close()

