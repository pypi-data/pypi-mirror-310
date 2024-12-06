import unittest

import numpy as np

from smartTable import SmartTable

class TestSmartTable(unittest.TestCase):
    def test_initialization(self):
        table = SmartTable(shape=(2,3))
        self.assertEqual(table.data.shape, (2, 3))

    def test_add_row(self):
        table = SmartTable(shape=(2,3))
        table.add_row([1, 2, 3])
        self.assertEqual(table.data.shape, (3, 3))

    def test_summarize(self):
        table = SmartTable().from_numpy(np.array([[4, 4], [10, 12]]))
        summary = table.summarize()
        self.assertEqual(summary["mean"], 7.5)
