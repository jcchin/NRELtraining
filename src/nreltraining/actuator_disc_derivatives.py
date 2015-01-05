from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float

import numpy as np

class ActuatorDisc(Component):
    """Simple wind turbine model based on actuator disc theory"""

    # inputs
    a = Float(.5, iotype="in", desc="Induced Velocity Factor")
    Area = Float(10, iotype="in", desc="Rotor disc area", units="m**2", low=0)
    rho = Float(1.225, iotype="in", desc="air density", units="kg/m**3")
    Vu = Float(11, iotype="in", desc="Freestream air velocity, upstream of rotor", units="m/s")

    # outputs
    Vr = Float(iotype="out", desc="Air velocity at rotor exit plane", units="m/s")
    Vd = Float(iotype="out", desc="Slipstream air velocity, dowstream of rotor", units="m/s")
    Ct = Float(iotype="out", desc="Thrust Coefficient")
    thrust = Float(iotype="out", desc="Thrust produced by the rotor", units="N")
    Cp = Float(iotype="out", desc="Power Coefficient")
    power = Float(iotype="out", desc="Power produced by the rotor", units="W")

    def execute(self):
        # we use 'a' and 'V0' a lot, so make method local variables

        a = self.a
        Vu = self.Vu

        qA = .5*self.rho*self.Area*Vu**2

        self.Vd = Vu*(1-2 * a)
        self.Vr = .5*(self.Vu + self.Vd)

        self.Ct = 4*a*(1-a)
        self.thrust = self.Ct*qA

        self.Cp = self.Ct*(1-a)
        self.power = self.Cp*qA*Vu

    def provideJ(self):
        self.J = np.zeros((6, 4))

        # pre-compute commonly needed quantities
        a_times_area = self.a*self.Area
        rho_times_vu = self.rho*self.Vu
        one_minus_a = 1 - self.a 
        a_area_rho_vu = a_times_area*rho_times_vu

        # d_vr/d_a
        self.J[0, 0] = - self.Vu
        # d_vr/d_Vu
        self.J[0, 3] = 1 - self.a

        # d_vd/d_a
        self.J[1, 0] = -2*self.Vu
        # d_vd/d_Vu
        self.J[1, 3] = 1 - 2*self.a

        # d_ct/d_a
        self.J[2, 0] = 4 - 8*self.a

        # d_thrust/d_a
        self.J[3, 0] = self.Area*self.Vu**2*self.rho*(-4.0*self.a + 2.0)
        # d_thrust/d_area
        self.J[3, 1] = 2.0*self.Vu**2*self.a*self.rho*one_minus_a
        # d_thrust/d_rho
        self.J[3, 2] = 2.0*a_times_area*self.Vu**2*(one_minus_a)
        # d_thrust/d_Vu
        self.J[3, 3] = 4.0*a_area_rho_vu*(one_minus_a)

        # d_cp/d_a
        self.J[4, 0] = 4*self.a*(2*self.a - 2) + 4*(one_minus_a)**2

        # d_power/d_a
        self.J[5, 0] = 2.0*self.Area*self.Vu**3*self.a*self.rho*(2*self.a - 2) + 2.0*self.Area*self.Vu**3*self.rho*one_minus_a**2
        # d_power/d_area
        self.J[5, 1] = 2.0*self.Vu**3*self.a*self.rho*one_minus_a**2
        # d_power/d_rho
        self.J[5, 2] = 2.0*a_times_area*self.Vu**3*(one_minus_a)**2
        # d_power/d_vu
        self.J[5, 3] = 6.0*self.Area*self.Vu**2*self.a*self.rho*one_minus_a**2

        return self.J

    def list_deriv_vars(self):
        input_keys = ('a', 'Area', 'rho', 'Vu')
        output_keys = ('Vr', 'Vd','Ct','thrust','Cp','power',)
        return input_keys, output_keys

if __name__ == "__main__":

    comp = ActuatorDisc()
    comp.run()

    comp.check_gradient()



