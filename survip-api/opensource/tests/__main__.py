import unittest
from .building import TestBuilding
from .city import TestCity
from .citytype import TestCityType
from .constructiontype import TestConstructionType
from .country import TestCountry
from .county import TestCounty
from .firesafetydepartment import TestFireSafetyDepartment
from .firehydrant import TestFireHydrant
from .inspection import TestInspection
from .lane import TestLane
from .region import TestRegion
from .risklevel import TestRiskLevel
from .state import TestState
from .survey import TestSurvey


def get_test_opensource(suite=None):
	if suite is None:
		suite = unittest.TestSuite()

	suite.addTest(unittest.makeSuite(TestBuilding))
	suite.addTest(unittest.makeSuite(TestCity))
	suite.addTest(unittest.makeSuite(TestCityType))
	suite.addTest(unittest.makeSuite(TestConstructionType))
	suite.addTest(unittest.makeSuite(TestCountry))
	suite.addTest(unittest.makeSuite(TestCounty))
	suite.addTest(unittest.makeSuite(TestFireHydrant))
	suite.addTest(unittest.makeSuite(TestFireSafetyDepartment))
	suite.addTest(unittest.makeSuite(TestInspection))
	suite.addTest(unittest.makeSuite(TestLane))
	suite.addTest(unittest.makeSuite(TestRegion))
	suite.addTest(unittest.makeSuite(TestRiskLevel))
	suite.addTest(unittest.makeSuite(TestState))
	suite.addTest(unittest.makeSuite(TestSurvey))

	return suite