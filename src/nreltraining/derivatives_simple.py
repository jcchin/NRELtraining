
import numpy as np

from openmdao.lib.drivers.api import SLSQPdriver

from openmdao.main.api import Component, Assembly, set_as_top
from openmdao.lib.datatypes.api import Float, Array

import time

class simpleComp(Component):

    x = Float(np.pi, iotype="in")
    y = Float(2., iotype="in")

    A = Array(np.ones(100, dtype=np.float), iotype="in")

    z = Float(3., iotype="out")

    def execute(self):

        self.z = self.x**2 * self.y + sum(self.A - 3.)

    def list_deriv_vars(self):
        return ("x", "y", "A",), ("z",)

    def provideJ(self):
        pass
        J = np.zeros((1, len(self.A) + 2))

        J[0,0] = 2*self.x*self.y
        J[0,1] = self.x**2
        J[0,2:] = 1.

        return J


# comp = simpleComp()
# comp.run()
# comp.check_gradient(mode="forward")
# quit()


class opt(Assembly):

    def configure(self):

        self.add("comp1", simpleComp())
        self.add("comp2", simpleComp())

        self.add('driver', SLSQPdriver())
        self.driver.workflow.add(["comp1", "comp2"])
        
        self.connect("comp1.z", "comp2.x")
        self.connect("comp1.x", "comp2.A[0]")
        self.connect("comp1.z", "comp2.A[1]")


        self.driver.add_parameter('comp1.A', low=-20, high=20)
        self.driver.add_parameter('comp1.x', low=0, high=10)
        self.driver.add_parameter('comp1.y', low=0, high=10)

        self.driver.add_objective('comp2.z')


import time
assm = opt()

t = time.time()
assm.run()
print time.time() - t

print "z:", assm.comp2.z