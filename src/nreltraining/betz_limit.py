from openmdao.main.api import Assembly
from openmdao.lib.drivers.slsqpdriver import SLSQPdriver
from nreltraining.nreltraining import ActuatorDisk #Import components from the plugin

class Betz_Limit(Assembly):
    """Simple wind turbine assembly to calculate the Betz Limit"""

    # Inputs would go here

    # Outputs would go here
    # Cp = Float(iotype="out", desc="Power Coefficient")

    def configure(self):
    """things to be configured go here"""

    aDisk = self.add('aDisk', ActuatorDisk())

    driver = self.driver.add('driver', SLSQPdriver())
    driver.add_parameter('aDisk.a', low=0, high=1)
    driver.add_objective('-aDisk.Cp')
    driver.workflow.add('aDisk')

    # self.connect('self.Cp', 'self.aDisk.cp') #promote Cp to the assembly output
    self.create_passthrough('self.aDisk.Cp') #shortcut for commented code above

if __name__ == "__main__":

    assembly = Betz_Limit()
    assembly.run

    print assembly.Cp