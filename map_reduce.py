import requests
import re
import collections
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple


def fetch_text(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def map_words(text_chunk: str) -> List[Tuple[str, int]]:
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    return [(word, 1) for word in words]


def reduce_word_counts(pairs: List[Tuple[str, int]]) -> collections.Counter:
    counter = collections.Counter()
    for word, count in pairs:
        counter[word] += count
    return counter


def chunk_text(text: str, num_chunks: int) -> List[str]:
    lines = text.splitlines()
    chunk_size = len(lines) // num_chunks
    return ['\n'.join(lines[i:i + chunk_size]) for i in range(0, len(lines), chunk_size)]


def visualize_top_words(counter: collections.Counter, top_n: int = 10):
    most_common = counter.most_common(top_n)
    words, counts = zip(*most_common)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title(f"Топ {top_n} найчастіше вживаних слів")
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Наприклад, "Гордість і упередження"
    text = fetch_text(url)

    num_threads = 4
    chunks = chunk_text(text, num_threads)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        mapped = executor.map(map_words, chunks)

    all_pairs = [pair for sublist in mapped for pair in sublist]

    word_counts = reduce_word_counts(all_pairs)

    visualize_top_words(word_counts, top_n=10)


if __name__ == "__main__":
    main()
