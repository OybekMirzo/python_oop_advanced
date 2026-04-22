Problem 5 (Advanced): Batch Iterator

You are building a data processing tool. Create a reusable iterator system that takes a list and a batch size, and yields sublists (batches) of that size. The last batch may be smaller if there aren’t enough elements left.

1. Create a class BatchIterator that implements __iter__ and __next__. It stores the data list and the batch size. Each call to __next__ slices the first batch_size elements off the front of the list and returns them. When the list is empty, raise StopIteration.
2. Create a class Batched that stores the original data and batch size. Its __iter__ must return a new BatchIterator each time so the object can be looped over multiple times.

Input
b = Batched([1, 2, 3, 4, 5, 6, 7], 3)

for batch in b:
    print(batch)

print('---')

for batch in b:
    print(batch)

Expected Output
[1, 2, 3]
[4, 5, 6]
[7]
---
[1, 2, 3]
[4, 5, 6]
[7]