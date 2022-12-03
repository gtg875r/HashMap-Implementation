# Name: Aaron Fowler
# OSU Email: fowleraa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: #6 HashMap
# Due Date: 12/2/2022
# Description: open addressing implementation of hash map

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Takes a key/value pair, and creates a hash value.  The method searches for a space in the DA that is vacant,
        and if the space is filled, recalculates the hash value until a space is found.  Once a space is found the
        method creates a new hash object and inserts the object at the hash index that was vacant.
        """

        if self.table_load() >= 0.5:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        hash_key = self._hash_function(key) % self.get_capacity()
        j_value = 1
        hash_value = self._buckets.get_at_index(hash_key)

        while hash_value is not None:  # or hash_value >= self._capacity
            if self._buckets.get_at_index(hash_key).key == key:
                if self._buckets.get_at_index(hash_key).is_tombstone is True:
                    self._size += 1
                hash_item = HashEntry(key, value)
                self._buckets.set_at_index(hash_key, hash_item)
                return
            hash_key = (self._hash_function(key) + j_value**2) % self.get_capacity()
            j_value += 1
            hash_value = self._buckets.get_at_index(hash_key)


        hash_item = HashEntry(key, value)
        self._buckets.set_at_index(hash_key, hash_item)
        self._size += 1

        return

    def table_load(self) -> float:
        """
        Calculates and returns the table load.  size divided by capacity.
        """

        table_size = self.get_size()
        table_capacity = self.get_capacity()
        final_load = table_size / table_capacity
        return final_load

    def empty_buckets(self) -> int:
        """
        Surveys the entire dynamic array for how many indicies are None, and returns that number.
        """

        total_empty_buckets = 0
        original_da_length = self._buckets.length()

        for bucket_index in range(original_da_length):
            if self._buckets.get_at_index(bucket_index) is None:
                total_empty_buckets += 1
        return total_empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes a new capacity as a parameter, if the number is prime it creates a new dynamic array of that capacity,
        and then re-hashes each value and puts() them into the new DA.  If the number is not prime, it rounds up to
        the nearest prime number and creates a DA of that capacity and then re-hashes each value and puts() them into
        the new DA.
        """

        if new_capacity < self._size:
            return

        new_buckets = DynamicArray()
        old_buckets = self._buckets

        if self._is_prime(new_capacity):

            current_capacity = self._capacity
            self._capacity = new_capacity
            for space in range(self._capacity):
                new_buckets.append(None)
            self._buckets = new_buckets
            self._size = 0
            for item_index in range(current_capacity):
                if old_buckets.get_at_index(item_index):
                    hash_item = old_buckets.get_at_index(item_index)
                    old_key = hash_item.key
                    old_value = hash_item.value
                    tombstone = hash_item.is_tombstone
                    if tombstone is not True:
                        self.put(old_key, old_value)

        else:
            new_capacity = self._next_prime(new_capacity)
            current_capacity = self._capacity
            self._capacity = new_capacity
            for space in range(self._capacity):
                new_buckets.append(None)
            self._buckets = new_buckets
            self._size = 0
            for item_index in range(current_capacity):
                if old_buckets.get_at_index(item_index) is not None:
                    hash_item = old_buckets.get_at_index(item_index)
                    old_key = hash_item.key
                    old_value = hash_item.value
                    self.put(old_key, old_value)

        return

    def get(self, key: str) -> object:
        """
        Takes a key as a parameter, and then searches the Dynamic Array for that key.  If the key is found, and is not
        a tombstone, the method returns the hash object.  Else it returns None.
        """

        hash_key = self._hash_function(key) % self.get_capacity()
        j_value = 1
        hash_value = self._buckets.get_at_index(hash_key)

        while hash_value is not None:  #  or hash_value >= self._capacity
            if hash_value.key == key:
                if hash_value.is_tombstone is False:
                    return hash_value.value
                else:
                    return None
            else:
                hash_key = (self._hash_function(key) + j_value ** 2) % self.get_capacity()
                j_value += 1
                hash_value = self._buckets.get_at_index(hash_key)
        return None

    def contains_key(self, key: str) -> bool:
        """
        Searches the Dyanmic Array for a key.  If the key is found, and the hash object is not a tombstone, then the
        method returns True.  If not key is not found, or the object is a tombstone, the method returns False.
        """

        hash_key = self._hash_function(key) % self.get_capacity()
        j_value = 1
        hash_value = self._buckets.get_at_index(hash_key)
        count = 0
        if hash_value is None:
            return False
        while (hash_value is not None) or (count == self._size):  # or hash_value >= self._capacity
            if hash_value.key == key:
                if hash_value.is_tombstone is False:
                    return True
                else:
                    return False
            else:
                hash_key = (self._hash_function(key) + j_value ** 2) % self.get_capacity()
                j_value += 1
                hash_value = self._buckets.get_at_index(hash_key)
                count += 1
                if hash_value is None:
                    return False

        return False

    def remove(self, key: str) -> None:
        """
        Searches the Dyanamic Array for a hash object with this key.  If the key is found, and the item is not already
        a tombstone, the object is set to be a tombstone, and the size of the hash map is reduced by 1.
         If not found, nothing happens.
        """

        if self.contains_key(key) is True:

            hash_key = self._hash_function(key) % self.get_capacity()
            j_value = 1
            hash_value = self._buckets.get_at_index(hash_key)
            count = 0
            if hash_value is None:
                return

            while hash_value is not None or count == self._size:  # or hash_value >= self._capacity
                if hash_value.key == key:
                    if hash_value.is_tombstone is False:
                        hash_value.is_tombstone = True
                        self._size -= 1

                    return
                else:
                    hash_key = (self._hash_function(key) + j_value ** 2) % self.get_capacity()
                    j_value += 1
                    hash_value = self._buckets.get_at_index(hash_key)
                    count += 1
                    if hash_value is None:
                        return

        return

    def clear(self) -> None:
        """
        Clears the contents of the has map, but does not change the capacity of the hash map.  Updates with an empty
        new Dyanmic Array.
        """

        new_da = DynamicArray()
        for space in range(self._capacity):
            new_da.append(None)
        self._buckets = new_da

        self._size = 0
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method that returns a dyanmic array of every key/value pair in the hash map as a list of tuples.
        """

        return_da = DynamicArray()
        original_da_length = self._buckets.length()

        for bucket_index in range(original_da_length):
            if self._buckets.get_at_index(bucket_index) is not None:
                if self._buckets.get_at_index(bucket_index).is_tombstone is False:
                    hash_item = self._buckets.get_at_index(bucket_index)
                    return_da.append((hash_item.key, hash_item.value))
        return return_da

    def __iter__(self):
        """
        Creates starting point for the hash map to iterate from.
        """

        self._index = 0
        return self

    def __next__(self):
        """
        Returns the value of the current index (so long as it's not a tombstone), and then increments the index by 1.
        """

        if self._index >= self._buckets.length():
            raise StopIteration

        try:
            value = self._buckets.get_at_index(self._index)
        except:
            raise StopIteration

        while value is None or value.is_tombstone is True:
            self._index += 1
            try:
                value = self._buckets.get_at_index(self._index)
            except:
                raise StopIteration
            if self._index >= self._buckets.length():
                raise StopIteration

        self._index += 1

        return value


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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
