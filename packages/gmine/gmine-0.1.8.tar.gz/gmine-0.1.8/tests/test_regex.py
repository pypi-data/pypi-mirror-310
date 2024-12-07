import unittest
from unittest import TestCase

from gmine.regex import satisfy


class MyTest(TestCase):
    def test_satisfy(self):
        """Basic test case for satisfy function"""
        para1 = "I waited at the roadside for ROC"
        para2 = "dog"

        cnf = "roadside and waited and ( ' Regional Operations ' or ' regional operations ' or ROC )"
        self.assertTrue(satisfy(para1, cnf))
        self.assertFalse(satisfy(para2, cnf))

    def test_satisfy2(self):
        """Edge cases"""
        para1 = "I waited at the roadside for ROC"
        para2 = "dog"

        cnf = "  roadside    and    waited and ( ' Regional Operations ' or ' regional operations ' or ROC )"
        self.assertTrue(satisfy(para1, cnf))
        self.assertFalse(satisfy(para2, cnf))


if __name__ == "__main__":
    unittest.main()
