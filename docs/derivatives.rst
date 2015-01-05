=============================================================
Using the OpenMDAO derivatives system
=============================================================

Many optimization algorithms make use of gradients. By default, OpenMDAO
will finite difference it during the calculation of the full model gradient. However, an optimization process can often be sped up by having a component supply its own derivatives.

In OpenMDAO, derivatives can be specified in the component API by following
these two steps:

    1. Define a ``list_deriv_vars`` function that tell openmdao which inputs and outputs you have derivatives of
    2. Define a ``provideJ`` method that calculates and returns the Jacobian.

Let's return to the actuator disc component, and show how derivatives can be specified:

.. testcode:: simple_component_actuatordisk_review

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

Let's create a copy of this file called ``actuator_disc_derivatives.py``, that
we will use to implement derivatives. Having it as a separate file from the
derivates-free actuator disc file will allow for easy comparison later.

The two function we need to add to the actuator disc component are 
``list_deriv_vars`` and ``provideJ``.

The first function indicates which derivatives you're proving.
The order that you provide the variables in is important. 

.. testcode:: simple_component_actuatordisk_listderivvars

    def list_deriv_vars(self):
        input_keys = ('a', 'Area', 'rho', 'Vu')
        output_keys = ('Vr', 'Vd','Ct','thrust','Cp','power',)
        return input_keys, output_keys


The second function, ``provideJ``, calculates and returns a matrix (the Jacobian)
of the derivatives, evaluated at the current state of the model. The order of the columns is the same as set for the ``inputs`` portion of ``list_deriv_vars``, and the order of the rows is the same as the order of ``outputs``.

.. testcode:: simple_component_actuatordisk_provideJ

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
        self.J[3, 0] = -2.0*self.Area*self.Vu**2*self.a*self.rho + 2.0*self.Area*self.Vu**2*self.rho*one_minus_a
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

Running the Optimization, with derivatives
---------------------------

To summarize, ``actuator_disc_derivatives.py`` is displayed in its entirety below:

.. testcode:: simple_assembly_betzlimit

    from openmdao.main.api import Component
    from openmdao.lib.datatypes.api import Float

    import numpy as np

    class ActuatorDisc(Component):
        """Simple wind turbine model based on actuator disc theory"""

        # inputs
        a = Float(.5, iotype="in", desc="Induced Velocity Factor")
        Area = Float(10, iotype="in", desc="Rotor disc area", units="m**2", low=0)
        rho = Float(1.225, iotype="in", desc="air density", units="kg/m**3")
        Vu = Float(10, iotype="in", desc="Freestream air velocity, upstream of rotor", units="m/s")

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
            self.J[3, 0] = -2.0*self.Area*self.Vu**2*self.a*self.rho + 2.0*self.Area*self.Vu**2*self.rho*one_minus_a
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

Modify ``betz_limit.py`` to import ``ActuatorDisc`` from ``actuator_disc_derivatives.py``
instead of ``actuator_disc.py``. 


Running ``python betz_limit.py`` we see that the optimization takes less time
when derivatives are provided.
