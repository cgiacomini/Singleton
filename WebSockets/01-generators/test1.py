def first_n_new(n):
    """Yields the first n numbers starting from where it left off."""
    num = 0
    while True:
        new_start = yield num
        if new_start is not None:
            num = new_start
        num += 1
        if num >= n:
            break

# Example usage with restarting from a specific value
gen = first_n_new(100)  # Initial iteration (starts from 0)
print(next(gen))
print(next(gen))
print(next(gen))
print(gen.send(10)) # Restart from 10 (skips 1-9)
print(next(gen))
