import timeit
import matplotlib.pyplot as plt
from functools import lru_cache


class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    def __init__(self):
        self.root = None
        self.memo = {}

    def insert(self, key, value):
        self.memo[key] = value
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_node(key, self.root)

    def _insert_node(self, key, current_node):
        if key < current_node.data:
            if current_node.left_node:
                self._insert_node(key, current_node.left_node)
            else:
                current_node.left_node = Node(key, current_node)
        else:
            if current_node.right_node:
                self._insert_node(key, current_node.right_node)
            else:
                current_node.right_node = Node(key, current_node)

    def find(self, key):
        node = self.root
        while node is not None:
            if key < node.data:
                node = node.left_node
            elif key > node.data:
                node = node.right_node
            else:
                self._splay(node)
                return self.memo.get(key)
        return None

    def _splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child
        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_splay(n, tree: SplayTree):
    if n <= 1:
        tree.insert(n, n)
        return n

    if (cached := tree.find(n)) is not None:
        return cached

    tree.insert(0, 0)
    tree.insert(1, 1)

    for i in range(2, n + 1):
        if tree.find(i) is None:
            a_val = tree.find(i - 2)
            b_val = tree.find(i - 1)
            tree.insert(i, a_val + b_val)

    return tree.find(n)


values = list(range(0, 1001, 50))
lru_times = []
splay_times = []

for n in values:
    fibonacci_lru.cache_clear()
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
    lru_times.append(lru_time)

    splay_tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, splay_tree), number=1)
    splay_times.append(splay_time)


print(f"{'n':<10}{'LRU Cache Time (s)':<22}{'Splay Tree Time (s)'}")
print("-" * 50)
for n, lru, splay in zip(values, lru_times, splay_times):
    print(f"{n:<10}{lru:<22.10f}{splay:.10f}")


plt.figure(figsize=(10, 6))
plt.plot(values, lru_times, label='LRU Cache', marker='o')
plt.plot(values, splay_times, label='Splay Tree', marker='x')
plt.xlabel('n')
plt.ylabel('Середній час виконання (секунди)')
plt.title('Порівняння fibonacci_lru vs fibonacci_splay')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
