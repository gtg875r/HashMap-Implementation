# Name: Aaron Fowler
# OSU Email: fowleraa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: #6 HashMap
# Due Date: 12/2/2022
# Description:


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        """

        if self.table_load() >= 1:
            new_capacity = self._next_prime(self._capacity * 2)
            self.resize_table(new_capacity)

        hash_key = self._hash_function(key) % self.get_capacity()

        key_linkedlist = self._buckets.get_at_index(hash_key)
        list_size = key_linkedlist.length()
        if list_size > 0:
            try:
                key_linkedlist.remove(key)
            except:
                pass
            self._buckets.set_at_index(list_size, LinkedList())
            key_linkedlist.insert(0, value)
            self._size += 1
        else:
            key_linkedlist.insert(0, value)

            self._size += 1
        # while list_size > 0:
        #     # print(hash_key)
        #     if hash_key >= self._capacity-1:
        #         # hash_key = hash_key - self._capacity+1
        #         key_linkedlist = self._buckets.get_at_index(hash_key-1)
        #         list_size = key_linkedlist.length()
        #         break
        #     else:
        #         hash_key += 1
        #         key_linkedlist = self._buckets.get_at_index(hash_key)
        #         list_size = key_linkedlist.length()

        # key_linkedlist.


        return

    def empty_buckets(self) -> int:
        """
        TODO: Write this implementation
        """

        total_empty_buckets = 0
        original_da_length = self._buckets.length()

        for bucket_index in range(original_da_length):
            linked_list = self._buckets.get_at_index(bucket_index)
            linked_list_length = linked_list.length()
            if linked_list_length == 0:
                total_empty_buckets += 1
        return total_empty_buckets


    def table_load(self) -> float:
        """
        TODO: Write this implementation
        """

        table_size = self.get_size()
        table_capacity = self.get_capacity()
        final_load = table_size/table_capacity
        return final_load

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """

        original_da_length = self._buckets.length()

        for bucket_index in range(original_da_length):
            self._buckets.set_at_index(bucket_index, LinkedList())

        self._size = 0
        return


    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """

        new_buckets = DynamicArray()
        old_buckets = self._buckets

        if self._is_prime(new_capacity):

            current_capacity = self._capacity
            self._capacity = new_capacity
            for item_index in range(self._capacity):
                new_buckets.append(LinkedList())
            self._buckets = new_buckets
            for item_index in range(current_capacity):
                if old_buckets.get_at_index(item_index).length() > 0:
                    list_needed = old_buckets.get_at_index(item_index)
                    node_needed = list_needed.contains(0)
                    new_hash = self._hash_function(node_needed.key) % self.get_capacity()
                    self.put(new_hash, node_needed)

        else:
            new_capacity = self._next_prime(30)
            current_capacity = self._capacity
            self._capacity = new_capacity
            self._buckets = new_buckets
            for item_index in range(current_capacity):
                if old_buckets.get_at_index(item_index).length() > 0:
                    list_needed = old_buckets.get_at_index(item_index)
                    node_needed = list_needed.contains(0)
                    print(node_needed.key)
                    new_hash = self._hash_function(node_needed.key) % self.get_capacity()
                    self.put(new_hash, node_needed)

        return

    def get(self, key: str):
        """
        TODO: Write this implementation
        """

        da_length = self._buckets.length()
        hash_key = self._hash_function(key) % self.get_capacity()

        for list_index in range(da_length):
            if list_index == hash_key:
                if self._buckets.get_at_index(list_index).length() > 0:
                    list_needed = self._buckets.get_at_index(list_index)
                    node_needed = list_needed.contains(0)
                    return node_needed.value
                else:
                    return None


    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """
        da_length = self._buckets.length()
        hash_key = self._hash_function(key) % self.get_capacity()

        for list_index in range(da_length):
            if list_index == hash_key:
                if self._buckets.get_at_index(list_index).length() > 0:

                    return True
                else:
                    return False


    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """

        hash_key = self._hash_function(key)

        original_da_length = self._buckets.length()
        new_linked_list = LinkedList()

        for bucket_index in range(original_da_length):
            if bucket_index == hash_key:
                self._buckets.set_at_index(new_linked_list)

        self._size -= 1

        return


    def get_keys_and_values(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        return_da = DynamicArray
        original_da_length = self._buckets.length()

        for bucket_index in range(original_da_length):
            linked_list = self._buckets.get_at_index(bucket_index)
            linked_list_length = linked_list.length()
            for item in range(linked_list_length):
                final_value = linked_list.contains(item)
                return_da.append((str(bucket_index), str(final_value)))
        return return_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    TODO: Write this implementation
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
