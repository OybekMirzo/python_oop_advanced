class BatchIterator:
    def __init__(self, data, batch_size):
        self.data = data[:]
        self.batch_size = batch_size

    def __iter__(self):
        return self

    def __next__(self):
        if not self.data:
            raise StopIteration

        batch = self.data[:self.batch_size]
        self.data = self.data[self.batch_size:]
        return batch


class Batched:
    def __init__(self, data, batch_size):
        self.data = data
        self.batch_size = batch_size

    def __iter__(self):
        return BatchIterator(self.data, self.batch_size)
    

b = Batched([1, 2, 3, 4, 5, 6, 7], 3)

for batch in b:
    print(batch)

print('---')

for batch in b:
    print(batch)
