import unittest
from pdcool.database import DBUtil


class DatabaseTest(unittest.TestCase):
    def test_queryone(self):
        db = DBUtil()
        val = db.queryone("select * from stock")[0]
        self.assertIsNotNone(val)


if __name__ == "__main__":
    unittest.main()
