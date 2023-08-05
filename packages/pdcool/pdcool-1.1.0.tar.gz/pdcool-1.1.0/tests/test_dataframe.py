import unittest
from pdtool.dataframe import *


class DataframeTest(unittest.TestCase):
    def test_generate_simple_dataframe(self):
        df = generate_simple_dataframe()
        show_dataframe(df)

    def test_dataframe_from_sql(self):
        df = dataframe_from_sql("select * from stock")
        show_dataframe(df)


if __name__ == "__main__":
    unittest.main()
