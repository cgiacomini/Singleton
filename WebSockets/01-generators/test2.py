# Send Method Purpose:
# Resumes Execution: 
#     When a generator function yields using the yield keyword,
#     its execution pauses at that point. 
#     The send() method is used to resume the generator's execution from the
#     paused state.
# Sends Value:
#     You can optionally send a value along with the send() method call. 
#     This value becomes the result of the current yield expression within the
#     generator function. It allows you to dynamically influence the 
#     generator's behavior based on the sent value.

def simple_generator():
  print("Starting the generator...")
  value = yield  # Pause at the first yield
  print(f"Received value: {value}")
  another_value = yield value * 2  # Pause at the second yield
  print(f"Received another value: {another_value}")
  print("Generator finishing...")

# Create the generator object
generator = simple_generator()

# Start the generator (sends None as the initial value)
first_result = next(generator)  # "Starting the generator..."
print(first_result)  # None (result of the first yield)

# Send a value to the generator (modifies the second yield)
second_result = generator.send(10)  # "Received value: 10"
print(second_result)  # 20 (value * 2 from the second yield)

# Generator finishes execution
try:
  third_result = generator.send("hello")  # This will raise a StopIteration exception
except StopIteration as e:
  print(e.value)  # "Generator finishing..." (if the generator returns a value)

print("Generator iteration complete.")