
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
        J = np.zeros((1, len(self.A) + 2))

        J[0,0] = 2*self.x*self.y
        J[0,1] = self.x**2
        J[0,2:] = 1.

        return J

# comp = simpleComp()
# comp.check_gradient()

# class opt(Assembly):

#     def configure(self):

#         self.add("comp", simpleComp())

#         self.add('driver', SLSQPdriver())
#         self.driver.workflow.add("comp")
        
#         self.driver.add_parameter('comp.A', low=-20, high=20)
#         self.driver.add_parameter('comp.x', low=0, high=10)
#         self.driver.add_parameter('comp.y', low=0, high=10)

#         self.driver.add_objective('comp.z')


# import time
# assm = opt()

# t = time.time()
# assm.run()
# print time.time() - t

# print "z:", assm.comp.z