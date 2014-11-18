
import unittest


from openmdao.main.api import Assembly, set_as_top
from openmdao.lib.drivers.slsqpdriver import SLSQPdriver
from openmdao.lib.drivers.doedriver import DOEdriver
from openmdao.lib.doegenerators.api import FullFactorial
from openmdao.lib.casehandlers.api import ListCaseRecorder

from openmdao.util.testutil import assert_rel_error

from nreltraining.nreltraining import *


class ActuatorDiskTestCase(unittest.TestCase):

    def setUp(self):
        self.top = set_as_top(Assembly())
        self.top.add('ad', ActuatorDisk())
        self.top.driver.workflow.add('ad')

    def tearDown(self):
        pass

    def test_ActuatorDisk(self):
        self.assertEqual(self.top.get('ad.Cp'), 0.)

        self.top.run()

        self.assertEqual(self.top.get('ad.Cp'), 0.5)

        self.top.replace('driver', SLSQPdriver())
        self.top.driver.add_parameter('ad.a', low=0, high=1)
        self.top.driver.add_objective('-ad.Cp')

        self.top.run()

        assert_rel_error(self, self.top.ad.a, 0.333, 0.005)
        assert_rel_error(self, self.top.ad.Cp, 0.593, 0.005)  # Betz Limit



class AutoBEMTestCase(unittest.TestCase):

    def setUp(self):
        self.top = set_as_top(Assembly())
        self.top.add('b', AutoBEM())
        self.top.driver.workflow.add('b')

    def tearDown(self):
        pass

    def test_AutoBEM_DOE(self):
        # perform a DOE
        self.top.replace('driver', DOEdriver())
        self.top.driver.DOEgenerator = FullFactorial(3)

        self.top.driver.add_parameter('b.chord_hub', low=.1, high=2)
        self.top.driver.add_parameter('b.chord_tip', low=.1, high=2)
        self.top.driver.add_parameter('b.rpm',       low=20, high=300)
        self.top.driver.add_parameter('b.twist_hub', low=-5, high=50)
        self.top.driver.add_parameter('b.twist_tip', low=-5, high=50)

        self.top.run()

        self.assertEqual(self.top.b.exec_count, 243)

    def test_AutoBEM_Opt(self):
        # perform optimization
        self.top.replace('driver', SLSQPdriver())

        self.top.driver.add_parameter('b.chord_hub', low=.1, high=2)
        self.top.driver.add_parameter('b.chord_tip', low=.1, high=2)
        self.top.driver.add_parameter('b.rpm',       low=20, high=300)
        self.top.driver.add_parameter('b.twist_hub', low=-5, high=50)
        self.top.driver.add_parameter('b.twist_tip', low=-5, high=50)
        # self.top.driver.add_parameter('b.r_tip',     low=1, high=10)

        self.top.driver.add_objective('-b.data.Cp')

        self.top.run()

        assert_rel_error(self, self.top.b.data.Cp, 0.57, 0.01)


if __name__ == '__main__':
    unittest.main()

