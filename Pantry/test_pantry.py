"""
This is my first time doing unit tests in python. I tried to get something quick built using AI.
The tests are not working and I will need to refactor when I learn more about Unit Tests in Python. 
"""

import pantry
import unittest

class TestPantry(unittest.TestCase):

    # Set up will clear all items in pantry before each test: 
    def setUp(self):
        pantry.c.execute("DELETE FROM pantry")

    # Adding a new item will create a table in pantry 
    def test_add_new_item(self):
        pantry.add_item("Milk", 1, "Dairy", "2024-07-01")
        items = pantry.query_all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][0], "Milk")
        self.assertEqual(items[0][1], 1)
        self.assertEqual(items[0][2], "Dairy")
        self.assertEqual(items[0][3], "2024-07-01")

    # Adding an existing item will update the item size
    def test_add_existing_item(self):
        pantry.add_item("Milk", 1, "Dairy", "2024-07-01")
        pantry.add_item("Milk", 2, "Dairy", "2024-07-01")
        items = pantry.query_all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][0], "Milk")
        self.assertEqual(items[0][1], 3) # Quantity should be updated to 3
        self.assertEqual(items[0][2], "Dairy")
        self.assertEqual(items[0][3], "2024-07-01")

    # Searching for an existing item will give an item 
    def test_search_existing_item(self):
        pantry.add_item("Milk", 1, "Dairy", "2024-07-01")
        results = pantry.search_item("Milk")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "Milk")
        self.assertEqual(results[0][1], 1)
        self.assertEqual(results[0][2], "Dairy")
        self.assertEqual(results[0][3], "2024-07-01")
    # Searching for a non existing item will give a no item message
    def test_search_nonexisting_item(self):
        results = pantry.search_item("Bread")
        self.assertEqual(len(results), 0)

    # View all items will display all items
    def test_view_all_items(self):
        pantry.add_item("Milk", 1, "Dairy", "2024-07-01")
        pantry.add_item("Bread", 2, "Grains", "2024-07-05")
        items = pantry.query_all()
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0][0], "Milk")
        self.assertEqual(items[0][1], 1)
        self.assertEqual(items[0][2], "Dairy")
        self.assertEqual(items[0][3], "2024-07-01")
        self.assertEqual(items[1][0], "Bread")
        self.assertEqual(items[1][1], 2)
        self.assertEqual(items[1][2], "Grains")
        self.assertEqual(items[1][3], "2024-07-05")
    
if __name__ == "__main__":
    unittest.main()