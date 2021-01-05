from RoutingTable import RoutingTable
from Route import Route
import unittest

class Unittest(unittest.TestCase):

    
    def test_if_list_gets_sorted_correctly(self):
        routing_table = []
        routing_table.append(Route(b'0000', b'5656', 3))
        routing_table.append(Route(b'5600', b'5776', 7))
        routing_table.append(Route(b'2300', b'5656', 1))
        RoutingTable.find_best_route(5600)
        self.assertEquals(b'5776')

if __name__ == '__main__':
    unittest.main()