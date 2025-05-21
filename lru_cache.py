import random
import time
from collections import OrderedDict

N = 100_000
Q = 50_000
CACHE_SIZE = 1000

array = [random.randint(1, 100) for _ in range(N)]

queries = []
for _ in range(Q):
    if random.random() < 0.7:
        i = random.randint(0, N - 2)
        val = random.randint(i, N - 1)
        queries.append(('Range', i, val))
    else:
        i = random.randint(0, N - 1)
        val = random.randint(1, 100)
        queries.append(('Update', i, val))


class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate(self, index):
        keys_to_delete = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_delete:
            del self.cache[key]


def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])


def update_no_cache(array, index, value):
    array[index] = value


cache = LRUCache(CACHE_SIZE)


def range_sum_with_cache(array, L, R):
    cached = cache.get((L, R))
    if cached is not None:
        return cached
    total = sum(array[L:R+1])
    cache.put((L, R), total)
    return total


def update_with_cache(array, index, value):
    array[index] = value
    cache.invalidate(index)


array_no_cache = array[:]
array_with_cache = array[:]

start = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_no_cache(array_no_cache, query[1], query[2])
    else:
        update_no_cache(array_no_cache, query[1], query[2])
time_no_cache = time.time() - start

start = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_with_cache(array_with_cache, query[1], query[2])
    else:
        update_with_cache(array_with_cache, query[1], query[2])
time_with_cache = time.time() - start


print(f"Час виконання без кешування: {time_no_cache:.2f} секунд")
print(f"Час виконання з LRU-кешем: {time_with_cache:.2f} секунд")
