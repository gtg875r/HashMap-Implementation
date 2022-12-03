# Name: Aaron Fowler
# OSU Email: fowleraa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: #6 HashMap
# Due Date: 12/2/2022
# Description: Chaining implementation of hash map


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
        Computes a hash key to add a key/value pair.  Appends the key/value pair as a SL Node to the linked list located
         at the hash key.
        """
        if self.table_load() >= 1:
            new_capacity = self._next_prime(self._capacity * 2)
            self.resize_table(new_capacity)

        hash_key = self._hash_function(key) % self.get_capacity()

        key_linkedlist = self._buckets.get_at_index(hash_key)
        list_size = key_linkedlist.length()
        if list_size > 0:
            try:
                contain_test = key_linkedlist.remove(key)
                if contain_test is True:
                    self._size -= 1
            except:
                pass
            key_linkedlist.insert(key, value)
            self._size += 1
        else:
            key_linkedlist.insert(key, value)

            self._size += 1

        return

    def empty_buckets(self) -> int:
        """
        Surveys all the linked lists in the dynamic array, and counts/returns how many are empty.
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
        Calculates and returns the table load.  size divided by capacity.
        """

        table_size = self.get_size()
        table_capacity = self.get_capacity()
        final_load = table_size/table_capacity
        return final_load

    def clear(self) -> None:
        """
        Clears the contents of the has map, but does not change the capacity of the hash map.  Updates with an empty
        new Dyanmic Array.
        """

        original_da_length = self._buckets.length()

        for bucket_index in range(original_da_length):
            self._buckets.set_at_index(bucket_index, LinkedList())

        self._size = 0
        return


    def resize_table(self, new_capacity: int) -> None:
        """
        Takes a new capacity as a parameter, if the number is prime it extends the dynamic array to that capacity,
        and then re-hashes each value and puts() them into the respective linked list.  If the number is not prime,
        it rounds up to the nearest prime number and then follows the same procedure.
        """

        if new_capacity < 1:
            return

        new_buckets = DynamicArray()
        old_buckets = self._buckets

        if self._is_prime(new_capacity):

            current_capacity = self._capacity
            self._capacity = new_capacity
            for item_index in range(self._capacity):
                new_buckets.append(LinkedList())
            self._buckets = new_buckets
            self._size = 0
            for item_index in range(current_capacity):
                if old_buckets.get_at_index(item_index).length() > 0:
                    for item in old_buckets.get_at_index(item_index):
                        old_key = item.key
                        old_value = item.value
                        self.put(old_key, old_value)


        else:
            new_capacity = self._next_prime(new_capacity)
            current_capacity = self._capacity
            self._capacity = new_capacity
            for item_index in range(self._capacity):
                new_buckets.append(LinkedList())
            self._buckets = new_buckets
            self._size = 0
            for item_index in range(current_capacity):
                if old_buckets.get_at_index(item_index).length() > 0:
                    for item in old_buckets.get_at_index(item_index):
                        old_key = item.key
                        old_value = item.value
                        self.put(old_key, old_value)

        return

    def get(self, key: str):
        """
        Takes a key as a parameter, and then searches the respective linked list for that key.  If the key is found,
        the method returns the SL object.  Else it returns None.
        """

        hash_key = self._hash_function(key) % self.get_capacity()

        linked_list = self._buckets.get_at_index(hash_key)
        for item in linked_list:
            if item.key == key:
                return item.value

        return None



    def contains_key(self, key: str) -> bool:
        """
        Searches each linked list in the dyanmic array for the key that is provided as a parameter.  If the key is
        found then the method returns True.  If not key is not found the method returns False.
        """
        hash_key = self._hash_function(key) % self.get_capacity()

        linked_list = self._buckets.get_at_index(hash_key)
        for item in linked_list:
            if item.key == key:
                return True

        return False


    def remove(self, key: str) -> None:
        """
        Searches the Linked List for a SL object with this key.  If the key is found, then the object is removed from
        the list and the size of the Hash Map is reduced by 1.  If not found, nothing happens.
        """

        hash_key = self._hash_function(key) % self.get_capacity()

        linked_list = self._buckets.get_at_index(hash_key)
        for item in linked_list:
            if item.key == key:
                linked_list.remove(key)
                self._size -= 1

        return


    def get_keys_and_values(self) -> DynamicArray:
        """
        Method that returns a dyanmic array of every key/value pair in the hash map as a list of tuples.
        """
        return_da = DynamicArray()
        original_da_length = self._buckets.length()

        for bucket_index in range(original_da_length):
            linked_list = self._buckets.get_at_index(bucket_index)
            for item in linked_list:
                return_da.append((item.key, item.value))
        return return_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Function that takes a dyanmic array, and creates a hash map from the values in the array.  Based on that hash map,
    the mode is found.  The function returns a dyanmic array of the values with the highest frequency (or value with
    the highest frequency), as well as the number of times that/those values are found.  These two items are returned
    as a tuple.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    final_da = DynamicArray()

    da_length = da.length()
    for da_index in range(da_length):
        new_item = da.get_at_index(da_index)
        contains_new_item = map.contains_key(new_item)

        if contains_new_item is True:
            current_value = map.get(new_item) + 1
            map.put(new_item, current_value)
            current_highest_key = final_da.get_at_index(0)

            if current_value == map.get(current_highest_key):
                if new_item != current_highest_key:
                    final_da.append(new_item)
            elif current_value > map.get(current_highest_key):
                final_da = DynamicArray()
                final_da.append(new_item)

        else:
            map.put(new_item, 1)
            if final_da.length() == 0:
                final_da.append(new_item)
            else:
                current_value = 1
                current_highest_key = final_da.get_at_index(0)

                if current_value == map.get(current_highest_key):
                    if new_item != current_highest_key:
                        final_da.append(new_item)



    a_mode = final_da.get_at_index(0)
    mode_value = map.get(a_mode)

    return (final_da, mode_value)




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
