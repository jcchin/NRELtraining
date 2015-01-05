from openmdao.main.api import Assembly
from openmdao.lib.drivers.api import SLSQPdriver
from actuator_disc_derivatives import ActuatorDisc #Import components from the plugin

import time

class Betz_Limit(Assembly):
    """Simple wind turbine assembly to calculate the Betz Limit"""

    # Inputs would go here

    # Outputs would go here
    # Cp = Float(iotype="out", desc="Power Coefficient")

    def configure(self):
        """things to be configured go here"""

        aDisc = self.add('aDisc', ActuatorDisc())

        driver = self.add('driver', SLSQPdriver())

        driver.add_parameter('aDisc.a', low=0, high=1)
        driver.add_parameter('aDisc.Area', low=0, high=1)
        driver.add_parameter('aDisc.rho', low=0, high=1)
        driver.add_parameter('aDisc.Vu', low=0, high=1)

        driver.add_objective('-aDisc.Cp')
        driver.workflow.add('aDisc')

        driver.tolerance = .00000001

        # self.connect('self.Cp', 'self.aDisc.cp') #promote Cp to the assembly output

        self.create_passthrough('aDisc.Cp') #shortcut for commented code above

if __name__ == "__main__":

    assembly = Betz_Limit()
    t = time.time()
    assembly.run()
    print "time:", time.time() - t
    print "execution count:", assembly.aDisc.exec_count
    print
    print "Cp:", assembly.Cp