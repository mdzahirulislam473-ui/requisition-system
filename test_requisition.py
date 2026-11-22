"""
test_requisition.py
Automated unit tests for the Requisition class.
Run with:  python -m unittest -v
"""

import unittest

from requisition import Requisition


class TestRequisition(unittest.TestCase):

    def setUp(self):
        Requisition.reset()

    def test_unique_ids(self):
        a = Requisition("FN01", "A")
        b = Requisition("FN02", "B")
        self.assertEqual(a.requisition_id, 10001)
        self.assertEqual(b.requisition_id, 10002)

    def test_total_is_calculated(self):
        r = Requisition("FN19", "John Paul")
        self.assertEqual(r.add_requisition([("Paper", 150), ("Toner", 300)]), 450)

    def test_under_500_auto_approved(self):
        r = Requisition("FN19", "John Paul")
        r.add_requisition([("Paper", 499.99)])
        self.assertEqual(r.approve_requisition(), "Approved")
        self.assertEqual(r.approval_reference, "FN19001")

    def test_exactly_500_is_pending(self):
        r = Requisition("FN20", "Tracy Brown")
        r.add_requisition([("Monitor", 500)])
        self.assertEqual(r.approve_requisition(), "Pending")
        self.assertIsNone(r.approval_reference)

    def test_manager_approves_pending(self):
        r = Requisition("FN20", "Tracy Brown")
        r.add_requisition([("Monitor", 1000)])
        r.approve_requisition()
        self.assertEqual(r.respond_requisition("Approved"), "Approved")
        self.assertEqual(r.approval_reference, "FN20001")

    def test_manager_rejects_pending(self):
        r = Requisition("FN15", "Emma")
        r.add_requisition([("Laptop", 3500)])
        r.approve_requisition()
        self.assertEqual(r.respond_requisition("not approved"), "Not approved")

    def test_cannot_change_non_pending(self):
        r = Requisition("FN19", "John")
        r.add_requisition([("Pen", 10)])
        r.approve_requisition()
        self.assertEqual(r.respond_requisition("not approved"), "Approved")

    def test_invalid_decision(self):
        r = Requisition("FN20", "Tracy")
        r.add_requisition([("Monitor", 1000)])
        r.approve_requisition()
        with self.assertRaises(ValueError):
            r.respond_requisition("maybe")

    def test_invalid_items(self):
        r = Requisition("FN20", "Tracy")
        with self.assertRaises(ValueError):
            r.add_requisition([])
        with self.assertRaises(ValueError):
            r.add_requisition([("Pen", -1)])
        with self.assertRaises(ValueError):
            r.add_requisition([("Pen", "abc")])

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            Requisition("FN01", "A", "31/02/2024")

    def test_statistics_update(self):
        cheap = Requisition("FN01", "A")
        cheap.add_requisition([("Pen", 10)])
        cheap.approve_requisition()
        big = Requisition("FN02", "B")
        big.add_requisition([("Laptop", 2000)])
        big.approve_requisition()

        stats = Requisition.requisition_statistics(show=False)
        self.assertEqual(stats, {"submitted": 2, "approved": 1,
                                 "pending": 1, "not_approved": 0})

        big.respond_requisition("not approved")
        stats = Requisition.requisition_statistics(show=False)
        self.assertEqual(stats["pending"], 0)
        self.assertEqual(stats["not_approved"], 1)


if __name__ == "__main__":
    unittest.main()
