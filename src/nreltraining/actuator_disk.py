from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float

class ActuatorDisk(Component):
    """Simple wind turbine model based on actuator disk theory"""

    # inputs
    a = Float(.5, iotype="in", desc="Induced Velocity Factor")
    Area = Float(10, iotype="in", desc="Rotor disk area", units="m**2", low=0)
    rho = Float(1.225, iotype="in", desc="air density", units="kg/m**3")
    Vu = Float(10, iotype="in", desc="Freestream air velocity, upstream of rotor", units="m/s")

    # outputs
    Vr = Float(iotype="out", desc="Air velocity at rotor exit plane", units="m/s")
    Vd = Float(iotype="out", desc="Slipstream air velocity, downstream of rotor", units="m/s")
    Ct = Float(iotype="out", desc="Thrust Coefficient")
    thrust = Float(iotype="out", desc="Thrust produced by the rotor", units="N")
    Cp = Float(iotype="out", desc="Power Coefficient")
    power = Float(iotype="out", desc="Power produced by the rotor", units="W")

    def execute(self):
            # we use 'a' and 'Vu' a lot, so make method local variables

            a = self.a
            Vu = self.Vu
            qA = .5*self.rho*self.Area*Vu**2

            self.Vd = Vu*(1-2 * a)
            self.Vr = .5*(self.Vu + self.Vd)

            self.Ct = 4*a*(1-a)
            self.thrust = self.Ct*qA

            self.Cp = self.Ct*(1-a)
            self.power = self.Cp*qA*Vu

if __name__ == "__main__":

    comp = ActuatorDisk()
    comp.run()

    print comp.power
    print comp.thrust