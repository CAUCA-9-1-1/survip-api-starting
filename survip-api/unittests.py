import unittest
from opensource.tests.building import TestBuilding
from opensource.tests.inspection import TestInspection

if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TestBuilding))
	suite.addTest(unittest.makeSuite(TestInspection))
	runner = unittest.TextTestRunner()

	print(runner.run(suite))
