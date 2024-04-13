class Cache:
    def __init__(self, cache_size, block_size, mapping_technique):
        self.cache_size = cache_size
        self.block_size = block_size
        self.mapping_technique = mapping_technique
        if mapping_technique == "direct":
            self.num_blocks = cache_size // block_size
            self.cache = [-1] * self.num_blocks
        elif mapping_technique == "set associative":
            self.num_sets = cache_size // (
                block_size * 2
            )  # Assuming 2-way set associative
            self.cache = [
                [-1] * 2 for _ in range(self.num_sets)
            ]  # 2-way set associative cache
        elif mapping_technique == "associative":
            self.cache = {}  # Associative cache using a dictionary
        else:
            raise ValueError("Invalid cache mapping technique")
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def access(self, address):
        tag, index = self.get_tag_and_index(address)
        if self.mapping_technique == "direct":
            if self.cache[index] == tag:
                self.hits += 1
                print(f"Cache hit for address {address}")
            else:
                self.misses += 1
                if self.cache[index] != -1:
                    self.evictions += 1
                    print(f"Cache eviction for address {address}")
                self.cache[index] = tag
                print(
                    f"Cache miss for address {address}, block {index} updated with tag {tag}"
                )
        elif self.mapping_technique == "set associative":
            set_index = index % self.num_sets
            if tag in self.cache[set_index]:
                self.hits += 1
                print(f"Cache hit for address {address}")
            else:
                self.misses += 1
                if -1 in self.cache[set_index]:
                    self.cache[set_index][self.cache[set_index].index(-1)] = tag
                    print(
                        f"Cache miss for address {address}, tag {tag} added to set {set_index}"
                    )
                else:
                    self.evictions += 1
                    print(f"Cache eviction for address {address}")
                    self.cache[set_index][0] = tag  # Replace the first block in the set
                    print(
                        f"Cache miss for address {address}, tag {tag} added to set {set_index}"
                    )
        elif self.mapping_technique == "associative":
            if tag in self.cache:
                self.hits += 1
                print(f"Cache hit for address {address}")
            else:
                self.misses += 1
                if len(self.cache) < self.cache_size // self.block_size:
                    self.cache[tag] = index
                    print(f"Cache miss for address {address}, tag {tag} added")
                else:
                    self.evictions += 1
                    print(f"Cache eviction for address {address}")
                    # Remove a random entry from the cache
                    removed_tag = next(iter(self.cache))
                    del self.cache[removed_tag]
                    self.cache[tag] = index
                    print(f"Cache miss for address {address}, tag {tag} added")
        else:
            raise ValueError("Invalid cache mapping technique")

    def get_tag_and_index(self, address):
        binary_address = bin(address)[2:].zfill(32)
        tag_bits = binary_address[
            : -int(self.cache_size.bit_length() - self.block_size.bit_length())
        ]
        index_bits = binary_address[
            -int(self.cache_size.bit_length() - self.block_size.bit_length()) :
        ]
        return tag_bits, int(index_bits, 2)


def main():
    main_memory_capacity = int(input("Enter the capacity of main memory (in bytes): "))
    cache_capacity = int(input("Enter the capacity of the cache memory (in bytes): "))
    block_size = int(input("Enter the block size (in bytes): "))
    mapping_technique = input(
        "Enter the cache mapping technique (direct/set associative/associative): "
    ).lower()

    cache = Cache(cache_capacity, block_size, mapping_technique)

    memory_trace = list(
        map(
            int,
            input("Enter a sequence of memory addresses separated by space: ").split(),
        )
    )

    for address in memory_trace:
        cache.access(address)

    print("\nCache Hits:", cache.hits)
    print("Cache Misses:", cache.misses)
    print("Cache Evictions:", cache.evictions)


if __name__ == "__main__":
    main()
